import win32com.client
import pythoncom
import time, shutil, os, hashlib

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp.bak"
hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

print("=== COM Save만으로 파일이 변경되는지 테스트 ===")
shutil.copy2(bak_path, hwp_path)
md5_before = md5(hwp_path)
size_before = os.path.getsize(hwp_path)
print(f"복원후: {size_before:,} bytes, MD5={md5_before}")

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

print(f"PageCount: {hwp.PageCount}")

print("\nCOM Save 실행 (수정 없이)")
try:
    hwp.Save()
    print("  Save 완료")
except Exception as e:
    print(f"  Save 실패: {e}")

try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()

md5_after = md5(hwp_path)
size_after = os.path.getsize(hwp_path)
print(f"\nSave후: {size_after:,} bytes, MD5={md5_after}")
print(f"변경됨: {md5_before != md5_after}")
print(f"크기 변화: {size_after - size_before:+,} bytes")

import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

text = extract_text_from_hwp_binary(hwp_path)
print(f"\n바이너리 추출: {len(text):,}자")

china_patterns = [
    ("저장성(절강성·浙江省)", "절강성(浙江)"),
    ("안후이성(안휘성·安徽省)", "안휘성(安徽)"),
    ("푸젠성(복건성·福建省)", "복건성(福建)"),
    ("쑤저우(소주·苏州)", "소주(苏州)"),
]

for src, dst in china_patterns:
    src_count = text.count(src)
    dst_count = text.count(dst)
    status = "원본유지" if src_count > 0 and dst_count == 0 else f"변경됨(src={src_count},dst={dst_count})"
    print(f"  '{src}' -> '{dst}': {status}")
