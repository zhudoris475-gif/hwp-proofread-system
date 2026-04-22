"""
HWP Direct Modification using Hwp.exe directly
Open HWP file and run macro for direct modification
"""
import subprocess
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

        # Create PowerShell script to open HWP file
        powershell_script = f"""
        $ErrorActionPreference = "Stop"

        try {{
            # Open HWP file
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
            $corrections = @(
                {{Find=" 한 ", Replace=" 한"}},
                {{Find=" 두 ", Replace=" 두"}},
                {{Find=" 세 ", Replace=" 세"}},
                {{Find=" 네 ", Replace=" 네"}},
                {{Find=" 다 ", Replace=" 다"}},
                {{Find=" 사 ", Replace=" 사"}},
                {{Find=" 오 ", Replace=" 오"}},
                {{Find=" 육 ", Replace=" 육"}},
                {{Find=" 칠 ", Replace=" 칠"}},
                {{Find=" 팔 ", Replace=" 팔"}},
                {{Find=" 구 ", Replace=" 구"}}
            )

            foreach ($corr in $corrections) {{
                $text = $text.Replace($corr.Find, $corr.Replace)
            }}

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

        # Run PowerShell script
        result = subprocess.run(
            ["powershell", "-Command", powershell_script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=30
        )

        if result.returncode != 0:
            print(f"PowerShell script failed!")
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
