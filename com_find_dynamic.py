import win32com.client
import pythoncom
import os, time

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

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

hwp.Open(hwp_path, "HWP", "forceopen:true")
time.sleep(2)

test_patterns = [
    "저장성",
    "절강성",
    "浙江省",
    "안후이성",
    "안휘성",
    "푸젠성",
    "복건성",
    "쑤저우",
    "소주",
    "중국",
    "유럽",
    "뜻으로",
    "한 것",
]

print("=" * 60)
print("  COM Find 검사 (dynamic Dispatch)")
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
