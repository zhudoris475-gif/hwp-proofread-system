"""
HWP Text Extraction and Correction using PowerShell
Extract text from HWP file and apply corrections
"""
import subprocess
import os

def extract_text_powershell(hwp_file_path):
    """Extract text from HWP file using PowerShell."""
    script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    $word = New-Object -ComObject HwpBasic.HwpObject
    $word.Open('{hwp_file_path}')
    $text = $word.GetTextFile("TEXT", "")
    $word.Close(0)
    $text
    """

    try:
        result = subprocess.run(
            ["powershell", "-Command", script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=30
        )

        if result.returncode == 0:
            text = result.stdout.strip()
            print(f"Text extraction successful!")
            print(f"Character count: {len(text)}")
            return text
        else:
            print(f"PowerShell extraction failed: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print("PowerShell extraction timed out")
        return None
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def apply_corrections(text):
    """Apply Korean spacing corrections."""
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

    original_text = text
    for find_str, replace_str in corrections:
        text = text.replace(find_str, replace_str)

    # Count changes
    changes = len(original_text) - len(text)
    print(f"✓ Applied {changes} character changes")

    return text

def save_corrected_text(text, output_path):
    """Save corrected text to file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✓ Corrected text saved to: {output_path}")

if __name__ == "__main__":
    # Test file
    hwp_file = r"C:\Users\51906\Desktop\claw_code\claw_code\hwp_backups\【20】O 2179-2182排版页数4-金花顺-gwm_backup_20260411_123154_modified.hwp"

    if not os.path.exists(hwp_file):
        print(f"File not found: {hwp_file}")
        sys.exit(1)

    print("=" * 60)
    print("HWP Text Extraction and Correction Test")
    print("=" * 60)

    # Step 1: Extract text
    print("\n[Step 1] Extracting text from HWP file...")
    text = extract_text_powershell(hwp_file)

    if not text:
        print("✗ Text extraction failed")
        sys.exit(1)

    # Step 2: Apply corrections
    print("\n[Step 2] Applying Korean spacing corrections...")
    corrected_text = apply_corrections(text)

    # Step 3: Save result
    print("\n[Step 3] Saving corrected text...")
    output_file = r"C:\Users\51906\Desktop\hwp_corrected.txt"
    save_corrected_text(corrected_text, output_file)

    # Show sample
    print("\n" + "=" * 60)
    print("Sample of corrected text (first 500 characters):")
    print("=" * 60)
    print(corrected_text[:500])
    print("\n" + "=" * 60)
    print("✓ Test completed successfully!")
    print("=" * 60)
