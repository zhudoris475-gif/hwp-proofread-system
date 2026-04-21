import win32com.client
import pythoncom
import os, time

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
time.sleep(1)

search_patterns = [
    ("저장성(절강성·浙江省)", "교정전"),
    ("절강성(浙江)", "교정후"),
    ("안후이성(안휘성·安徽省)", "교정전"),
    ("안휘성(安徽)", "교정후"),
    ("푸젠성(복건성·福建省)", "교정전"),
    ("복건성(福建)", "교정후"),
    ("쑤저우(소주·苏州)", "교정전"),
    ("소주(苏州)", "교정후"),
    ("저장성", "키워드"),
    ("절강성", "키워드"),
    ("안후이성", "키워드"),
    ("안휘성", "키워드"),
    ("푸젠성", "키워드"),
    ("복건성", "키워드"),
]

print("=" * 60)
print("  COM Find로 교정 여부 확인")
print("=" * 60)

for pattern, label in search_patterns:
    try:
        ctrl = hwp.CreateAction("Find")
        pset = ctrl.CreateSet()
        ctrl.GetDefault(pset)
        pset.SetItem("FindString", pattern)
        pset.SetItem("Direction", 0)
        pset.SetItem("FindType", 1)
        result = ctrl.Execute(pset)
        status = "FOUND" if result else "NOT FOUND"
        print(f"  [{label}] '{pattern}': {status}")
    except Exception as e:
        try:
            hwp.HAction.GetDefault("Find", hwp.HParameterSet.HFindReplace.HSet)
            hwp.HParameterSet.HFindReplace.FindString = pattern
            hwp.HParameterSet.HFindReplace.Direction = 0
            hwp.HParameterSet.HFindReplace.FindType = 1
            result = hwp.HAction.Execute("Find", hwp.HParameterSet.HFindReplace.HSet)
            status = "FOUND" if result else "NOT FOUND"
            print(f"  [{label}] '{pattern}': {status}")
        except Exception as e2:
            print(f"  [{label}] '{pattern}': ERROR - {e2}")

hwp.Quit()
pythoncom.CoUninitialize()
