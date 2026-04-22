"""
HWP Text Extraction Test
Extract text from HWP file using COM automation
"""
import win32com.client as win32
import os

def extract_text_hwp(hwp_file_path):
    """Extract text from HWP file using GetTextFile method."""
    hwp = win32.Dispatch("HwpBasic.HwpObject")

    try:
        print(f"Opening HWP file: {hwp_file_path}")
        hwp.Open(hwp_file_path)

        # Extract text using GetTextFile
        text = hwp.GetTextFile("TEXT", "")

        print(f"Text extraction successful!")
        print(f"Character count: {len(text)}")
        print(f"Line count: {len(text.splitlines())}")
        print(f"Paragraph count: {len([p for p in text.split('\n\n') if p.strip()])}")

        # Show first 500 characters
        print(f"\nFirst 500 characters:")
        print(text[:500])

        return text

    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

    finally:
        try:
            hwp.Close(0)
        except:
            pass

if __name__ == "__main__":
    # Test file
    hwp_file = r"C:\Users\51906\Desktop\claw_code\claw_code\hwp_backups\【20】O 2179-2182排版页数4-金花顺-gwm_backup_20260411_123154_modified.hwp"

    if os.path.exists(hwp_file):
        text = extract_text_hwp(hwp_file)

        if text:
            # Save to file
            output_file = r"C:\Users\51906\Desktop\hwp_extracted_text.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"\nText saved to: {output_file}")
    else:
        print(f"File not found: {hwp_file}")
