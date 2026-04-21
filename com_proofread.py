# -*- coding: utf-8 -*-
import os, sys, io, time, shutil, re, struct, zlib, subprocess, tempfile, ctypes, glob

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

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "com_proofread_log.txt")
RULES_FILE = r"C:\Users\doris\Desktop\xwechat_files\WORD\rules_documentation.txt"
CHINA_PLACE_FILE = r"C:\Users\doris\Desktop\xwechat_files\WORD\rules_china_place.txt"
HWP_DIR = r"C:\사전"

LDQ = '\u201c'
RDQ = '\u201d'
LSQ = '\u2018'
RSQ = '\u2019'

PROTECT_LIST = [
    "이것", "그것", "저것", "이것저것",
    "산하", "강하",
    "뜻밖", "제대로", "그대로", "함께", "사뿐", "가듯",
    "그만큼", "뜻대로", "마음대로",
    "대·수수깡", "신부·유전학", "장중보옥·금지옎엽", "물건·쓸모없는", "시문·음악",
    "흉·복벽의", "기초작업·공사", "체재·출판년월일", "활동·운동의", "산지·西山",
    "5·4운동", "아시아·태평양", "나라·주", "열대·아열대",
    "는데", "은데", "인데", "한데", "한대로",
    "한적하다", "한가하다", "한적한", "한적이", "한지",
    "판적", "두발", "할지", "할지어다", "할지라도", "할지니",
    "별의별것",
    "방안", "방안하다", "체포방안", "구급방안", "설계방안", "한어병음방안",
    "방안을", "방안이", "방안은", "방안도",
    "집안", "집안살림", "한집안", "집안일", "집안사람",
    "집안이", "집안을", "집안은", "집안도", "집안에",
    "쓸데없는", "쓸데없이", "쓸데없다",
    "무엇인지", "살고있는", "알데", "간적", "본적", "간지",
    "산들바", "산지",
    "쓸수있다", "쓸수없다", "쓸수있으나", "쓸수없음",
    "입안에", "입안이", "입안을",
]

_PROTECT_EXACT = {"산하", "강하"}


def is_protected(pattern):
    for p in PROTECT_LIST:
        if p in _PROTECT_EXACT:
            idx = pattern.find(p)
            while idx != -1:
                if idx == 0 or not pattern[idx - 1].isalpha():
                    return True
                idx = pattern.find(p, idx + 1)
        else:
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
                if src != dst and src not in seen:
                    seen.add(src)
                    rules.append((src, dst))
    return rules


def log_msg(msg, fh=None):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    if fh:
        try:
            fh.write(line + "\n")
            fh.flush()
        except:
            pass


def kill_hwp_processes():
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", "Hwp.exe"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            log_msg("HWP 프로세스 종료됨")
            time.sleep(2)
    except Exception:
        pass


def remove_readonly(filepath):
    try:
        kernel32 = ctypes.windll.kernel32
        attrs = kernel32.GetFileAttributesW(filepath)
        if attrs != -1 and (attrs & 1):
            kernel32.SetFileAttributesW(filepath, attrs & ~1)
    except Exception:
        pass


def decompress_chain(data):
    for wbits in [-15, 15, 31]:
        try:
            return zlib.decompress(data, wbits)
        except:
            pass
    dc = zlib.decompressobj(wbits=-15)
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
        records.append({"tag_id": tag_id, "level": level, "payload": payload})
        offset += header_size + size
    return records


def extract_text_olefile(filepath):
    if olefile is None:
        return ""
    texts = []
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
            records = parse_records(dec)
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


def connect_hwp_com():
    if win32com is None:
        log_msg("COM 자동화 모듈 없음")
        return None

    prog_id = "HWPFrame.HwpObject"

    try:
        hwp = win32com.client.Dispatch(prog_id)
        hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
        log_msg(f"HWP COM 연결 성공: {prog_id} (Dispatch)")
        return hwp
    except Exception as e:
        log_msg(f"HWP COM 연결 실패: {e}")
        return None


