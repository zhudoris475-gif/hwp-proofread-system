import win32com.client
import pythoncom
import os, time

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp.bak"

pythoncom.CoInitialize()
CLSCTX_LOCAL_SERVER = 4

hwp = win32com.client.dynamic.Dispatch("HWPFrame.HwpObject")

for module_name in ("FilePathCheckerModule", "SecurityModule"):
    try:
        hwp.RegisterModule("FilePathCheckDLL", module_name)
    except:
        pass
try:
    hwp.SetMessageBoxMode(0x00020000)
except:
    pass

hwp.Open(bak_path, "HWP", "forceopen:true")
time.sleep(2)

test_patterns = [
    "저장성",
    "절강성",
    "안후이성",
    "푸젠성",
    "쑤저우",
    "중국",
    "유럽",
    "사전",
]

print("=" * 60)
print("  원본 백업 COM Find 검사")
print("=" * 60)

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

hwp.Quit()
pythoncom.CoUninitialize()
