import win32com.client
import pythoncom
import time

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

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

print("\n--- 교정된 패턴 Find 검증 ---")
find_patterns = [
    "절강성(浙江)",
    "안휘성(安徽)",
    "복건성(福建)",
    "소주(苏州)",
]

for pattern in find_patterns:
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

print("\n--- 원본 패턴 Find 검증 (없어야 함) ---")
orig_patterns = [
    "저장성(절강성·浙江省)",
    "안후이성(안휘성·安徽省)",
    "푸젠성(복건성·福建省)",
    "쑤저우(소주·苏州)",
]

for pattern in orig_patterns:
    try:
        hwp.HAction.GetDefault("Find", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = pattern
        hwp.HParameterSet.HFindReplace.Direction = 0
        hwp.HParameterSet.HFindReplace.FindType = 1
        result = hwp.HAction.Execute("Find", hwp.HParameterSet.HFindReplace.HSet)
        status = "FOUND (BAD!)" if result else "NOT FOUND (OK)"
        print(f"  '{pattern}': {status}")
    except Exception as e:
        print(f"  '{pattern}': ERROR - {e}")

print("\n--- 일반 키워드 Find 검증 ---")
general_patterns = ["중국", "유럽", "옛친구", "옛 친구", "뜻으로", "뜻으로,"]

for pattern in general_patterns:
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
