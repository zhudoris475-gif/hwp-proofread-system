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

print("=== 중한 교정 - 단계별 저장 테스트 ===")
print()

shutil.copy2(bak_path, hwp_path)
print(f"원본 복원: {os.path.getsize(hwp_path):,} bytes")

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

print("\n--- 교정 1개만 적용 후 저장 테스트 ---")
try:
    hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
    hwp.HParameterSet.HFindReplace.FindString = "저장성(절강성·浙江省)"
    hwp.HParameterSet.HFindReplace.ReplaceString = "절강성(浙江)"
    hwp.HParameterSet.HFindReplace.Direction = 0
    hwp.HParameterSet.HFindReplace.ReplaceMode = 1
    hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
    hwp.HParameterSet.HFindReplace.FindType = 1
    result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
    print(f"  AllReplace 결과: {result}")
except Exception as e:
    print(f"  AllReplace 에러: {e}")

time.sleep(1)

print("\n--- Save 시도 ---")
try:
    hwp.Save()
    print("  Save 성공!")
except Exception as e:
    print(f"  Save 실패: {e}")
    print(f"  에러 타입: {type(e)}")

print("\n--- SaveAs 시도 ---")
try:
    hwp.SaveAs(hwp_path, "HWP", "")
    print("  SaveAs 성공!")
except Exception as e:
    print(f"  SaveAs 실패: {e}")

print("\n--- 다른 경로로 SaveAs 시도 ---")
temp_path = os.path.join(os.environ['TEMP'], 'test_save.hwp')
try:
    hwp.SaveAs(temp_path, "HWP", "")
    print(f"  SaveAs 성공: {temp_path}")
    if os.path.exists(temp_path):
        print(f"  임시 파일 크기: {os.path.getsize(temp_path):,} bytes")
except Exception as e:
    print(f"  SaveAs도 실패: {e}")

print("\n--- HWP 상태 확인 ---")
try:
    pc = hwp.PageCount
    print(f"  PageCount: {pc}")
except Exception as e:
    print(f"  PageCount 에러: {e}")

try:
    hwp.Clear(1)
except:
    pass
try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()

print(f"\n--- 결과 파일 확인 ---")
md5_after = md5(hwp_path)
print(f"  원본 파일: {os.path.getsize(hwp_path):,} bytes, MD5={md5_after[:12]}...")

if os.path.exists(temp_path):
    import sys
    sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
    from hwp_ollama_proofread import extract_text_from_hwp_binary
    text = extract_text_from_hwp_binary(temp_path)
    print(f"  임시파일 텍스트: {len(text):,}자")
    cnt = text.count("절강성(浙江)")
    print(f"  '절강성(浙江)': {cnt}회")
    os.remove(temp_path)
