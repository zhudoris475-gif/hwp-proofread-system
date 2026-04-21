import win32com.client
import pythoncom
import os, time, shutil, hashlib

bak_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp.bak"
hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

print("=== 중한 교정 재적용 (SaveAs 방식) ===")
print()

shutil.copy2(bak_path, hwp_path)
md5_before = md5(hwp_path)
print(f"1. 원본 복원: {os.path.getsize(hwp_path):,} bytes, MD5={md5_before[:12]}...")

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
print(f"2. HWP 열기 성공 (PageCount={hwp.PageCount})")

corrections = [
    ("저장성(절강성·浙江省)", "절강성(浙江)", "중한규칙"),
    ("안후이성(안휘성·安徽省)", "안휘성(安徽)", "중한규칙"),
    ("푸젠성(복건성·福建省)", "복건성(福建)", "중한규칙"),
    ("쑤저우(소주·苏州)", "소주(苏州)", "중한규칙"),
    ("한것", "한 것", "띄어쓰기"),
    ("소중한것", "소중한 것", "띄어쓰기"),
    ("진것", "진 것", "띄어쓰기"),
    ("유럽안", "유럽 안", "띄어쓰기"),
    ("해 보다", "해보다", "붙여쓰기"),
    ("옛 친구", "옛친구", "붙여쓰기"),
    ("뜻으로,", "뜻으로", "구두점"),
]

print("\n3. 교정 적용:")
applied = 0
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
        if result:
            applied += 1
            print(f"  [OK] [{rule_type}] '{src}' -> '{dst}'")
        else:
            print(f"  [SKIP] [{rule_type}] '{src}' -> '{dst}' (매치 없음)")
    except Exception as e:
        print(f"  [ERROR] [{rule_type}] '{src}' -> '{dst}': {e}")

print(f"\n  적용 성공: {applied}건")

print("\n4. 파일 저장 (SaveAs 방식):")
save_ok = False
try:
    hwp.SaveAs(hwp_path, "HWP", "")
    save_ok = True
    print("  SaveAs 성공")
except Exception as e1:
    print(f"  SaveAs 실패: {e1}")
    try:
        hwp.Save()
        save_ok = True
        print("  Save 성공 (fallback)")
    except Exception as e2:
        print(f"  Save도 실패: {e2}")

try:
    hwp.Clear(1)
except:
    pass
try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()

md5_after = md5(hwp_path)
size_after = os.path.getsize(hwp_path)
print(f"\n5. 파일 상태: {size_after:,} bytes, MD5={md5_after[:12]}...")
print(f"  파일 변경됨: {md5_before != md5_after}")

print("\n6. 바이너리 추출 검증:")
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

all_ok = True
for src, dst in china_patterns:
    src_count = text.count(src)
    dst_count = text.count(dst)
    ok = src_count == 0 and dst_count > 0
    if not ok:
        all_ok = False
    print(f"  [{'OK' if ok else 'FAIL'}] '{src}' -> '{dst}': 원본={src_count}, 교정={dst_count}")

other_checks = [
    ("한 것", "한것"),
    ("소중한 것", "소중한것"),
    ("진 것", "진것"),
    ("유럽 안", "유럽안"),
    ("해보다", "해 보다"),
    ("옛친구", "옛 친구"),
    ("뜻으로", "뜻으로,"),
]

for correct, wrong in other_checks:
    c_count = text.count(correct)
    w_count = text.count(wrong)
    ok = c_count > 0 or w_count == 0
    print(f"  [{'OK' if ok else 'CHECK'}] '{correct}': {c_count}회, '{wrong}': {w_count}회")

print(f"\n{'='*60}")
if all_ok and save_ok:
    print("  중한 교정 정상 적용 확인!")
else:
    print("  문제 있음 - 추가 조치 필요")
print(f"{'='*60}")
