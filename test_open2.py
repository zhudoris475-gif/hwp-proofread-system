# -*- coding: utf-8 -*-
import sys, io, time
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import win32com.client

original = r"C:\사전\【21】P 2183-2268排版页数86-金花顺.hwp"
temp_hwp = r"C:\Users\doris\AppData\Local\Temp\hwp_proofread\work_56384.hwp"

print("Creating COM object...")
hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
print("COM created")

print(f"Opening original: {original}")
r = hwp.Open(original, "", "")
print(f"Open original result: {r}")

if r:
    print("Original opened successfully!")
    hwp.Clear(1)
else:
    print("Original open FAILED")
    hwp.Clear(1)

time.sleep(2)

print(f"\nOpening temp: {temp_hwp}")
r2 = hwp.Open(temp_hwp, "", "")
print(f"Open temp result: {r2}")

if r2:
    print("Temp opened successfully!")
    hwp.Clear(1)
else:
    print("Temp open FAILED")
    hwp.Clear(1)

hwp.Quit()
