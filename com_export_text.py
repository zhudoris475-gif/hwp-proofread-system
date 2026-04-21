import win32com.client
import pythoncom
import os, time

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"
export_path = r"c:\Users\doris\.agent-skills\hwp_exported_text.txt"

pythoncom.CoInitialize()
CLSCTX_LOCAL_SERVER = 4

hwp = win32com.client.dynamic.Dispatch("HWPFrame.HwpObject")

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
time.sleep(2)

print(f"PageCount: {hwp.PageCount}")

try:
    hwp.HAction.GetDefault("TextSelectAll", hwp.HParameterSet.HSelAll.HSet)
    hwp.HAction.Execute("TextSelectAll", hwp.HParameterSet.HSelAll.HSet)
    text_len = hwp.GetSelectedTextLength()
    print(f"SelectedTextLength: {text_len}")
    hwp.Run("Cancel")
except Exception as e:
    print(f"TextSelectAll: {e}")

try:
    hwp.SaveAs(export_path, "TEXT", "")
    print(f"텍스트 내보내기 성공: {export_path}")
    if os.path.exists(export_path):
        with open(export_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        print(f"내보낸 텍스트 크기: {len(content):,}자")
        
        china_patterns = [
            "저장성(절강성·浙江省)",
            "절강성(浙江)",
            "안후이성(안휘성·安徽省)",
            "안휘성(安徽)",
            "푸젠성(복건성·福建省)",
            "복건성(福建)",
            "쑤저우(소주·苏州)",
            "소주(苏州)",
        ]
        print("\n중한 패턴 검색:")
        for p in china_patterns:
            cnt = content.count(p)
            print(f"  '{p}': {cnt}회")
except Exception as e:
    print(f"SaveAs TEXT error: {e}")

try:
    hwp.Quit()
except:
    pass
pythoncom.CoUninitialize()
