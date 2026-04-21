import sys, os, time, re, struct, zlib
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
try:
    import olefile
except ImportError:
    olefile = None

def analyze_hwp_header(filepath, label):
    """HWP 헤더 구조 직접 분석"""
    print(f"\n{'='*70}")
    print(f"{label} - HWP 헤더 구조 분석")
    print(f"{'='*70}")

    try:
        ole = olefile.OleFileIO(filepath, write_mode=False)
        streams = ole.listdir()

        # BodyText 스트림 분석
        for sp in streams:
            if sp and sp[0] == "BodyText":
                stream_name = '/'.join(sp) if len(sp) > 1 else 'BodyText'
                raw = ole.openstream(stream_name).read()
                print(f"\n{stream_name} 스트림 크기: {len(raw):,} bytes")

                # 첫 100바이트 직접 분석
                print(f"\n[1] 첫 100바이트 직접 분석:")
                for i in range(0, min(100, len(raw)), 4):
                    chunk = raw[i:i+4]
                    if len(chunk) < 4:
                        break

                    # 4바이트씩 읽기
                    val1 = struct.unpack('<I', chunk)[0]
                    chunk2 = raw[i+4:i+8] if i+8 <= len(raw) else chunk[4:]
                    val2 = struct.unpack('<H', chunk2[:2])[0] if len(chunk2) >= 2 else 0
                    val3 = struct.unpack('<H', chunk2[2:4])[0] if len(chunk2) >= 4 else 0

                    print(f"  Offset {i:4d}: {chunk.hex():12s} = 0x{val1:08X}, 타입=0x{val2:04X}, 미사용=0x{val3:04X}")

                # HWP 레코드 구조 찾기
                print(f"\n[2] 레코드 구조 찾기:")

                # HWP 5.0 레코드 헤더 포맷:
                # [4 bytes] Length (little endian)
                # [2 bytes] Record Type (little endian)
                # [2 bytes] Unknown

                records = []
                pos = 0

                while pos < len(raw):
                    if pos + 4 > len(raw):
                        break

                    # 첫 4바이트 읽기
                    length_bytes = raw[pos:pos+4]
                    rec_len = struct.unpack('<I', length_bytes)[0]

                    # 값이 너무 크면 잘못된 헤더
                    if rec_len > len(raw) - pos:
                        print(f"  ⚠️  잘못된 헤더: pos={pos}, rec_len={rec_len}, 남은={len(raw)-pos}")
                        # 다음 바이트부터 다시 시도
                        pos += 1
                        continue

                    # 타입 추출
                    if rec_len >= 6:
                        rec_type = struct.unpack('<H', raw[pos+4:pos+6])[0]
                        unknown = struct.unpack('<H', raw[pos+6:pos+8])[0]

                        records.append({
                            'pos': pos,
                            'length': rec_len,
                            'type': rec_type,
                            'unknown': unknown,
                            'data': raw[pos+8:pos+8+rec_len]
                        })

                        print(f"  레코드 {len(records):3d}: pos={pos:6d}, 길이={rec_len:7d}, 타입=0x{rec_type:04X}, 미사용=0x{unknown:04X}, 데이터={raw[pos+8:pos+20].hex()[:30]}...")

                        pos += 4 + rec_len
                    else:
                        # 길이가 너무 작음
                        pos += 1

                    if len(records) >= 50:
                        print(f"  ... (상위 50개 레코드까지)")
                        break

                print(f"\n[3] 레코드 타입 분포:")
                type_counts = {}
                for rec in records:
                    type_name = f"0x{rec['type']:04X}"
                    type_counts[type_name] = type_counts.get(type_name, 0) + 1

                for type_name, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {type_name}: {count}개")

                # 텍스트 레코드 추출 (타입 0x0001)
                print(f"\n[4] 텍스트 레코드 추출 (타입 0x0001):")
                text_records = []

                for i, rec in enumerate(records):
                    if rec['type'] == 0x0001:
                        text_records.append(rec)
                        try:
                            text = rec['data'].decode('utf-8', errors='ignore')
                            if text.strip():
                                print(f"  레코드 {i+1}: '{text[:60]}...'")
                        except:
                            pass

                print(f"  텍스트 레코드 수: {len(text_records)}개")

                # 텍스트 추출
                all_text = ""
                for rec in text_records:
                    try:
                        text = rec['data'].decode('utf-8', errors='ignore')
                        all_text += text
                    except:
                        pass

                print(f"\n[5] 추출된 텍스트:")
                print(f"  총 길이: {len(all_text):,}자")
                print(f"  줄 수: {len(all_text.splitlines()):,}줄")
                print(f"  샘플: {all_text[:500]}")

                ole.close()
                return all_text

        ole.close()
        return ""

    except Exception as e:
        print(f"  ❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return ""

# 파일 경로
original_file = r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920.hwp"
modified_file = r"C:\Users\doris\xwechat_files\zhuchunyan331793_600e\msg\file\2026-04\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"

print("="*70)
print("HWP 헤더 구조 분석 및 비교")
print("="*70)

original_text = analyze_hwp_header(original_file, "원본 파일")
modified_text = analyze_hwp_header(modified_file, "수정본 파일")

print(f"\n{'='*70}")
print("비교 분석")
print(f"{'='*70}")

if original_text and modified_text:
    print(f"\n원본: {len(original_text):,}자")
    print(f"수정본: {len(modified_text):,}자")
    print(f"차이: {len(original_text) - len(modified_text):,}자")

    original_lines = original_text.splitlines()
    modified_lines = modified_text.splitlines()

    only_in_original = [l for l in original_lines if l and l not in modified_lines]
    only_in_modified = [l for l in modified_lines if l and l not in original_lines]

    print(f"\n삭제된 줄: {len(only_in_original)}개")
    for i, line in enumerate(only_in_original[:20], 1):
        print(f"  {i}. {line[:100]}")

    print(f"\n추가된 줄: {len(only_in_modified)}개")
    for i, line in enumerate(only_in_modified[:20], 1):
        print(f"  {i}. {line[:100]}")

print(f"\n{'='*70}")
print("완료")
print(f"{'='*70}")
