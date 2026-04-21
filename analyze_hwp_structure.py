import sys, os, time, re, struct, zlib
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
try:
    import olefile
except ImportError:
    olefile = None

def analyze_hwp_record_structure(filepath):
    """HWP 레코드 구조 분석"""
    print("="*70)
    print("HWP 레코드 구조 분석")
    print("="*70)

    try:
        ole = olefile.OleFileIO(filepath, write_mode=False)
        streams = ole.listdir()

        print(f"\n[1] OLE 스트림 구조:")
        for stream in streams:
            print(f"  - {stream}")

        # BodyText 스트림 분석
        for sp in streams:
            if sp and sp[0] == "BodyText":
                print(f"\n[2] BodyText/{sp[1] if len(sp) > 1 else 'Section0'} 스트림 분석:")
                raw = ole.openstream('/'.join(sp)).read()
                print(f"  전체 크기: {len(raw):,} bytes")

                # 레코드 파싱
                records = []
                pos = 0
                record_count = 0

                while pos < len(raw):
                    if pos + 4 > len(raw):
                        break

                    # 레코드 헤더 (4 bytes)
                    header = raw[pos:pos+4]
                    rec_len = struct.unpack('<I', header)[0]

                    if rec_len == 0:
                        pos += 4
                        continue

                    if pos + rec_len > len(raw):
                        print(f"  ⚠️  레코드 길이 오류: pos={pos}, rec_len={rec_len}, 파일크기={len(raw)}")
                        break

                    # 레코드 데이터
                    rec_data = raw[pos+4:pos+4+rec_len]
                    records.append({
                        'header': header,
                        'length': rec_len,
                        'data': rec_data
                    })

                    pos += 4 + rec_len
                    record_count += 1

                    if record_count >= 100:  # 상위 100개만 분석
                        print(f"  상위 100개 레코드까지 분석 (총 {len(raw):,} bytes)")
                        break

                print(f"  레코드 수: {record_count:,}")

                # 레코드 타입 분석
                print(f"\n[3] 레코드 타입별 분포:")

                # 첫 번째 레코드 헤더 분석 (타입 추정)
                if records:
                    first_header = records[0]['header']
                    print(f"  첫 레코드 헤더: {first_header.hex()}")

                    # 레코드 타입 추정 (HWP 버전 5.0)
                    # Header: [4 bytes] Length
                    # Type: byte[2] (little endian)
                    # Unknown: byte[2]

                    type_bytes = records[0]['data'][:2]
                    print(f"  추정 타입 바이트: {type_bytes.hex()}")

                    # 유명한 HWP 레코드 타입들
                    text_record_types = {
                        0x0001: "텍스트 레코드 (TEXT)",
                        0x0002: "텍스트 속성 레코드 (PROP)",
                        0x0003: "글꼴 정보 레코드 (FONT)",
                        0x0004: "그룹 레코드 (GRP)",
                        0x0005: "문단 정보 레코드 (PARA)",
                        0x0006: "문자 속성 레코드 (CHAR)",
                        0x0007: "테이블 레코드 (TABLE)",
                        0x0008: "그림 레코드 (PICTURE)",
                        0x0009: "하이퍼링크 레코드 (HYPERLINK)",
                        0x000A: "객체 레코드 (OBJECT)",
                        0x0010: "문자 모양 레코드 (CHARFORM)",
                        0x0011: "문단 모양 레코드 (PARAFORM)",
                        0x0012: "글꼴 모양 레코드 (FONTFORM)",
                    }

                    for type_code, type_name in text_record_types.items():
                        if type_bytes == type_code.to_bytes(2, 'little'):
                            print(f"  ✅ 타입 확인: {type_name}")
                            break
                    else:
                        print(f"  ⚠️  알 수 없는 타입")

                # 텍스트 레코드 추출 시도
                print(f"\n[4] 텍스트 레코드 추출 시도:")

                text_records = []
                for i, rec in enumerate(records[:50]):  # 상위 50개 레코드
                    header_hex = rec['header'].hex()
                    data_preview = rec['data'][:20].hex()

                    # 타입 추정
                    if len(rec['data']) >= 2:
                        type_bytes = rec['data'][:2].hex()
                        print(f"  레코드 {i+1}: 길이={rec['length']}, 헤더={header_hex}, 타입={type_bytes}, 데이터={data_preview}...")

                        # 텍스트 레코드 타입 판별
                        if type_bytes == "0001":
                            text_records.append(rec)
                            try:
                                text = rec['data'][2:].decode('utf-8', errors='ignore')
                                if text.strip():
                                    print(f"    → 텍스트 레코드: '{text[:50]}...'")
                            except:
                                pass

                print(f"\n  텍스트 레코드 수: {len(text_records)}개")

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
                print(f"\n  텍스트 샘플 (상위 500자):")
                print(f"  {all_text[:500]}")

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
print("\n[원본 파일 분석]")
original_text = analyze_hwp_record_structure(original_file)

# 수정본 파일 분석
print("\n\n[수정본 파일 분석]")
modified_text = analyze_hwp_record_structure(modified_file)

# 비교 분석
print("\n" + "="*70)
print("비교 분석")
print("="*70)

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
        print(f"\n[삭제된 내용] (상위 20개):")
        for i, line in enumerate(only_in_original[:20], 1):
            print(f"  {i}. {line[:100]}")

    if only_in_modified:
        print(f"\n[추가된 내용] (상위 20개):")
        for i, line in enumerate(only_in_modified[:20], 1):
            print(f"  {i}. {line[:100]}")

print("\n" + "="*70)
print("분석 완료")
print("="*70)
