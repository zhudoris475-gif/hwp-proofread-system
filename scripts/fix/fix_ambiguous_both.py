import sys, os, time, re, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

FILES = {
    "K": r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp",
    "J": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp",
}

R = 60

def kill_hwp():
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(5)

def judge_split(word, ctx):
    if word == "간적":
        if any(w in ctx for w in ["간 적이", "적이 있", "적이없", "적이 없"]):
            return True
        return False

    if word == "간지":
        if any(w in ctx for w in ["간지기일", "간지(干支)", "륙십간지", "육십간지", "간지법", "간지로"]):
            return False
        return False

    if word == "산지":
        if any(w in ctx for w in ["원산지", "집산지", "생산지", "산지가", "산지의", "산지로", "산지에서"]):
            return False
        return False

    if word == "할지":
        if any(w in ctx for w in ["할지라도", "할지언정", "할지도"]):
            return False
        if any(w in ctx for w in ["할 지", "지 모른", "지 결정", "지 알", "지를 결"]):
            return True
        return False

    if word == "한지":
        if any(w in ctx for w in ["한지에", "한지로", "종이", "도화지", "전지", "한지를"]):
            return False
        if any(w in ctx for w in ["한 지가", "한 지를", "출근한지", "된지", "지 거의", "지이다"]):
            return True
        return False

    if word == "강하":
        return False

    if word == "산하":
        return False

    if word == "그만큼":
        return False

    if word == "뜻대로":
        return False

    if word == "알데":
        if any(w in ctx for w in ["데히드", "히드"]):
            return False
        return False

    if word == "포름알데":
        return False

    if word == "놀포름알데":
        return False

    if word == "메타알데":
        return False

    if word == "아쎄트알데":
        return False

    return False

def find_all_contexts(text, word, dst):
    replacements = []
    idx = 0
    while True:
        pos = text.find(word, idx)
        if pos == -1:
            break
        start = max(0, pos - R)
        end = min(len(text), pos + len(word) + R)
        ctx = text[start:end].replace('\r', ' ').replace('\n', ' ')

        should_split = judge_split(word, ctx)
        if should_split:
            replacements.append((word, dst, ctx))

        idx = pos + len(word)
    return replacements

def main():
    for label, fpath in FILES.items():
        if not os.path.exists(fpath):
            continue

        text = extract_text_from_hwp_binary(fpath)
        print(f"\n{'=' * 70}")
        print(f"  [{label}] {os.path.basename(fpath)}")
        print(f"{'=' * 70}")

        ambiguous_words = [
            ("간적", "간 적"),
            ("간지", "간 지"),
            ("산지", "산 지"),
            ("할지", "할 지"),
            ("한지", "한 지"),
        ]

        all_corrections = []
        for word, dst in ambiguous_words:
            reps = find_all_contexts(text, word, dst)
            if reps:
                print(f"  [{word}] → [{dst}] {len(reps)}건 분리")
                for _, _, ctx in reps[:3]:
                    print(f"    ...{ctx[:60]}...")
                all_corrections.extend(reps)

        nosplit_words = ["강하", "산하", "그만큼", "뜻대로", "알데", "포름알데", "놀포름알데", "메타알데", "아쎄트알데"]
        print(f"\n  유지 항목 (분리불가):")
        for w in nosplit_words:
            cnt = text.count(w)
            if cnt > 0:
                print(f"    '{w}' ({cnt}건 유지)")

        if not all_corrections:
            print(f"\n  수정 불필요")
            continue

        print(f"\n  총 분리 적용: {len(all_corrections)}건")

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
            for src, dst, ctx in all_corrections:
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
                    time.sleep(0.15)
                except Exception as e:
                    print(f"    [FAIL] '{src}' ({e})")

            print(f"  적용: {total}/{len(all_corrections)}건")

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

        time.sleep(3)

if __name__ == "__main__":
    main()
