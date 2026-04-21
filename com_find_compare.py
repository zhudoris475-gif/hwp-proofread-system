import win32com.client
import pythoncom
import os, time

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp.bak"
hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

pythoncom.CoInitialize()
CLSCTX_LOCAL_SERVER = 4

def com_find_test(filepath, label):
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

    hwp.Open(filepath, "HWP", "forceopen:true")
    time.sleep(1)

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
        "苏州",
        "중국",
        "사전",
        "유럽",
    ]

    print(f"\n--- {label} ---")
    for pattern in test_patterns:
        try:
            ctrl = hwp.CreateAction("Find")
            pset = ctrl.CreateSet()
            ctrl.GetDefault(pset)
            pset.SetItem("FindString", pattern)
            pset.SetItem("Direction", 0)
            pset.SetItem("FindType", 1)
            result = ctrl.Execute(pset)
            status = "FOUND" if result else "NOT FOUND"
            print(f"  '{pattern}': {status}")
        except Exception as e:
            print(f"  '{pattern}': ERROR - {e}")

    hwp.Quit()

com_find_test(bak_path, "원본 백업 (.bak)")
com_find_test(hwp_path, "교정후 파일 (.hwp)")

pythoncom.CoUninitialize()
