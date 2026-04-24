# -*- coding: utf-8 -*-
"""
HWP 교정 시스템 v19.0
- AI 모델 + 규칙 기반 하이브리드
- 상세 로그 시스템
- 모든 교정 과정 기록
"""
import os
os.environ["HF_HOME"] = r"D:\软件\hf_cache"
os.environ["TRANSFORMERS_CACHE"] = r"D:\软件\hf_cache"
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import sys
import io
import json
import time
import shutil
import re
import struct
import zlib
import traceback
from datetime import datetime
from typing import List, Tuple, Dict, Optional, Any

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
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = False
except ImportError:
    TRANSFORMERS_AVAILABLE = False

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "hwp_proofread_v19_log.txt")
RULES_FILE = os.path.join(SCRIPT_DIR, "rules_documentation.txt")
CHINA_PLACE_FILE = os.path.join(SCRIPT_DIR, "rules_china_place.txt")
REGEX_FILE = os.path.join(SCRIPT_DIR, "rules_regex.txt")
REGEX_ENABLED = True
HWP_DIR = r"C:\Users\51906\Desktop\nExt\新词典"
REPORT_DIR = os.path.join(SCRIPT_DIR, "reports")

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:3b-korean-corrector"
OLLAMA_DOT_TIMEOUT = 300
OLLAMA_QUOTE_TIMEOUT = 300

AI_MODELS_DIR = os.path.join(SCRIPT_DIR, "ai_models")
LOCAL_MODEL_PATH = r"D:\huggingface\HUGING\qwen25_base_model"
LOCAL_LORA_PATH = r"D:\huggingface\HUGING\qwen25_optimized_retraining"
GEC_MODEL_NAME = LOCAL_MODEL_PATH
TYPOS_MODEL_NAME = LOCAL_MODEL_PATH

SECTION_HEADERS = {'띄어쓰기', '붙여쓰기'}

PROTECT_LIST = [
    "이것", "그것", "저것", "이것저것",
    "산하", "강하",
    "뜻밖", "제대로", "그대로", "함께", "사뿐", "가듯",
    "그만큼", "뜻대로", "마음대로",
    "대·수수깡", "신부·유전학", "장중보옥·금지예엽", "물건·쓸모없는", "시문·음악",
    "흉·복벽의", "기초작업·공사", "체재·출판년월일", "활동·운동의", "산지·西山",
    "5·4운동", "아시아·태평양", "나라·주", "열대·아열대",
    "는데", "은데", "인데",
    "한데", "한대로",
    "한적하다", "한가하다", "한적한", "한적이",
    "한지", "판적", "두발",
    "할지", "할지어다", "할지라도", "할지니",
    "별의별것",
    "방안", "방안하다", "체포방안", "구급방안", "설계방안", "한어병음방안",
    "방안을", "방안이", "방안은", "방안도", "방안에", "방안에서", "방안으로",
    "집안", "집안살림", "한집안", "집안일", "집안사람",
    "집안이", "집안을", "집안은", "집안도", "집안에",
    "집안식구", "집안형편", "집안살림이", "집안이였", "집안으로",
    "쓸데없는", "쓸데없이", "쓸데없다", "쓸데없는것", "쓸데없는말",
    "무엇인지", "살고있는", "알데", "간적", "본적", "간지",
    "산들바", "산지",
    "쓸수있다", "쓸수없다", "쓸수있으나", "쓸수없음", "쓸수있", "쓸수없",
    "입안에", "입안이", "입안을", "입안으로", "입안의",
    "든것", "든것이", "든것을", "든것이다", "만든것", "모든것", "모든것이", "모든것을",
    "인것", "인것같다", "인것을", "인것이", "기술적인것",
    "옛것", "옛것을", "옛것이",
    "유럽안",
]

_PROTECT_EXACT = {"산하", "강하"}


