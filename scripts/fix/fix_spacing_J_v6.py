import sys, os, time, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

SRC = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp"
OUT = r"C:\Users\doris\Desktop\J_spacing_fixed.hwp"

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
    text = extract_text_from_hwp_binary(SRC)
    print(f"원본 텍스트: {len(text):,}자")

    needed = []
    for src, dst in ALL_FIXES:
        cnt = text.count(src)
        if cnt > 0:
            needed.append((src, dst, cnt))
            print(f"  '{src}' → '{dst}' ({cnt}건)")

    kill_hwp()
    pythoncom.CoInitialize()
    try:
        hwp = win32com.client.dynamic.Dispatch("HWPFrame.HwpObject")
        try:
            hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        except Exception as e:
            print(f"RegisterModule: {e}")
        try:
            hwp.SetMessageBoxMode(0x00020000)
        except Exception as e:
            print(f"SetMessageBoxMode: {e}")

        hwp.Open(SRC, "HWP", "forceopen:true")
        print(f"파일 열기 성공")

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

        saved = False

        try:
            result = hwp.SaveAs(OUT, "HWP", "")
            print(f"SaveAs 메서드: {result}")
            saved = True
        except Exception as e:
            print(f"SaveAs 메서드 오류: {e}")

        if not saved:
            try:
                hwp.HAction.GetDefault("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
                hwp.HParameterSet.HFileOpenSave.filename = OUT
                hwp.HParameterSet.HFileOpenSave.Format = "HWP"
                result = hwp.HAction.Execute("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
                print(f"SaveAs Action: {result}")
                saved = True
            except Exception as e:
                print(f"SaveAs Action 오류: {e}")

        if not saved:
            try:
                hwp.HAction.GetDefault("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
                hwp.HParameterSet.HFileOpenSave.filename = OUT
                hwp.HParameterSet.HFileOpenSave.Format = "HWP"
                hwp.HParameterSet.HFileOpenSave.Attributes = 0
                result = hwp.HAction.Execute("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
                print(f"SaveAs Action(v2): {result}")
                saved = True
            except Exception as e:
                print(f"SaveAs Action(v2) 오류: {e}")

        if not saved:
            try:
                hwp.Run("FileSaveAs")
                time.sleep(2)
                print("Run FileSaveAs 시도")
            except Exception as e:
                print(f"Run FileSaveAs 오류: {e}")

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

    if os.path.exists(OUT):
        size = os.path.getsize(OUT)
        text2 = extract_text_from_hwp_binary(OUT)
        print(f"\n✅ 파일 저장 성공! 크기={size:,}바이트, 텍스트={len(text2):,}자")

        remaining = 0
        for src, dst, cnt in needed:
            new_cnt = text2.count(src)
            correct_cnt = text2.count(dst)
            if new_cnt > 0:
                print(f"  ⚠️ '{src}' 아직 {new_cnt}건 남음 (올바름={correct_cnt})")
                remaining += new_cnt
            else:
                print(f"  ✅ '{src}' → '{dst}' (올바름={correct_cnt})")

        if remaining == 0:
            print(f"\n✅ 모든 띄어쓰기 수정 완료!")
        else:
            print(f"\n⚠️ {remaining}건 남음")
    else:
        print(f"\n❌ 파일 저장 실패")

if __name__ == "__main__":
    main()
