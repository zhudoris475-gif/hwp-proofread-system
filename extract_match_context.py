# -*- coding: utf-8 -*-
"""
HWP 파일에서 오매치 의심 규칙의 실제 매치 문맥 추출
- hwp_ollama_proofread.py에서 필요한 함수 로직 직접 복사 (import 시 ValueError 방지)
- 오매치 의심 패턴(suspect_patterns)에 해당하는 규칙만 필터링하여 문맥 출력
"""
import os, sys, io, struct, zlib
from datetime import datetime

# UTF-8 콘솔 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

try:
    import olefile
except ImportError:
    olefile = None
    print("WARNING: olefile not installed, cannot extract HWP text")

# ==================== PROTECT_LIST 복사 (hwp_ollama_proofread.py에서 그대로 복사) ====================
PROTECT_LIST = [
    "것이다", "것입니다", "것이었다", "것이었나", "것이니",
    "것이라", "것이지", "것이네", "것임다",
    "것이야", "것이고", "것인데", "것이라서",
    "것이지만", "것이라면",
    "이것", "그것", "저것", "이것저것",
    "재수", "분수", "싹수", "요수", "차수", "간수", "본수",
    "수학", "수술", "수영", "수고", "수집", "수요",
    "부적", "적극", "적성", "적응", "적대", "적자", "적중",
    "적법", "적용", "적립", "적색", "적정", "적합", "적절",
    "지구", "지식", "지도", "지역", "지위", "지혜", "지진",
    "지시", "지배", "지름", "지향", "지점", "지출",
    "소중", "공중", "대중", "명중", "집중", "귀중", "궁중",
    "열중", "수중", "신중", "민중", "고중", "연중",
    "동안", "불안", "편안", "해안", "공안", "미안", "고안",
    "평안", "안정", "안전", "안심", "안내",
    "단위", "행위", "권위", "지위", "주위", "바위", "키위",
    "호위", "동위", "스위스", "상위", "하위", "최위",
    "산하", "강하", "천하", "지하", "수하", "문하", "연하", "진하",
    "뜻밖", "제대로", "그대로", "함께", "사뿐", "가듯",
    "말한대로", "짐작한대로", "환한대로", "가난한대로", "약속한대로",
    "경험한대로", "선택한대로", "결정한대로", "바란대로", "기대한대로",
    "생각한대로", "느낀대로", "본대로", "들은대로", "한대로",
    "할지어다", "할지라도", "할지니",
    "별의별것",
    "대·수수깡", "신부·유전학", "장중보옥·금지옥엽", "물건·쓸모없는", "시문·음악",
    "흉·복벽의", "기초작업·공사", "체재·출판년월일", "활동·운동의", "산지·西山",
    "5·4운동", "아시아·태평양", "나라·주", "열대·아열대",
    "는데", "은데", "인데",
    "한데", "편한데", "어려운데",
    "한적하다", "한가하다",
    "한지",
    "방안하다",
]

SECTION_HEADERS = {'띄어쓰기', '붙여쓰기'}

def is_protected(pattern):
    for p in PROTECT_LIST:
        if p in pattern:
            return True
    return False

