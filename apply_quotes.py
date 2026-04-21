import win32com.client
import pythoncom
import os, time, subprocess

hwp_path = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp"

subprocess.run(["powershell", "-Command", "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"], capture_output=True)
time.sleep(2)

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

quote_corrections = [
    ("\u201c噢\u201d", "\u2018噢\u2019"),
    ("\u201c瓯\u201d", "\u2018瓯\u2019"),
    ("\u201c欧姆\u201d", "\u2018欧姆\u2019"),
    ("\u201c欧洲安全和合作会议\u201d", "\u2018欧洲安全和合作会议\u2019"),
    ("\u201c欧洲共同体\u201d", "\u2018欧洲共同体\u2019"),
    ("\u201c欧洲联盟\u201d", "\u2018欧洲联盟\u2019"),
    ("\u201c欧洲共同市场\u201d", "\u2018欧洲共同市场\u2019"),
    ("\u201c欧洲大战\u201d", "\u2018欧洲大战\u2019"),
    ("\u201c欧洲煤钢联营\u201d", "\u2018欧洲煤钢联营\u2019"),
    ("\u201c欧洲原子能联营\u201d", "\u2018欧洲原子能联营\u2019"),
    ("\u201c欧洲经济共同体(共同市场)\u201d", "\u2018欧洲经济共同体(共同市场)\u2019"),
    ("\u201c偶B)\u201d", "\u2018偶B)\u2019"),
]

print("\n따옴표 교정 적용:")
applied = 0
for i, (src, dst) in enumerate(quote_corrections):
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
            print(f"  [{i+1}/{len(quote_corrections)}] [OK] '{src}' -> '{dst}'")
        else:
            print(f"  [{i+1}/{len(quote_corrections)}] [SKIP] '{src}'")
        time.sleep(0.5)
    except Exception as e:
        print(f"  [{i+1}/{len(quote_corrections)}] [ERROR] '{src}': {e}")

print(f"\n적용 성공: {applied}건")

time.sleep(1)
save_ok = False
try:
    hwp.Save()
    save_ok = True
    print("Save 성공!")
except Exception as e:
    print(f"Save 실패: {e}")

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

print("\n따옴표 교정 확인:")
for src, dst in quote_corrections:
    src_cnt = text.count(src)
    dst_cnt = text.count(dst)
    ok = src_cnt == 0 and dst_cnt > 0
    print(f"  [{'OK' if ok else 'CHECK'}] '{src}' -> '{dst}': 원본={src_cnt}, 교정={dst_cnt}")
