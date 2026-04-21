import os

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
bak_path = hwp_path + ".bak"

for label, path in [("교정후", hwp_path), ("원본백업", bak_path)]:
    with open(path, "rb") as f:
        header = f.read(32)
        f.seek(0, 2)
        size = f.tell()
    print(f"{label}: {path}")
    print(f"  크기: {size:,} bytes")
    print(f"  헤더(hex): {header[:16].hex()}")
    ascii_repr = header[:8].decode("ascii", errors="replace")
    print(f"  헤더(ascii): {ascii_repr}")
    if header[:4] == b"\xd0\xcf\x11\xe0":
        print(f"  형식: OLE (정상 HWP)")
    else:
        print(f"  형식: 비정상!")
    print()
