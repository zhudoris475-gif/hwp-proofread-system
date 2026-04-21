# -*- coding: utf-8 -*-
import os, sys, io, json, time, shutil, re, struct, subprocess, zlib

try:
    import requests
except ImportError:
    requests = None
    import urllib.request
    import urllib.error

try:
    import olefile
except ImportError:
    olefile = None

from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "hwp_ollama_proofread_log.txt")
RULES_FILE = os.path.join(SCRIPT_DIR, "rules_documentation.txt")
CHINA_PLACE_FILE = os.path.join(SCRIPT_DIR, "rules_china_place.txt")
REGEX_FILE = os.path.join(SCRIPT_DIR, "rules_regex.txt")
REGEX_ENABLED = False
LEGACY_HWP_DIR = r"C:\Users\51906\Desktop\next"
REPORT_DIR = os.path.join(SCRIPT_DIR, "reports")

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "korean-corrector:latest"
OLLAMA_DOT_TIMEOUT = 300
OLLAMA_QUOTE_TIMEOUT = 300
OLLAMA_FALLBACK_MODELS = [
    "qwen2.5:7b",
    "qwen3b-korean-spacing:latest",
    "qwen3b-spacing:latest",
    "llama3.2:latest",
]
_OLLAMA_MODEL_CACHE = {"resolved": None, "names": None}

LDQ = '\u201c'
RDQ = '\u201d'
LSQ = '\u2018'
RSQ = '\u2019'

FORCE_SINGLE_QUOTE_TERMS = {
    "欧洲安全和合作会议",
    "欧洲共同体",
    "欧洲联盟",
    "欧洲共同市场",
    "欧洲大战",
    "欧洲煤钢联营",
    "欧洲原子能联营",
    "欧洲经济共同体",
    "欧洲经济共同体(共同市场)",
}

SECTION_HEADERS = {'띄어쓰기', '붙여쓰기'}

PROTECT_LIST = [
    # 대명사 (띄어쓰기 불가)
    "이것", "그것", "저것", "이것저것",
    # 하 한자어 오매치 (산하=산 아래, 강하=강 아래)
    "산하", "강하",
    # 관용구
    "뜻밖", "제대로", "그대로", "함께", "사뿐", "가듯",
    "그만큼", "뜻대로", "마음대로",
    # 가운데점 유지 (비병렬/합성명사/수식/관용구/의학/분야)
    "대·수수깡", "신부·유전학", "장중보옥·금지옥엽", "물건·쓸모없는", "시문·음악",
    "흉·복벽의", "기초작업·공사", "체재·출판년월일", "활동·운동의", "산지·西山",
    "5·4운동", "아시아·태평양", "나라·주", "열대·아열대",
    # 연결어미 (~는데 등)
    "는데", "은데", "인데",
    # 한데 오매치 (연결어미 -ㄴ데와 충돌)
    "한데",
    # 한대로 오매치 방지
    "한대로",
    # 한적 오매치 방지 (한가하다/한적하다, 한적한 곳)
    "한적하다", "한가하다", "한적한", "한적이",
    # 한지 오매치 방지 (기간: 입대한지, 거뿐한지, 충분한지)
    "한지",
    # 판적 오매치 방지 (비판적, 갑판적, 맹목적)
    "판적",
    # 두발 오매치 방지 (신체: 앞발, 진두발)
    "두발",
    # 할지 오매치 (고어)
    "할지", "할지어다", "할지라도", "할지니",
    # 별것 오매치 방지 (별의별것)
    "별의별것",
    # 방안 오매치 방지 (합성명사 + 단독)
    "방안", "방안하다", "체포방안", "구급방안", "설계방안", "한어병음방안",
    "방안을", "방안이", "방안은", "방안도",
    # 집안 오매치 방지 (가정/가문 + 단독)
    "집안", "집안살림", "한집안", "집안일", "집안사람",
    "집안이", "집안을", "집안은", "집안도", "집안에",
    # 쓸데 오매치 방지 (쓸데없다 관용구)
    "쓸데없는", "쓸데없이", "쓸데없다",
    # 무엇인지 오매치 방지 (한 단어)
    "무엇인지",
    # 살고있는 오매치 방지 (보조용언 결합)
    "살고있는",
    # 알데 오매치 방지 (화학물질명: 세네시알데히드)
    "알데",
    # 간적 오매치 방지 (시간적/공간적)
    "간적",
    # 본적 오매치 방지 (원적/기본적)
    "본적",
    # 간지 오매치 방지 (간지대/육십간지)
    "간지",
    # 산들바 오매치 방지 (산들바람)
    "산들바",
    # 산지 오매치 방지 (산이 있는 곳, 원산지, 산지·西山)
    "산지",
    # 쓸수 오매치 방지 (보조용언 결합: 쓸수 있다)
    "쓸수있다", "쓸수없다", "쓸수있으나", "쓸수없음",
    # 입안 오매치 방지 (신체 부위)
    "입안에", "입안이", "입안을",
]


def bootstrap_log(message):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [부트스트랩] {message}")


def is_32bit_python():
    return struct.calcsize("P") == 4


def parse_python_launcher_32bit(stdout_text):
    candidates = []
    for line in stdout_text.splitlines():
        line = line.strip()
        if "-32" not in line:
            continue
        m = re.search(r'-V:(?P<version>[0-9.]+-32)\s+\*?\s*(?P<path>[A-Za-z]:\\.*?python\.exe)\s*$', line, re.IGNORECASE)
        if not m:
            continue
        version_text = m.group("version").replace("-32", "")
        version_key = tuple(int(part) for part in version_text.split(".") if part.isdigit())
        candidates.append((version_key, m.group("path").strip()))
    candidates.sort(reverse=True)
    return [path for _, path in candidates]


