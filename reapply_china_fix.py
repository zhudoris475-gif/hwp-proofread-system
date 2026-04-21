import win32com.client
import pythoncom
import os, time, shutil

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp.bak"
hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

print("1단계: 원본 백업에서 복원")
shutil.copy2(bak_path, hwp_path)
print(f"  복원 완료: {os.path.getsize(hwp_path):,} bytes")

print("\n2단계: COM으로 교정 적용")
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

corrections = [
    ("저장성(절강성·浙江省)", "절강성(浙江)", "중한규칙"),
    ("안후이성(안휘성·安徽省)", "안휘성(安徽)", "중한규칙"),
    ("푸젠성(복건성·福建省)", "복건성(福建)", "중한규칙"),
    ("쑤저우(소주·苏州)", "소주(苏州)", "중한규칙"),
]

total = 0
for src, dst, rule_type in corrections:
    try:
        hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = src
        hwp.HParameterSet.HFindReplace.ReplaceString = dst
        hwp.HParameterSet.HFindReplace.Direction = 0
        hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        hwp.HParameterSet.HFindReplace.FindType = 1
        result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        print(f"  [{rule_type}] '{src}' -> '{dst}': result={result}")
        total += 1
    except Exception as e:
        print(f"  [{rule_type}] '{src}' -> '{dst}': ERROR - {e}")

print(f"\n  총 교정 시도: {total}건")

print("\n3단계: 파일 저장")
try:
    hwp.Save()
    print("  COM Save 완료")
except Exception as e:
    print(f"  COM Save 실패: {e}")

try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()

print(f"\n4단계: 파일 크기 확인")
print(f"  교정후 크기: {os.path.getsize(hwp_path):,} bytes")
print(f"  원본백업 크기: {os.path.getsize(bak_path):,} bytes")

print("\n5단계: 바이너리 추출로 검증")
import sys
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

text = extract_text_from_hwp_binary(hwp_path)
print(f"  추출 텍스트: {len(text):,}자")

china_patterns = [
    ("저장성(절강성·浙江省)", "절강성(浙江)"),
    ("안후이성(안휘성·安徽省)", "안휘성(安徽)"),
    ("푸젠성(복건성·福建省)", "복건성(福建)"),
    ("쑤저우(소주·苏州)", "소주(苏州)"),
]

for src, dst in china_patterns:
    src_count = text.count(src)
    dst_count = text.count(dst)
    status = "OK" if src_count == 0 and dst_count > 0 else "FAIL"
    print(f"  [{status}] '{src}' -> '{dst}': 원본={src_count}, 교정={dst_count}")
