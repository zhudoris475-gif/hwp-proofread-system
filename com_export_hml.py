import win32com.client
import pythoncom
import os, time

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
export_hml = r"c:\Users\doris\.agent-skills\hwp_exported.hml"

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
time.sleep(2)

try:
    hwp.SaveAs(export_hml, "HML", "")
    print(f"HML 내보내기 성공: {export_hml}")
    if os.path.exists(export_hml):
        sz = os.path.getsize(export_hml)
        print(f"HML 파일 크기: {sz:,} bytes")
except Exception as e:
    print(f"HML 내보내기 실패: {e}")

try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()