def find_32bit_python():
    py_launcher = shutil.which("py")
    if not py_launcher:
        return None
    try:
        result = subprocess.run(
            [py_launcher, "-0p"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            check=False,
        )
    except Exception:
        return None

    candidates = parse_python_launcher_32bit(result.stdout or "")
    return candidates[0] if candidates else None


def maybe_relaunch_with_32bit_python():
    if sys.platform != 'win32':
        return
    if is_32bit_python():
        return
    if os.environ.get("HWP_ALREADY_RELAUNCHED_32BIT") == "1":
        return
    if "--no-32bit-reexec" in sys.argv[1:]:
        bootstrap_log("`--no-32bit-reexec` 옵션으로 자동 32비트 전환을 건너뜁니다.")
        return

    py32 = find_32bit_python()
    if not py32:
        bootstrap_log("32비트 Python을 찾지 못해 현재 인터프리터로 계속 진행합니다.")
        return

    current_python = os.path.abspath(sys.executable).lower()
    target_python = os.path.abspath(py32).lower()
    if current_python == target_python:
        return

    bootstrap_log(f"64비트 Python 감지: {sys.executable}")
    bootstrap_log(f"32비트 Python으로 재실행: {py32}")
    cmd = [py32, os.path.abspath(__file__)] + sys.argv[1:]
    env = os.environ.copy()
    env["HWP_ALREADY_RELAUNCHED_32BIT"] = "1"
    try:
        completed = subprocess.run(cmd, env=env, check=False)
    except Exception as e:
        bootstrap_log(f"32비트 재실행 실패: {e}")
        return
    raise SystemExit(completed.returncode)


def resolve_default_hwp_dir():
    candidates = [
        os.environ.get("HWP_DIR", "").strip(),
        os.getcwd(),
        SCRIPT_DIR,
        LEGACY_HWP_DIR,
    ]
    for path in candidates:
        if path and os.path.isdir(path):
            return os.path.abspath(path)
    return SCRIPT_DIR


def log(msg, fh=None):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    if fh:
        try:
            fh.write(line + "\n")
            fh.flush()
        except:
            pass


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


def load_china_place_rules():
    return parse_rules(CHINA_PLACE_FILE)


def load_regex_rules():
    if not REGEX_ENABLED:
        return []
    if not os.path.exists(REGEX_FILE):
        return []
    rules = []
    with open(REGEX_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ' -> ' not in line:
                continue
            parts = line.split(' -> ', 1)
            if len(parts) == 2:
                pattern = parts[0].strip()
                replacement = parts[1].strip()
                for sep in ['  # ', '\t#']:
                    idx = replacement.find(sep)
                    if idx >= 0:
                        replacement = replacement[:idx].strip()
                if replacement.endswith('  #'):
                    replacement = replacement[:-3].strip()
                # 역참조 \1 -> \\1 변환 (re.sub용)
                replacement = replacement.replace('\\1', '\x01REF1\x01').replace('\\2', '\x01REF2\x01').replace('\\3', '\x01REF3\x01')
                replacement = replacement.replace('\x01REF1\x01', '\\1').replace('\x01REF2\x01', '\\2').replace('\x01REF3\x01', '\\3')
                has_group_ref = bool(re.search(r'\\\d', replacement))
                has_meta = bool(re.search(r'[()\\[\]{}*+?|^$]', pattern))
                if not has_meta and not has_group_ref:
                    continue
                if ' ' in pattern and ' ' not in replacement:
                    continue
                try:
                    re.compile(pattern)
                    rules.append((pattern, replacement))
                except re.error as e:
                    print(f"  [정규식 오류] '{pattern}': {e}")
    # 긴 패턴 우선 매치 (할수있다가 할수보다 먼저 매치되도록)
    rules.sort(key=lambda r: len(r[0]), reverse=True)
    return rules


# 산하/강하 오매치: 단독으로만 매칭 (합성어 내 부분매칭 방지)
_PROTECT_EXACT = {"산하", "강하"}

def is_protected(pattern):
    for p in PROTECT_LIST:
        if p in _PROTECT_EXACT:
            # 단어 경계 매칭: 앞에 한글이 오면 안됨
            idx = pattern.find(p)
            while idx != -1:
                if idx == 0 or not pattern[idx-1].isalpha():
                    return True
                idx = pattern.find(p, idx + 1)
        else:
            if p in pattern:
                return True
    return False


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


def compress_to_size(data, target_size):
    for level in range(1, 10):
        co = zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=-15)
        compressed = co.compress(data) + co.flush()
        if len(compressed) <= target_size:
            return compressed + b'\x00' * (target_size - len(compressed))
    return None


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


def serialize_records(records):
    buf = bytearray()
    for rec in records:
        tag_id = rec["tag_id"]
        level = rec["level"]
        payload = rec["payload"]
        size = len(payload)
        if size < 0xFFF:
            hdr = (size << 20) | (level << 10) | tag_id
            buf += struct.pack('<I', hdr)
        else:
            hdr = (0xFFF << 20) | (level << 10) | tag_id
            buf += struct.pack('<II', hdr, size)
        buf += payload
    return bytes(buf)


def extract_text_from_hwp_binary(filepath, log_fh=None):
    if olefile is None:
        raise RuntimeError("olefile 모듈이 없습니다.")

    texts = []
    ole = olefile.OleFileIO(filepath, write_mode=False)
    try:
        streams = ole.listdir()
        body_streams = [s for s in streams if s and s[0] == "BodyText"]
        log(f"  바이너리 본문 추출: BodyText 스트림 {len(body_streams)}개", log_fh)

        for stream_path in body_streams:
            stream_name = '/'.join(stream_path)
            raw = ole.openstream(stream_name).read()
            dec = decompress_chain(raw)
            if dec is None:
                log(f"  {stream_name}: 압축 해제 실패", log_fh)
                continue

            try:
                records = parse_records(dec)
            except Exception as e:
                log(f"  {stream_name}: 레코드 파싱 실패 - {e}", log_fh)
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

    return "\n".join(texts)


def ollama_is_available():
    return resolve_ollama_model() is not None


def get_ollama_model_names(force_refresh=False):
    if not force_refresh and _OLLAMA_MODEL_CACHE["names"] is not None:
        return list(_OLLAMA_MODEL_CACHE["names"])
    try:
        if requests:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
            if r.status_code != 200:
                return []
            data = r.json()
        else:
            req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status != 200:
                    return []
                data = json.loads(resp.read().decode('utf-8'))
    except Exception:
        return []

    models = data.get("models", []) if isinstance(data, dict) else []
    names = []
    for item in models:
        if not isinstance(item, dict):
            continue
        for key in ("name", "model"):
            value = str(item.get(key, "")).strip()
            if value and value not in names:
                names.append(value)
    _OLLAMA_MODEL_CACHE["names"] = names
    return list(names)


def resolve_ollama_model(force_refresh=False):
    if not force_refresh and _OLLAMA_MODEL_CACHE["resolved"]:
        return _OLLAMA_MODEL_CACHE["resolved"]

    available_names = get_ollama_model_names(force_refresh=force_refresh)
    if not available_names:
        _OLLAMA_MODEL_CACHE["resolved"] = None
        return None

    candidates = [OLLAMA_MODEL] + [m for m in OLLAMA_FALLBACK_MODELS if m != OLLAMA_MODEL]
    for candidate in candidates:
        if candidate in available_names:
            _OLLAMA_MODEL_CACHE["resolved"] = candidate
            return candidate

    _OLLAMA_MODEL_CACHE["resolved"] = available_names[0]
    return available_names[0]


def get_ollama_message_text(response_json):
    if not isinstance(response_json, dict):
        return ""
    msg = response_json.get("message")
    if isinstance(msg, dict):
        content = msg.get("content")
        if isinstance(content, str):
            return content
    content = response_json.get("response")
    if isinstance(content, str):
        return content
    return ""


def normalize_ollama_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = [str(v).strip() for v in value if str(v).strip()]
        return ",".join(parts)
    return str(value).strip()


def post_ollama_chat(payload, timeout=120, max_retries=2):
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            if requests:
                r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=timeout)
                data = r.json()
                if isinstance(data, dict) and data.get("error"):
                    raise RuntimeError(str(data.get("error")))
                return data
            req = urllib.request.Request(
                f"{OLLAMA_URL}/api/chat",
                data=json.dumps(payload).encode('utf-8'),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if isinstance(data, dict) and data.get("error"):
                    raise RuntimeError(str(data.get("error")))
                return data
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(5 * (attempt + 1))
    raise last_error


def parse_ollama_json_array(resp_text):
    all_items = []
    seen_keys = set()
    start = resp_text.find('[')
    while start >= 0:
        depth = 0
        parsed = None
        for i in range(start, len(resp_text)):
            if resp_text[i] == '[':
                depth += 1
            elif resp_text[i] == ']':
                depth -= 1
                if depth == 0:
                    try:
                        parsed = json.loads(resp_text[start:i + 1])
                    except json.JSONDecodeError:
                        parsed = None
                    break
        if isinstance(parsed, list):
            for item in parsed:
                if not isinstance(item, dict):
                    continue
                key = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                all_items.append(item)
        start = resp_text.find('[', start + 1)

    if all_items:
        return all_items

    start = resp_text.find('[')
    if start < 0:
        return []
    depth = 0
    for i in range(start, len(resp_text)):
        if resp_text[i] == '[':
            depth += 1
        elif resp_text[i] == ']':
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(resp_text[start:i + 1])
                except json.JSONDecodeError:
                    break
    end = resp_text.rfind(']') + 1
    if end > start:
        try:
            return json.loads(resp_text[start:end])
        except json.JSONDecodeError:
            pass
    return []


def is_dot_related_rule(orig, repl=""):
    return any(ch in orig or ch in repl for ch in ("·", "•", "・"))


def build_dot_parallel_candidate_pattern():
    # 순수 한글 병렬 나열을 넓게 잡되, 한글 덩어리 내부 부분매치는 피한다.
    return re.compile(r'(?<![가-힣])[가-힣]{1,20}(?:·[가-힣]{1,20}){1,7}(?![가-힣])')


def collect_rule_based_dot_corrections(text, log_fh=None):
    corrections = []
    seen = set()
    token_hist = {}
    # 순수 한글 2단어 이상 병렬 나열은 규칙으로 먼저 쉼표 교정한다.
    pattern = build_dot_parallel_candidate_pattern()
    candidate_count = 0
    for match in pattern.finditer(text):
        orig = match.group(0)
        if orig in seen:
            continue
        seen.add(orig)
        candidate_count += 1
        token_count = orig.count('·') + 1
        token_hist[token_count] = token_hist.get(token_count, 0) + 1
        log(f"  [가운데점-병렬 후보 {token_count}단어]: '{orig}'", log_fh)
        if any(token and token in orig for token in PROTECT_LIST):
            log(f"  [가운데점-규칙 유지]: '{orig}' (보호어 예외)", log_fh)
            continue
        corr = orig.replace('·', ',')
        if orig == corr:
            continue
        corrections.append((orig, corr))
        log(f"  [가운데점-규칙 교정]: '{orig}' -> '{corr}' ({token_count}단어 병렬 나열)", log_fh)
    if candidate_count:
        log(f"  [가운데점-규칙 후보 수]: {candidate_count}개", log_fh)
        for token_count in sorted(token_hist):
            log(f"  [가운데점-규칙 후보 {token_count}단어]: {token_hist[token_count]}개", log_fh)
    if corrections:
        log(f"  [가운데점-규칙 요약]: {len(corrections)}개", log_fh)
    return corrections


def collect_dot_corrections_with_ollama(text, log_fh=None, prehandled_dot_items=None):
    corrections = []
    dot_contexts = []
    for dot in ["·", "•", "・"]:
        for m in re.finditer(r'.{0,15}' + re.escape(dot) + r'.{0,15}', text):
            ctx = m.group().strip()
            if ctx and ctx not in dot_contexts:
                dot_contexts.append(ctx)

    if not dot_contexts:
        log("  가운데점 대상 없음", log_fh)
        return corrections

    phonetic_pattern = re.compile(r'[a-z]\d*[·•・]|[·•・][a-z]\d*', re.IGNORECASE)
    filtered = []
    excluded_phonetics = []
    for ctx in dot_contexts:
        if phonetic_pattern.search(ctx):
            excluded_phonetics.append(ctx)
        else:
            filtered.append(ctx)

    log(f"  가운데점 문맥 발견: {len(dot_contexts)}개 (발음기호 제외: {len(filtered)}개)", log_fh)
    for i, ctx in enumerate(filtered[:50]):
        log(f"    [{i + 1}] {ctx}", log_fh)
    if len(filtered) > 50:
        log(f"    ... 외 {len(filtered) - 50}개 생략", log_fh)
    if excluded_phonetics:
        log(f"  [가운데점 제외-발음기호]: {len(excluded_phonetics)}개", log_fh)
        for i, ctx in enumerate(excluded_phonetics[:20]):
            log(f"    [발음기호 제외 {i + 1}] {ctx}", log_fh)
        if len(excluded_phonetics) > 20:
            log(f"    ... 외 {len(excluded_phonetics) - 20}개 생략", log_fh)

    # 3단계 핵심: 순수 한글 병렬 2~4개 단어는 Ollama 여부와 무관하게 규칙으로 우선 교정한다.
    log("  [3단계 기준] 순수 한글 병렬 2~4개 단어는 Ollama와 무관하게 규칙 우선 교정", log_fh)
    prehandled_dot_items = [item for item in (prehandled_dot_items or []) if item]
    prehandled_contexts = []
    working_filtered = []
    for ctx in filtered:
        if any(item in ctx for item in prehandled_dot_items):
            prehandled_contexts.append(ctx)
        else:
            working_filtered.append(ctx)
    if prehandled_dot_items:
        log(f"  [가운데점 선반영 항목]: {len(prehandled_dot_items)}개", log_fh)
        for item in prehandled_dot_items[:30]:
            log(f"    [선반영 항목] {item}", log_fh)
        if len(prehandled_dot_items) > 30:
            log(f"    ... 외 {len(prehandled_dot_items) - 30}개 생략", log_fh)
    if prehandled_contexts:
        log(f"  [가운데점 선반영 문맥 제외]: {len(prehandled_contexts)}개", log_fh)
        for ctx in prehandled_contexts[:30]:
            log(f"    [선반영 문맥 제외] {ctx}", log_fh)
        if len(prehandled_contexts) > 30:
            log(f"    ... 외 {len(prehandled_contexts) - 30}개 생략", log_fh)

    rule_based_corrections = collect_rule_based_dot_corrections(text, log_fh)
    corrections.extend(rule_based_corrections)
    rule_based_originals = {orig for orig, _ in rule_based_corrections}
    resolved_model = resolve_ollama_model()
    if not resolved_model:
        log("  Ollama 미실행 - 3단계는 규칙 교정만 적용", log_fh)
        log(
            f"  가운데점 교정 결과: {len(corrections)}개 교정 / {len(filtered)}개 검토 문맥 중 "
            f"(전체 {len(dot_contexts)}개, 발음기호 제외 {len(excluded_phonetics)}개)",
            log_fh,
        )
        return corrections

    ollama_candidates = []
    rule_based_contexts = []
    for ctx in working_filtered:
        if any(orig in ctx for orig in rule_based_originals):
            rule_based_contexts.append(ctx)
        else:
            ollama_candidates.append(ctx)
    if rule_based_contexts:
        log(f"  [가운데점 규칙-선반영 문맥 제외]: {len(rule_based_contexts)}개", log_fh)

    max_ctx = 4
    ollama_rule_signature = (
        "가운데점-Ollama 규칙셋: 2~4개 병렬 나열 최우선, 병렬+따위/등/뿐, "
        "단위/수량 유지, 발음기호 유지, 비병렬 연결 유지, "
        "책제목/편명 유지, 한자 포함 유지"
    )
    log(f"  [Ollama 규칙셋명]: {ollama_rule_signature}", log_fh)
    log(f"  [Ollama 사용 모델]: {resolved_model}", log_fh)
    log(
        f"  [Ollama 참고 규칙 파일]: "
        f"{os.path.basename(CHINA_PLACE_FILE)}, "
        f"{os.path.basename(RULES_FILE)}, "
        f"{os.path.basename(REGEX_FILE)}",
        log_fh,
    )
    all_untouched_contexts = []
    attempt_success = False
    for attempt in range(3):
        batch = ollama_candidates[:max_ctx]
        if not batch:
            break
        batch_payload = [{"id": i + 1, "context": ctx} for i, ctx in enumerate(batch)]
        dot_list = json.dumps(batch_payload, ensure_ascii=False, indent=2)
        dot_prompt = f"""당신은 조선어 교정 전문가입니다.

[규칙셋명]
{ollama_rule_signature}

[참고 규칙 파일]
- 중한 규칙: {os.path.basename(CHINA_PLACE_FILE)}
- TXT 통합규칙: {os.path.basename(RULES_FILE)}
- 정규식 규칙: {os.path.basename(REGEX_FILE)}

가운데점(·, •, ・) 교정 규칙:

	1. **병렬 단어 나열** (특히 2~4개 동등 단어는 무조건 우선 교정): 가운데점 → 쉼표(,)로 변경
	   - 서울·부산 → 서울,부산
	   - 사랑·평화·행복 → 사랑,평화,행복
	   - 정치·경제·사회·문화 → 정치,경제,사회,문화
	   - 금전·재화따위 → 금전,재화따위
	1a. **병렬+따위/등/뿐**: 병렬 단어 뒤에 따위/등/뿐이 붙어도 쉼표 사용
	   - 권리·의무따위 → 권리,의무따위
	   - 사과·배·포도등 → 사과,배,포도등
	   - 구상·수식·풍격을 → 구상,수식,풍격을
	   - 구상·수식·풍격 → 구상,수식,풍격
	   - 닭·칠면조·메추라기따위를 → 닭,칠면조,메추라기따위를
	   - 불만·원한따위가 → 불만,원한따위가
	   - 의견·주장따위가 → 의견,주장따위가
	   - 금·은·백금이외의 → 금,은,백금이외의
	   - 문집·시집따위가 → 문집,시집따위가
	   - 신문·잡지따위 → 신문,잡지따위
	   - 사진·필림따위를 → 사진,필림따위를
	   - 담장·건물사이의 → 담장,건물사이의
	   - 동정·배려따위를 → 동정,배려따위를
	   - 전선·전화선따위를 → 전선,전화선따위를
	   - 난로·벽따위를 → 난로,벽따위를
	   - 간악·절도·사악·음행의 → 간악,절도,사악,음행의
	   - 새·짐승·물고기·자라 → 새,짐승,물고기,자라
	   - 책상·의자사이의 → 책상,의자사이의
	   - 단어·문장뜻은 → 단어,문장뜻은
   - 마오쩌둥·저우언라이 → 모택동·주은래
	2a. **2~4개 단어+따위/때/사이**: 병렬 단어(2~4개) 뒤에 따위/때/사이가 붙어도 쉼표 사용
	   - 구상·수식따위 → 구상,수식따위
	   - 정치·경제때 → 정치,경제때
	   - 담장·건물사이 → 담장,건물사이
	   - 사과·배따위 → 사과,배따위
	   - 산·들때 → 산,들때
	   - 집·나무사이 → 집,나무사이
	   - 정치·경제·사회·문화때 → 정치,경제,사회,문화때
3. **단위/수량 구분**: 단위 사이 가운데점은 유지
   - 3·5미터 → 유지
4. **단독 가운데점** (목록 기호 • 등): 변경하지 않음
5. **사전 발음기호**(l1·ba 등 영문+숫자+가운데점): 변경하지 않음
6. **비병렬 연결**: 단어가 동등하지 않거나 수식/부연 관계면 유지
	   - 신부(神父)·유전학의 → 유지 (서로 다른 범주)
	   - 한자·음훈 → 유지 (설명 관계)
	   - 5·4운동시기까지의 → 유지 (숫자+명사 합성)
	   - 아시아·태평양지역의 → 유지 (합성 명사)
	   - 나라·주 → 유지 (합성 명사)
	7. **책제목·편명**: 고전 책 제목과 편명 사이 가운데점은 유지
	   - 韓非子·觀行 → 유지
	   - 論語·學而 → 유지
	8. **한자 포함 가운데점**: 가운데점 양쪽 어느 한쪽이라도 한자(漢字)가 포함되면 유지
	   - 시가(詩歌)·문장 → 유지 (한자 포함)
	   - 북경(北京)·상해(上海) → 유지 (한자 포함)
	   - 사랑·평화(平和) → 유지 (한자 포함)

		**핵심**: 순수 한국어 병렬 나열(한자·괄호·숫자 없는 동등한 단어 2~4개)은 Ollama 여부와 무관하게 반드시 쉼표(,)로 변경한다. 그 외 5개 이상 병렬이나 애매한 문맥은 Ollama가 보조 판단한다. 한자 포함·중국어 포함·숫자 포함·괄호 포함·인명·비병렬연결·책제목·편명은 모두 유지. 지명 격식(한글(한자))이 아닌 가운데점은 절대 수정하지 않음.

아래는 검토 대상 JSON 배열이다.
각 항목의 id와 context를 보고 판단하라.

{dot_list}

반드시 JSON 배열 1개만 출력하라. 설명문, 머리말, 꼬리말 금지.
출력 각 항목 형식:
[{{"id":1,"action":"convert|keep","original":"서울·부산","corrected":"서울,부산","reason":"병렬 단어"}}]
유지 항목은 corrected를 빈 문자열로 두어라.
original은 문맥 속 실제 가운데점 표현만 넣어라.
JSON 배열만 출력하라."""

        try:
            response_json = post_ollama_chat({
                "model": resolved_model,
                "messages": [{"role": "user", "content": dot_prompt}],
                "stream": False,
                "options": {"num_predict": 1200, "temperature": 0}
            }, timeout=OLLAMA_DOT_TIMEOUT)
            resp_text = get_ollama_message_text(response_json)
            preview = resp_text[:300] if resp_text else "(빈 응답)"
            log(f"  [가운데점-Ollama 응답] (시도 {attempt+1}, 문맥 {len(batch)}개): {preview}", log_fh)
            if not resp_text.strip():
                raise RuntimeError("빈 응답")
            arr = parse_ollama_json_array(resp_text)
            log(f"  [가운데점-Ollama 파싱]: 응답 {len(resp_text)}자 / JSON 항목 {len(arr)}개", log_fh)
            if not arr:
                raise RuntimeError("JSON 항목 0개")
            responded_originals = []
            responded_context_ids = set()
            for item in arr:
                if not isinstance(item, dict):
                    continue
                ctx_id = item.get("id")
                if isinstance(ctx_id, int) and 1 <= ctx_id <= len(batch):
                    responded_context_ids.add(ctx_id)
                action = normalize_ollama_text(item.get("action", "")).lower()
                orig = normalize_ollama_text(item.get("original", ""))
                corr = re.sub(r'\s*,\s*', ',', normalize_ollama_text(item.get("corrected", "")))
                reason = normalize_ollama_text(item.get("reason", "")) or "사유 미제공"
                if orig and orig in text:
                    responded_originals.append(orig)
                if action == "convert" and orig and corr and orig != corr and orig in text:
                    if orig in rule_based_originals:
                        continue
                    cnt = text.count(orig)
                    corrections.append((orig, corr))
                    log(f"  [가운데점 교정]: '{orig}' -> '{corr}' ({reason}, {cnt}회)", log_fh)
                elif action == "keep" and orig:
                    log(f"  [가운데점 유지]: '{orig}' ({reason or '교정 불필요'})", log_fh)
            untouched_contexts = []
            for idx, ctx in enumerate(batch, 1):
                if idx in responded_context_ids:
                    continue
                if any(orig and orig in ctx for orig in responded_originals):
                    continue
                untouched_contexts.append(ctx)
            if untouched_contexts:
                for ctx in untouched_contexts[:50]:
                    log(f"  [가운데점 유지-문맥]: '{ctx}' (Ollama 교정 항목 없음)", log_fh)
                if len(untouched_contexts) > 50:
                    log(f"  [가운데점 유지-문맥]: ... 외 {len(untouched_contexts) - 50}개 생략", log_fh)
            all_untouched_contexts = untouched_contexts
            log(
                f"  [가운데점-상세요약] 전체 {len(dot_contexts)}개 / 발음기호 제외 {len(excluded_phonetics)}개 / "
                f"중한 선반영 제외 {len(prehandled_contexts)}개 / 규칙 선반영 {len(rule_based_corrections)}개 / 유효 문맥 {len(batch)}개 / Ollama 응답 {len(arr)}개 / 실제 교정 {len(corrections)}개 / "
                f"무응답 유지 {len(untouched_contexts)}개",
                log_fh,
            )
            attempt_success = True
            break
        except Exception as e:
            log(f"  가운데점 Ollama 오류 (시도 {attempt+1}, 문맥 {max_ctx}개): {e}", log_fh)
            if attempt < 2:
                max_ctx = max_ctx // 2
                log(f"  문맥을 {max_ctx}개로 줄여서 재시도...", log_fh)
                time.sleep(3)
            else:
                log(f"  가운데점 Ollama 최종 실패", log_fh)

    if not attempt_success and ollama_candidates:
        log("  [가운데점-Ollama 개별 재시도] 배치 실패로 문맥별 재질의 시작", log_fh)
        all_untouched_contexts = []
        for idx, ctx in enumerate(ollama_candidates[:12], 1):
            single_prompt = f"""당신은 조선어 교정 전문가입니다.

[규칙셋명]
{ollama_rule_signature}

다음 문맥 1개만 보고 판단하라.
문맥: {ctx}

반드시 JSON 배열 1개만 출력하라.
교정이 필요하면:
[{{"action":"convert","original":"서울·부산","corrected":"서울,부산","reason":"병렬 단어"}}]
교정이 불필요하면:
[{{"action":"keep","original":"","corrected":"","reason":"교정 불필요"}}]"""
            try:
                response_json = post_ollama_chat({
                    "model": resolved_model,
                    "messages": [{"role": "user", "content": single_prompt}],
                    "stream": False,
                    "options": {"num_predict": 300, "temperature": 0}
                }, timeout=OLLAMA_DOT_TIMEOUT)
                resp_text = get_ollama_message_text(response_json)
                arr = parse_ollama_json_array(resp_text)
                log(f"  [가운데점-Ollama 개별 응답 {idx}]: 응답 {len(resp_text)}자 / JSON 항목 {len(arr)}개", log_fh)
                matched = False
                for item in arr:
                    if not isinstance(item, dict):
                        continue
                    action = normalize_ollama_text(item.get("action", "")).lower()
                    orig = normalize_ollama_text(item.get("original", ""))
                    corr = re.sub(r'\s*,\s*', ',', normalize_ollama_text(item.get("corrected", "")))
                    reason = normalize_ollama_text(item.get("reason", "")) or "사유 미제공"
                    if action == "convert" and orig and corr and orig != corr and orig in text:
                        cnt = text.count(orig)
                        corrections.append((orig, corr))
                        log(f"  [가운데점 교정-개별]: '{orig}' -> '{corr}' ({reason}, {cnt}회)", log_fh)
                        matched = True
                        break
                    if action == "keep":
                        matched = True
                        log(f"  [가운데점 유지-개별]: '{ctx}' ({reason})", log_fh)
                        break
                if not matched:
                    all_untouched_contexts.append(ctx)
                    log(f"  [가운데점 유지-개별무응답]: '{ctx}'", log_fh)
            except Exception as e:
                all_untouched_contexts.append(ctx)
                log(f"  [가운데점 개별 오류 {idx}]: {e}", log_fh)

    log(
        f"  가운데점 교정 결과: {len(corrections)}개 교정 / {len(working_filtered)}개 검토 문맥 중 "
        f"(전체 {len(dot_contexts)}개, 중한 선반영 제외 {len(prehandled_contexts)}개)",
        log_fh,
    )
    return corrections


def should_convert_double_to_single(q):
    q = q.strip()
    if not q:
        return False, "빈 내용"
    # 사용자가 지정한 중문 명사군은 성구가 아니라 단따옴표 대상임을 로그에 명시한다.
    if q in FORCE_SINGLE_QUOTE_TERMS:
        return True, "중문 고정 명사"

    if len(q) > 30:
        return False, f"30자 초과 ({len(q)}자)"

    has_hangul = bool(re.search(r'[가-힣]', q))
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', q))

    if re.search(r'[\n\r]', q):
        return False, "대화형 문장"
    if any(ch in q for ch in "，。？！；："):
        return False, "대화형 문장"
    if re.search(r'(吗|呢|吧|啊|呀|啦|嘛|么)$', q):
        return False, "대화형 문장"

    # 중문 표제어/용어/명칭은 길이가 다소 길어도 단따옴표로 통일한다.
    if has_chinese:
        return True, "중문 단어/구"

    if re.fullmatch(r'[零一二三四五六七八九十百千万兩两〇○]+', q):
        return True, "중문 숫자형"
    if has_hangul and not has_chinese:
        if re.fullmatch(r'[가-힣·ㆍ\- ]{1,9}', q):
            return True, "한글 단어/구"
        return False, "한글 어구(길이초과)"
    if re.fullmatch(r'[가-힣A-Za-z0-9\u4e00-\u9fff·ㆍ\- ]{1,12}', q):
        return True, "단어/구"

    if has_hangul and has_chinese:
        return False, "중한혼합"
    if has_chinese:
        return False, "중문(한자)"
    return False, "기타 어구"


def collect_quote_hit_map(text):
    hit_map = {}

    for q in re.findall(re.escape(LDQ) + r'([^' + re.escape(RDQ) + r']{1,50})' + re.escape(RDQ), text):
        orig = f"{LDQ}{q}{RDQ}"
        hit_map[orig] = hit_map.get(orig, {"quoted": q, "count": 0})
        hit_map[orig]["count"] += 1

    for q in re.findall(r'"([^"\r\n]{1,50})"', text):
        orig = f'"{q}"'
        hit_map[orig] = hit_map.get(orig, {"quoted": q, "count": 0})
        hit_map[orig]["count"] += 1

    return hit_map


def collect_quote_corrections(text, log_fh=None):
    corrections = []
    resolved_model = resolve_ollama_model()
    if not resolved_model:
        log("  Ollama 미실행 - 따옴표 규칙 건너뜀", log_fh)
        return corrections

    hit_map = collect_quote_hit_map(text)

    if not hit_map:
        log("  따옴표 대상 없음", log_fh)
        return corrections

    quote_items = list(hit_map.items())
    log(f"  따옴표 후보 발견: {len(quote_items)}개", log_fh)
    candidate_lines = []
    for i, (orig, meta) in enumerate(quote_items, 1):
        hint_convert, hint_reason = should_convert_double_to_single(meta["quoted"])
        hint_label = "변환권고" if hint_convert else "유지권고"
        candidate_lines.append(
            f"  {i}. {orig} | 출현 {meta['count']}회 | 사전힌트: {hint_label} ({hint_reason})"
        )
        if i <= 50:
            log(f"    [따옴표 후보 {i}] {orig} ({meta['count']}회, {hint_label}: {hint_reason})", log_fh)
    if len(quote_items) > 50:
        log(f"    ... 외 {len(quote_items) - 50}개 생략", log_fh)

    ollama_rule_signature = (
        "따옴표-Ollama 규칙셋: 중문 표제어/용어/명칭 단따옴표, "
        "중문 고정 명사 우선 단따옴표, 대화형 문장 유지, 긴 어구 유지, 중한혼합 유지"
    )
    log(f"  [Ollama 규칙셋명]: {ollama_rule_signature}", log_fh)
    log(f"  [Ollama 사용 모델]: {resolved_model}", log_fh)
    log(
        f"  [Ollama 참고 규칙 파일]: "
        f"{os.path.basename(CHINA_PLACE_FILE)}, "
        f"{os.path.basename(RULES_FILE)}, "
        f"{os.path.basename(REGEX_FILE)}",
        log_fh,
    )
    log(
        f"  [따옴표 고정 명사]: {len(FORCE_SINGLE_QUOTE_TERMS)}개",
        log_fh,
    )

    prompt = f"""당신은 조선어 교정 전문가입니다.

[규칙셋명]
{ollama_rule_signature}

[참고 규칙 파일]
- 중한 규칙: {os.path.basename(CHINA_PLACE_FILE)}
- TXT 통합규칙: {os.path.basename(RULES_FILE)}
- 정규식 규칙: {os.path.basename(REGEX_FILE)}

[중문 고정 명사]
{", ".join(sorted(FORCE_SINGLE_QUOTE_TERMS))}

[판단 원칙]
1. 중문 표제어, 용어, 명칭, 고정 명사는 겉따옴표를 단따옴표로 바꾼다.
2. 대화형 문장, 감탄/의문/명령 표현, 문장부호가 있는 문장은 유지한다.
3. 중한혼합, 긴 설명문, 일반 인용문은 유지한다.
4. 최종 출력에서 교정이 필요한 항목만 "convert", 유지할 항목은 "keep"으로 표시한다.
5. 따옴표 내부 글자는 바꾸지 말고 바깥 겉따옴표만 판단한다.

[후보 목록]
{chr(10).join(candidate_lines)}

출력 형식:
[
  {{"original":"“欧洲联盟”","action":"convert","reason":"중문 고정 명사"}},
  {{"original":"“你好吗？”","action":"keep","reason":"대화형 문장"}}
]
JSON 배열만 출력하라."""

    try:
        response_json = post_ollama_chat({
            "model": resolved_model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"num_predict": 800, "temperature": 0}
        }, timeout=OLLAMA_QUOTE_TIMEOUT)
        resp_text = get_ollama_message_text(response_json)
        preview = resp_text[:300] if resp_text else "(빈 응답)"
        log(f"  [따옴표-Ollama 응답]: {preview}", log_fh)
        if not resp_text.strip():
            raise RuntimeError("빈 응답")
        arr = parse_ollama_json_array(resp_text)
        log(f"  [따옴표-Ollama 파싱]: 응답 {len(resp_text)}자 / JSON 항목 {len(arr)}개", log_fh)

        responded = set()
        keep_count = 0
        for item in arr:
            if not isinstance(item, dict):
                continue
            orig = item.get("original", "").strip()
            action = item.get("action", "").strip().lower()
            reason = item.get("reason", "").strip() or "사유 미제공"
            if not orig or orig not in hit_map:
                continue
            responded.add(orig)
            q = hit_map[orig]["quoted"]
            count = hit_map[orig]["count"]
            if action == "convert":
                corr = f"{LSQ}{q}{RSQ}"
                corrections.append((orig, corr))
                log(f"  [따옴표 교정]: '{orig}' -> '{corr}' ({reason}, {count}회)", log_fh)
            else:
                keep_count += 1
                log(f"  [따옴표 유지]: '{orig}' ({reason}, {count}회)", log_fh)

        no_response_items = []
        for orig, meta in quote_items:
            if orig in responded:
                continue
            no_response_items.append(orig)
            log(f"  [따옴표 유지-응답없음]: '{orig}' (Ollama 응답 없음, {meta['count']}회)", log_fh)

        log(
            f"  [따옴표-상세요약] 후보 {len(quote_items)}개 / Ollama 응답 {len(arr)}개 / "
            f"교정 {len(corrections)}개 / 유지 {keep_count}개 / 응답없음 {len(no_response_items)}개",
            log_fh,
        )
    except Exception as e:
        log(f"  따옴표 Ollama 오류: {e}", log_fh)

    log(f"  따옴표 교정: {len(corrections)}개", log_fh)
    return corrections