class DetailedLogger:
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.log_fh = None
        self.start_time = None
        self.correction_count = 0
        self.stage_times = {}
        self.errors = []
        self.warnings = []
        
    def open(self):
        self.log_fh = open(self.log_file, 'a', encoding='utf-8', errors='replace')
        self.start_time = time.time()
        
    def close(self):
        if self.log_fh:
            self.log_fh.close()
            self.log_fh = None
            
    def log(self, msg: str, level: str = "INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] [{level}] {msg}"
        print(line)
        if self.log_fh:
            try:
                self.log_fh.write(line + "\n")
                self.log_fh.flush()
            except:
                pass
                
    def log_section(self, title: str):
        self.log("")
        self.log("=" * 60)
        self.log(f"  {title}")
        self.log("=" * 60)
        
    def log_stage_start(self, stage: str):
        self.stage_times[stage] = time.time()
        self.log(f"\n--- {stage} 시작 ---")
        
    def log_stage_end(self, stage: str):
        if stage in self.stage_times:
            elapsed = time.time() - self.stage_times[stage]
            self.log(f"--- {stage} 완료 (소요: {elapsed:.2f}초) ---")
            
    def log_correction(self, stage: str, original: str, corrected: str, reason: str = ""):
        self.correction_count += 1
        reason_str = f" ({reason})" if reason else ""
        self.log(f"  [{stage}] 교정 #{self.correction_count}: '{original}' -> '{corrected}'{reason_str}")
        
    def log_error(self, stage: str, error: str, detail: str = ""):
        self.errors.append({"stage": stage, "error": error, "detail": detail})
        self.log(f"  [{stage}] 오류: {error}", "ERROR")
        if detail:
            self.log(f"    상세: {detail}", "ERROR")
            
    def log_warning(self, stage: str, warning: str):
        self.warnings.append({"stage": stage, "warning": warning})
        self.log(f"  [{stage}] 경고: {warning}", "WARN")
        
    def log_summary(self):
        total_time = time.time() - self.start_time if self.start_time else 0
        self.log("")
        self.log("=" * 60)
        self.log("  교정 요약")
        self.log("=" * 60)
        self.log(f"  총 교정 수: {self.correction_count}")
        self.log(f"  총 소요 시간: {total_time:.2f}초")
        self.log(f"  오류 수: {len(self.errors)}")
        self.log(f"  경고 수: {len(self.warnings)}")
        if self.errors:
            self.log("\n  오류 목록:")
            for e in self.errors:
                self.log(f"    - [{e['stage']}] {e['error']}")
        if self.warnings:
            self.log("\n  경고 목록:")
            for w in self.warnings:
                self.log(f"    - [{w['stage']}] {w['warning']}")


class AIModelManager:
    def __init__(self, logger: DetailedLogger):
        self.logger = logger
        self.model = None
        self.tokenizer = None
        self.models_loaded = False
        
    def load_models(self):
        if not TRANSFORMERS_AVAILABLE:
            self.logger.log_warning("AI", "transformers 라이브러리 없음 - AI 모델 비활성화")
            return False
            
        self.logger.log_stage_start("AI 모델 로드")
        
        try:
            self.logger.log("  Qwen2.5 모델 로드 중: " + LOCAL_MODEL_PATH)
            self.tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH)
            self.model = AutoModelForCausalLM.from_pretrained(
                LOCAL_MODEL_PATH,
                torch_dtype=torch.bfloat16,
                device_map="auto"
            )
            self.model.eval()
            self.logger.log("  Qwen2.5 모델 로드 완료")
            
            self.models_loaded = True
            self.logger.log_stage_end("AI 모델 로드")
            return True
            
        except Exception as e:
            self.logger.log_error("AI 모델 로드", str(e), traceback.format_exc())
            return False
            
    def correct_text(self, text: str, task: str = "grammar") -> Tuple[str, bool]:
        if not self.models_loaded or not self.model:
            return text, False
            
        try:
            if task == "grammar":
                prompt = f"다음 문장의 문법을 교정하세요. 원문의 의미를 유지하면서 자연스러운 한국어로 수정하세요:\n{text}\n\n교정된 문장:"
            else:
                prompt = f"다음 문장의 오타를 교정하세요:\n{text}\n\n교정된 문장:"
            
            inputs = self.tokenizer(prompt, return_tensors="pt")
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_new_tokens=128,
                    do_sample=False,
                    temperature=0.1
                )
            
            corrected = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            if "교정된 문장:" in corrected:
                corrected = corrected.split("교정된 문장:")[-1].strip()
            return corrected, corrected != text
        except Exception as e:
            self.logger.log_error(task, str(e))
            return text, False
            
    def correct_grammar(self, text: str) -> Tuple[str, bool]:
        return self.correct_text(text, "grammar")
            
    def correct_typos(self, text: str) -> Tuple[str, bool]:
        return self.correct_text(text, "typos")


