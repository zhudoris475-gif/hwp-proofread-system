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
time.sleep(2)

try:
    hwp.HAction.GetDefault("TextSelectAll", hwp.HParameterSet.HSelAll.HSet)
    hwp.HAction.Execute("TextSelectAll", hwp.HParameterSet.HSelAll.HSet)
    text_len = hwp.GetSelectedTextLength()
    print(f"COM GetSelectedTextLength: {text_len}")
    hwp.Run("Cancel")
except Exception as e:
    print(f"TextSelectAll error: {e}")

try:
    text = hwp.GetSelectedText(0, 500)
    print(f"GetSelectedText (first 500): {repr(text[:200])}")
except Exception as e:
    print(f"GetSelectedText error: {e}")

try:
    hwp.MovePos(0, 0, 0)
    text = hwp.GetWordText(0, 0, 100)
    print(f"GetWordText: {repr(text[:200])}")
except Exception as e:
    print(f"GetWordText error: {e}")

try:
    field_list = hwp.GetFieldList()
    print(f"GetFieldList: {repr(field_list[:200])}")
except Exception as e:
    print(f"GetFieldList error: {e}")

try:
    page_count = hwp.PageCount
    print(f"PageCount: {page_count}")
except Exception as e:
    print(f"PageCount error: {e}")

try:
    hwp.Save()
    print("Save OK")
except Exception as e:
    print(f"Save error: {e}")

hwp.Quit()
pythoncom.CoUninitialize()
