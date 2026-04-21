# -*- coding: utf-8 -*-
import sys, io, time
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import win32com.client

temp_hwp = r"C:\Users\doris\AppData\Local\Temp\hwp_proofread\work_56384.hwp"

print("Creating COM object...")
hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
print("COM created")

print(f"Opening: {temp_hwp}")
r = hwp.Open(temp_hwp, "", "")
print(f"Open result: {r}")

if r:
    print("File opened successfully!")
    hwp.Clear(1)
else:
    print("File open FAILED")
    print("Trying with HWP format parameter...")
    r2 = hwp.Open(temp_hwp, "HWP", "")
    print(f"Open with HWP param: {r2}")
    if not r2:
        r3 = hwp.Open(temp_hwp, "HWP", "forceopen:true")
        print(f"Open with forceopen: {r3}")
    hwp.Clear(1)
