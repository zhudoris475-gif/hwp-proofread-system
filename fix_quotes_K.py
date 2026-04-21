import sys, os, time, re, subprocess
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import win32com.client
import pythoncom
from hwp_ollama_proofread import extract_text_from_hwp_binary

K_MAIN = r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp"
QUOTE_THRESHOLD = 10

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
    text = extract_text_from_hwp_binary(K_MAIN)
    pattern = re.compile(r'\u201c([^\u201c\u201d]+)\u201d')
    short_quotes = []
    for m in pattern.finditer(text):
        content = m.group(1)
        full = m.group(0)
        if len(content) < QUOTE_THRESHOLD:
            short_quotes.append((full, "\u2018" + content + "\u2019", content))

    print(f"K파일 단어 따옴표: {len(short_quotes)}건")
    if not short_quotes:
        print("수정 불필요")
        return

    for full, repl, content in short_quotes[:10]:
        print(f"  '{full}' → '{repl}'")

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

        hwp.Open(K_MAIN, "HWP", "forceopen:true")
        print("파일 열기 성공")

        total = 0
        for full, repl, content in short_quotes:
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = full
                hwp.HParameterSet.HFindReplace.ReplaceString = repl
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 0x0101
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 0
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    total += 1
                    print(f"  [OK] '{full}' → '{repl}'")
                else:
                    print(f"  [SKIP] '{full}'")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [FAIL] '{full}' ({e})")

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
    text_after = extract_text_from_hwp_binary(K_MAIN)
    pattern2 = re.compile(r'\u201c([^\u201c\u201d]+)\u201d')
    remaining = pattern2.findall(text_after)
    short_r = [m for m in remaining if len(m) < QUOTE_THRESHOLD]
    print(f"  남은 단어 따옴표: {len(short_r)}개")
    if len(short_r) == 0:
        print("  ✅ 모두 완료!")
    else:
        for m in short_r[:5]:
            print(f"    \"{m}\"")

if __name__ == "__main__":
    main()