def parse_rules(rules_file: str) -> List[Tuple[str, str]]:
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


def load_china_place_rules() -> List[Tuple[str, str]]:
    return parse_rules(CHINA_PLACE_FILE)


def load_regex_rules() -> List[Tuple[str, re.Pattern, str]]:
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
                replacement = replacement.replace('\\1', '\x01REF1\x01').replace('\\2', '\x01REF2\x01').replace('\\3', '\x01REF3\x01')
                replacement = replacement.replace('\x01REF1\x01', '\\1').replace('\x01REF2\x01', '\\2').replace('\x01REF3\x01', '\\3')
                has_group_ref = bool(re.search(r'\\\d', replacement))
                has_meta = bool(re.search(r'[()\\[\]{}*+?|^$]', pattern))
                if not has_meta and not has_group_ref:
                    continue
                if ' ' in pattern and ' ' not in replacement:
                    continue
                try:
                    compiled = re.compile(pattern)
                    rules.append((pattern, compiled, replacement))
                except re.error as e:
                    print(f"  [정규식 오류] '{pattern}': {e}")
    rules.sort(key=lambda r: len(r[0]), reverse=True)
    return rules


def is_protected(pattern: str) -> bool:
    for p in PROTECT_LIST:
        if p in _PROTECT_EXACT:
            idx = pattern.find(p)
            while idx != -1:
                if idx == 0 or not pattern[idx-1].isalpha():
                    return True
                idx = pattern.find(p, idx + 1)
        else:
            if p in pattern:
                return True
    return False


def decompress_stream(data: bytes) -> Optional[bytes]:
    for wbits in [-15, 15, 31]:
        try:
            return zlib.decompress(data, wbits)
        except:
            continue
    return None


def decompress_stream_incremental(data: bytes) -> Optional[bytes]:
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


def decompress_stream_multi_segment(data: bytes) -> Optional[bytes]:
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


def decompress_chain(data: bytes) -> Optional[bytes]:
    dec = decompress_stream(data)
    if dec is not None:
        return dec
    dec = decompress_stream_incremental(data)
    if dec is not None:
        return dec
    dec = decompress_stream_multi_segment(data)
    return dec


def compress_to_size(data: bytes, target_size: int) -> Optional[bytes]:
    for level in range(1, 10):
        co = zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=-15)
        compressed = co.compress(data) + co.flush()
        if len(compressed) <= target_size:
            return compressed + b'\x00' * (target_size - len(compressed))
    return None


def parse_records(data: bytes) -> List[Dict]:
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


def serialize_records(records: List[Dict]) -> bytes:
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


def extract_text_from_hwp_binary(filepath: str, logger: DetailedLogger) -> str:
    if olefile is None:
        raise RuntimeError("olefile 모듈이 없습니다.")

    texts = []
    ole = olefile.OleFileIO(filepath, write_mode=False)
    try:
        streams = ole.listdir()
        body_streams = [s for s in streams if s and s[0] == "BodyText"]
        logger.log(f"  바이너리 본문 추출: BodyText 스트림 {len(body_streams)}개")

        for stream_path in body_streams:
            stream_name = '/'.join(stream_path)
            raw = ole.openstream(stream_name).read()
            dec = decompress_chain(raw)
            if dec is None:
                logger.log_warning("HWP 추출", f"{stream_name}: 압축 해제 실패")
                continue

            try:
                records = parse_records(dec)
            except Exception as e:
                logger.log_error("HWP 추출", f"{stream_name}: 레코드 파싱 실패", str(e))
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


