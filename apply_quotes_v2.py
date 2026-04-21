import win32com.client
import pythoncom
import os, time, subprocess

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

subprocess.run(["powershell", "-Command", "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"], capture_output=True)
time.sleep(3)

pythoncom.CoInitialize()
CLSCTX_LOCAL_SERVER = 4
hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=CLSCTX_LOCAL_SERVER)

for module_name in ("FilePathCheckerModule", "SecurityModule"):
    try:
        hwp.RegisterModule("FilePathCheckDLL", module_name)
    except:
        pass
try:
    hwp.SetMessageBoxMode(0x00020000)
except:
    pass

hwp.Open(hwp_path, "HWP", "forceopen:true")
time.sleep(3)
print(f"HWP 열기 성공 (PageCount={hwp.PageCount})")

print("\n--- 방법1: 개별 따옴표 문자 교체 ---")
quote_char_replacements = [
    ("\u201c", "\u2018"),
    ("\u201d", "\u2019"),
]

for src, dst in quote_char_replacements:
    try:
        hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = src
        hwp.HParameterSet.HFindReplace.ReplaceString = dst
        hwp.HParameterSet.HFindReplace.Direction = 0
        hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        hwp.HParameterSet.HFindReplace.FindType = 1
        result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        print(f"  '{src}' -> '{dst}': result={result}")
    except Exception as e:
        print(f"  '{src}' -> '{dst}': ERROR - {e}")
    time.sleep(0.5)

time.sleep(1)
save_ok = False
try:
    hwp.Save()
    save_ok = True
    print("\nSave 성공!")
except Exception as e:
    print(f"\nSave 실패: {e}")

try:
    hwp.Clear(1)
except:
    pass
try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()

print(f"\n파일 크기: {os.path.getsize(hwp_path):,} bytes")

import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

text = extract_text_from_hwp_binary(hwp_path)
print(f"추출 텍스트: {len(text):,}자")

left_double = text.count("\u201c")
right_double = text.count("\u201d")
left_single = text.count("\u2018")
right_single = text.count("\u2019")

print(f"\n따옴표 현황:")
print(f"  큰따옴표 왼쪽: {left_double}회")
print(f"  큰따옴표 오른쪽: {right_double}회")
print(f"  작은따옴표 왼쪽: {left_single}회")
print(f"  작은따옴표 오른쪽: {right_single}회")

if left_double == 0 and right_double == 0:
    print("\n  따옴표 교정 성공!")
else:
    print(f"\n  따옴표 교정 미완료 (큰따옴표 {left_double + right_double}개 남음)")
