import win32com.client
import pythoncom
import time

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

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

print("\n--- InitScan/GetText 방식으로 텍스트 읽기 ---")
try:
    scan_result = hwp.InitScan(0, 0x07, 0, 1, "All", "")
    print(f"InitScan result: {scan_result}")
    
    if scan_result:
        all_text = []
        count = 0
        while count < 500:
            result = hwp.GetText()
            if result == "" or result is None:
                break
            if isinstance(result, tuple):
                text_part = str(result[0]) if len(result) > 0 else ""
            else:
                text_part = str(result)
            if text_part == "" or text_part == "0":
                break
            all_text.append(text_part)
            count += 1
        
        full_text = "".join(all_text)
        print(f"GetText: {count}개 세그먼트, 총 {len(full_text):,}자")
        
        if len(full_text) > 0:
            print(f"처음 200자: {full_text[:200]}")
        
        china_patterns = [
            ("저장성(절강성·浙江省)", "절강성(浙江)"),
            ("안후이성(안휘성·安徽省)", "안휘성(安徽)"),
            ("푸젠성(복건성·福建省)", "복건성(福建)"),
            ("쑤저우(소주·苏州)", "소주(苏州)"),
        ]
        
        print("\n중한 패턴 검색:")
        for src, dst in china_patterns:
            src_count = full_text.count(src)
            dst_count = full_text.count(dst)
            print(f"  '{src}': {src_count}회, '{dst}': {dst_count}회")
        
        print("\n일반 키워드:")
        for kw in ["중국", "유럽", "절강성", "안휘성", "복건성", "소주"]:
            cnt = full_text.count(kw)
            print(f"  '{kw}': {cnt}회")
        
        hwp.ReleaseScan()
except Exception as e:
    print(f"InitScan/GetText error: {e}")
    import traceback
    traceback.print_exc()

try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()
