import olefile, struct, zlib, os, subprocess, time

src = r'C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp'
out = r'c:\Users\doris\.agent-skills\L_output_new.hwp'

print('=== 1. olefile로 출력 파일 전체 스트림 읽기 테스트 ===')
try:
    ole = olefile.OleFileIO(out)
    for sp in ole.listdir():
        sn = '/'.join(sp)
        try:
            raw = ole.openstream(sn).read()
            try:
                dec = zlib.decompress(raw, -15)
                print(f'  {sn}: 압축={len(raw):,}, 해제={len(dec):,} ✅')
            except:
                print(f'  {sn}: 크기={len(raw):,} (비압축) ✅')
        except Exception as e:
            print(f'  {sn}: ❌ 읽기 실패 - {e}')
    ole.close()
except Exception as e:
    print(f'  ❌ OLE 열기 실패: {e}')

print()
print('=== 2. 압축 데이터 무결성 검증 ===')
ole = olefile.OleFileIO(out)
raw_out = ole.openstream('BodyText/Section0').read()
try:
    dec_out = zlib.decompress(raw_out, -15)
    print(f'  압축해제 성공: {len(raw_out):,} → {len(dec_out):,}')
except Exception as e:
    print(f'  ❌ 압축해제 실패: {e}')
    ole.close()
    exit(1)

def parse_records(data):
    records = []
    offset = 0
    while offset < len(data) - 4:
        raw = struct.unpack_from('<I', data, offset)[0]
        tag_id = raw & 0x3FF
        level = (raw >> 10) & 0x3FF
        size = (raw >> 20) & 0xFFF
        if size == 0xFFF:
            if offset + 8 > len(data): break
            size = struct.unpack_from('<I', data, offset + 4)[0]
            header_size = 8
        else:
            header_size = 4
        if offset + header_size + size > len(data): break
        records.append({'tag_id': tag_id, 'level': level, 'size': size})
        offset += header_size + size
    return records, offset

recs, end_off = parse_records(dec_out)
print(f'  레코드: {len(recs)}개, 끝 offset: {end_off:,}/{len(dec_out):,}, 잔여: {len(dec_out)-end_off}')

text_recs = [r for r in recs if r['tag_id'] == 67]
print(f'  텍스트 레코드: {len(text_recs)}개')
ole.close()

print()
print('=== 3. 원본과 출력 Section0 바이너리 비교 ===')
with open(src, 'rb') as f:
    d_s = f.read()
with open(out, 'rb') as f:
    d_o = f.read()

ole_s = olefile.OleFileIO(src)
ole_o = olefile.OleFileIO(out)

raw_s = ole_s.openstream('BodyText/Section0').read()
raw_o = ole_o.openstream('BodyText/Section0').read()

print(f'원본 압축데이터: {len(raw_s):,} bytes')
print(f'출력 압축데이터: {len(raw_o):,} bytes')

dec_s = zlib.decompress(raw_s, -15)
dec_o = zlib.decompress(raw_o, -15)
print(f'원본 해제데이터: {len(dec_s):,} bytes')
print(f'출력 해제데이터: {len(dec_o):,} bytes')

recs_s, _ = parse_records(dec_s)
recs_o, _ = parse_records(dec_o)
print(f'원본 레코드: {len(recs_s)}개')
print(f'출력 레코드: {len(recs_o)}개')

ole_s.close()
ole_o.close()

print()
print('=== 4. 파일 전체 바이너리 차이 분석 ===')
diff_count = 0
diff_ranges = []
in_diff = False
diff_start = 0
for i in range(min(len(d_s), len(d_o))):
    if d_s[i] != d_o[i]:
        if not in_diff:
            diff_start = i
            in_diff = True
        diff_count += 1
    else:
        if in_diff:
            diff_ranges.append((diff_start, i))
            in_diff = False
if in_diff:
    diff_ranges.append((diff_start, min(len(d_s), len(d_o))))

print(f'총 차이 바이트: {diff_count:,}')
print(f'차이 구간: {len(diff_ranges)}개')
for start, end in diff_ranges[:20]:
    print(f'  0x{start:06X}-0x{end:06X} ({end-start:,} bytes)')

print()
print('=== 5. Section0 섹터 데이터 직접 비교 ===')
ole_s2 = olefile.OleFileIO(src)
fat_s2 = ole_s2.fat
sid_s2 = ole_s2._find(['BodyText', 'Section0'])
entry_s2 = ole_s2.direntries[sid_s2]
chain_s2 = []
cur = entry_s2.isectStart
while cur >= 0 and cur < len(fat_s2):
    chain_s2.append(cur)
    cur = fat_s2[cur]
    if len(chain_s2) > 100000: break

ole_o2 = olefile.OleFileIO(out)
fat_o2 = ole_o2.fat
sid_o2 = ole_o2._find(['BodyText', 'Section0'])
entry_o2 = ole_o2.direntries[sid_o2]
chain_o2 = []
cur = entry_o2.isectStart
while cur >= 0 and cur < len(fat_o2):
    chain_o2.append(cur)
    cur = fat_o2[cur]
    if len(chain_o2) > 100000: break

print(f'원본 FAT 체인: {len(chain_s2)}개 섹터, start={entry_s2.isectStart}')
print(f'출력 FAT 체인: {len(chain_o2)}개 섹터, start={entry_o2.isectStart}')
print(f'FAT 체인 동일: {chain_s2 == chain_o2}')

sect_diffs = 0
for i in range(min(len(chain_s2), len(chain_o2))):
    off_s = 512 + chain_s2[i] * 512
    off_o = 512 + chain_o2[i] * 512
    if d_s[off_s:off_s+512] != d_o[off_o:off_o+512]:
        sect_diffs += 1

print(f'차이 섹터: {sect_diffs}/{min(len(chain_s2), len(chain_o2))}')

ole_s2.close()
ole_o2.close()

print()
print('=== 6. HWP 파일 직접 열기 테스트 ===')
hwp_exe = r'C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\Hwp.exe'
if os.path.exists(hwp_exe):
    try:
        proc = subprocess.Popen([hwp_exe, out])
        time.sleep(8)
        poll = proc.poll()
        if poll is None:
            print(f'  ✅ HWP 실행 중 (PID={proc.pid})')
        elif poll == 0:
            print(f'  HWP 정상 종료 (코드: 0)')
        else:
            print(f'  ⚠️ HWP 종료됨 (코드: {poll})')
    except Exception as e:
        print(f'  ❌ 실행 실패: {e}')
else:
    print(f'  HWP 실행 파일 없음')