def close_hwp_com(hwp):
    try:
        if hwp is not None:
            hwp.Quit()
    except Exception:
        try:
            if hwp is not None:
                hwp.Clear(1)
        except Exception:
            pass


def process_single_file(filepath, txt_rules, china_rules, log_fh=None):
    fname = os.path.basename(filepath)
    log_msg(f"\n{'=' * 60}", log_fh)
    log_msg(f"파일: {fname}", log_fh)
    log_msg(f"{'=' * 60}", log_fh)

    remove_readonly(filepath)

    full_text = extract_text_olefile(filepath)
    log_msg(f"텍스트 추출: {len(full_text):,}자", log_fh)

    if not full_text.strip():
        log_msg("텍스트 없음 - 건너뜀", log_fh)
        return 0, []

    corrections = []

    log_msg("--- 1단계: 중한 규칙 ---", log_fh)
    china_matched = set()
    for orig, repl in china_rules:
        if orig in full_text:
            cnt = full_text.count(orig)
            corrections.append((orig, repl, "중한규칙", cnt))
            china_matched.add(orig)
            log_msg(f"  [중한]: '{orig}' -> '{repl}' ({cnt})", log_fh)

    log_msg("--- 2단계: TXT 규칙 ---", log_fh)
    for src, dst in txt_rules:
        if src in full_text and not is_protected(src):
            skip = False
            for cms in china_matched:
                if src in cms or cms in src:
                    skip = True
                    break
            if skip:
                continue
            cnt = full_text.count(src)
            corrections.append((src, dst, "TXT규칙", cnt))
            log_msg(f"  [TXT]: '{src}' -> '{dst}' ({cnt})", log_fh)

    log_msg("--- 3단계: 따옴표 규칙 ---", log_fh)
    for q in re.findall(re.escape(LDQ) + r'([^' + re.escape(RDQ) + r']{1,50})' + re.escape(RDQ), full_text):
        orig = f"{LDQ}{q}{RDQ}"
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', q))
        if has_chinese and len(q) <= 6:
            corr = f"{LSQ}{q}{RSQ}"
            corrections.append((orig, corr, "따옴표", 1))
            log_msg(f"  [따옴표]: '{orig}' -> '{corr}'", log_fh)

    log_msg(f"총 교정 항목: {len(corrections)}개", log_fh)

    if not corrections:
        log_msg("교정 항목 없음", log_fh)
        return 0, corrections

    existing_bak = filepath + ".bak"
    if not os.path.exists(existing_bak):
        try:
            shutil.copy2(filepath, existing_bak)
            log_msg(f"백업 생성: {os.path.basename(existing_bak)}", log_fh)
        except Exception as e:
            log_msg(f"백업 실패: {e}", log_fh)

    log_msg("--- COM 안전 저장 시작 ---", log_fh)
    hwp = connect_hwp_com()
    if hwp is None:
        log_msg("COM 연결 실패", log_fh)
        return 0, corrections

    temp_dir = os.path.join(os.environ.get('TEMP', tempfile.gettempdir()), 'hwp_proofread')
    os.makedirs(temp_dir, exist_ok=True)
    safe_name = f"work_{id(filepath) % 100000}.hwp"
    temp_hwp = os.path.join(temp_dir, safe_name)
    if os.path.exists(temp_hwp):
        os.remove(temp_hwp)
    shutil.copy2(filepath, temp_hwp)
    log_msg(f"임시 파일: {temp_hwp}", log_fh)

    total_applied = 0
    try:
        open_result = hwp.Open(temp_hwp, "", "")
        if not open_result:
            log_msg("COM: 파일 열기 실패", log_fh)
            close_hwp_com(hwp)
            return 0, corrections
        log_msg("COM: 파일 열기 성공 (임시파일)", log_fh)

        for i, (orig, repl, rule_type, cnt) in enumerate(corrections):
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
                    total_applied += cnt
                    log_msg(f"  [{i+1}/{len(corrections)}] OK: '{orig}' -> '{repl}'", log_fh)
                else:
                    log_msg(f"  [{i+1}/{len(corrections)}] No match: '{orig}'", log_fh)
            except Exception as e:
                log_msg(f"  [{i+1}/{len(corrections)}] Error: '{orig}' - {e}", log_fh)

        try:
            hwp.Save()
            log_msg("COM 저장 완료 (임시파일)", log_fh)
        except Exception as e:
            log_msg(f"COM 저장 실패: {e}", log_fh)
            close_hwp_com(hwp)
            return 0, corrections

    except Exception as e:
        log_msg(f"COM 처리 실패: {e}", log_fh)
        close_hwp_com(hwp)
        return 0, corrections

    close_hwp_com(hwp)
    time.sleep(2)
    kill_hwp_processes()

    remove_readonly(filepath)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        shutil.copy2(temp_hwp, filepath)
        log_msg(f"원본 복원: {filepath}", log_fh)
    except PermissionError:
        log_msg("복사 실패 (PermissionError), 재시도...", log_fh)
        time.sleep(3)
        kill_hwp_processes()
        remove_readonly(filepath)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            shutil.copy2(temp_hwp, filepath)
            log_msg(f"원본 복원 (재시도): {filepath}", log_fh)
        except Exception as e2:
            log_msg(f"복사 실패: {e2}", log_fh)
            log_msg(f"결과 파일: {temp_hwp}", log_fh)
    except Exception as e:
        log_msg(f"복사 실패: {e}", log_fh)
        log_msg(f"결과 파일: {temp_hwp}", log_fh)

    log_msg(f"적용 결과: {total_applied}건 수정", log_fh)
    return total_applied, corrections


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args:
        target = HWP_DIR
    else:
        target = args[0].strip('"')

    files = []
    if target.lower().endswith('.hwp'):
        matched = glob.glob(target)
        if matched:
            files = matched
    elif glob.glob(os.path.join(target, "*.hwp")):
        files = glob.glob(os.path.join(target, "*.hwp"))

    if not files:
        files = [os.path.join(HWP_DIR, f) for f in os.listdir(HWP_DIR)
                 if f.endswith('.hwp') and not f.startswith('~')]
        files = [f for f in files if os.path.exists(f)]

    if not files:
        log_msg(f"HWP 파일 없음: {target}")
        return

    txt_rules = parse_rules(RULES_FILE)
    china_rules = parse_rules(CHINA_PLACE_FILE)

    log_msg("=" * 60)
    log_msg("HWP 교정 (COM + DispatchEx + forceopen)")
    log_msg(f"대상: {len(files)}개 파일")
    log_msg(f"중한 규칙: {len(china_rules)}개")
    log_msg(f"TXT 규칙: {len(txt_rules)}개")
    log_msg("=" * 60)

    kill_hwp_processes()

    with open(LOG_FILE, 'a', encoding='utf-8') as log_fh:
        log_msg(f"\n{'#' * 60}", log_fh)
        log_msg(f"HWP 교정: {time.strftime('%Y-%m-%d %H:%M:%S')}", log_fh)
        log_msg(f"중한 규칙: {len(china_rules)}개", log_fh)
        log_msg(f"TXT 규칙: {len(txt_rules)}개", log_fh)
        log_msg(f"{'#' * 60}\n", log_fh)

        grand_total = 0
        all_file_results = []

        for i, fp in enumerate(files):
            log_msg(f"\n[{i + 1}/{len(files)}] 처리 시작", log_fh)
            applied, corrections = process_single_file(fp, txt_rules, china_rules, log_fh)
            grand_total += applied
            all_file_results.append((os.path.basename(fp), len(corrections), applied))
            time.sleep(1)

        log_msg(f"\n{'=' * 60}", log_fh)
        log_msg("전체 완료!", log_fh)
        log_msg(f"{'=' * 60}", log_fh)
        for fname, items, applied in all_file_results:
            log_msg(f"  {fname}: {items}개 항목, {applied}건 적용", log_fh)
        log_msg(f"\n총 적용 건수: {grand_total}건", log_fh)
        log_msg(f"{'=' * 60}\n", log_fh)

    log_msg(f"\n완료! 로그: {LOG_FILE}")


if __name__ == "__main__":
    main()
