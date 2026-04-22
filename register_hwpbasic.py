"""
Register HwpBasic COM Object
Register HwpBasic.dll to enable COM automation
"""
import subprocess
import os
import sys

# Set UTF-8 encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def register_hwpbasic():
    """Register HwpBasic COM object."""

    # Find HwpBasic.dll
    possible_paths = [
        r"C:\Program Files (x86)\Hnc\Office 2022\HOffice120\Bin\HwpBasic.dll",
        r"C:\Program Files (x86)\Hnc\Office 2022\HOffice120\Bin\HwpBasic80.dll",
        r"C:\Program Files (x86)\Hnc\Hwp80\HwpBasic.dll",
    ]

    dll_path = None
    for path in possible_paths:
        if os.path.exists(path):
            dll_path = path
            break

    if not dll_path:
        print("HwpBasic.dll not found!")
        print("Searching in all HWP installation directories...")

        # Search for HwpBasic.dll
        search_paths = [
            r"C:\Program Files (x86)\Hnc",
            r"C:\Program Files\Hnc",
            r"C:\Program Files (x86)\Hnc\Office 2022",
            r"C:\Program Files\Hnc\Office 2022",
        ]

        for search_path in search_paths:
            if os.path.exists(search_path):
                print(f"\nSearching in: {search_path}")
                for root, dirs, files in os.walk(search_path):
                    if "HwpBasic.dll" in files:
                        dll_path = os.path.join(root, "HwpBasic.dll")
                        print(f"Found: {dll_path}")
                        break
                if dll_path:
                    break

        if not dll_path:
            print("HwpBasic.dll not found anywhere!")
            return False

    print(f"\nFound HwpBasic.dll: {dll_path}")

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
    print("HWP COM Object Registration")
    print("="*60)

    success = register_hwpbasic()

    if success:
        print("\nNow you can use HwpBasic.HwpObject in Python!")
        print("Example:")
        print("  import win32com.client as win32")
        print("  hwp = win32.Dispatch('HwpBasic.HwpObject')")
        print("  hwp.Open('file.hwp')")
    else:
        print("\nRegistration failed. Please try manually:")
        print(f"  regsvr32 \"{dll_path}\"")