def collect_china_korean_corrections(text, china_rules, log_fh=None):
    corrections = []
    matched_rules = 0
    total_hits = 0
    dot_rule_hits = 0
    for orig, repl in china_rules:
        if orig in text:
            cnt = text.count(orig)
            corrections.append((orig, repl))
            matched_rules += 1
            total_hits += cnt
            if is_dot_related_rule(orig, repl):
                dot_rule_hits += cnt
                log(f"  [중한-가운데점]: '{orig}' -> '{repl}' ({cnt}개)", log_fh)
            elif '나라' in orig:
                log(f"  [중한-나라→조]: '{orig}' -> '{repl}' ({cnt}개)", log_fh)
            elif '성' in orig or '시' in orig or '구' in orig or '역' in orig:
                log(f"  [중한-지명]: '{orig}' -> '{repl}' ({cnt}개)", log_fh)
            else:
                log(f"  [중한-변환]: '{orig}' -> '{repl}' ({cnt}개)", log_fh)
    if matched_rules == 0:
        log(f"  [중한-요약] 검사 {len(china_rules)}개 규칙, 매치 없음", log_fh)
    else:
        log(
            f"  [중한-요약] 검사 {len(china_rules)}개 규칙, 매치 {matched_rules}개 규칙 / "
            f"{total_hits}회 (가운데점 {dot_rule_hits}회)",
            log_fh,
        )
    return corrections


