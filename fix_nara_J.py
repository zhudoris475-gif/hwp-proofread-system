import sys, os, time, re, subprocess, shutil
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary, log

J_STEP4 = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_step4.hwp"
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
    shutil.copy2(J_STEP4, J_MAIN)
    print(f"step4 → 메인 파일 복사 완료")

    text = extract_text_from_hwp_binary(J_MAIN)
    needed = []
    for src, dst in NARA_RULES:
        cnt = text.count(src)
        if cnt > 0:
            needed.append((src, dst, cnt))

    if not needed:
        print("나라→조 미적용 없음")
        return

    print(f"나라→조 미적용: {len(needed)}종, 총 {sum(c for _,_,c in needed)}건")
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

        hwp.Open(J_MAIN, "HWP", "forceopen:true")
        print("파일 열기 성공")

        total = 0
        for src, dst, cnt in needed:
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 1
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 0
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    total += cnt
                    print(f"  [OK] '{src}' → '{dst}' ({cnt}건)")
                else:
                    print(f"  [SKIP] '{src}' → '{dst}'")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [FAIL] '{src}' ({e})")

        try:
            hwp.Save()
            print(f"저장 완료 ({total}건)")
        except Exception as e:
            print(f"저장 실패: {e}")
            return

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
        return
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

    time.sleep(3)

    print(f"\n--- 검증 ---")
    text_after = extract_text_from_hwp_binary(J_MAIN)
    remaining = 0
    for src, dst in NARA_RULES:
        cnt = text_after.count(src)
        if cnt > 0:
            print(f"  아직 남음: '{src}' {cnt}건")
            remaining += cnt
    if remaining == 0:
        print("  ✅ 나라→조 모두 완료!")
    else:
        print(f"  ⚠️ {remaining}건 남음")

if __name__ == "__main__":
    main()