def ollama_is_available() -> bool:
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


def post_ollama_chat(payload: Dict, timeout: int = 120, max_retries: int = 2) -> Dict:
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


def parse_ollama_json_array(resp_text: str) -> List:
    all_items = []
    pos = 0
    while pos < len(resp_text):
        start = resp_text.find('[', pos)
        if start < 0:
            break
        depth = 0
        end = start
        for i in range(start, len(resp_text)):
            if resp_text[i] == '[':
                depth += 1
            elif resp_text[i] == ']':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end > start:
            try:
                arr = json.loads(resp_text[start:end])
                if isinstance(arr, list) and len(arr) > 0:
                    all_items.extend(arr)
            except json.JSONDecodeError:
                pass
        pos = end if end > start else start + 1
    return all_items


def apply_dot_rules(text: str, logger: DetailedLogger) -> List[Tuple[str, str]]:
    corrections = []
    seen = set()

    quoted_dot_pattern = re.compile(r"([''""‘'][^'""’']+[''""’'])([·•・])([''""‘'][^'""’']+[''""’'])")
    for m in quoted_dot_pattern.finditer(text):
        orig = m.group(0)
        if orig in seen:
            continue
        seen.add(orig)
        repl = f"{m.group(1)}, {m.group(3)}"
        corrections.append((orig, repl))
        logger.log_correction("가운데점-따옴표", orig, repl, "따옴표 내 병렬")

    multi_quoted_dot = re.compile(r"([''""‘'][^'""’']+[''""’'])([·•・])([''""‘'][^'""’']+[''""’'])([·•・])([''""‘'][^'""’']+[''""’'])")
    for m in multi_quoted_dot.finditer(text):
        orig = m.group(0)
        if orig in seen:
            continue
        seen.add(orig)
        parts = re.split(r"[·•・]", orig)
        repl = ", ".join(parts)
        corrections.append((orig, repl))
        logger.log_correction("가운데점-따옴표", orig, repl, "따옴표 내 다중 병렬")

    dot_pattern = re.compile(r'([가-힣A-Za-z\u4e00-\u9fff]+)([·•・])([가-힣A-Za-z\u4e00-\u9fff]+)')
    matches = dot_pattern.findall(text)

    for left, dot, right in matches:
        orig = f"{left}{dot}{right}"
        if orig in seen:
            continue
        seen.add(orig)

        if re.search(r'[가-힣]\([가-힣·•・\u4e00-\u9fff]+\)', orig):
            logger.log(f"  [가운데점 유지-지명]: '{orig}' (지명 병렬)")
            continue

        if re.search(r'[\u4e00-\u9fff]{2,}[·•・][\u4e00-\u9fff]{2,}', orig):
            ctx_start = max(0, text.find(orig) - 30)
            ctx_end = min(len(text), text.find(orig) + len(orig) + 30)
            ctx = text[ctx_start:ctx_end]
            if '(' in ctx or '（' in ctx or '《' in ctx or '》' in ctx:
                logger.log(f"  [가운데점 유지-지명/책제목]: '{orig}'")
                continue

        if re.search(r'[가-힣]{2,}[·•・][가-힣]{2,}', orig):
            repl = f"{left}, {right}"
            corrections.append((orig, repl))
            logger.log_correction("가운데점", orig, repl, "병렬 단어")

    multi_dot = re.compile(r'([가-힣\u4e00-\u9fff]+)([·•·])([가-힣\u4e00-\u9fff]+)([·•·])([가-힣\u4e00-\u9fff]+)')
    for m in multi_dot.finditer(text):
        orig = m.group(0)
        if orig in seen:
            continue
        seen.add(orig)

        ctx_start = max(0, text.find(orig) - 30)
        ctx_end = min(len(text), text.find(orig) + len(orig) + 30)
        ctx = text[ctx_start:ctx_end]
        if '(' in ctx or '（' in ctx or '《' in ctx or '》' in ctx:
            logger.log(f"  [가운데점 유지-지명/책제목]: '{orig}'")
            continue

        parts = re.split(r'[·•·]', orig)
        if len(parts) >= 3:
            repl = ', '.join(parts)
            corrections.append((orig, repl))
            logger.log_correction("가운데점", orig, repl, "다중 병렬")

    return corrections