def process_hwp_file(filepath, txt_rules, regex_rules, china_rules, log_fh=None):
    fname = os.path.basename(filepath)
    log(f"\n{'=' * 60}", log_fh)
    log(f"파일: {fname}", log_fh)
    log(f"{'=' * 60}", log_fh)

    if olefile is None:
        log("  olefile 모듈 없음 - 처리 불가", log_fh)
        return 0, []

    all_corrections = []
    total_applied = 0

    existing_bak = filepath + ".bak"
    if not os.path.exists(existing_bak):
        try:
            shutil.copy2(filepath, existing_bak)
            log(f"  백업 생성: {os.path.basename(existing_bak)}", log_fh)
        except Exception as e:
            log(f"  백업 실패: {e}", log_fh)

    text = extract_text_from_hwp_binary(filepath, log_fh)
    log(f"  텍스트 추출: {len(text):,}자", log_fh)

    log(f"\n--- 1단계: 중한 규칙 (나라→조 + 지명 + 변환) ---", log_fh)
    china_corrections = collect_china_korean_corrections(text, china_rules, log_fh)
    china_matched_srcs = set()
    china_total_hits = 0
    for orig, repl in china_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, "중한규칙", cnt))
        china_matched_srcs.add(orig)
        china_total_hits += cnt

    log(f"\n--- 2단계: TXT 통합규칙 ({len(txt_rules)}개) ---", log_fh)
    txt_matched_rules = 0
    txt_total_hits = 0
    txt_protected_skips = 0
    txt_overlap_skips = 0
    for src, dst in txt_rules:
        if src not in text:
            continue
        if is_protected(src):
            txt_protected_skips += 1
            continue
        skip = False
        for cms in china_matched_srcs:
            if src in cms or cms in src:
                skip = True
                break
        if skip:
            txt_overlap_skips += 1
            continue
        cnt = text.count(src)
        txt_matched_rules += 1
        txt_total_hits += cnt
        all_corrections.append((src, dst, "TXT규칙", cnt))
        log(f"  [TXT]: '{src}' -> '{dst}' ({cnt}개)", log_fh)
    if txt_matched_rules == 0:
        log(f"  [TXT-요약] 검사 {len(txt_rules)}개 규칙, 매치 없음 (보호어 제외 {txt_protected_skips}개, 중한중복 제외 {txt_overlap_skips}개)", log_fh)
    else:
        log(f"  [TXT-요약] 검사 {len(txt_rules)}개 규칙, 매치 {txt_matched_rules}개 규칙 / {txt_total_hits}회 (보호어 제외 {txt_protected_skips}개, 중한중복 제외 {txt_overlap_skips}개)", log_fh)

    if regex_rules:
        log(f"\n--- 2.5단계: 정규식 규칙 ({len(regex_rules)}개) ---", log_fh)
        txt_src_set = {src for src, dst in txt_rules}
        regex_seen = set()
        for pattern, replacement in regex_rules:
            try:
                has_meta = bool(re.search(r'[()\\[\]{}*+?|^$]', pattern))
                if not has_meta and pattern in txt_src_set:
                    continue
                for m in re.finditer(pattern, text):
                    orig = m.group(0)
                    if orig in regex_seen:
                        continue
                    # 문맥 검증: 앞이 공백이면 이미 띄어쓰기 됨
                    pos = m.start()
                    if pos > 0 and text[pos - 1] == ' ':
                        continue
                    # PROTECT_LIST 필터 (오매치 방지)
                    if is_protected(orig):
                        continue
                    # 치환: 역참조 수동 처리 (re.sub의 \1 인식 문제 회피)
                    corr = replacement
                    for gi in range(min(len(m.groups()), 9), 0, -1):
                        corr = corr.replace(f'\\{gi}', m.group(gi) or '')
                    if orig != corr:
                        regex_seen.add(orig)
                        cnt = text.count(orig)
                        all_corrections.append((orig, corr, "정규식", cnt))
                        log(f"  [정규식]: '{orig}' -> '{corr}' ({cnt}개)", log_fh)
            except re.error as e:
                log(f"  [정규식 오류]: '{pattern}' - {e}", log_fh)

    log(f"\n--- 3단계: 가운데점 Ollama 규칙 ---", log_fh)
    dot_corrections = collect_dot_corrections_with_ollama(text, log_fh)
    dot_total_hits = 0
    for orig, repl in dot_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, "가운데점", cnt))
        dot_total_hits += cnt
    log(f"  [가운데점-요약] 교정 {len(dot_corrections)}개 항목 / {dot_total_hits}회", log_fh)

    log(f"\n--- 4단계: 따옴표 Ollama 규칙 ---", log_fh)
    quote_corrections = collect_quote_corrections(text, log_fh)
    quote_total_hits = 0
    for orig, repl in quote_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, "따옴표", cnt))
        quote_total_hits += cnt
    log(f"  [따옴표-요약] 교정 {len(quote_corrections)}개 항목 / {quote_total_hits}회", log_fh)

    log(f"\n  총 교정 항목: {len(all_corrections)}개", log_fh)
    log(
        "  단계별 합계: "
        f"1단계 {len(china_corrections)}개/{china_total_hits}회, "
        f"2단계 {txt_matched_rules}개/{txt_total_hits}회, "
        f"3단계 {len(dot_corrections)}개/{dot_total_hits}회, "
        f"4단계 {len(quote_corrections)}개/{quote_total_hits}회",
        log_fh
    )

    if not all_corrections:
        log(f"  교정 항목 없음 - 파일 수정 없음", log_fh)
        return 0, all_corrections

    log(f"\n--- COM API 수정 시작 (안전 모드 방지) ---", log_fh)

    try:
        import win32com.client
    except ImportError:
        log(f"  win32com 모듈 없음 - COM API 사용 불가", log_fh)
        return 0, all_corrections

    temp_dir = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'hwp_proofread')
    os.makedirs(temp_dir, exist_ok=True)
    temp_hwp = os.path.join(temp_dir, f"proofread_{os.path.basename(filepath)}")

    try:
        shutil.copy2(filepath, temp_hwp)
        log(f"  임시 복사: {temp_hwp}", log_fh)
    except PermissionError:
        log(f"  파일 잠금 - HWP 프로세스 종료 시도", log_fh)
        try:
            subprocess.run(["taskkill", "/F", "/IM", "Hwp.exe"], capture_output=True, timeout=10)
            time.sleep(2)
            shutil.copy2(filepath, temp_hwp)
            log(f"  임시 복사 재시도 성공", log_fh)
        except Exception as e2:
            log(f"  임시 복사 실패: {e2}", log_fh)
            return 0, all_corrections
    except Exception as e:
        log(f"  임시 복사 오류: {e}", log_fh)
        return 0, all_corrections

    try:
        hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
        log(f"  COM: HWPFrame.HwpObject 생성 (조기 바인딩)", log_fh)
    except Exception as e:
        log(f"  COM 조기 바인딩 실패, 지연 바인딩 시도: {e}", log_fh)
        try:
            hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
            log(f"  COM: HWPFrame.HwpObject 생성 (지연 바인딩)", log_fh)
        except Exception as e2:
            log(f"  COM 객체 생성 최종 실패: {e2}", log_fh)
            return 0, all_corrections

    try:
        hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
        open_result = hwp.Open(temp_hwp, "", "")
        if not open_result:
            log(f"  COM: 파일 열기 실패", log_fh)
            hwp.Clear(1)
            return 0, all_corrections
        log(f"  COM: 파일 열기 성공", log_fh)
    except Exception as e:
        log(f"  COM: 파일 열기 오류: {e}", log_fh)
        try:
            hwp.Clear(1)
        except:
            pass
        return 0, all_corrections

    applied = 0
    for i, (orig, repl, rule_type, cnt) in enumerate(all_corrections):
        try:
            pset = hwp.HParameterSet.HFindReplace
            hwp.HAction.GetDefault("AllReplace", pset.HSet)
            pset.FindString = orig
            pset.ReplaceString = repl
            pset.Direction = 0
            pset.WholeWordOnly = 0
            pset.MatchCase = 0
            pset.UseWildCards = 0
            pset.ReplaceMode = 1
            pset.SeveralWords = 0
            result = hwp.HAction.Execute("AllReplace", pset.HSet)
            if result:
                applied += 1
                log(f"  [{i+1}/{len(all_corrections)}] OK: '{orig}' -> '{repl}'", log_fh)
            else:
                log(f"  [{i+1}/{len(all_corrections)}] No match: '{orig}'", log_fh)
        except Exception as e:
            log(f"  [{i+1}/{len(all_corrections)}] Error: '{orig}' - {e}", log_fh)

    total_applied = applied

    try:
        hwp.Save()
        log(f"  COM: 파일 저장 완료", log_fh)
    except Exception as e:
        log(f"  COM: 저장 오류: {e}", log_fh)

    try:
        hwp.Clear(1)
        log(f"  COM: 해제 완료", log_fh)
    except:
        pass

    if total_applied > 0:
        try:
            shutil.copy2(temp_hwp, filepath)
            log(f"  원본 교체 완료: {filepath}", log_fh)
        except Exception as e:
            log(f"  원본 교체 실패: {e} - 결과 파일: {temp_hwp}", log_fh)

    log(f"\n  적용 결과: {total_applied}건 수정", log_fh)
    return total_applied, all_corrections


