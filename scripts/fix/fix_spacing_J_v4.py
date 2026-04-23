import sys, os, time, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

DST = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"

ALL_FIXES = [
    ("해보다", "해 보다"),
    ("해본", "해 본"),
    ("해봐", "해 봐"),
    ("살펴보다", "살펴 보다"),
    ("생각해보다", "생각해 보다"),
    ("생각해봐", "생각해 봐"),
    ("흥정해본", "흥정해 본"),
    ("시탐해보다", "시탐해 보다"),
    ("조사해보다", "조사해 보다"),
    ("검사해보다", "검사해 보다"),
    ("넘어질번", "넘어질 번"),
    ("한번도", "한 번도"),
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
    text = extract_text_from_hwp_binary(DST)
    print(f"텍스트: {len(text):,}자")

    needed = []
    for src, dst in ALL_FIXES:
        cnt = text.count(src)
        if cnt > 0:
            needed.append((src, dst, cnt))
            print(f"  '{src}' → '{dst}' ({cnt}건)")

    if not needed:
        print("수정 불필요")
        return

    print(f"\n총 {len(needed)}종 수정")

    kill_hwp()
    pythoncom.CoInitialize()
    try:
        hwp = win32com.client.dynamic.Dispatch("HWPFrame.HwpObject")
        try:
            hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
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

        hwp.Open(DST, "HWP", "forceopen:true")
        print(f"파일 열기 성공")

        test_find = hwp.HAction.GetDefault("Find", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = "해보다"
        hwp.HParameterSet.HFindReplace.Direction = 0
        hwp.HParameterSet.HFindReplace.FindType = 0
        test_result = hwp.HAction.Execute("Find", hwp.HParameterSet.HFindReplace.HSet)
        print(f"테스트 Find '해보다': {test_result}")

        total = 0
        for src, dst, cnt in needed:
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 0x0100
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 0
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    total += 1
                    print(f"  [OK] '{src}' → '{dst}'")
                else:
                    print(f"  [SKIP] '{src}' → '{dst}'")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [FAIL] '{src}' ({e})")

        print(f"적용: {total}종")

        try:
            hwp.Save()
            print(f"저장 성공")
        except Exception as e:
            print(f"Save 실패: {e}")
            try:
                hwp.SaveAs(DST, "HWP", "")
                print(f"SaveAs 성공")
            except Exception as e2:
                print(f"SaveAs도 실패: {e2}")

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

if __name__ == "__main__":
    main()
