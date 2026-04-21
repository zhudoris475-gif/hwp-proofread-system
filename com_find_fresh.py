import win32com.client
import pythoncom
import os, time

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp.bak"

pythoncom.CoInitialize()
CLSCTX_LOCAL_SERVER = 4
hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=CLSCTX_LOCAL_SERVER)

for module_name in ("FilePathCheckerModule", "SecurityModule"):
    try:
        hwp.RegisterModule("FilePathCheckDLL", module_name)
        print(f"보안 모듈 등록: {module_name}")
    except:
        pass
try:
    hwp.SetMessageBoxMode(0x00020000)
except:
    pass

print("파일 열기 시도...")
hwp.Open(bak_path, "HWP", "forceopen:true")
time.sleep(3)
print("파일 열기 완료")

test_patterns = [
    "저장성",
    "중국",
    "유럽",
    "사전",
    "O",
]

print("\nCOM Find 검사 (원본 백업, DispatchEx):")
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

try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()
