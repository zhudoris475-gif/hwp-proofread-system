import sys
print(sys.version)
try:
    import win32com.client
    print("win32com OK")
except ImportError as e:
    print(f"win32com MISSING: {e}")

try:
    import pythoncom
    print("pythoncom OK")
except ImportError as e:
    print(f"pythoncom MISSING: {e}")

try:
    import olefile
    print("olefile OK")
except ImportError as e:
    print(f"olefile MISSING: {e}")
