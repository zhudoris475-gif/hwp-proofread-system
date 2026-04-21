# -*- coding: utf-8 -*-
import sys, io, os, shutil
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import win32com.client

original = r"C:\사전\【21】P 2183-2268排版页数86-金花顺.hwp"
work_dir = r"C:\HWP_Work"
os.makedirs(work_dir, exist_ok=True)
work_file = os.path.join(work_dir, "work.hwp")

if os.path.exists(work_file):
    os.remove(work_file)
shutil.copy2(original, work_file)
print(f"Copied to: {work_file}")
print(f"File size: {os.path.getsize(work_file)}")

with open(work_file, 'rb') as f:
    header = f.read(8)
    print(f"Header bytes: {header.hex()}")
    print(f"Is OLE: {header[:4] == b'\\xd0\\xcf\\x11\\xe0'}")

print("\nCreating COM object...")
hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
print("COM created")

print(f"Opening: {work_file}")
r = hwp.Open(work_file, "", "")
print(f"Open result: {r}")

if r:
    print("SUCCESS! File opened!")
    hwp.Clear(1)
else:
    print("FAILED to open")
    hwp.Clear(1)

hwp.Quit()