def parse_rules(rules_file):
    rules = []
    seen = set()
    arrow_chars = [' -> ', chr(8594)]
    with open(rules_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            arrow = None
            for a in arrow_chars:
                if a in line:
                    arrow = a
                    break
            if arrow is None:
                continue
            parts = line.split(arrow)
            if len(parts) == 2:
                src = parts[0].strip()
                dst = parts[1].strip()
                if src in SECTION_HEADERS:
                    continue
                if src != dst and src not in seen:
                    seen.add(src)
                    rules.append((src, dst))
    return rules

# ==================== HWP 텍스트 추출 함수 복사 (hwp_ollama_proofread.py에서 직접 복사) ====================

def decompress_stream(data):
    for wbits in [-15, 15, 31]:
        try:
            return zlib.decompress(data, wbits)
        except:
            continue
    return None

def decompress_stream_incremental(data):
    for wbits in [-15, 15]:
        dc = zlib.decompressobj(wbits=wbits)
        result = b''
        for i in range(0, len(data), 65536):
            chunk = data[i:i + 65536]
            try:
                result += dc.decompress(chunk)
            except zlib.error:
                break
        try:
            result += dc.flush()
        except:
            pass
        if result:
            return result
    return None

def decompress_stream_multi_segment(data):
    for wbits in [-15, 15, 31]:
        try:
            return zlib.decompress(data, wbits)
        except:
            pass
    for start_off in range(0, min(len(data), 100000), 1024):
        dc = zlib.decompressobj(wbits=-15)
        result = b''
        for i in range(start_off, len(data), 65536):
            chunk = data[i:i + 65536]
            try:
                dec_chunk = dc.decompress(chunk)
                result += dec_chunk
            except zlib.error:
                break
        try:
            result += dc.flush()
        except:
            pass
        if len(result) > 10000:
            return result
    return None

def decompress_chain(data):
    dec = decompress_stream(data)
    if dec is not None:
        return dec
    dec = decompress_stream_incremental(data)
    if dec is not None:
        return dec
    dec = decompress_stream_multi_segment(data)
    return dec

def parse_records(data):
    records = []
    offset = 0
    while offset < len(data) - 4:
        raw = struct.unpack_from('<I', data, offset)[0]
        tag_id = raw & 0x3FF
        level = (raw >> 10) & 0x3FF
        size = (raw >> 20) & 0xFFF
        if size == 0xFFF:
            if offset + 8 > len(data):
                break
            size = struct.unpack_from('<I', data, offset + 4)[0]
            header_size = 8
        else:
            header_size = 4
        if offset + header_size + size > len(data):
            break
        payload = data[offset + header_size:offset + header_size + size]
        records.append({
            "tag_id": tag_id,
            "level": level,
            "payload": payload,
        })
        offset += header_size + size
    return records

def extract_text_from_hwp_binary(filepath):
    """HWP 바이너리에서 BodyText 추출 (olefile 사용)"""
    if olefile is None:
        return ""
    texts = []
    try:
        ole = olefile.OleFileIO(filepath, write_mode=False)
        try:
            streams = ole.listdir()
            body_streams = [s for s in streams if s and s[0] == "BodyText"]
            for stream_path in body_streams:
                stream_name = '/'.join(stream_path)
                raw = ole.openstream(stream_name).read()
                dec = decompress_chain(raw)
                if dec is None:
                    continue
                try:
                    records = parse_records(dec)
                except Exception:
                    continue
                parts = []
                for rec in records:
                    if rec.get("tag_id") != 67:
                        continue
                    try:
                        parts.append(rec["payload"].decode("utf-16-le", errors="replace"))
                    except Exception:
                        continue
                if parts:
                    texts.append(''.join(parts))
        finally:
            ole.close()
    except Exception as e:
        print(f"  [오류] {filepath}: {e}")
    return "\n".join(texts)


# ==================== 메인 로직 ====================

target_dir = r"C:\Users\51906\Desktop\사전"
txt_rules_file = r"C:\Users\51906\Desktop\rules_documentation.txt"
china_rules_file = r"C:\Users\51906\Desktop\rules_china_place.txt"

print("=" * 70)
print("HWP 오매치 의심 규칙 매치 문맥 추출")
print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# 규칙 로드
txt_rules = parse_rules(txt_rules_file)
china_rules = parse_rules(china_rules_file)
all_rules = txt_rules + china_rules
print(f"\nTXT 규칙: {len(txt_rules)}개, 중국 지명 규칙: {len(china_rules)}개, 총: {len(all_rules)}개")

# 오매치 의심 패턴
suspect_patterns = [
    "집안", "방안", "입안", "수밖", "줄밖", "문밖",
    "한적", "판적", "한지", "한데",
    "쓸데", "쓸수", "할바",
    "든것", "모든것", "인것",
    "두발", "한 발",
    "무엇인지",
    "살고있는",
]

# HWP 파일 목록 (backup, bak 제외)
hwp_files = []
for f in os.listdir(target_dir):
    if f.endswith('.hwp') and '.backup' not in f and not f.endswith('.bak'):
        hwp_files.append(f)

print(f"HWP 파일: {len(hwp_files)}개")
for f in sorted(hwp_files):
    print(f"  - {f[:60]}...")

# 파일별 텍스트 추출 및 매치 분석
print("\n" + "=" * 70)
print("텍스트 추출 및 매치 분석")
print("=" * 70)

# 결과 수집
results_match = []    # 정상 매치
results_false = []    # 오매치 의심
results_summary = {}  # 패턴별 요약

for fname in sorted(hwp_files):
    fpath = os.path.join(target_dir, fname)
    text = extract_text_from_hwp_binary(fpath)

    if not text:
        print(f"\n[{fname[:40]}] 텍스트 추출 실패 또는 빈 텍스트")
        continue

    text_len = len(text)
    print(f"\n[{fname[:40]}] 텍스트 {text_len}자 추출 완료")

    for src, dst in all_rules:
        if src not in text:
            continue
        if is_protected(src):
            continue

        # 오매치 의심 패턴인지 확인
        is_suspect = any(s in src for s in suspect_patterns)
        if not is_suspect:
            continue

        # 문맥 추출 (앞뒤 30자)
        idx = 0
        contexts = []
        while True:
            pos = text.find(src, idx)
            if pos == -1:
                break
            start = max(0, pos - 30)
            end = min(len(text), pos + len(src) + 30)
            ctx_before = text[start:pos].replace('\n', ' ').replace('\r', '')
            ctx_match = text[pos:pos+len(src)]
            ctx_after = text[pos+len(src):end].replace('\n', ' ').replace('\r', '')
            contexts.append((ctx_before, ctx_match, ctx_after))
            idx = pos + 1
            if len(contexts) >= 5:  # 최대 5개까지만
                break

        if contexts:
            entry = {
                'file': fname[:30],
                'src': src,
                'dst': dst,
                'count': len(contexts),
                'contexts': contexts
            }

            # 오매치 판별 로직
            false_match = False
            for before, match, after in contexts:
                # 집안: "집안에" 등 가정 의미면 오매치
                if src == "집안" and ("에" in after[:3] or "의" in after[:3] or "에서" in after[:4] or "으로" in after[:4]):
                    false_match = True
                # 방안: "방안에" 등 방 내부 의미면 오매치
                if src == "방안" and ("에" in after[:3] or "의" in after[:3] or "에서" in after[:4]):
                    false_match = True
                # 입안: "입안에" 등 입 안쪽 의미면 오매치
                if src == "입안" and ("에" in after[:3] or "으로" in after[:4]):
                    false_match = True
                # 한데: "더운 한데" "추운 한데" 등은 정상, "한데" 단독은 의심
                if src == "한데" and ("춥" in before or "덥" in before or "어렵" in before):
                    false_match = False
                # 한지: 지명/인명이면 오매치
                if src == "한지" and ("의" in after[:3] or "에서" in after[:4] or "에" in after[:3]):
                    false_match = True
                # 무엇인지: 정상 조합
                if src == "무엇인지":
                    false_match = True
                # 살고있는: 정상 표현
                if src == "살고있는":
                    false_match = True
                # 든것, 모든것, 인것: 문맥 확인
                if src in ("든것", "모든것", "인것"):
                    false_match = True
                # 쓸데, 쓸수: 문맥 확인
                if src == "쓸데" and ("없" in after[:5] or "있" in after[:5]):
                    false_match = True
                if src == "쓸수" and ("있" in after[:5]):
                    false_match = True

            if false_match:
                results_false.append(entry)
            else:
                results_match.append(entry)

            # 패턴별 요약
            key = f"'{src}' -> '{dst}'"
            if key not in results_summary:
                results_summary[key] = {'match': 0, 'false': 0, 'contexts': []}
            if false_match:
                results_summary[key]['false'] += len(contexts)
            else:
                results_summary[key]['match'] += len(contexts)
            results_summary[key]['contexts'].extend(contexts[:3])

# ==================== 결과 출력 ====================
print("\n" + "=" * 70)
print("결과 요약")
print("=" * 70)

if results_false:
    print(f"\n[오매치 의심] {len(results_false)}건")
    print("-" * 60)
    for entry in results_false:
        print(f"\n  파일: {entry['file']}")
        print(f"  규칙: '{entry['src']}' -> '{entry['dst']}' ({entry['count']}개)")
        for i, (before, match, after) in enumerate(entry['contexts'], 1):
            print(f"    [{i}] ...{before}[{match}]{after}...")
else:
    print("\n[오매치 의심] 0건")

if results_match:
    print(f"\n[정상 매치] {len(results_match)}건")
    print("-" * 60)
    for entry in results_match:
        print(f"\n  파일: {entry['file']}")
        print(f"  규칙: '{entry['src']}' -> '{entry['dst']}' ({entry['count']}개)")
        for i, (before, match, after) in enumerate(entry['contexts'], 1):
            print(f"    [{i}] ...{before}[{match}]{after}...")
else:
    print("\n[정상 매치] 0건")

# 패턴별 요약
print("\n" + "=" * 70)
print("패턴별 요약")
print("=" * 70)
for key, info in sorted(results_summary.items()):
    total = info['match'] + info['false']
    status = "오매치" if info['false'] > info['match'] else ("정상" if info['match'] > info['false'] else "혼합")
    print(f"  {key}: 총 {total}개 (정상 {info['match']}, 오매치 의심 {info['false']}) -> [{status}]")

print("\n" + "=" * 70)
print("완료")
print("=" * 70)
