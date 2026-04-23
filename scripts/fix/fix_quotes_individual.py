import win32com.client
import pythoncom
import os, time, subprocess
import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary, log

HWP_PATH = r"C:\Users\doris\Desktop\K 1694-1786--93--20240920.hwp"

def kill_hwp_processes():
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(2)

def main():
    kill_hwp_processes()

    text = extract_text_from_hwp_binary(HWP_PATH)
    left_double = text.count("\u201c")
    right_double = text.count("\u201d")
    left_single = text.count("\u2018")
    right_single = text.count("\u2019")

    log(f"교정전 상태:")
    log(f"  큰따옴표: 왼쪽={left_double}, 오른쪽={right_double}")
    log(f"  작은따옴표: 왼쪽={left_single}, 오른쪽={right_single}")

    if left_double == 0 and right_double == 0:
        log("  이미 따옴표 교정 완료됨")
        return

    pythoncom.CoInitialize()
    CLSCTX_LOCAL_SERVER = 4
    try:
        hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=CLSCTX_LOCAL_SERVER)
        for module_name in ("FilePathCheckerModule", "SecurityModule"):
            try:
                hwp.RegisterModule("FilePathCheckDLL", module_name)
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

        log("HWP COM 연결 성공")
        hwp.Open(HWP_PATH, "HWP", "forceopen:true")
        log("파일 열기 성공")

        replacements = [
            ("\u201c", "\u2018"),
            ("\u201d", "\u2019"),
        ]

        for src, dst in replacements:
            log(f"\n  교체: '{src}' (U+{ord(src):04X}) -> '{dst}' (U+{ord(dst):04X})")
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 1
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 0
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                log(f"  결과: {result}")
            except Exception as e:
                log(f"  오류: {e}")
            time.sleep(1)

        try:
            hwp.Save()
            log("COM 저장 완료")
        except Exception as e:
            log(f"COM 저장 실패: {e}")
            return

        try:
            hwp.Quit()
        except Exception:
            pass

    except Exception as e:
        log(f"COM 오류: {e}")
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

    log(f"\n--- 교정 후 검증 ---")
    text_after = extract_text_from_hwp_binary(HWP_PATH)
    left_double_after = text_after.count("\u201c")
    right_double_after = text_after.count("\u201d")
    left_single_after = text_after.count("\u2018")
    right_single_after = text_after.count("\u2019")

    log(f"  큰따옴표: 왼쪽={left_double_after}, 오른쪽={right_double_after}")
    log(f"  작은따옴표: 왼쪽={left_single_after}, 오른쪽={right_single_after}")

    if left_double_after == 0 and right_double_after == 0:
        log("  따옴표 교정 성공!")
    else:
        log(f"  따옴표 교정 미완료 (큰따옴표 {left_double_after + right_double_after}개 남음)")

if __name__ == "__main__":
    main()
