import sys, os, time, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

FILES = {
    "J": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp",
}

SPACING_FIXES = [
    ("고있다", "고 있다"),
    ("고있는", "고 있는"),
    ("고있었", "고 있었"),
    ("고있겠", "고 있겠"),
    ("고있지", "고 있지"),
    ("고있고", "고 있고"),
    ("고있어", "고 있어"),
    ("고있음", "고 있음"),
    ("해보다", "해 보다"),
    ("해본", "해 본"),
    ("해봐", "해 봐"),
    ("해봐도", "해 봐도"),
    ("해봐라", "해 봐라"),
    ("해봐요", "해 봐요"),
    ("해봤", "해 봤"),
    ("먹어보다", "먹어 보다"),
    ("읽어보다", "읽어 보다"),
    ("살펴보다", "살펴 보다"),
    ("생각해보다", "생각해 보다"),
    ("생각해봐", "생각해 봐"),
    ("생각해봐도", "생각해 봐도"),
    ("생각해봐라", "생각해 봐라"),
    ("흥정해본", "흥정해 본"),
    ("시탐해보다", "시탐해 보다"),
    ("조사해보다", "조사해 보다"),
    ("검사해보다", "검사해 보다"),
    ("역할따위", "역할 따위"),
    ("갈등따위", "갈등 따위"),
    ("넘어질번", "넘어질 번"),
    ("한번도", "한 번도"),
    ("한번은", "한 번은"),
    ("두번다시", "두 번 다시"),
    ("한꺼번에", "한꺼번에"),
]

def kill_hwp():
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(5)

def main():
    for label, fpath in FILES.items():
        if not os.path.exists(fpath):
            print(f"[{label}] 파일 없음: {fpath}")
            continue

        text = extract_text_from_hwp_binary(fpath)
        needed = []
        for src, dst in SPACING_FIXES:
            cnt = text.count(src)
            if cnt > 0:
                needed.append((src, dst, cnt))

        if not needed:
            print(f"[{label}] 띄어쓰기 수정 불필요")
            continue

        print(f"[{label}] 띄어쓰기 수정: {len(needed)}종")
        for src, dst, cnt in needed:
            print(f"  '{src}' → '{dst}' ({cnt}건)")

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
            for src, dst, cnt in needed:
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
                        total += cnt
                        print(f"  [OK] '{src}' → '{dst}' ({cnt}건)")
                    else:
                        print(f"  [SKIP] '{src}' → '{dst}'")
                    time.sleep(0.2)
                except Exception as e:
                    print(f"  [FAIL] '{src}' ({e})")

            try:
                hwp.Save()
                print(f"  저장 완료 ({total}건)")
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

if __name__ == "__main__":
    main()
