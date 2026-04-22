"""
Find HwpBasic.dll in HWP installation
Search for HwpBasic.dll in all HWP installation directories
"""
import os
import sys

# Set UTF-8 encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def find_hwpbasic_dll():
    """Find HwpBasic.dll in HWP installation directories."""

    # Common HWP installation paths
    search_paths = [
        r"C:\Program Files (x86)\Hnc",
        r"C:\Program Files\Hnc",
        r"C:\Program Files (x86)\Hnc\Office 2022",
        r"C:\Program Files\Hnc\Office 2022",
        r"C:\Program Files (x86)\Hnc\Hwp80",
        r"C:\Program Files\Hnc\Hwp80",
        r"D:\Program Files\Hnc\Office 2022",
        r"D:\Program Files\Hnc\Hwp80",
    ]

    dll_found = []

    print("="*60)
    print("Searching for HwpBasic.dll...")
    print("="*60)

    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue

        print(f"\nSearching in: {search_path}")

        for root, dirs, files in os.walk(search_path):
            if "HwpBasic.dll" in files:
                dll_path = os.path.join(root, "HwpBasic.dll")
                dll_found.append(dll_path)
                print(f"  Found: {dll_path}")

    if dll_found:
        print("\n" + "="*60)
        print(f"Found {len(dll_found)} HwpBasic.dll file(s)!")
        print("="*60)

        for dll_path in dll_found:
            print(f"\n{dll_path}")
            print(f"Size: {os.path.getsize(dll_path)} bytes")

        return dll_found
    else:
        print("\n" + "="*60)
        print("HwpBasic.dll not found!")
        print("="*60)

        # Try to find any HWP related DLLs
        print("\nSearching for HWP related DLLs...")

        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue

            print(f"\nSearching in: {search_path}")

            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.lower().startswith("hwp") and file.lower().endswith(".dll"):
                        dll_path = os.path.join(root, file)
                        print(f"  Found: {file}")
                        print(f"    Path: {dll_path}")

        return []

if __name__ == "__main__":
    dll_files = find_hwpbasic_dll()

    if dll_files:
        print("\n" + "="*60)
        print("Found HwpBasic.dll!")
        print("="*60)
        print("\nNext steps:")
        print("1. Note the DLL file path above")
        print("2. Run as Administrator:")
        print(f"   regsvr32 \"{dll_files[0]}\"")
        print("\n3. Then try running the test script again")
    else:
        print("\n" + "="*60)
        print("HwpBasic.dll not found!")
        print("="*60)
        print("\nRecommendation:")
        print("1. Reinstall HwpOffice to ensure proper installation")
        print("2. Or check HWP installation directory manually")
        print("3. HWP installation directory is typically:")
        print("   - C:\\Program Files (x86)\\Hnc\\Office 2022")
        print("   - C:\\Program Files\\Hnc\\Office 2022")
