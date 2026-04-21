import sys
import os
import time
import shutil
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

TARGET_FILE = r"C:\사전\【20】O 2179-2182排版页수4-金花顺-.backup"

def test_com():
    import win32com.client

    temp_dir = os.path.join(tempfile.gettempdir(), "hwp_proofread")
    os.makedirs(temp_dir, exist_ok=True)
    temp_hwp = os.path.join(temp_dir, "proofread_temp.hwp")
    shutil.copy2(TARGET_FILE, temp_hwp)
    print(f"Copied to: {temp_hwp}")

    hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
    print("COM: Created")

    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    print("COM: RegisterModule done")

    result = hwp.Open(temp_hwp, "", "")
    print(f"COM: Open result = {result}")

    print("\n--- Test 1: hwp.Find with 1 arg ---")
    try:
        r = hwp.Find("5")
        print(f"  Find('5') = {r}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n--- Test 2: hwp.Find with multiple args ---")
    try:
        r = hwp.Find("5", 0, 0, 0)
        print(f"  Find('5', 0, 0, 0) = {r}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n--- Test 3: hwp.Replace ---")
    try:
        hwp.MovePos(3, 0, 0)
        r = hwp.Replace("5", "FIVE", 0, 0, 0, 0, 1)
        print(f"  Replace('5','FIVE',...) = {r}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n--- Test 4: HAction.GetDefault + Execute ---")
    try:
        act = hwp.HAction
        pset = hwp.HParameterSet.HFindReplace
        r = act.GetDefault("AllReplace", pset.HSet)
        print(f"  GetDefault result = {r}")
        pset.FindStr = "5"
        pset.ReplaceStr = "FIVE"
        pset.Direction = 0
        pset.WholeWordOnly = 0
        pset.IgnoreCase = 0
        pset.UseWildCard = 0
        pset.ReplaceMode = 1
        pset.ReplaceAll = 1
        r = act.Execute("AllReplace", pset.HSet)
        print(f"  Execute result = {r}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n--- Test 5: HAction with Dispatch (late binding) ---")
    try:
        pset = hwp.HParameterSet.HFindReplace
        print(f"  pset type = {type(pset)}")
        print(f"  pset dir = {dir(pset)}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n--- Test 6: InitScan / GetScanResult ---")
    try:
        r = hwp.InitScan(0, 0, 0, 0, 0, "5")
        print(f"  InitScan result = {r}")
        if r:
            text = hwp.GetScanResult()
            print(f"  GetScanResult = '{text}'")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n--- Test 7: Execute script ---")
    try:
        r = hwp.Execute('ReplaceAll "5" "FIVE"')
        print(f"  Execute script result = {r}")
    except Exception as e:
        print(f"  Error: {e}")

    hwp.Clear(1)
    print("\nDone")

if __name__ == "__main__":
    test_com()
