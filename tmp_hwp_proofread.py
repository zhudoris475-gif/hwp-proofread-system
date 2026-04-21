# -*- coding: utf-8 -*-
import os, sys, io, json, time, shutil, re, struct, zlib

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

try:
    import win32com.client
    import pythoncom
except ImportError:
    win32com = None
    pythoncom = None

from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "hwp_ollama_proofread_log.txt")
RULES_FILE = r"C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config\rules_documentation.txt"
CHINA_PLACE_FILE = r"C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config\rules_china_place.txt"
REGEX_FILE = os.path.join(SCRIPT_DIR, "rules_regex.txt")
REGEX_ENABLED = False
HWP_DIR = r"C:\사전"
REPORT_DIR = os.path.join(SCRIPT_DIR, "reports")

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "korean-corrector:latest"
OLLAMA_DOT_TIMEOUT = 300
OLLAMA_QUOTE_TIMEOUT = 300

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


def connect_hwp_com(log_fh=None):
    if win32com is None or pythoncom is None:
        log("  COM 자동화 모듈 없음 - 안전 저장 경로 사용 불가", log_fh)
        return None

    pythoncom.CoInitialize()
    CLSCTX_LOCAL_SERVER = 4
    prog_id = "HWPFrame.HwpObject"

    try:
        hwp = win32com.client.DispatchEx(prog_id, clsctx=CLSCTX_LOCAL_SERVER)
        for module_name in ("FilePathCheckerModule", "SecurityModule"):
            try:
                hwp.RegisterModule("FilePathCheckDLL", module_name)
                log(f"  보안 모듈 등록: {module_name}", log_fh)
            except Exception:
                pass
        try:
            hwp.SetMessageBoxMode(0x00020000)
        except Exception:
            pass
        try:
            hwp.Visible = False
        except Exception:
            pass
        log(f"  HWP COM 연결 성공: {prog_id} (Out-of-Process)", log_fh)
        return hwp
    except Exception as e:
        log(f"  HWP COM 연결 실패: {e}", log_fh)
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass
        return None


def close_hwp_com(hwp):
    try:
        if hwp is not None:
            hwp.Quit()
    except Exception:
        pass
    try:
        if pythoncom is not None:
            pythoncom.CoUninitialize()
    except Exception:
        pass


def apply_corrections_via_com(filepath, all_corrections, log_fh=None):
    hwp = connect_hwp_com(log_fh)
    if hwp is None:
        return None

    total_applied = 0
    try:
        hwp.Open(filepath, "HWP", "forceopen:true")
        log("  보안 설정: 낮음(자동 열기 모듈 사용)", log_fh)

        try:
            hwp.HAction.GetDefault("TextSelectAll", hwp.HParameterSet.HSelAll.HSet)
            hwp.HAction.Execute("TextSelectAll", hwp.HParameterSet.HSelAll.HSet)
            text_len = hwp.GetSelectedTextLength()
            log(f"  COM 텍스트 길이: {text_len:,}자", log_fh)
            hwp.Run("Cancel")
        except Exception:
            pass

        for src, dst, rule_type, cnt in all_corrections:
            if cnt <= 0:
                continue
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 1
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 1
                hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                total_applied += cnt
                log(f"  [COM-{rule_type}]: '{src}' -> '{dst}' ({cnt}건 적용)", log_fh)
            except Exception as e:
                log(f"  [COM-{rule_type} 실패]: '{src}' -> '{dst}' ({e})", log_fh)

        try:
            hwp.Save()
            log("  COM 저장 완료", log_fh)
        except Exception as e:
            log(f"  COM 저장 실패: {e}", log_fh)
            return None

        return total_applied
    except Exception as e:
        log(f"  COM 처리 실패: {e}", log_fh)
        return None
    finally:
        close_hwp_com(hwp)


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
    try:
        if requests:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
            return r.status_code == 200
        else:
            req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
    except:
        return False


