import win32com.client
import pythoncom
import os, time, subprocess

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

subprocess.run(["powershell", "-Command", "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"], capture_output=True)
time.sleep(3)

pythoncom.CoInitialize()
CLSCTX_LOCAL_SERVER = 4
hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=CLSCTX_LOCAL_SERVER)

for module_name in ("FilePathCheckerModule", "SecurityModule"):
    try:
        hwp.RegisterModule("FilePathCheckDLL", module_name)
    except:
        pass
try:
    hwp.SetMessageBoxMode(0x00020000)
except:
    pass

hwp.Open(hwp_path, "HWP", "forceopen:true")
time.sleep(3)
print(f"HWP 열기 성공 (PageCount={hwp.PageCount})")

print("\n--- 방법1: FindType=0 (모든 텍스트) ---")
for src, dst in [("\u201c", "\u2018"), ("\u201d", "\u2019")]:
    try:
        hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = src
        hwp.HParameterSet.HFindReplace.ReplaceString = dst
        hwp.HParameterSet.HFindReplace.Direction = 0
        hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        hwp.HParameterSet.HFindReplace.FindType = 0
        result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        print(f"  FindType=0: '{src}' -> '{dst}': result={result}")
    except Exception as e:
        print(f"  FindType=0: '{src}' -> '{dst}': ERROR - {e}")
    time.sleep(0.5)

print("\n--- 방법2: FindType=256 (특수문자) ---")
for src, dst in [("\u201c", "\u2018"), ("\u201d", "\u2019")]:
    try:
        hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = src
        hwp.HParameterSet.HFindReplace.ReplaceString = dst
        hwp.HParameterSet.HFindReplace.Direction = 0
        hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        hwp.HParameterSet.HFindReplace.FindType = 256
        result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        print(f"  FindType=256: '{src}' -> '{dst}': result={result}")
    except Exception as e:
        print(f"  FindType=256: '{src}' -> '{dst}': ERROR - {e}")
    time.sleep(0.5)

print("\n--- 방법3: HAction 실행 스크립트 ---")
try:
    hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
    print(f"  InsertText 사용 가능")
except Exception as e:
    print(f"  InsertText: {e}")

print("\n--- 방법4: InitScan/GetText로 따옴표 위치 찾기 ---")
try:
    scan_result = hwp.InitScan(0, 0x07, 0, 1, "All", "")
    print(f"  InitScan: {scan_result}")
    if scan_result:
        count = 0
        found_quotes = False
        while count < 500:
            result = hwp.GetText()
            if result == "" or result is None:
                break
            if isinstance(result, tuple):
                text_part = str(result[0]) if len(result) > 0 else ""
            else:
                text_part = str(result)
            if text_part and ("\u201c" in text_part or "\u201d" in text_part):
                found_quotes = True
                print(f"  따옴표 발견: {repr(text_part[:100])}")
            count += 1
        if not found_quotes:
            print(f"  {count}개 세그먼트 스캔했으나 따옴표 없음")
        hwp.ReleaseScan()
except Exception as e:
    print(f"  InitScan 에러: {e}")

time.sleep(1)
try:
    hwp.Save()
    print("\nSave 성공!")
except Exception as e:
    print(f"\nSave 실패: {e}")

try:
    hwp.Clear(1)
except:
    pass
try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()

import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

text = extract_text_from_hwp_binary(hwp_path)
left_double = text.count("\u201c")
right_double = text.count("\u201d")
print(f"\n결과: 큰따옴표 왼쪽={left_double}, 오른쪽={right_double}")
