import olefile, struct, zlib, os

src = r'C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp'

out_files = [r'c:\Users\doris\.agent-skills\L_output_new.hwp', r'c:\Users\doris\.agent-skills\L_output.hwp']
out = None
for f in out_files:
    if os.path.exists(f):
        out = f
        break

if not out:
    print('출력 파일 없음!')
    exit()

print(f'출력 파일: {out}')
print(f'파일 크기: {os.path.getsize(out):,}')
print()

ole = olefile.OleFileIO(out, write_mode=False)
stream_list = ole.listdir()
stream_map = {}
for sp in stream_list:
    sn = '/'.join(sp)
    stream_map[sp[-1]] = sn

print('=== olefile 스트림 목록 ===')
for sp in stream_list:
    sn = '/'.join(sp)
    raw = ole.openstream(sn).read()
    try:
        dec = zlib.decompress(raw, -15)
        print(f'  {sn}: 압축={len(raw):,}, 해제={len(dec):,}')
    except:
        print(f'  {sn}: 압축={len(raw):,} (압축아님)')

ole.close()

print()
print('=== 디렉토리 엔트리 분석 (출력 파일) ===')
with open(out, 'rb') as f:
    data = f.read()

ole = olefile.OleFileIO(out, write_mode=False)
fat = ole.fat
sector_size = ole.sector_size

dir_start = struct.unpack_from('<I', data, 48)[0]
current = dir_start
chain = []
while current >= 0 and current < len(fat) and len(chain) < 100:
    chain.append(current)
    current = fat[current]

for sect in chain:
    sect_offset = sector_size + sect * sector_size
    for i in range(sector_size // 128):
        entry_offset = sect_offset + i * 128
        name_len = struct.unpack_from('<H', data, entry_offset + 64)[0]
        if name_len > 0 and name_len <= 64:
            name = data[entry_offset:entry_offset + name_len].decode('utf-16-le', errors='replace')
            obj_type = data[entry_offset + 66]
            start_sect = struct.unpack_from('<I', data, entry_offset + 116)[0]
            size_low = struct.unpack_from('<I', data, entry_offset + 120)[0]
            size_high = struct.unpack_from('<I', data, entry_offset + 124)[0]
            total_size = size_low + (size_high << 32)
            print(f'  [{sect}:{i}] "{name}" type={obj_type} size={total_size:,} start={start_sect} offset=0x{entry_offset:X}')

ole.close()

print()
print('=== 원본 vs 출력 Section0 디렉토리 엔트리 비교 ===')
for label, filepath in [('원본', src), ('출력', out)]:
    with open(filepath, 'rb') as f:
        d = f.read()
    ole_tmp = olefile.OleFileIO(filepath, write_mode=False)
    fat_tmp = ole_tmp.fat
    dir_s = struct.unpack_from('<I', d, 48)[0]
    cur = dir_s
    ch = []
    while cur >= 0 and cur < len(fat_tmp) and len(ch) < 100:
        ch.append(cur)
        cur = fat_tmp[cur]
    
    for sect in ch:
        sect_off = 512 + sect * 512
        for i in range(512 // 128):
            eo = sect_off + i * 128
            nl = struct.unpack_from('<H', d, eo + 64)[0]
            if nl > 0 and nl <= 64:
                nm = d[eo:eo + nl].decode('utf-16-le', errors='replace')
                if nm == 'Section0':
                    sl = struct.unpack_from('<I', d, eo + 120)[0]
                    sh = struct.unpack_from('<I', d, eo + 124)[0]
                    ss = struct.unpack_from('<I', d, eo + 116)[0]
                    print(f'  {label} Section0: offset=0x{eo:X}, size_low={sl:,}, size_high={sh}, start_sector={ss}')
                    print(f'    size_bytes = {d[eo+120:eo+128].hex()}')
    ole_tmp.close()

print()
print('=== 압축 데이터 끝 확인 ===')
ole1 = olefile.OleFileIO(src, write_mode=False)
ole2 = olefile.OleFileIO(out, write_mode=False)

raw1 = ole1.openstream('BodyText/Section0').read()
raw2 = ole2.openstream('BodyText/Section0').read()

dec1 = zlib.decompress(raw1, -15)
dec2 = zlib.decompress(raw2, -15)

print(f'원본: 압축={len(raw1):,}, 해제={len(dec1):,}')
print(f'출력: 압축={len(raw2):,}, 해제={len(dec2):,}')

last1 = 0
for i in range(len(raw1)-1, -1, -1):
    if raw1[i] != 0:
        last1 = i
        break
last2 = 0
for i in range(len(raw2)-1, -1, -1):
    if raw2[i] != 0:
        last2 = i
        break

print(f'원본 마지막 non-null: {last1:,} (0x{last1:X})')
print(f'출력 마지막 non-null: {last2:,} (0x{last2:X})')
print(f'원본 끝 20바이트: {raw1[-20:].hex()}')
print(f'출력 끝 20바이트: {raw2[-20:].hex()}')

rec1 = 0
off = 0
while off < len(dec1) - 4:
    r = struct.unpack_from('<I', dec1, off)[0]
    s = (r >> 20) & 0xFFF
    hs = 4
    if s == 0xFFF:
        s = struct.unpack_from('<I', dec1, off + 4)[0]
        hs = 8
    if off + hs + s > len(dec1):
        break
    rec1 += 1
    off += hs + s

rec2 = 0
off = 0
while off < len(dec2) - 4:
    r = struct.unpack_from('<I', dec2, off)[0]
    s = (r >> 20) & 0xFFF
    hs = 4
    if s == 0xFFF:
        s = struct.unpack_from('<I', dec2, off + 4)[0]
        hs = 8
    if off + hs + s > len(dec2):
        break
    rec2 += 1
    off += hs + s

print(f'원본 레코드: {rec1}개')
print(f'출력 레코드: {rec2}개')

ole1.close()
ole2.close()

print()
print('=== 핵심 진단: olefile로 읽은 압축크기 vs 디렉토리 엔트리 size ===')
for label, filepath in [('원본', src), ('출력', out)]:
    ole_t = olefile.OleFileIO(filepath, write_mode=False)
    raw_t = ole_t.openstream('BodyText/Section0').read()
    
    with open(filepath, 'rb') as f:
        d_t = f.read()
    fat_t = ole_t.fat
    dir_s = struct.unpack_from('<I', d_t, 48)[0]
    cur = dir_s
    ch = []
    while cur >= 0 and cur < len(fat_t) and len(ch) < 100:
        ch.append(cur)
        cur = fat_t[cur]
    
    for sect in ch:
        sect_off = 512 + sect * 512
        for i in range(512 // 128):
            eo = sect_off + i * 128
            nl = struct.unpack_from('<H', d_t, eo + 64)[0]
            if nl > 0 and nl <= 64:
                nm = d_t[eo:eo + nl].decode('utf-16-le', errors='replace')
                if nm == 'Section0':
                    dir_size = struct.unpack_from('<I', d_t, eo + 120)[0]
                    print(f'  {label}: olefile_read={len(raw_t):,}, dir_entry_size={dir_size:,}, 차이={len(raw_t)-dir_size:,}')
                    if len(raw_t) != dir_size:
                        print(f'    *** 불일치! ***')
    ole_t.close()