def collect_dot_corrections_with_ollama(text: str, logger: DetailedLogger) -> List[Tuple[str, str]]:
    corrections = []
    if not ollama_is_available():
        logger.log("  Ollama 미실행 - 규칙 기반 가운데점 교정 적용")
        return apply_dot_rules(text, logger)

    dot_contexts = []
    for dot in ["·", "•", "・"]:
        for m in re.finditer(r'.{0,15}' + re.escape(dot) + r'.{0,15}', text):
            ctx = m.group().strip()
            if ctx and ctx not in dot_contexts:
                dot_contexts.append(ctx)

    if not dot_contexts:
        logger.log("  가운데점 대상 없음")
        return corrections

    phonetic_pattern = re.compile(r'[a-z]\d*[·•・]|[·•・][a-z]\d*', re.IGNORECASE)
    filtered = [c for c in dot_contexts if not phonetic_pattern.search(c)]

    logger.log(f"  가운데점 문맥 발견: {len(dot_contexts)}개 (발음기호 제외: {len(filtered)}개)")
    for i, ctx in enumerate(filtered[:20]):
        logger.log(f"    [{i + 1}] {ctx}")
    if len(filtered) > 20:
        logger.log(f"    ... 외 {len(filtered) - 20}개 생략")

    batch_size = 50
    processed = 0
    for batch_start in range(0, len(filtered), batch_size):
        batch = filtered[batch_start:batch_start + batch_size]
        if not batch:
            continue

        dot_list = "\n".join([f'  {i + 1}. {c}' for i, c in enumerate(batch)])
        dot_prompt = f"""당신은 조선어 교정 전문가입니다. 가운데점(·, •, ・) 교정 규칙:

1. **병렬 단어 나열** (2개 이상 동등한 단어): 가운데점 → 쉼표+공백(, )으로 변경
   - 서울·부산 → 서울, 부산
   - 사랑·평화·행복 → 사랑, 평화, 행복

2. **지명/책제목/인명**: 가운데점 유지
   - 홍길동전·춘향전 (책 제목 병렬)
   - 베이징·상하이 (지명 병렬)

다음 문맥에서 가운데점 교정이 필요한 것만 JSON 배열로 반환:
[{{"원본": "...", "교정": "...", "이유": "병렬단어|지명유지|..."}}]

문맥 목록:
{dot_list}

교정이 필요한 것만 반환:"""

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": dot_prompt}],
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 2048}
        }

        logger.log(f"  [가운데점 배치 {batch_start // batch_size + 1}] 문맥 {len(batch)}개 처리 중...")

        try:
            resp = post_ollama_chat(payload, timeout=OLLAMA_DOT_TIMEOUT)
            resp_text = resp.get("message", {}).get("content", "")
            logger.log(f"  [가운데점-Ollama 응답] (문맥 {len(batch)}개): {resp_text[:200]}...")

            items = parse_ollama_json_array(resp_text)
            for item in items:
                if isinstance(item, dict) and "원본" in item and "교정" in item:
                    orig = item["원본"]
                    repl = item["교정"]
                    if orig != repl and orig in text:
                        corrections.append((orig, repl))
                        reason = item.get("이유", "Ollama 판단")
                        logger.log_correction("가운데점-Ollama", orig, repl, reason)
            processed += len(batch)
        except Exception as e:
            logger.log_error("가운데점-Ollama", str(e))
            processed += len(batch)
            continue

    logger.log(f"  가운데점 교정 결과: {len(corrections)}개 교정 / {processed}개 처리됨 (전체 {len(dot_contexts)}개)")
    if len(corrections) == 0:
        logger.log("  Ollama 응답 없음 - 규칙 기반 가운데점 교정 적용")
        return apply_dot_rules(text, logger)
    return corrections


