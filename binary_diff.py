import sys, os
OUT = r"c:\Users\doris\.agent-skills\L_output_new.hwp"
SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"

with open(SRC, 'rb') as f:
    src_data = f.read()

with open(OUT, 'rb') as f:
    out_data = f.read()

print(f"원본 크기: {len(src_data):,} bytes")
print(f"출력 크기: {len(out_data):,} bytes")
print(f"데이터 동일: {src_data == out_data}")

diff_positions = []
for i in range(min(len(src_data), len(out_data))):
    if src_data[i] != out_data[i]:
        diff_positions.append(i)
        if len(diff_positions) <= 30:
            print(f"위치 {i}: 원본=0x{src_data[i]:02X} 출력=0x{out_data[i]:02X}")

print(f"\n총 {len(diff_positions)}개 위치에서 차이")

if diff_positions:
    first_diff = diff_positions[0]
    print(f"\n첫 번째 차이 위치: {first_diff}")
    print(f"원본 위치 {first_diff} 주변: {src_data[first_diff-10:first_diff+20].hex()}")
    print(f"출력 위치 {first_diff} 주변: {out_data[first_diff-10:first_diff+20].hex()}")

    for i, pos in enumerate(diff_positions[:5]):
        sector = pos // 512
        offset = pos % 512
        print(f"\n차이 {i+1}: 바이트 위치 {pos} (섹터 {sector}, 오프셋 {offset})")
