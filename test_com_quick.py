import win32com.client
import pythoncom
import time

pythoncom.CoInitialize()
try:
    hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
    print("COM Dispatch OK")
    try:
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        print("RegisterModule OK")
    except Exception as e:
        print(f"RegisterModule: {e}")
    try:
        hwp.SetMessageBoxMode(0x00020000)
        print("SetMessageBoxMode OK")
    except Exception as e:
        print(f"SetMessageBoxMode: {e}")
    time.sleep(1)
    hwp.Quit()
    print("Quit OK")
except Exception as e:
    print(f"COM Error: {e}")
finally:
    pythoncom.CoUninitialize()
