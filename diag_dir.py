import olefile, struct

src = r'C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp'

with open(src, 'rb') as f:
    data = f.read()

ole = olefile.OleFileIO(src, write_mode=False)
fat = ole.fat

dir_start = struct.unpack_from('<I', data, 48)[0]
print(f"디렉토리 시작 섹터: {dir_start}")

current = dir_start
chain = []
while current >= 0 and current < len(fat) and len(chain) < 100:
    chain.append(current)
    current = fat[current]
print(f"디렉토리 섹터 체인: {chain}")

for sect in chain:
    sect_offset = 512 + sect * 512
    for i in range(512 // 128):
        entry_offset = sect_offset + i * 128
        name_len = struct.unpack_from('<H', data, entry_offset + 64)[0]
        if name_len > 0 and name_len <= 64:
            name = data[entry_offset:entry_offset + name_len].decode('utf-16-le', errors='replace')
            obj_type = data[entry_offset + 66]
            size_low = struct.unpack_from('<I', data, entry_offset + 120)[0]
            start_sect = struct.unpack_from('<I', data, entry_offset + 116)[0]
            print(f"  [{sect}:{i}] offset={entry_offset} (0x{entry_offset:X}) name=\"{name}\" type={obj_type} size={size_low:,} start={start_sect}")

ole.close()
