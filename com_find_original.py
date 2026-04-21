import win32com.client
import pythoncom
import time, shutil, os

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp.bak"
hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

print("=== 원본 파일에서 COM Find 테스트 ===")
shutil.copy2(bak_path, hwp_path)
print(f"원본 복원: {os.path.getsize(hwp_path):,} bytes")

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

print(f"PageCount: {hwp.PageCount}")

print("\n--- 원본 파일에서 Find 테스트 ---")
test_patterns = [
    "저장성",
    "절강성",
    "중국",
    "유럽",
    "O",
]

for pattern in test_patterns:
    try:
        hwp.HAction.GetDefault("Find", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = pattern
        hwp.HParameterSet.HFindReplace.Direction = 0
        hwp.HParameterSet.HFindReplace.FindType = 1
        result = hwp.HAction.Execute("Find", hwp.HParameterSet.HFindReplace.HSet)
        status = "FOUND" if result else "NOT FOUND"
        print(f"  '{pattern}': {status}")
    except Exception as e:
        print(f"  '{pattern}': ERROR - {e}")

print("\n--- FindType=0 (일반) 테스트 ---")
for pattern in ["중국", "유럽", "O"]:
    try:
        hwp.HAction.GetDefault("Find", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = pattern
        hwp.HParameterSet.HFindReplace.Direction = 0
        hwp.HParameterSet.HFindReplace.FindType = 0
        result = hwp.HAction.Execute("Find", hwp.HParameterSet.HFindReplace.HSet)
        status = "FOUND" if result else "NOT FOUND"
        print(f"  FindType=0 '{pattern}': {status}")
    except Exception as e:
        print(f"  FindType=0 '{pattern}': ERROR - {e}")

print("\n--- AllReplace 테스트 (간단한 패턴) ---")
try:
    hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
    hwp.HParameterSet.HFindReplace.FindString = "중국"
    hwp.HParameterSet.HFindReplace.ReplaceString = "중국"
    hwp.HParameterSet.HFindReplace.Direction = 0
    hwp.HParameterSet.HFindReplace.ReplaceMode = 1
    hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
    hwp.HParameterSet.HFindReplace.FindType = 1
    result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
    print(f"  AllReplace '중국'->'중국': result={result}")
except Exception as e:
    print(f"  AllReplace error: {e}")

try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()
