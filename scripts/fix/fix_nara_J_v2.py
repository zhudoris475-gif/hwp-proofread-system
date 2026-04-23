import sys, os, time, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

J_MAIN = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp"

NARA_RULES = [
    ("명(明)나라", "명(明)조"),
    ("한(漢)나라", "한(漢)조"),
    ("당(唐)나라", "당(唐)조"),
    ("송(宋)나라", "송(宋)조"),
    ("원(元)나라", "원(元)조"),
    ("진(秦)나라", "진(秦)조"),
    ("수(隋)나라", "수(隋)조"),
    ("진(晉)나라", "진(晉)조"),
    ("위(魏)나라", "위(魏)조"),
    ("오(吳)나라", "오(吳)조"),
    ("청(清)나라", "청(清)조"),
    ("요(遼)나라", "요(遼)조"),
    ("금(金)나라", "금(金)조"),
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

def main():
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

        hwp.Open(J_MAIN, "HWP", "forceopen:true")
        print("파일 열기 성공")

        print("\n--- 방법1: FindType=0 + ReplaceMode=0x0101 ---")
        for src, dst in NARA_RULES:
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 0x0101
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 0
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                print(f"  [{result}] '{src}' → '{dst}'")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [ERR] '{src}' ({e})")

        try:
            hwp.Save()
            print("저장 완료")
        except Exception as e:
            print(f"저장 실패: {e}")

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

    text = extract_text_from_hwp_binary(J_MAIN)
    remaining = 0
    for src, dst in NARA_RULES:
        cnt = text.count(src)
        if cnt > 0:
            print(f"  남음: '{src}' {cnt}건")
            remaining += cnt
    if remaining == 0:
        print("  ✅ 모두 완료!")
    else:
        print(f"  ⚠️ {remaining}건 남음 - 방법2 시도")

        kill_hwp()
        time.sleep(3)
        pythoncom.CoInitialize()

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

            hwp.Open(J_MAIN, "HWP", "forceopen:true")
            print("\n--- 방법2: FindType=0 + Direction=1(역방향) ---")
            for src, dst in NARA_RULES:
                try:
                    hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                    hwp.HParameterSet.HFindReplace.FindString = src
                    hwp.HParameterSet.HFindReplace.ReplaceString = dst
                    hwp.HParameterSet.HFindReplace.Direction = 1
                    hwp.HParameterSet.HFindReplace.ReplaceMode = 1
                    hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                    hwp.HParameterSet.HFindReplace.FindType = 0
                    result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                    print(f"  [{result}] '{src}' → '{dst}'")
                    time.sleep(0.3)
                except Exception as e:
                    print(f"  [ERR] '{src}' ({e})")

            try:
                hwp.Save()
                print("저장 완료")
            except Exception as e:
                print(f"저장 실패: {e}")

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
        text = extract_text_from_hwp_binary(J_MAIN)
        remaining = 0
        for src, dst in NARA_RULES:
            cnt = text.count(src)
            if cnt > 0:
                print(f"  남음: '{src}' {cnt}건")
                remaining += cnt
        if remaining == 0:
            print("  ✅ 모두 완료!")
        else:
            print(f"  ⚠️ 여전히 {remaining}건 남음")

if __name__ == "__main__":
    main()