def apply_quote_rules(text: str, logger: DetailedLogger) -> List[Tuple[str, str]]:
    corrections = []
    seen = set()

    quote_patterns = [
        (re.compile(r'"'), '"', "중국어 따옴표 → 한국어 따옴표"),
        (re.compile(r'"'), '"', "중국어 따옴표 → 한국어 따옴표"),
        (re.compile(r"'"), ''', "중국어 작은따옴표 → 한국어 작은따옴표"),
        (re.compile(r"'"), ''', "중국어 작은따옴표 → 한국어 작은따옴표"),
    ]

    for pattern, replacement, reason in quote_patterns:
        matches = list(pattern.finditer(text))
        if matches:
            orig = pattern.pattern
            if orig not in seen:
                seen.add(orig)
                count = len(matches)
                logger.log_correction("따옴표", orig, replacement, f"{reason} ({count}개)")
                corrections.append((orig, replacement))

    return corrections


def collect_quote_corrections_with_ollama(text: str, logger: DetailedLogger) -> List[Tuple[str, str]]:
    corrections = []
    if not ollama_is_available():
        logger.log("  Ollama 미실행 - 규칙 기반 따옴표 교정 적용")
        return apply_quote_rules(text, logger)

    quote_contexts = []
    for quote in ['"', "'", '"', ''', ''']:
        pattern = re.compile(r'.{0,20}' + re.escape(quote) + r'.{0,20}')
        for m in pattern.finditer(text):
            ctx = m.group().strip()
            if ctx and ctx not in quote_contexts:
                quote_contexts.append(ctx)

    if not quote_contexts:
        logger.log("  따옴표 대상 없음")
        return corrections

    logger.log(f"  따옴표 문맥 발견: {len(quote_contexts)}개")
    for i, ctx in enumerate(quote_contexts[:20]):
        logger.log(f"    [{i + 1}] {ctx}")
    if len(quote_contexts) > 20:
        logger.log(f"    ... 외 {len(quote_contexts) - 20}개 생략")

    batch_size = 30
    processed = 0
    for batch_start in range(0, len(quote_contexts), batch_size):
        batch = quote_contexts[batch_start:batch_start + batch_size]
        if not batch:
            continue

        quote_list = "\n".join([f'  {i + 1}. {c}' for i, c in enumerate(batch)])
        quote_prompt = f"""당신은 조선어 교정 전문가입니다. 따옴표 교정 규칙:

1. **대화문**: 큰따옴표(" ") 사용
2. **인용구**: 큰따옴표(" ") 사용
3. **강조**: 작은따옴표(' ') 사용
4. **단어 강조**: 작은따옴표(' ') 사용

다음 문맥에서 따옴표 교정이 필요한 것만 JSON 배열로 반환:
[{{"원본": "...", "교정": "...", "이유": "대화문|인용구|..."}}]

문맥 목록:
{quote_list}

교정이 필요한 것만 반환:"""

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": quote_prompt}],
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 2048}
        }

        logger.log(f"  [따옴표 배치 {batch_start // batch_size + 1}] 문맥 {len(batch)}개 처리 중...")

        try:
            resp = post_ollama_chat(payload, timeout=OLLAMA_QUOTE_TIMEOUT)
            resp_text = resp.get("message", {}).get("content", "")
            logger.log(f"  [따옴표-Ollama 응답] (문맥 {len(batch)}개): {resp_text[:200]}...")

            items = parse_ollama_json_array(resp_text)
            for item in items:
                if isinstance(item, dict) and "원본" in item and "교정" in item:
                    orig = item["원본"]
                    repl = item["교정"]
                    if orig != repl and orig in text:
                        corrections.append((orig, repl))
                        reason = item.get("이유", "Ollama 판단")
                        logger.log_correction("따옴표-Ollama", orig, repl, reason)
            processed += len(batch)
        except Exception as e:
            logger.log_error("따옴표-Ollama", str(e))
            processed += len(batch)
            continue

    logger.log(f"  따옴표 교정 결과: {len(corrections)}개 교정 / {processed}개 처리됨 (전체 {len(quote_contexts)}개)")
    if len(corrections) == 0:
        logger.log("  Ollama 응답 없음 - 규칙 기반 따옴표 교정 적용")
        return apply_quote_rules(text, logger)
    return corrections


