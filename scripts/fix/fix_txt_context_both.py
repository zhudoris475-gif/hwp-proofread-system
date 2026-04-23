import sys, os, time, re, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

FILES = {
    "K": r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp",
    "J": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp",
}

SPLIT_RULES = [
    ("해본적", "해본 적"),
    ("들어본적", "들어본 적"),
    ("겪어본적", "겪어본 적"),
    ("판적", "판 적"),
    ("줄밖", "줄 밖"),
    ("말한대로", "말한 대로"),
    ("한대로", "한 대로"),
    ("늘어놓을줄밖", "늘어놓을줄 밖"),
]

NOSPLIT_WORDS = [
    "강하", "산하", "뜻대로", "그만큼", "많은데", "깊은데",
    "알데", "포름알데", "놀포름알데", "메타알데", "아쎄트알데",
]

def kill_hwp():
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(3)

def get_context_corrections(text, word, dst):
    corrections = []
    R = 40
    idx = 0
    while True:
        pos = text.find(word, idx)
        if pos == -1:
            break
        start = max(0, pos - R)
        end = min(len(text), pos + len(word) + R)
        ctx = text[start:end].replace('\r', ' ').replace('\n', ' ')

        should_split = False

        if word == "집안":
            if any(w in ctx for w in ["집안에", "집안에서", "집안으로", "집안의", "집안까지"]):
                before = ctx[:ctx.find("집안")]
                if not any(w in before for w in ["가족", "식구", "문중", "종중", "가문"]):
                    should_split = True
            if not should_split and "온 집안이" in ctx:
                should_split = False

        elif word == "하는데":
            if any(w in ctx for w in ["하는데 필요", "하는데 쓰", "하는데 사용", "하는데 소요", "하는데 있", "하는데 나"]):
                should_split = True

        elif word == "한데":
            if any(w in ctx for w in ["한데 필요", "한데 쓰", "한데 사용", "한데 있", "한데 나"]):
                should_split = True

        elif word == "본적":
            if any(w in ctx for w in ["본적이", "본 적이"]):
                should_split = True

        elif word == "방안":
            if any(w in ctx for w in ["방안에", "방안에서", "방안으로", "방안의", "방안은"]):
                if not any(w in ctx for w in ["구급방안", "구급책", "연산방안"]):
                    should_split = True

        elif word == "간적":
            if any(w in ctx for w in ["간 적이", "적이 있", "적이없"]):
                should_split = True

        elif word == "간지":
            if any(w in ctx for w in ["간지기일", "간지(干支)", "륙십간지"]):
                should_split = False

        elif word == "산지":
            if any(w in ctx for w in ["원산지", "집산지", "생산지", "산지가", "산지의"]):
                should_split = False

        elif word == "할지":
            if any(w in ctx for w in ["할지라도", "할지언정", "할지도"]):
                should_split = False
            elif any(w in ctx for w in ["할 지", "지 모른", "지 결정"]):
                should_split = True

        elif word == "한지":
            if any(w in ctx for w in ["한지에", "한지로", "종이"]):
                should_split = False
            elif any(w in ctx for w in ["한 지가", "한 지를", "출근한지", "된지"]):
                should_split = True

        elif word == "두발":
            if any(w in ctx for w in ["진두발", "구두발표", "구두토론", "구두담판", "구두협정", "구두통보", "구두제출"]):
                should_split = False
            elif any(w in ctx for w in ["두발로", "두발을"]):
                should_split = True

        if should_split:
            corrections.append((word, dst, ctx))

        idx = pos + len(word)

    return corrections

def apply_com_replacements(filepath, corrections_list):
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

        hwp.Open(filepath, "HWP", "forceopen:true")
        print(f"  파일 열기 성공")

        total = 0
        for src, dst, ctx in corrections_list:
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 0x0101
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 0
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    total += 1
                    print(f"    [OK] '{src}' → '{dst}'")
                else:
                    print(f"    [SKIP] '{src}' → '{dst}'")
                time.sleep(0.3)
            except Exception as e:
                print(f"    [FAIL] '{src}' ({e})")

        try:
            hwp.Save()
            print(f"  저장 완료 ({total}건)")
        except Exception as e:
            print(f"  저장 실패: {e}")
            return False

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
        return False
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

    return True

def main():
    for label, fpath in FILES.items():
        if not os.path.exists(fpath):
            print(f"\n[{label}] 파일 없음")
            continue

        text = extract_text_from_hwp_binary(fpath)
        print(f"\n{'=' * 70}")
        print(f"  [{label}] {os.path.basename(fpath)}")
        print(f"{'=' * 70}")

        all_corrections = []

        print(f"\n  --- 무조건 분리 규칙 ---")
        for src, dst in SPLIT_RULES:
            cnt = text.count(src)
            if cnt > 0:
                print(f"    '{src}' → '{dst}' ({cnt}건)")
                for _ in range(cnt):
                    all_corrections.append((src, dst, ""))

        print(f"\n  --- 문맥 판별 규칙 ---")
        context_words = [
            ("집안", "집 안"),
            ("하는데", "하는 데"),
            ("한데", "한 데"),
            ("본적", "본 적"),
            ("방안", "방 안"),
            ("간적", "간 적"),
            ("간지", "간 지"),
            ("산지", "산 지"),
            ("할지", "할 지"),
            ("한지", "한 지"),
            ("두발", "두 발"),
        ]

        for word, dst in context_words:
            corrections = get_context_corrections(text, word, dst)
            if corrections:
                print(f"    '{word}' → '{dst}' ({len(corrections)}건 분리)")
                all_corrections.extend(corrections)

        print(f"\n  --- 유지 규칙 (분리불가) ---")
        for word in NOSPLIT_WORDS:
            cnt = text.count(word)
            if cnt > 0:
                print(f"    '{word}' ({cnt}건 유지)")

        total_corrections = len(all_corrections)
        print(f"\n  총 적용: {total_corrections}건")

        if total_corrections == 0:
            print(f"  수정 불필요")
            continue

        if not apply_com_replacements(fpath, all_corrections):
            print(f"  COM 수정 실패")
            continue

        time.sleep(3)

if __name__ == "__main__":
    main()
