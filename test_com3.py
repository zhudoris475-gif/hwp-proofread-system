import struct
print(f"Python: {struct.calcsize('P')*8}bit")
import win32com.client, pythoncom
pythoncom.CoInitialize()
try:
    hwp = win32com.client.Dispatch('HWPFrame.HwpObject')
    print(f"COM Dispatch 성공! Version: {hwp.Version}")
except Exception as e:
    print(f"COM 실패: {e}")