def post_ollama_chat(payload, timeout=120, max_retries=2):
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            if requests:
                r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=timeout)
                return r.json()
            req = urllib.request.Request(
                f"{OLLAMA_URL}/api/chat",
                data=json.dumps(payload).encode('utf-8'),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(5 * (attempt + 1))
    raise last_error


def parse_ollama_json_array(resp_text):
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


def collect_dot_corrections_with_ollama(text, log_fh=None):
    corrections = []
    if not ollama_is_available():
        log("  Ollama 미실행 - 가운데점 규칙 건너뜀", log_fh)
        return corrections

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
    filtered = [c for c in dot_contexts if not phonetic_pattern.search(c)]

    log(f"  가운데점 문맥 발견: {len(dot_contexts)}개 (발음기호 제외: {len(filtered)}개)", log_fh)
    for i, ctx in enumerate(filtered[:50]):
        log(f"    [{i + 1}] {ctx}", log_fh)
    if len(filtered) > 50:
        log(f"    ... 외 {len(filtered) - 50}개 생략", log_fh)

    max_ctx = 50
    for attempt in range(3):
        batch = filtered[:max_ctx]
        if not batch:
            break

        # [규칙 파일 경로]
        # TXT 규칙: C:\Users\51906\Desktop\rules_documentation.txt (5,288개)
        # 중국 지명: C:\Users\51906\Desktop\rules_china_place.txt (236개)
        # 정규식(비활성): C:\Users\51906\Desktop\rules_regex.txt (1,032개)
        dot_list = "\n".join([f'  {i + 1}. {c}' for i, c in enumerate(batch)])
        dot_prompt = f"""당신은 조선어 교정 전문가입니다. 가운데점(·, •, ・) 교정 규칙:

	1. **병렬 단어 나열** (2개 이상 동등한 단어): 가운데점 → 쉼표+공백(, )으로 변경
	   - 서울·부산 → 서울, 부산
	   - 사랑·평화·행복 → 사랑, 평화, 행복
	   - 정치·경제·사회·문화 → 정치, 경제, 사회, 문화
	   - 금전·재화따위 → 금전, 재화따위
	1a. **병렬+따위/등/뿐**: 병렬 단어 뒤에 따위/등/뿐이 붙어도 쉼표 사용
	   - 권리·의무따위 → 권리, 의무따위
	   - 사과·배·포도등 → 사과, 배, 포도등
	   - 구상·수식·풍격을 → 구상, 수식, 풍격을
	   - 구상·수식·풍격 → 구상, 수식, 풍격
	   - 닭·칠면조·메추라기따위를 → 닭, 칠면조, 메추라기따위를
	   - 불만·원한따위가 → 불만, 원한따위가
	   - 의견·주장따위가 → 의견, 주장따위가
	   - 금·은·백금이외의 → 금, 은, 백금 이외의
	   - 문집·시집따위가 → 문집, 시집따위가
	   - 신문·잡지따위 → 신문, 잡지따위
	   - 사진·필림따위를 → 사진, 필림따위를
	   - 담장·건물사이의 → 담장, 건물 사이의
	   - 동정·배려따위를 → 동정, 배려따위를
	   - 전선·전화선따위를 → 전선, 전화선따위를
	   - 난로·벽따위를 → 난로, 벽 따위를
	   - 간악·절도·사악·음행의 → 간악, 절도, 사악, 음행의
	   - 새·짐승·물고기·자라 → 새, 짐승, 물고기, 자라
	   - 책상·의자사이의 → 책상, 의자 사이의
	   - 단어·문장뜻은 → 단어, 문장 뜻은
   - 마오쩌둥·저우언라이 → 모택동·주은래
	2a. **2~3개 단어+따위/때/사이**: 병렬 단어(2~3개) 뒤에 따위/때/사이가 붙어도 쉼표 사용
	   - 구상·수식따위 → 구상, 수식따위
	   - 정치·경제때 → 정치, 경제때
	   - 담장·건물사이 → 담장, 건물사이
	   - 사과·배따위 → 사과, 배따위
	   - 산·들때 → 산, 들 때
	   - 집·나무사이 → 집, 나무사이
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

		**핵심**: 순수 한국어 병렬 나열(한자·괄호·숫자 없는 동등한 단어 2개 이상)만 쉼표+공백으로 변경. 한자 포함·중국어 포함·숫자 포함·괄호 포함·인명·비병렬연결·책제목·편명은 모두 유지. 지명 격식(한글(한자))이 아닌 가운데점은 절대 수정하지 않음.

아래 문맥에서 가운데점 교정이 필요한 항목만 출력:

{dot_list}

출력 형식:
[{{"original":"서울·부산", "corrected":"서울, 부산", "reason":"병렬 단어"}}]
교정 불필요하면 []"""

        try:
            response_json = post_ollama_chat({
                "model": OLLAMA_MODEL,
                "messages": [{"role": "user", "content": dot_prompt}],
                "stream": False,
                "options": {"num_predict": 2000}
            }, timeout=OLLAMA_DOT_TIMEOUT)
            resp_text = response_json.get("message", {}).get("content", "")
            log(f"  [가운데점-Ollama 응답] (시도 {attempt+1}, 문맥 {len(batch)}개): {resp_text[:300]}", log_fh)
            arr = parse_ollama_json_array(resp_text)
            for item in arr:
                if not isinstance(item, dict):
                    continue
                orig = item.get("original", "").strip()
                corr = item.get("corrected", "").strip()
                reason = item.get("reason", "")
                if orig and corr and orig != corr and orig in text:
                    cnt = text.count(orig)
                    corrections.append((orig, corr))
                    log(f"  [가운데점 교정]: '{orig}' -> '{corr}' ({reason}, {cnt}회)", log_fh)
                elif orig and (not corr or orig == corr):
                    log(f"  [가운데점 유지]: '{orig}' ({reason or '교정 불필요'})", log_fh)
            break
        except Exception as e:
            log(f"  가운데점 Ollama 오류 (시도 {attempt+1}, 문맥 {max_ctx}개): {e}", log_fh)
            if attempt < 2:
                max_ctx = max_ctx // 2
                log(f"  문맥을 {max_ctx}개로 줄여서 재시도...", log_fh)
                time.sleep(3)
            else:
                log(f"  가운데점 Ollama 최종 실패", log_fh)

    log(f"  가운데점 교정 결과: {len(corrections)}개 교정 / {len(filtered)}개 유효 문맥 중 (전체 {len(dot_contexts)}개)", log_fh)
    return corrections


def should_convert_double_to_single(q):
    q = q.strip()
    if not q:
        return False, "빈 내용"
    if len(q) > 20:
        return False, f"20자 초과 ({len(q)}자)"

    has_hangul = bool(re.search(r'[가-힣]', q))
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', q))

    if re.search(r'[\n\r]', q):
        return False, "대화형 문장"
    if any(ch in q for ch in "，。？！；：,.?!;:"):
        return False, "대화형 문장"
    if re.search(r'(吗|呢|吧|啊|呀|啦|嘛|么)$', q):
        return False, "대화형 문장"

    if re.fullmatch(r'[零一二三四五六七八九十百千万兩两〇○]+', q):
        return True, "중문 숫자형"
    if re.fullmatch(r'[\u4e00-\u9fff()（）]{1,20}', q):
        return True, "중문 단어/명칭"
    if has_hangul and not has_chinese:
        if re.fullmatch(r'[가-힣·ㆍ\- ]{1,9}', q):
            return True, "한글 단어/구"
        return False, "한글 어구(길이초과)"
    if re.fullmatch(r'[가-힣A-Za-z0-9\u4e00-\u9fff·ㆍ()（）\- ]{1,20}', q):
        return True, "단어/구"

    if has_hangul and has_chinese:
        return False, "중한혼합"
    if has_chinese:
        return False, "중문(한자)"
    return False, "기타 어구"


def collect_quote_corrections(text, log_fh=None):
    LDQ = '\u201c'
    RDQ = '\u201d'
    LSQ = '\u2018'
    RSQ = '\u2019'

    corrections = []
    hit_map = {}

    for q in re.findall(re.escape(LDQ) + r'([^' + re.escape(RDQ) + r']{1,50})' + re.escape(RDQ), text):
        orig = f"{LDQ}{q}{RDQ}"
        hit_map[orig] = hit_map.get(orig, {"quoted": q, "count": 0})
        hit_map[orig]["count"] += 1

    for q in re.findall(r'"([^"\r\n]{1,50})"', text):
        orig = f'"{q}"'
        hit_map[orig] = hit_map.get(orig, {"quoted": q, "count": 0})
        hit_map[orig]["count"] += 1

    if not hit_map:
        log("  따옴표 대상 없음", log_fh)
        return corrections

    for orig, meta in hit_map.items():
        q = meta["quoted"]
        count = meta["count"]
        convert, reason = should_convert_double_to_single(q)
        if convert:
            corr = f"{LSQ}{q}{RSQ}"
            corrections.append((orig, corr))
            log(f"  [따옴표 변환]: '{orig}' -> '{corr}' ({reason}, {count}회)", log_fh)
        else:
            log(f"  [따옴표 유지]: '{orig}' ({reason}, {count}회)", log_fh)

    log(f"  따옴표 교정: {len(corrections)}개", log_fh)
    return corrections


def collect_china_korean_corrections(text, china_rules, log_fh=None):
    corrections = []
    for orig, repl in china_rules:
        if orig in text:
            cnt = text.count(orig)
            corrections.append((orig, repl))
            if '나라' in orig:
                log(f"  [중한-나라→조]: '{orig}' -> '{repl}' ({cnt}개)", log_fh)
            elif '성' in orig or '시' in orig or '구' in orig or '역' in orig:
                log(f"  [중한-지명]: '{orig}' -> '{repl}' ({cnt}개)", log_fh)
            else:
                log(f"  [중한-변환]: '{orig}' -> '{repl}' ({cnt}개)", log_fh)
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
    for orig, repl in china_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, "중한규칙", cnt))
        china_matched_srcs.add(orig)

    log(f"\n--- 2단계: TXT 통합규칙 ({len(txt_rules)}개) ---", log_fh)
    for src, dst in txt_rules:
        if src in text and not is_protected(src):
            skip = False
            for cms in china_matched_srcs:
                if src in cms or cms in src:
                    skip = True
                    break
            if skip:
                continue
            cnt = text.count(src)
            all_corrections.append((src, dst, "TXT규칙", cnt))
            log(f"  [TXT]: '{src}' -> '{dst}' ({cnt}개)", log_fh)

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

    log(f"\n--- 3단계: 가운데점 Ollama ---", log_fh)
    dot_corrections = collect_dot_corrections_with_ollama(text, log_fh)
    for orig, repl in dot_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, "가운데점", cnt))

    log(f"\n--- 4단계: 따옴표 규칙 ---", log_fh)
    quote_corrections = collect_quote_corrections(text, log_fh)
    for orig, repl in quote_corrections:
        cnt = text.count(orig)
        all_corrections.append((orig, repl, "따옴표", cnt))

    log(f"\n  총 교정 항목: {len(all_corrections)}개", log_fh)

    if not all_corrections:
        log(f"  교정 항목 없음 - 파일 수정 없음", log_fh)
        return 0, all_corrections

    log(f"\n--- COM 안전 저장 시작 ---", log_fh)
    total_applied = apply_corrections_via_com(filepath, all_corrections, log_fh)
    if total_applied is None:
        log("  COM 저장 실패 - 바이너리 직접 수정은 중단", log_fh)
        return 0, all_corrections

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
            f.write(f"HWP 교정 결과 리포트 v17.0 (바이너리 + Ollama)\n")
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

    stage = "all"
    for arg in sys.argv[1:]:
        if arg.startswith("--stage="):
            stage = arg.split("=", 1)[1].strip().lower()

    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args:
        print("=" * 55)
        print("  HWP 교정 v17.0 (바이너리 + Ollama)")
        print("  중한규칙 + TXT규칙 + 정규식 + 가운데점Ollama + 따옴표")
        print(f"  규칙: {RULES_FILE}")
        print(f"  대상: {HWP_DIR}")
        print("  --stage=check|all")
        print("=" * 55)
        target = HWP_DIR
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
        files = [os.path.join(HWP_DIR, f) for f in os.listdir(HWP_DIR)
                 if f.endswith('.hwp') and not f.startswith('~')]
        files = [f for f in files if os.path.exists(f)]

    if not files:
        log(f"HWP 파일 없음: {target}")
        return

    txt_rules = parse_rules(RULES_FILE)
    china_rules = load_china_place_rules()
    regex_rules = load_regex_rules()
    ollama_ok = ollama_is_available()

    log(f"대상: {len(files)}개 파일")
    log(f"중한 규칙: {len(china_rules)}개")
    log(f"TXT 규칙: {len(txt_rules)}개")
    log(f"정규식 규칙: {len(regex_rules)}개")
    log(f"Ollama: {'연결됨' if ollama_ok else '미연결 (가운데점 규칙 제외)'}")
    log(f"로그: {LOG_FILE}")

    with open(LOG_FILE, 'a', encoding='utf-8') as log_fh:
        log(f"\n\n{'#' * 60}", log_fh)
        log(f"HWP 교정 v17.0: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", log_fh)
        log(f"중한 규칙: {len(china_rules)}개", log_fh)
        log(f"TXT 규칙: {len(txt_rules)}개", log_fh)
        log(f"정규식 규칙: {len(regex_rules)}개", log_fh)
        log(f"Ollama: {'연결됨' if ollama_ok else '미연결'}", log_fh)
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
                for src, dst in china_rules:
                    if src in text:
                        cnt = text.count(src)
                        match_count += cnt
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

