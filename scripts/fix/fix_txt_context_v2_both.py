import sys, os, time, re, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

FILES = {
    "K": r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp",
    "J": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp",
}

R = 50

def kill_hwp():
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(3)

def judge_split(word, ctx):
    if word == "집안":
        if any(w in ctx for w in ["집안일", "집안사람", "집안식구", "문중", "종중", "가문", "온 집안이", "온 집안"]):
            return False
        if any(w in ctx for w in ["집안에", "집안에서", "집안으로", "집안의", "집안까지", "집안은"]):
            before = ctx[:ctx.find("집안")]
            if any(w in before for w in ["가족", "식구", "문중", "종중", "가문"]):
                return False
            return True
        return False

    if word == "하는데":
        if any(w in ctx for w in ["하는데 필요", "하는데 쓰", "하는데 사용", "하는데 소요", "하는데 있", "하는데 나", "하는데 드"]):
            return True
        return False

    if word == "한데":
        if any(w in ctx for w in ["한데 필요", "한데 쓰", "한데 사용", "한데 있", "한데 나", "한데 드"]):
            return True
        return False

    if word == "본적":
        if any(w in ctx for w in ["본적이", "본 적이"]):
            return True
        return False

    if word == "방안":
        if any(w in ctx for w in ["방안에", "방안에서", "방안으로", "방안의", "방안은", "방안이"]):
            if not any(w in ctx for w in ["구급방안", "구급책", "연산방안", "기본연산방안"]):
                return True
        return False

    if word == "간적":
        if any(w in ctx for w in ["간 적이", "적이 있", "적이없"]):
            return True
        return False

    if word == "간지":
        if any(w in ctx for w in ["간지기일", "간지(干支)", "륙십간지", "육십간지", "간지법"]):
            return False
        return False

    if word == "산지":
        if any(w in ctx for w in ["원산지", "집산지", "생산지", "산지가", "산지의"]):
            return False
        return False

    if word == "할지":
        if any(w in ctx for w in ["할지라도", "할지언정", "할지도"]):
            return False
        if any(w in ctx for w in ["할 지", "지 모른", "지 결정", "지 알"]):
            return True
        return False

    if word == "한지":
        if any(w in ctx for w in ["한지에", "한지로", "종이", "도화지", "전지"]):
            return False
        if any(w in ctx for w in ["한 지가", "한 지를", "출근한지", "된지", "지 거의"]):
            return True
        return False

    if word == "두발":
        if any(w in ctx for w in ["진두발", "구두발표", "구두토론", "구두담판", "구두협정", "구두통보", "구두제출", "구두로"]):
            return False
        if any(w in ctx for w in ["두발로", "두발을"]):
            return True
        return False

    return False

def find_context_replacements(text, word, dst):
    replacements = []
    idx = 0
    while True:
        pos = text.find(word, idx)
        if pos == -1:
            break
        start = max(0, pos - R)
        end = min(len(text), pos + len(word) + R)
        ctx = text[start:end].replace('\r', ' ').replace('\n', ' ')

        if judge_split(word, ctx):
            extended_start = max(0, pos - 5)
            extended_end = min(len(text), pos + len(word) + 5)
            extended = text[extended_start:extended_end].replace('\r', ' ').replace('\n', ' ')
            replacements.append((extended, word, dst, ctx))

        idx = pos + len(word)
    return replacements

def apply_find_replace_one(hwp, find_str, replace_str):
    try:
        hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = find_str
        hwp.HParameterSet.HFindReplace.ReplaceString = replace_str
        hwp.HParameterSet.HFindReplace.Direction = 0
        hwp.HParameterSet.HFindReplace.ReplaceMode = 0x0101
        hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        hwp.HParameterSet.HFindReplace.FindType = 0
        result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        return result
    except Exception as e:
        print(f"    [ERR] {e}")
        return False

def process_file(label, fpath):
    if not os.path.exists(fpath):
        print(f"\n[{label}] 파일 없음")
        return

    text = extract_text_from_hwp_binary(fpath)
    print(f"\n{'=' * 70}")
    print(f"  [{label}] {os.path.basename(fpath)}")
    print(f"{'=' * 70}")

    simple_rules = [
        ("해본적", "해본 적"),
        ("들어본적", "들어본 적"),
        ("겪어본적", "겪어본 적"),
        ("판적", "판 적"),
        ("줄밖", "줄 밖"),
        ("늘어놓을줄밖", "늘어놓을줄 밖"),
        ("말한대로", "말한 대로"),
        ("한대로", "한 대로"),
    ]

    context_words = [
        ("집안", "집 안"),
        ("하는데", "하는 데"),
        ("한데", "한 데"),
        ("본적", "본 적"),
        ("방안", "방 안"),
        ("간적", "간 적"),
        ("할지", "할 지"),
        ("한지", "한 지"),
        ("두발", "두 발"),
    ]

    all_replacements = []

    for src, dst in simple_rules:
        cnt = text.count(src)
        if cnt > 0:
            for _ in range(cnt):
                all_replacements.append((src, dst, "simple"))

    for word, dst in context_words:
        reps = find_context_replacements(text, word, dst)
        for extended, src, dst, ctx in reps:
            all_replacements.append((src, dst, f"ctx:{extended[:30]}"))

    print(f"  총 교정: {len(all_replacements)}건")
    for src, dst, note in all_replacements[:20]:
        print(f"    '{src}' → '{dst}' ({note})")
    if len(all_replacements) > 20:
        print(f"    ... 외 {len(all_replacements) - 20}건")

    if not all_replacements:
        print(f"  수정 불필요")
        return

    kill_hwp()
    pythoncom.CoInitialize()
    CLSCTX_LOCAL_SERVER = 4
    try:
        hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=CLSCTX_LOCAL_SERVER)
        for mod in ("FilePathCheckerModule", "SecurityModule"):
            try:
                hwp.RegisterModule("FilePathCheckDLL", mod)
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

        hwp.Open(fpath, "HWP", "forceopen:true")
        print(f"  파일 열기 성공")

        total = 0
        for src, dst, note in all_replacements:
            result = apply_find_replace_one(hwp, src, dst)
            if result:
                total += 1
            time.sleep(0.1)

        print(f"  적용: {total}/{len(all_replacements)}건")

        try:
            hwp.Save()
            print(f"  저장 완료")
        except Exception as e:
            print(f"  저장 실패: {e}")

        try:
            hwp.Quit()
        except Exception:
            pass

    except Exception as e:
        print(f"  COM 오류: {e}")
        try:
            hwp.Quit()
        except Exception:
            pass
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

def main():
    for label, fpath in FILES.items():
        process_file(label, fpath)
        kill_hwp()
        time.sleep(3)

if __name__ == "__main__":
    main()
