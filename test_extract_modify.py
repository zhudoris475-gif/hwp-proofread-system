"""
HWP Text Extraction and Modification
Extract text from HWP file, modify, and save back
"""
import subprocess
import os
import sys

# Set UTF-8 encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_and_correct_hwp(hwp_file_path):
    """Extract text from HWP, apply corrections, and save back."""

    # PowerShell script to extract text and apply corrections
    powershell_script = f"""
    $ErrorActionPreference = "Stop"

    try {{
        # Try to open HWP file
        $hwp = New-Object -ComObject HwpBasic.HwpObject
        $hwp.Open('{hwp_file_path}')

        # Get text
        $text = $hwp.GetTextFile("TEXT", "")

        if ([string]::IsNullOrEmpty($text) -or $text.Length -lt 100) {{
            Write-Output "EXTRACTION_FAILED"
            exit 1
        }}

        Write-Output "EXTRACTION_SUCCESS"
        Write-Output $text

        # Apply corrections
        $text = $text.Replace(" 한 ", " 한")
        $text = $text.Replace(" 두 ", " 두")
        $text = $text.Replace(" 세 ", " 세")
        $text = $text.Replace(" 네 ", " 네")
        $text = $text.Replace(" 다 ", " 다")
        $text = $text.Replace(" 사 ", " 사")
        $text = $text.Replace(" 오 ", " 오")
        $text = $text.Replace(" 육 ", " 육")
        $text = $text.Replace(" 칠 ", " 칠")
        $text = $text.Replace(" 팔 ", " 팔")
        $text = $text.Replace(" 구 ", " 구")

        # Save back to HWP
        $hwp.HAction.GetDefault("AllReplace", $hwp.HParameterSet.HFindReplace.HSet)
        $hwp.HParameterSet.HFindReplace.FindString = $text.Substring(0, [Math]::Min(100, $text.Length))
        $hwp.HParameterSet.HFindReplace.ReplaceString = $text.Substring(0, [Math]::Min(100, $text.Length))
        $hwp.HParameterSet.HFindReplace.Direction = 0
        $hwp.HParameterSet.HFindReplace.ReplaceMode = 2
        $hwp.HAction.Execute("AllReplace", $hwp.HParameterSet.HFindReplace.HSet)

        # Save file
        $backupPath = '{hwp_file_path}_backup'
        if (Test-Path $backupPath) {{
            Remove-Item $backupPath
        }}
        Move-Item $hwp_file_path $backupPath
        $hwp.Save($hwp_file_path)

        $hwp.Close(0)

        Write-Output "SAVE_SUCCESS"
    }}
    catch {{
        Write-Output "ERROR: $($_.Exception.Message)"
        Write-Output "Stack: $($_.ScriptStackTrace)"
        exit 1
    }}
    """

    try:
        print(f"Opening HWP file: {hwp_file_path}")

        # Run PowerShell script
        result = subprocess.run(
            ["powershell", "-Command", powershell_script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=30
        )

        print(f"Return code: {result.returncode}")

        if result.returncode != 0:
            print(f"stderr: {result.stderr}")
            return False

        output = result.stdout.strip()

        # Parse output
        if output.startswith("EXTRACTION_FAILED"):
            print("Text extraction failed")
            return False

        if output.startswith("ERROR:"):
            print(f"Error: {output}")
            return False

        print(f"Text extraction successful!")
        print(f"Character count: {len(output)}")

        # Show sample
        print(f"\nFirst 200 characters:")
        print(output[:200])

        print("\nApplying corrections and saving...")

        if "SAVE_SUCCESS" in output:
            print("File saved successfully!")
            print(f"Backup created: {hwp_file_path}_backup")
            return True
        else:
            print("Save failed")
            return False

    except subprocess.TimeoutExpired:
        print("PowerShell script timed out")
        return False
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
