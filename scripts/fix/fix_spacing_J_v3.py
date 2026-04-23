import sys, os, time, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

SRC = r"C:\Users\doris\Desktop\hwp_backup\【大中朝 14】J 1419-1693--275--20240920.hwp"
DST = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"

ALL_FIXES = [
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
    ("먹어보다", "먹어 보다"),
    ("읽어보다", "읽어 보다"),
    ("살펴보다", "살펴 보다"),
    ("생각해보다", "생각해 보다"),
    ("생각해봐", "생각해 봐"),
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
    text = extract_text_from_hwp_binary(SRC)
    print(f"백업 텍스트: {len(text):,}자")

    needed = []
    for src, dst in ALL_FIXES:
        cnt = text.count(src)
        if cnt > 0:
            needed.append((src, dst, cnt))

    print(f"수정 필요: {len(needed)}종")
    for src, dst, cnt in needed:
        print(f"  '{src}' → '{dst}' ({cnt}건)")

    if not needed:
        print("수정 불필요")
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

        hwp.Open(SRC, "HWP", "forceopen:true")
        print(f"파일 열기 성공: {SRC}")

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
                    total += 1
                    print(f"  [OK] '{src}' → '{dst}'")
                else:
                    print(f"  [SKIP] '{src}' → '{dst}'")
                time.sleep(0.2)
            except Exception as e:
                print(f"  [FAIL] '{src}' ({e})")

        print(f"적용: {total}종")

        try:
            hwp.HAction.GetDefault("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
            hwp.HParameterSet.HFileOpenSave.filename = DST
            hwp.HParameterSet.HFileOpenSave.Format = "HWP"
            result = hwp.HAction.Execute("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
            if result:
                print(f"SaveAs 성공: {DST}")
            else:
                print(f"SaveAs 실패(Action)")
        except Exception as e:
            print(f"SaveAs 오류: {e}")

        try:
            hwp.Quit()
        except Exception:
            pass

    except Exception as e:
        print(f"COM 오류: {e}")
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

    if os.path.exists(DST):
        text2 = extract_text_from_hwp_binary(DST)
        print(f"\n저장된 파일 텍스트: {len(text2):,}자")

        remaining = 0
        for src, dst, cnt in needed:
            new_cnt = text2.count(src)
            if new_cnt > 0:
                print(f"  ⚠️ '{src}' 아직 {new_cnt}건 남음")
                remaining += new_cnt
            else:
                correct_cnt = text2.count(dst)
                print(f"  ✅ '{src}' → '{dst}' (올바름={correct_cnt})")

        if remaining == 0:
            print(f"\n✅ 모든 띄어쓰기 수정 완료!")
        else:
            print(f"\n⚠️ {remaining}건 남음")
    else:
        print(f"\n❌ 파일 저장 실패")

if __name__ == "__main__":
    main()
