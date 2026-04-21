import olefile, struct, zlib, os

src = r'C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp'
out = r'c:\Users\doris\.agent-skills\L_output_new.hwp'

print('=== 1. OLE 헤더 비교 ===')
with open(src, 'rb') as f:
    h_s = f.read(512)
with open(out, 'rb') as f:
    h_o = f.read(512)

print(f'파일크기: 원본={os.path.getsize(src):,}, 출력={os.path.getsize(out):,}')
print(f'매직넘버: 원본={h_s[:8].hex()}, 출력={h_o[:8].hex()}')
print(f'헤더 동일: {h_s == h_o}')

if h_s != h_o:
    diffs = []
    for i in range(512):
        if h_s[i] != h_o[i]:
            diffs.append((i, h_s[i], h_o[i]))
    print(f'  차이 {len(diffs)}개:')
    for off, v_s, v_o in diffs[:20]:
        print(f'    @ {off} (0x{off:X}): 원본=0x{v_s:02X}, 출력=0x{v_o:02X}')

print()
print('=== 2. OLE 헤더 상세 (출력 파일) ===')
ver_min = struct.unpack_from('<H', h_o, 24)[0]
ver_maj = struct.unpack_from('<H', h_o, 26)[0]
sect_pow = struct.unpack_from('<H', h_o, 30)[0]
fat_count = struct.unpack_from('<I', h_o, 44)[0]
dir_start = struct.unpack_from('<I', h_o, 48)[0]
mini_cutoff = struct.unpack_from('<I', h_o, 56)[0]
mini_fat_start = struct.unpack_from('<I', h_o, 60)[0]
mini_fat_count = struct.unpack_from('<I', h_o, 64)[0]
difat_start = struct.unpack_from('<I', h_o, 68)[0]
difat_count = struct.unpack_from('<I', h_o, 72)[0]
print(f'  버전: {ver_maj}.{ver_min}')
print(f'  섹터크기: 2^{sect_pow} = {1 << sect_pow}')
print(f'  FAT 섹터 수: {fat_count}')
print(f'  첫 디렉토리 섹터: {dir_start}')
print(f'  미니스트림 컷오프: {mini_cutoff}')
print(f'  첫 미니FAT 섹터: {mini_fat_start}')
print(f'  미니FAT 섹터 수: {mini_fat_count}')
print(f'  첫 DIFAT 섹터: {difat_start}')
print(f'  DIFAT 섹터 수: {difat_count}')

print()
print('=== 3. FAT 체인 검증: Section0 ===')
ole = olefile.OleFileIO(out)
fat = ole.fat
sector_size = ole.sector_size

sp = ['BodyText', 'Section0']
sid = ole._find(sp)
entry = ole.direntries[sid]
stream_size = entry.size
start_sector = entry.isectStart
print(f'  sid={sid}, size={stream_size:,}, start_sector={start_sector}')

chain = []
current = start_sector
while current >= 0 and current < len(fat):
    chain.append(current)
    current = fat[current]
    if len(chain) > 100000:
        break

print(f'  FAT 체인: {len(chain)}개 섹터')
print(f'  체인으로 커버: {len(chain) * sector_size:,} bytes')
print(f'  디렉토리 size: {stream_size:,} bytes')
needed = (stream_size + sector_size - 1) // sector_size
print(f'  필요 섹터: {needed}')
print(f'  여유 섹터: {len(chain) - needed}')

last_sect = chain[-1]
print(f'  마지막 섹터: {last_sect}, FAT값: {fat[last_sect]} (EOF=-2)')

with open(out, 'rb') as f:
    last_offset = sector_size + last_sect * sector_size
    f.seek(last_offset)
    last_data = f.read(sector_size)

non_null_end = sector_size
for i in range(sector_size - 1, -1, -1):
    if last_data[i] != 0:
        non_null_end = i + 1
        break
print(f'  마지막 섹터 유효데이터: {non_null_end} bytes')

print()
print('=== 4. 모든 디렉토리 엔트리 비교 ===')
with open(src, 'rb') as f:
    d_s = f.read()
with open(out, 'rb') as f:
    d_o = f.read()

ole_s = olefile.OleFileIO(src)
ole_o = olefile.OleFileIO(out)