def apply_corrections(text: str, corrections: List[Tuple[str, str]], logger: DetailedLogger) -> str:
    if not corrections:
        return text

    sorted_corrections = sorted(corrections, key=lambda x: len(x[0]), reverse=True)
    for orig, repl in sorted_corrections:
        if orig in text:
            text = text.replace(orig, repl)
            logger.log(f"    적용: '{orig}' -> '{repl}'")
    return text


def proofread_file(filepath: str, rules: List[Tuple[str, str]], china_rules: List[Tuple[str, str]],
                   regex_rules: List[Tuple[str, re.Pattern, str]], ai_manager: AIModelManager,
                   logger: DetailedLogger, stages: str = "all") -> Tuple[str, int]:
    logger.log_section(f"파일: {os.path.basename(filepath)}")
    
    text = extract_text_from_hwp_binary(filepath, logger)
    logger.log(f"  텍스트 추출: {len(text):,}자")
    
    all_corrections = []
    
    if stages in ["all", "1"]:
        logger.log_stage_start("1단계: 중한 규칙")
        stage_corrections = []
        for src, dst in china_rules:
            if src in text and not is_protected(src):
                count = text.count(src)
                stage_corrections.append((src, dst))
                logger.log_correction("중한-지명", src, dst, f"{count}개")
        all_corrections.extend(stage_corrections)
        text = apply_corrections(text, stage_corrections, logger)
        logger.log(f"  1단계 결과: {len(stage_corrections)}개 교정")
        logger.log_stage_end("1단계")

    if stages in ["all", "2"]:
        logger.log_stage_start("2단계: TXT 통합규칙")
        stage_corrections = []
        for src, dst in rules:
            if src in text and not is_protected(src):
                count = text.count(src)
                stage_corrections.append((src, dst))
                if count <= 5:
                    logger.log_correction("TXT규칙", src, dst, f"{count}개")
        all_corrections.extend(stage_corrections)
        text = apply_corrections(text, stage_corrections, logger)
        logger.log(f"  2단계 결과: {len(stage_corrections)}개 교정")
        logger.log_stage_end("2단계")

    if stages in ["all", "2.5"] and regex_rules:
        logger.log_stage_start("2.5단계: 정규식 규칙")
        stage_corrections = []
        for pattern, compiled, replacement in regex_rules:
            new_text = compiled.sub(replacement, text)
            if new_text != text:
                matches = compiled.findall(text)
                if matches:
                    sample = matches[0] if isinstance(matches[0], str) else str(matches[0])
                    logger.log_correction("정규식", sample, replacement.replace('\\1', '...'), f"{len(matches)}개")
                    stage_corrections.append((pattern, replacement))
                text = new_text
        logger.log(f"  2.5단계 결과: {len(stage_corrections)}개 교정")
        logger.log_stage_end("2.5단계: 정규식 규칙")

    if stages in ["all", "3"]:
        logger.log_stage_start("3단계: 가운데점 교정")
        stage_corrections = collect_dot_corrections_with_ollama(text, logger)
        all_corrections.extend(stage_corrections)
        text = apply_corrections(text, stage_corrections, logger)
        logger.log(f"  3단계 결과: {len(stage_corrections)}개 교정")
        logger.log_stage_end("3단계")

    if stages in ["all", "4"]:
        logger.log_stage_start("4단계: 따옴표 교정")
        stage_corrections = collect_quote_corrections_with_ollama(text, logger)
        quote_patterns = [
            (re.compile(r'"'), '"'),
            (re.compile(r'"'), '"'),
            (re.compile(r"'"), '''),
            (re.compile(r"'"), '''),
        ]
        quote_count = 0
        for pattern, replacement in quote_patterns:
            new_text = pattern.sub(replacement, text)
            if new_text != text:
                matches = pattern.findall(text)
                count = len(matches)
                logger.log_correction("따옴표", pattern.pattern, replacement, f"중국어→한국어 ({count}개)")
                text = new_text
                quote_count += 1
        logger.log(f"  4단계 결과: {quote_count}개 교정")
        logger.log_stage_end("4단계")

    if stages in ["all", "5"] and ai_manager.models_loaded:
        logger.log_stage_start("5단계: AI 문법 교정")
        corrected, changed = ai_manager.correct_grammar(text)
        if changed:
            logger.log_correction("AI-문법", text[:100] + "...", corrected[:100] + "...", "GEC 모델")
            text = corrected
        logger.log_stage_end("5단계")

    if stages in ["all", "6"] and ai_manager.models_loaded:
        logger.log_stage_start("6단계: AI 오타 교정")
        corrected, changed = ai_manager.correct_typos(text)
        if changed:
            logger.log_correction("AI-오타", text[:100] + "...", corrected[:100] + "...", "Typos 모델")
            text = corrected
        logger.log_stage_end("6단계")

    return text, len(all_corrections)


