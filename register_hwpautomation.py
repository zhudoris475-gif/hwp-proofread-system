"""
Register HwpAutomation COM Object
Register HwpAutomation.dll to enable COM automation
"""
import subprocess
import os
import sys

# Set UTF-8 encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def register_hwpautomation():
    """Register HwpAutomation COM object."""

    # Find HwpAutomation.dll
    dll_path = r"C:\Program Files (x86)\Hnc\Office 2022\HOffice120\Bin\HwpAutomation.dll"

    if not os.path.exists(dll_path):
        print(f"HwpAutomation.dll not found at: {dll_path}")
        return False

    print(f"Found HwpAutomation.dll: {dll_path}")

    try:
        print("\nAttempting to register COM object...")

        # Register using regsvr32
        regsvr32_path = r"C:\Windows\System32\regsvr32.exe"

        # Method 1: Register DLL
        result1 = subprocess.run(
            [regsvr32_path, dll_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        print(f"\nRegistration result (Method 1):")
        print(f"Return code: {result1.returncode}")
        if result1.stdout:
            print(f"stdout: {result1.stdout}")
        if result1.stderr:
            print(f"stderr: {result1.stderr}")

        # Method 2: Register with /i (install)
        result2 = subprocess.run(
            [regsvr32_path, "/i", dll_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        print(f"\nRegistration result (Method 2):")
        print(f"Return code: {result2.returncode}")
        if result2.stdout:
            print(f"stdout: {result2.stdout}")
        if result2.stderr:
            print(f"stderr: {result2.stderr}")

        if result1.returncode == 0 or result2.returncode == 0:
            print("\n" + "="*60)
            print("SUCCESS! COM object registered successfully!")
            print("="*60)
            print("\nNow you can use HwpAutomation in Python!")
            print("Example:")
            print("  import win32com.client as win32")
            print("  hwp = win32.Dispatch('HwpAutomation.HwpAutomation')")
            print("  hwp.Open('file.hwp')")
            return True
        else:
            print("\n" + "="*60)
            print("FAILED! COM object registration failed!")
            print("="*60)
            return False

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("HWP COM Object Registration (HwpAutomation)")
    print("="*60)

    success = register_hwpautomation()

    if success:
        print("\nNow try running the test script again!")
    else:
        print("\nRegistration failed. Please try manually:")
        print(f"  regsvr32 \"{dll_path}\"")
