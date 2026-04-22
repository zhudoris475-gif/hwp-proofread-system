"""
HWP Direct Correction Test
Use AllReplace API to directly modify HWP document
"""
import win32com.client as win32
import os
import sys

def correct_hwp_document(hwp_file_path):
    """Directly correct HWP document using AllReplace API."""
    # Try to find HWP installation
    possible_paths = [
        r"C:\Program Files\Hancom\HwpOffice\HwpBasic.exe",
        r"C:\Program Files (x86)\Hancom\HwpOffice\HwpBasic.exe",
        r"D:\Program Files\Hancom\HwpOffice\HwpBasic.exe",
        r"C:\Program Files\Hangul\HwpOffice\HwpBasic.exe",
    ]

    hwp_path = None
    for path in possible_paths:
        if os.path.exists(path):
            hwp_path = path
            print(f"Found HWP at: {path}")
            break

    if not hwp_path:
        print("HWP not found in standard locations. Please install HwpOffice.")
        return False

    try:
        print(f"Opening HWP file: {hwp_file_path}")
        hwp = win32.Dispatch(hwp_path)

        # Sample correction: Fix spacing issues
        # Example: "한 개" -> "한개", "두 마리" -> "두마리"
        corrections = [
            (" 한 ", " 한"),   # Add space after Korean particles
            (" 두 ", " 두"),   # Add space after Korean particles
            (" 세 ", " 세"),   # Add space after Korean particles
            (" 네 ", " 네"),   # Add space after Korean particles
            (" 다 ", " 다"),   # Add space after Korean particles
            (" 사 ", " 사"),   # Add space after Korean particles
            (" 오 ", " 오"),   # Add space after Korean particles
            (" 육 ", " 육"),   # Add space after Korean particles
            (" 칠 ", " 칠"),   # Add space after Korean particles
            (" 팔 ", " 팔"),   # Add space after Korean particles
            (" 구 ", " 구"),   # Add space after Korean particles
        ]

        print(f"\nApplying {len(corrections)} corrections...")

        for find_str, replace_str in corrections:
            # Get default AllReplace parameters
            hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)

            # Set parameters
            hwp.HParameterSet.HFindReplace.FindString = find_str
            hwp.HParameterSet.HFindReplace.ReplaceString = replace_str
            hwp.HParameterSet.HFindReplace.Direction = 0  # Search all
            hwp.HParameterSet.HFindReplace.ReplaceMode = 2  # Replace all occurrences

            # Execute correction
            result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)

            if result == 1:
                print(f"  ✓ Corrected: '{find_str}' -> '{replace_str}'")
            else:
                print(f"  ✗ Not found: '{find_str}'")

        # Save the file
        backup_path = hwp_file_path + "_backup"
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rename(hwp_file_path, backup_path)

        hwp.Save(hwp_file_path)
        print(f"\n✓ File saved: {hwp_file_path}")
        print(f"✓ Backup created: {backup_path}")

        # Close the file
        hwp.Close(0)
        print("✓ File closed successfully")

        return True

    except Exception as e:
        print(f"Error during correction: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        try:
            hwp.Close(0)
        except:
            pass

if __name__ == "__main__":
    # Test file
    hwp_file = r"C:\Users\51906\Desktop\claw_code\claw_code\hwp_backups\【20】O 2179-2182排版页数4-金花顺-gwm_backup_20260411_123154_modified.hwp"

    if os.path.exists(hwp_file):
        success = correct_hwp_document(hwp_file)

        if success:
            print("\n✓ HWP document correction completed successfully!")
        else:
            print("\n✗ HWP document correction failed!")
    else:
        print(f"File not found: {hwp_file}")
