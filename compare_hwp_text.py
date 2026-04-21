import sys, os, time, re, struct, zlib
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
try:
    import olefile
except ImportError:
    olefile = None

def extract_text_from_hwp(filepath):
    """HWP 파일에서 텍스트 추출"""
    try:
        ole = olefile.OleFileIO(filepath, write_mode=False)
        streams = ole.listdir()

        # BodyText 스트림 찾기
        for sp in streams:
            if sp and sp[0] == "BodyText":
                raw = ole.openstream('/'.join(sp)).read()
                dec = zlib.decompress(raw, -15)
                ole.close()
                return dec.decode('utf-8', errors='ignore')

        ole.close()
        return ""
    except Exception as e:
        print(f"오류 발생: {e}")
        return ""

def analyze_text(text, label):
    """텍스트 분석"""
    print(f"\n{'='*60}")
    print(f"{label} 분석")
    print(f"{'='*60}")
    print(f"총 문자 수: {len(text):,}자")
    print(f"총 바이트 수: {len(text.encode('utf-8')):,}bytes")
    print(f"줄 수: {len(text.splitlines()):,}줄")
    print(f"공백 포함: {text.count(' '):,}개")

    # 긴 줄 분석
    lines = text.splitlines()
    long_lines = [l for l in lines if len(l) > 100]
    if long_lines:
        print(f"\n긴 줄 (100자 이상) {len(long_lines)}개:")
        for i, line in enumerate(long_lines[:10], 1):
            print(f"  {i}. [{len(line)}자] {line[:80]}...")

    # 짧은 줄 분석
    short_lines = [l for l in lines if len(l) > 0 and len(l) < 5]
    if short_lines:
        print(f"\n매우 짧은 줄 (5자 미만) {len(short_lines)}개:")
        for i, line in enumerate(short_lines[:20], 1):
            print(f"  {i}. [{len(line)}자] '{line}'")

    # 빈 줄 분석
    empty_lines = [l for l in lines if len(l) == 0]
    if empty_lines:
        print(f"\n빈 줄 {len(empty_lines)}개")

    return text

# 파일 경로
original_file = r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920.hwp"
modified_file = r"C:\Users\doris\xwechat_files\zhuchunyan331793_600e\msg\file\2026-04\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"

print("="*60)
print("HWP 파일 텍스트 추출 및 비교")
print("="*60)

# 원본 텍스트 추출
print("\n[1/2] 원본 파일 텍스트 추출 중...")
original_text = extract_text_from_hwp(original_file)
if original_text:
    analyze_text(original_text, "원본 파일")
else:
    print("원본 파일 텍스트 추출 실패!")

# 수정본 텍스트 추출
print("\n[2/2] 수정본 파일 텍스트 추출 중...")
modified_text = extract_text_from_hwp(modified_file)
if modified_text:
    analyze_text(modified_text, "수정본 파일")
else:
    print("수정본 파일 텍스트 추출 실패!")

# 비교 분석
print("\n" + "="*60)
print("비교 분석")
print("="*60)

original_len = len(original_text)
modified_len = len(modified_text)

print(f"\n문자 수 비교:")
print(f"  원본: {original_len:,}자")
print(f"  수정본: {modified_len:,}자")
print(f"  차이: {original_len - modified_len:,}자 ({((original_len - modified_len) / original_len * 100):.2f}%)")

# 내용 비교
original_lines = set(original_text.splitlines())
modified_lines = set(modified_text.splitlines())

only_in_original = original_lines - modified_lines
only_in_modified = modified_lines - original_lines

print(f"\n원본에만 있는 줄: {len(only_in_original)}개")
print(f"수정본에만 있는 줄: {len(only_in_modified)}개")

if only_in_original:
    print("\n[삭제된 내용 예시] (상위 30개):")
    for i, line in enumerate(list(only_in_original)[:30], 1):
        print(f"  {i}. {line[:100]}")

if only_in_modified:
    print("\n[추가된 내용 예시] (상위 30개):")
    for i, line in enumerate(list(only_in_modified)[:30], 1):
        print(f"  {i}. {line[:100]}")

# 퍼센트 일치 확인
common_ratio = len(original_lines & modified_lines) / len(original_lines) * 100
print(f"\n줄 단위 일치율: {common_ratio:.2f}%")

# 문장 단위 비교
sentences_original = re.split(r'[.!?。！？]', original_text)
sentences_modified = re.split(r'[.!?。！？]', modified_text)

# 빈 문장 제거
sentences_original = [s for s in sentences_original if len(s.strip()) > 0]
sentences_modified = [s for s in sentences_modified if len(s.strip()) > 0]

matched_sentences = 0
for sent in sentences_modified:
    sent_clean = sent.strip()
    if sent_clean and sent_clean in original_text:
        matched_sentences += 1

print(f"\n문장 단위 일치율: {matched_sentences}/{len(sentences_modified)} ({matched_sentences/len(sentences_modified)*100:.2f}%)")

print("\n" + "="*60)
print("분석 완료")
print("="*60)
