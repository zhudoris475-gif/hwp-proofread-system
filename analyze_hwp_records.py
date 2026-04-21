import sys, os, time, re, struct, zlib
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
try:
    import olefile
except ImportError:
    olefile = None

def analyze_hwp_records(filepath, label):
    """HWP 레코드 구조 분석 (올바른 헤더 포맷)"""
    print(f"\n{'='*70}")
    print(f"{label} - HWP 레코드 구조 분석")
    print(f"{'='*70}")

    try:
        ole = olefile.OleFileIO(filepath, write_mode=False)
        streams = ole.listdir()

        print(f"\n[1] OLE 스트림 구조:")
        for stream in streams:
            print(f"  - {stream}")

        # BodyText 스트림 분석
        for sp in streams:
            if sp and sp[0] == "BodyText":
                stream_name = '/'.join(sp) if len(sp) > 1 else 'BodyText'
                print(f"\n[2] {stream_name} 스트림 분석:")
                raw = ole.openstream(stream_name).read()
                print(f"  전체 크기: {len(raw):,} bytes")

                # HWP 레코드 헤더 포맷 (HWP 5.0)
                # Header: [4 bytes] Length (little endian)
                # Type: [2 bytes] Record Type (little endian)
                # Unknown: [2 bytes]

                records = []
                pos = 0
                record_count = 0

                while pos < len(raw):
                    if pos + 4 > len(raw):
                        break

                    # 레코드 길이 (little endian)
                    rec_len = struct.unpack('<I', raw[pos:pos+4])[0]

                    if rec_len == 0:
                        pos += 4
                        continue

                    if rec_len > len(raw) - pos - 4:
                        print(f"  ⚠️  레코드 길이 오류: pos={pos}, rec_len={rec_len}, 남은={len(raw)-pos}")
                        break

                    # 레코드 데이터
                    rec_data = raw[pos+4:pos+4+rec_len]

                    # 타입 추출
                    rec_type = 0
                    if len(rec_data) >= 2:
                        rec_type = struct.unpack('<H', rec_data[:2])[0]

                    records.append({
                        'pos': pos,
                        'length': rec_len,
                        'type': rec_type,
                        'data': rec_data
                    })

                    pos += 4 + rec_len
                    record_count += 1

                    if record_count >= 100:
                        print(f"  상위 100개 레코드까지 분석")
                        break

                print(f"  레코드 수: {record_count:,}")

                # 레코드 타입 분포
                print(f"\n[3] 레코드 타입 분포 (상위 30개):")
                type_counts = {}

                for i, rec in enumerate(records[:30]):
                    type_name = f"타입{rec['type']:04X}"
                    type_counts[type_name] = type_counts.get(type_name, 0) + 1

                    data_preview = rec['data'][:15].hex()
                    print(f"  레코드 {i+1:3d}: 길이={rec['length']:7d}, 타입={rec['type']:04X} ({type_name:15s}), 데이터={data_preview}...")

                print(f"\n  타입별 빈도:")
                for type_name, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"    {type_name}: {count}개")

                # 텍스트 레코드 추출 (타입 0x0001은 일반 텍스트)
                print(f"\n[4] 텍스트 레코드 추출 (타입 0x0001):")
                text_records = []

                for i, rec in enumerate(records[:100]):
                    if rec['type'] == 0x0001:
                        text_records.append(rec)
                        try:
                            # 타입 바이트 제외하고 텍스트 추출
                            text = rec['data'][2:].decode('utf-8', errors='ignore')
                            if text.strip():
                                print(f"  레코드 {i+1}: '{text[:60]}...'")
                        except:
                            pass

                print(f"  텍스트 레코드 수: {len(text_records)}개")

                # 텍스트 레코드에서 실제 텍스트 추출
                print(f"\n[5] 실제 텍스트 추출:")
                all_text = ""
                for rec in text_records:
                    try:
                        text = rec['data'][2:].decode('utf-8', errors='ignore')
                        all_text += text
                    except:
                        pass

                print(f"  추출된 텍스트: {len(all_text):,}자")
                print(f"  줄 수: {len(all_text.splitlines()):,}줄")

                # 텍스트 샘플 출력
                if all_text:
                    print(f"\n  텍스트 샘플 (상위 800자):")
                    print(f"  {all_text[:800]}")

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
print("HWP 레코드 구조 분석 및 비교")
print("="*70)

# 원본 파일 분석
original_text = analyze_hwp_records(original_file, "원본 파일")

# 수정본 파일 분석
modified_text = analyze_hwp_records(modified_file, "수정본 파일")

# 비교 분석
print(f"\n{'='*70}")
print("비교 분석")
print(f"{'='*70}")

if original_text and modified_text:
    print(f"\n원본 텍스트 길이: {len(original_text):,}자")
    print(f"수정본 텍스트 길이: {len(modified_text):,}자")
    print(f"차이: {len(original_text) - len(modified_text):,}자 ({(len(original_text) - len(modified_text)) / len(original_text) * 100:.2f}%)")

    # 줄 단위 비교
    original_lines = original_text.splitlines()
    modified_lines = modified_text.splitlines()

    only_in_original = [l for l in original_lines if l and l not in modified_lines]
    only_in_modified = [l for l in modified_lines if l and l not in original_lines]

    print(f"\n원본에만 있는 줄: {len(only_in_original)}개")
    print(f"수정본에만 있는 줄: {len(only_in_modified)}개")

    if only_in_original:
        print(f"\n[삭제된 내용] (상위 30개):")
        for i, line in enumerate(only_in_original[:30], 1):
            print(f"  {i}. {line[:120]}")

    if only_in_modified:
        print(f"\n[추가된 내용] (상위 30개):")
        for i, line in enumerate(only_in_modified[:30], 1):
            print(f"  {i}. {line[:120]}")

    # 공통 내용 확인
    common_lines = [l for l in original_lines if l in modified_lines]
    print(f"\n공통 줄: {len(common_lines):,}개 ({len(common_lines)/len(original_lines)*100:.2f}%)")

print(f"\n{'='*70}")
print("분석 완료")
print(f"{'='*70}")