def main():
    logger = DetailedLogger(LOG_FILE)
    logger.open()
    
    logger.log("")
    logger.log("#" * 60)
    logger.log("HWP 교정 시스템 v19.0")
    logger.log(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.log("#" * 60)
    
    logger.log_stage_start("규칙 로드")
    rules = parse_rules(RULES_FILE)
    china_rules = load_china_place_rules()
    regex_rules = load_regex_rules()
    logger.log(f"  중한 규칙: {len(china_rules)}개")
    logger.log(f"  TXT 규칙: {len(rules)}개")
    logger.log(f"  정규식 규칙: {len(regex_rules)}개")
    logger.log_stage_end("규칙 로드")
    
    logger.log_stage_start("AI 모델 초기화")
    ai_manager = AIModelManager(logger)
    ai_loaded = ai_manager.load_models()
    logger.log(f"  AI 모델 상태: {'로드됨' if ai_loaded else '비활성화'}")
    logger.log_stage_end("AI 모델 초기화")
    
    logger.log(f"  Ollama 상태: {'연결됨' if ollama_is_available() else '미실행'}")
    
    if not os.path.exists(HWP_DIR):
        logger.log_error("메인", f"HWP 디렉토리 없음: {HWP_DIR}")
        logger.close()
        return
        
    hwp_files = [f for f in os.listdir(HWP_DIR) if f.lower().endswith('.hwp')]
    logger.log(f"  HWP 파일: {len(hwp_files)}개")
    
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        
    for i, hwp_file in enumerate(hwp_files):
        logger.log(f"\n[{i + 1}/{len(hwp_files)}] 처리 시작")
        filepath = os.path.join(HWP_DIR, hwp_file)
        
        try:
            corrected_text, correction_count = proofread_file(
                filepath, rules, china_rules, regex_rules, ai_manager, logger
            )
            logger.log(f"  총 교정 항목: {correction_count}개")
        except Exception as e:
            logger.log_error("파일 처리", f"{hwp_file}: {str(e)}", traceback.format_exc())
            
    logger.log_summary()
    logger.close()


if __name__ == "__main__":
    main()