fat_s = ole_s.fat
fat_o = ole_o.fat
dir_start_s = struct.unpack_from('<I', d_s, 48)[0]
dir_start_o = struct.unpack_from('<I', d_o, 48)[0]

def get_dir_chain(data, fat, start):
    ch = []
    cur = start
    while cur >= 0 and cur < len(fat):
        ch.append(cur)
        cur = fat[cur]
        if len(ch) > 100:
            break
    return ch

chain_s = get_dir_chain(d_s, fat_s, dir_start_s)
chain_o = get_dir_chain(d_o, fat_o, dir_start_o)

print(f'원본 디렉토리 체인: {chain_s}')
print(f'출력 디렉토리 체인: {chain_o}')

entries_per_sect = sector_size // 128
for label, data, fat_t, chain in [('원본', d_s, fat_s, chain_s), ('출력', d_o, fat_o, chain_o)]:
    print(f'\n  [{label} 디렉토리 엔트리]')
    idx = 0
    for sect in chain:
        sect_offset = sector_size + sect * sector_size
        for i in range(entries_per_sect):
            eo = sect_offset + i * 128
            name_len = struct.unpack_from('<H', data, eo + 64)[0]
            obj_type = data[eo + 66]
            if name_len > 0 and name_len <= 64:
                name = data[eo:eo + name_len].decode('utf-16-le', errors='replace')
                start_sect = struct.unpack_from('<I', data, eo + 116)[0]
                size_low = struct.unpack_from('<I', data, eo + 120)[0]
                size_high = struct.unpack_from('<I', data, eo + 124)[0]
                child_id = struct.unpack_from('<I', data, eo + 76)[0]
                left_id = struct.unpack_from('<I', data, eo + 68)[0]
                right_id = struct.unpack_from('<I', data, eo + 72)[0]
                print(f'    [{idx}] name="{name}" type={obj_type} start={start_sect} size={size_low:,} size_h={size_high} child={child_id} left={left_id} right={right_id}')
            idx += 1

ole_s.close()
ole_o.close()

print()
print('=== 5. 원본 vs 출력 Section0 디렉토리 엔트리 직접 비교 ===')
for label, data, fat_t, chain in [('원본', d_s, fat_s, chain_s), ('출력', d_o, fat_o, chain_o)]:
    for sect in chain:
        sect_offset = sector_size + sect * sector_size
        for i in range(entries_per_sect):
            eo = sect_offset + i * 128
            name_len = struct.unpack_from('<H', data, eo + 64)[0]
            if name_len > 0 and name_len <= 64:
                name = data[eo:eo + name_len].decode('utf-16-le', errors='replace')
                if name == 'Section0':
                    print(f'  [{label}] offset=0x{eo:X}')
                    for field, foff in [('name_len', 64), ('type', 66), ('color', 67), ('left', 68), ('right', 72), ('child', 76), ('start_sect', 116), ('size_low', 120), ('size_high', 124)]:
                        if foff in [64]:
                            val = struct.unpack_from('<H', data, eo + foff)[0]
                        elif foff == 66 or foff == 67:
                            val = data[eo + foff]
                        else:
                            val = struct.unpack_from('<I', data, eo + foff)[0]
                        print(f'    {field}: {val}')

print()
print('=== 6. olefile로 읽은 크기 vs 디렉토리 엔트리 크기 ===')
for label, filepath in [('원본', src), ('출력', out)]:
    ole_t = olefile.OleFileIO(filepath)
    raw_t = ole_t.openstream('BodyText/Section0').read()
    with open(filepath, 'rb') as f:
        d_t = f.read()
    fat_t = ole_t.fat
    dir_s = struct.unpack_from('<I', d_t, 48)[0]
    ch = get_dir_chain(d_t, fat_t, dir_s)
    for sect in ch:
        sect_off = sector_size + sect * sector_size
        for i in range(entries_per_sect):
            eo = sect_off + i * 128
            nl = struct.unpack_from('<H', d_t, eo + 64)[0]
            if nl > 0 and nl <= 64:
                nm = d_t[eo:eo + nl].decode('utf-16-le', errors='replace')
                if nm == 'Section0':
                    dir_size = struct.unpack_from('<I', d_t, eo + 120)[0]
                    print(f'  {label}: olefile_read={len(raw_t):,}, dir_entry_size={dir_size:,}, match={len(raw_t)==dir_size}')
    ole_t.close()