def save_report(filepath, all_corrections, total_applied, log_fh=None):
    os.makedirs(REPORT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(filepath))[0]
    report_path = os.path.join(REPORT_DIR, f"{base}_교정결과_{ts}.txt")

    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"{'=' * 60}\n")
            f.write(f"HWP 교정 결과 리포트 v18.0 (COM API + Ollama)\n")
            f.write(f"{'=' * 60}\n")
            f.write(f"일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"파일: {os.path.basename(filepath)}\n")
            f.write(f"총 교정 항목: {len(all_corrections)}개\n")
            f.write(f"총 적용 건수: {total_applied}건\n")
            f.write(f"{'=' * 60}\n\n")

            by_type = {}
            for src, dst, rule_type, cnt in all_corrections:
                if rule_type not in by_type:
                    by_type[rule_type] = []
                by_type[rule_type].append((src, dst, cnt))

            if not by_type:
                f.write("[상세내역]\n")
                f.write(f"{'-' * 60}\n")
                f.write("  교정 항목이 없어 파일 변경이 없습니다.\n\n")
            else:
                for rule_type, items in by_type.items():
                    f.write(f"[{rule_type}] ({len(items)}개)\n")
                    f.write(f"{'-' * 60}\n")
                    for src, dst, cnt in items:
                        f.write(f"  '{src}' -> '{dst}' ({cnt}회)\n")
                    f.write(f"\n")

        log(f"리포트 저장: {report_path}", log_fh)
        return report_path
    except Exception as e:
        log(f"리포트 저장 오류: {e}", log_fh)
        return None


def main():
    import glob as _glob
    maybe_relaunch_with_32bit_python()
    default_hwp_dir = resolve_default_hwp_dir()

    stage = "all"
    for arg in sys.argv[1:]:
        if arg.startswith("--stage="):
            stage = arg.split("=", 1)[1].strip().lower()

    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args:
        print("=" * 55)
        print("  HWP 교정 v18.0 (COM API + Ollama)")
        print("  중한규칙 + TXT규칙 + 정규식 + 3단계Ollama(가운데점) + 4단계Ollama(따옴표)")
        print(f"  규칙: {RULES_FILE}")
        print(f"  대상: {default_hwp_dir}")
        print("  --stage=check|all")
        print("=" * 55)
        target = default_hwp_dir
    else:
        target = args[0].strip('"')

    files = []
    if target.lower().endswith('.hwp'):
        matched = _glob.glob(target)
        if matched:
            files = matched
    elif _glob.glob(os.path.join(target, "*.hwp")):
        files = _glob.glob(os.path.join(target, "*.hwp"))

    if not files:
        files = [os.path.join(default_hwp_dir, f) for f in os.listdir(default_hwp_dir)
                 if f.endswith('.hwp') and not f.startswith('~')]
        files = [f for f in files if os.path.exists(f)]

    if not files:
        log(f"HWP 파일 없음: {target}")
        return

    txt_rules = parse_rules(RULES_FILE)
    china_rules = load_china_place_rules()
    regex_rules = load_regex_rules()
    resolved_ollama_model = resolve_ollama_model()
    ollama_ok = bool(resolved_ollama_model)

    log(f"대상: {len(files)}개 파일")
    log(f"중한 규칙: {len(china_rules)}개")
    log(f"TXT 규칙: {len(txt_rules)}개")
    log(f"정규식 규칙: {len(regex_rules)}개")
    if ollama_ok:
        if resolved_ollama_model == OLLAMA_MODEL:
            log(f"Ollama: 연결됨 (모델: {resolved_ollama_model})")
        else:
            log(f"Ollama: 연결됨 (모델 폴백: {resolved_ollama_model}, 요청 모델: {OLLAMA_MODEL})")
    else:
        log(f"Ollama: 미연결 또는 사용 가능한 모델 없음 (3-4단계 제외)")
    log(f"로그: {LOG_FILE}")

    with open(LOG_FILE, 'a', encoding='utf-8') as log_fh:
        log(f"\n\n{'#' * 60}", log_fh)
        log(f"HWP 교정 v18.0: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", log_fh)
        log(f"중한 규칙: {len(china_rules)}개", log_fh)
        log(f"TXT 규칙: {len(txt_rules)}개", log_fh)
        log(f"정규식 규칙: {len(regex_rules)}개", log_fh)
        if ollama_ok:
            if resolved_ollama_model == OLLAMA_MODEL:
                log(f"Ollama: 연결됨 (모델: {resolved_ollama_model})", log_fh)
            else:
                log(f"Ollama: 연결됨 (모델 폴백: {resolved_ollama_model}, 요청 모델: {OLLAMA_MODEL})", log_fh)
        else:
            log(f"Ollama: 미연결 또는 사용 가능한 모델 없음", log_fh)
        log(f"단계: {stage}", log_fh)
        log(f"{'#' * 60}\n", log_fh)

        grand_total = 0
        all_file_results = []

        for i, fp in enumerate(files):
            log(f"\n[{i + 1}/{len(files)}] 처리 시작", log_fh)

            if stage == "check":
                text = extract_text_from_hwp_binary(fp, log_fh)
                log(f"  텍스트: {len(text):,}자", log_fh)
                match_count = 0
                check_dot_hits = 0
                for src, dst in china_rules:
                    if src in text:
                        cnt = text.count(src)
                        match_count += cnt
                        if is_dot_related_rule(src, dst):
                            check_dot_hits += cnt
                            log(f"  [CHECK-중한-가운데점]: '{src}' -> '{dst}' ({cnt}개)", log_fh)
                        else:
                            log(f"  [CHECK-중한]: '{src}' -> '{dst}' ({cnt}개)", log_fh)
                for src, dst in txt_rules:
                    if src in text and not is_protected(src):
                        cnt = text.count(src)
                        match_count += cnt
                        log(f"  [CHECK-TXT]: '{src}' -> '{dst}' ({cnt}개)", log_fh)
                for pattern, replacement in regex_rules:
                    try:
                        for m in re.finditer(pattern, text):
                            orig = m.group(0)
                            corr = re.sub(pattern, replacement, orig)
                            if orig != corr:
                                match_count += 1
                                log(f"  [CHECK-정규식]: '{orig}' -> '{corr}'", log_fh)
                    except re.error:
                        pass
                dot_corrections = collect_dot_corrections_with_ollama(text, log_fh)
                for orig, corr in dot_corrections:
                    match_count += 1
                    log(f"  [CHECK-가운데점]: '{orig}' -> '{corr}'", log_fh)
                quote_corrections = collect_quote_corrections(text, log_fh)
                for orig, corr in quote_corrections:
                    match_count += 1
                    log(f"  [CHECK-따옴표-Ollama]: '{orig}' -> '{corr}'", log_fh)
                log(f"  [CHECK-중한-요약] 가운데점 {check_dot_hits}개 포함", log_fh)
                log(f"  [CHECK-따옴표-요약] {len(quote_corrections)}개", log_fh)
                log(f"  매치 합계: {match_count}개", log_fh)
                all_file_results.append((os.path.basename(fp), match_count, 0))
            else:
                applied, corrections = process_hwp_file(fp, txt_rules, regex_rules, china_rules, log_fh)
                grand_total += applied
                all_file_results.append((os.path.basename(fp), len(corrections), applied))
                save_report(fp, corrections, applied, log_fh)

            time.sleep(1)

        log(f"\n{'=' * 60}", log_fh)
        log(f"전체 완료!", log_fh)
        log(f"{'=' * 60}", log_fh)
        for fname, items, applied in all_file_results:
            log(f"  {fname}: {items}개 항목, {applied}건 적용", log_fh)
        log(f"\n총 적용 건수: {grand_total}건", log_fh)
        log(f"{'=' * 60}\n", log_fh)

    log(f"\n완료! 로그: {LOG_FILE}")


if __name__ == "__main__":
    main()
