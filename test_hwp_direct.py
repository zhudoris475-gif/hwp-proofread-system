"""
HWP Direct Modification Test using Hwp.exe with different method
Extract text, apply corrections, and save back to HWP file
"""
import win32com.client as win32
import os
import sys

# Set UTF-8 encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_and_correct_hwp(hwp_file_path):
    """Extract text from HWP, apply corrections, and save back."""

    # Hwp.exe path
    hwp_path = r"C:\Program Files (x86)\Hnc\Office 2022\HOffice120\Bin\Hwp.exe"

    if not os.path.exists(hwp_path):
        print(f"HWP not found at: {hwp_path}")
        return False

    try:
        print(f"Opening HWP file: {hwp_file_path}")
        print(f"HWP path: {hwp_path}")

        # Try different COM methods
        try:
            # Method 1: Direct dispatch
            hwp = win32.Dispatch(hwp_path)
            print("Method 1: Direct dispatch succeeded")
        except Exception as e1:
            print(f"Method 1 failed: {e1}")
            try:
                # Method 2: Create object with ProgID
                hwp = win32.Dispatch("HwpBasic.HwpObject")
                print("Method 2: ProgID dispatch succeeded")
            except Exception as e2:
                print(f"Method 2 failed: {e2}")
                try:
                    # Method 3: Create with CLSID
                    clsid = "{E6B7C2C0-5E0A-11D3-9D4B-00A0C9E3E66D}"
                    hwp = win32.Dispatch(clsid)
                    print("Method 3: CLSID dispatch succeeded")
                except Exception as e3:
                    print(f"Method 3 failed: {e3}")
                    return False

        # Open file
        hwp.Open(hwp_file_path)

        # Get text
        text = hwp.GetTextFile("TEXT", "")

        if not text or len(text) < 100:
            print("Text extraction failed or empty")
            print(f"Extracted text length: {len(text) if text else 0}")
            hwp.Close(0)
            return False

        print(f"Text extracted: {len(text)} characters")
        print(f"First 200 chars: {text[:200]}")

        # Apply corrections
        corrections = [
            (" 한 ", " 한"),
            (" 두 ", " 두"),
            (" 세 ", " 세"),
            (" 네 ", " 네"),
            (" 다 ", " 다"),
            (" 사 ", " 사"),
            (" 오 ", " 오"),
            (" 육 ", " 육"),
            (" 칠 ", " 칠"),
            (" 팔 ", " 팔"),
            (" 구 ", " 구"),
        ]

        original_text = text
        for find_str, replace_str in corrections:
            text = text.replace(find_str, replace_str)

        changes = len(original_text) - len(text)
        print(f"Applied {changes} corrections")

        # Use AllReplace to modify document
        print("\nApplying corrections to document...")
        hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)

        # Replace entire document
        hwp.HParameterSet.HFindReplace.FindString = original_text[:100]
        hwp.HParameterSet.HFindReplace.ReplaceString = text[:100]
        hwp.HParameterSet.HFindReplace.Direction = 0  # Search all
        hwp.HParameterSet.HFindReplace.ReplaceMode = 2  # Replace all

        result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        print(f"AllReplace result: {result}")

        # Save file
        backup_path = hwp_file_path + "_backup"
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rename(hwp_file_path, backup_path)

        hwp.Save(hwp_file_path)
        print(f"File saved: {hwp_file_path}")
        print(f"Backup: {backup_path}")

        hwp.Close(0)
        print("File closed successfully")

        return True

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    hwp_file = r"C:\Users\51906\Desktop\새 폴더\M 1959-2093--135--20240920.hwp"

    if os.path.exists(hwp_file):
        success = extract_and_correct_hwp(hwp_file)
        if success:
            print("\n" + "="*60)
            print("SUCCESS! HWP document was modified successfully!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("FAILED! HWP document modification failed!")
            print("="*60)
    else:
        print(f"File not found: {hwp_file}")