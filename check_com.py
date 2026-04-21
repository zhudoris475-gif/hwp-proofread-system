import sys
print(f"Python {sys.version}")
print(f"Architecture: {'64-bit' if sys.maxsize > 2**32 else '32-bit'}")
try:
    import win32com.client
    hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
    print("COM OK: HWPFrame.HwpObject created from 32-bit Python!")
    hwp = None
except ImportError:
    print("pywin32 not installed in 32-bit Python")
    print("Need: pip install pywin32")
except Exception as e:
    print(f"COM error: {e}")
