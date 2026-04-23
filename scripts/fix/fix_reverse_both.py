import sys, os, time, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

FILES = {
    "K": r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp",
    "J": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp",
}

REVERSE_FIXES = [
    ("줄밖에", "줄 밖에"),
    ("한대", "한 대"),
    ("한대로", "한 대로"),
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
    for label, fpath in FILES.items():
        if not os.path.exists(fpath):
            continue

        text = extract_text_from_hwp_binary(fpath)
        needed = []
        for src, dst in REVERSE_FIXES:
            cnt = text.count(src)
            if cnt > 0:
                needed.append((src, dst, cnt))

        if not needed:
            print(f"[{label}] 역방향 수정 불필요")
            continue

        print(f"[{label}] 역방향 수정: {len(needed)}종")
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
                    time.sleep(0.3)
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

        time.sleep(3)

if __name__ == "__main__":
    main()
