import sys, os, time, re, struct, zlib
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
try:
    import olefile
except ImportError:
    olefile = None

def parse_records(data):
    """HWP 레코드 파싱 (실제 구조)"""
    records = []
    offset = 0

    while offset < len(data) - 4:
        raw = struct.unpack('<I', data[offset:offset+4])[0]
        tag_id = raw & 0x3FF
        level = (raw >> 10) & 0x3FF
        size = (raw >> 20) & 0xFFF

        if size == 0xFFF:
            if offset + 8 > len(data):
                break
            size = struct.unpack('<I', data[offset+4:offset+8])[0]
            header_size = 8
        else:
            header_size = 4

        if offset + header_size + size > len(data):
            break

        payload = data[offset + header_size:offset + header_size + size]
        records.append({
            "tag_id": tag_id,
            "level": level,
            "size": size,
            "payload": payload
        })

        offset += header_size + size

    return records

def extract_text_from_hwp(filepath, label):
    """HWP에서 텍스트 추출"""
    print(f"\n{'='*70}")
    print(f"{label} - HWP 텍스트 추출")
    print(f"{'='*70}")

    try:
        ole = olefile.OleFileIO(filepath, write_mode=False)
        streams = ole.listdir()

        # BodyText 스트림 분석
        for sp in streams:
            if sp and sp[0] == "BodyText":
                stream_name = '/'.join(sp) if len(sp) > 1 else 'BodyText'
                raw = ole.openstream(stream_name).read()
                print(f"\n{stream_name} 스트림: {len(raw):,} bytes")

                # 압축 해제
                try:
                    dec = zlib.decompress(raw, -15)
                    print(f"  압축 해제: {len(raw):,} → {len(dec):,} bytes")
                except zlib.error as e:
                    print(f"  ⚠️  압축 해제 실패: {e}")
                    ole.close()
                    return ""

                # 레코드 파싱
                records = parse_records(dec)
                print(f"  레코드 수: {len(records):,}")

                # 텍스트 레코드 추출 (tag_id = 67은 텍스트 레코드)
                print(f"\n  텍스트 레코드 추출 (tag_id=67):")

                text_records = []
                for i, rec in enumerate(records):
                    if rec.get("tag_id") == 67:
                        text_records.append(rec)
                        try:
                            text = rec["payload"].decode("utf-16-le", errors="replace")
                            if text.strip():
                                text_records[-1]['text'] = text
                                print(f"    레코드 {i+1}: '{text[:50]}...'")
                        except Exception as e:
                            pass

                print(f"  텍스트 레코드 수: {len(text_records)}개")

                # 텍스트 추출
                all_text = ""
                for rec in text_records:
                    if 'text' in rec:
                        all_text += rec['text']

                print(f"\n  추출된 텍스트:")
                print(f"    길이: {len(all_text):,}자")
                print(f"    줄 수: {len(all_text.splitlines()):,}줄")
                print(f"    샘플: {all_text[:300]}")

                ole.close()
                return all_text

        ole.close()
        return ""

    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return ""

def compare_texts(original_text, modified_text):
    """텍스트 비교"""
    print(f"\n{'='*70}")
    print("비교 분석")
    print(f"{'='*70}")

    print(f"\n원본: {len(original_text):,}자")
    print(f"수정본: {len(modified_text):,}자")
    print(f"차이: {len(original_text) - len(modified_text):,}자 ({(len(original_text) - len(modified_text)) / len(original_text) * 100:.2f}%)")

    original_lines = original_text.splitlines()
    modified_lines = modified_text.splitlines()

    only_in_original = [l for l in original_lines if l and l not in modified_lines]
    only_in_modified = [l for l in modified_lines if l and l not in original_lines]

    print(f"\n[삭제된 줄] {len(only_in_original)}개")
    if only_in_original:
        print(f"삭제된 내용 (상위 30개):")
        for i, line in enumerate(only_in_original[:30], 1):
            print(f"  {i}. {line[:120]}")

    print(f"\n[추가된 줄] {len(only_in_modified)}개")
    if only_in_modified:
        print(f"추가된 내용 (상위 30개):")
        for i, line in enumerate(only_in_modified[:30], 1):
            print(f"  {i}. {line[:120]}")

    # 공통 내용
    common_lines = [l for l in original_lines if l in modified_lines]
    print(f"\n공통 줄: {len(common_lines):,}개 ({len(common_lines)/len(original_lines)*100:.2f}%)")

    # 문장 단위 비교
    sentences_orig = re.split(r'[.!?。！？]', original_text)
    sentences_mod = re.split(r'[.!?。！？]', modified_text)
    sentences_orig = [s for s in sentences_orig if len(s.strip()) > 0]
    sentences_mod = [s for s in sentences_mod if len(s.strip()) > 0]

    matched = 0
    for sent in sentences_mod:
        if sent.strip() in original_text:
            matched += 1

    print(f"\n문장 일치율: {matched}/{len(sentences_mod)} ({matched/len(sentences_mod)*100:.2f}%)")

# 파일 경로
original_file = r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920.hwp"
modified_file = r"C:\Users\doris\xwechat_files\zhuchunyan331793_600e\msg\file\2026-04\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"

print("="*70)
print("HWP 텍스트 추출 및 비교")
print("="*70)

original_text = extract_text_from_hwp(original_file, "원본 파일")
modified_text = extract_text_from_hwp(modified_file, "수정본 파일")

if original_text and modified_text:
    compare_texts(original_text, modified_text)

print(f"\n{'='*70}")
print("완료")
print(f"{'='*70}")
