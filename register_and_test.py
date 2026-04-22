"""
Register HwpAutomation COM Object and Test
Register HwpAutomation.dll and test text extraction
"""
import subprocess
import os
import sys

# Set UTF-8 encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def register_and_test():
    """Register HwpAutomation.dll and test text extraction."""

    # HwpAutomation.dll path
    dll_path = r"C:\Program Files (x86)\Hnc\Office 2022\HOffice120\Bin\HwpAutomation.dll"

    if not os.path.exists(dll_path):
        print(f"HwpAutomation.dll not found at: {dll_path}")
        return False

    print(f"Found HwpAutomation.dll: {dll_path}")
    print(f"Size: {os.path.getsize(dll_path)} bytes")

    try:
        print("\n" + "="*60)
        print("Registering COM object...")
        print("="*60)

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
            print("SUCCESS! COM object registered!")
            print("="*60)

            # Test text extraction
            print("\n" + "="*60)
            print("Testing text extraction...")
            print("="*60)

            test_hwp_file = r"C:\Users\51906\Desktop\새 폴더\M 1959-2093--135--20240920.hwp"

            if os.path.exists(test_hwp_file):
                # Test PowerShell script
                powershell_script = f"""
                $ErrorActionPreference = "Stop"

                try {{
                    # Open HWP file
                    $hwp = New-Object -ComObject HwpBasic.HwpObject
                    $hwp.Open('{test_hwp_file}')

                    # Get text
                    $text = $hwp.GetTextFile("TEXT", "")

                    if ([string]::IsNullOrEmpty($text) -or $text.Length -lt 100) {{
                        Write-Output "EXTRACTION_FAILED"
                        exit 1
                    }}

                    Write-Output "EXTRACTION_SUCCESS"
                    Write-Output $text

                    $hwp.Close(0)
                }}
                catch {{
                    Write-Output "ERROR: $($_.Exception.Message)"
                    exit 1
                }}
                """

                result = subprocess.run(
                    ["powershell", "-Command", powershell_script],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    timeout=30
                )

                if result.returncode == 0:
                    output = result.stdout.strip()
                    if output.startswith("EXTRACTION_SUCCESS"):
                        print(f"Text extraction successful!")
                        print(f"Character count: {len(output)}")
                        print(f"\nFirst 200 characters:")
                        print(output[:200])
                        return True
                    else:
                        print(f"Text extraction failed: {output}")
                else:
                    print(f"PowerShell test failed: {result.stderr}")
            else:
                print(f"Test file not found: {test_hwp_file}")

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
    success = register_and_test()

    if success:
        print("\n" + "="*60)
        print("SUCCESS! COM object registered and tested!")
        print("="*60)
        print("\nNow you can use HwpBasic.HwpObject in Python!")
        print("Example:")
        print("  import win32com.client as win32")
        print("  hwp = win32.Dispatch('HwpBasic.HwpObject')")
        print("  hwp.Open('file.hwp')")
    else:
        print("\n" + "="*60)
        print("FAILED! COM object registration and test failed!")
        print("="*60)
        print("\nRecommendation:")
        print("1. Run as Administrator:")
        print(f"   regsvr32 \"{dll_path}\"")
        print("2. Or reinstall HwpOffice")
