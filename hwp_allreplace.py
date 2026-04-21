# -*- coding: utf-8 -*-
import sys, os, time, re, shutil

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
WORK_DIR = r"C:\Users\doris\.agent-skills"
OUT_DIR = r"C:\Users\doris\Desktop\xwechat_files\WORD"
REPORT_DIR = os.path.join(OUT_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

ts = time.strftime("%Y%m%d_%H%M%S")
WORK_FILE = os.path.join(WORK_DIR, f"O_com_{ts}.hwp")

shutil.copy2(SRC, WORK_FILE)
print(f"✅ 복사 완료")

sys.path.insert(0, r"C:\Users\doris\Desktop\xwechat_files\WORD")

from hwp_ollama_proofread_detailed import (
    collect_chinese_korean_corrections,
    collect_txt_corrections,
    collect_middle_dot_corrections,
    collect_quote_corrections_with_ollama as collect_quote_corrections,
    decompress_chain,
)

with open(WORK_FILE, 'rb') as f:
    data = f.read()

import olefile
ole = olefile.OleFileIO(WORK_FILE, write_mode=False)
stream = ole.openstream(['BodyText', 'Section0'])
comp = stream.read()
stream.close()
ole.close()

dec = decompress_chain(comp)
full_text = dec.decode('utf-16-le', errors='replace')
print(f"📝 텍스트 추출: {len(full_text)}자")

config_dir = r"C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config"
corrections = []

for fn, label in [
    (collect_chinese_korean_corrections, "중한"),
    (collect_txt_corrections, "TXT"),
    (collect_middle_dot_corrections, "가운데점"),
    (collect_quote_corrections, "따옴표"),
]:
    try:
        import io
        log_fh = io.StringIO()
        c = fn(full_text, config_dir, log_fh=log_fh)
        corrections.extend(c)
        print(f"  ✅ {label}: {len(c)}개")
    except Exception as e:
        print(f"  ⚠️ {label}: {e}")

print(f"\n📊 총: {len(corrections)}개")

if not corrections:
    print("→ 없음"); sys.exit(0)

try:
    import win32com.client
    import pythoncom
except ImportError:
    print("❌ win32com"); sys.exit(1)

pythoncom.CoInitialize()

try:
    hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=4)
    print("\n✅ COM 연결!")
    
    hwp.SetMessageBoxMode(0x00020000)
    
    hwp.Open(WORK_FILE, "HWP", "")
    time.sleep(1)
    print("✅ 파일 열림!")
    
    applied = skipped = 0
    log_lines = [f"HWP COM AllReplace 교정", f"시간: {time.strftime('%Y-%m-%d %H:%M:%S')}", "="*50]
    
    done_srcs = set()
    
    for src, dst, rule_name, count in corrections:
        if src in done_srcs:
            continue
        
        words = ' '.join(re.findall(r"[\uac00-\ud7af\u1100-\u11ff\u3130-\u318fA-Za-z0-9]+", src)[:4])
        
        try:
            hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
            
            fr_set = hwp.HParameterSet.HFindReplace.HSet
            fr_set.FindString = src
            fr_set.ReplaceString = dst
            fr_set.ReplaceMode = 1
            
            result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
            
            if result:
                applied += 1
                log_lines.append(f"✅ '{src}' -> '{dst}' ({rule_name}) | {words}")
                done_srcs.add(src)
            else:
                skipped += 1
                log_lines.append(f"⏭ '{src}' (실패)")
                
        except Exception as e:
            skipped += 1
            log_lines.append(f"❌ '{src}' -> {e}")
    
    out_name = f"O_COM_교정본_{ts}.hwp"
    out_path = os.path.join(OUT_DIR, out_name)
    
    hwp.SaveAs(out_path, "HWP", "")
    time.sleep(1)
    
    out_sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    
    log_lines.append(f"\n결과: {applied}건 / 스킵 {skipped}건")
    log_lines.append(f"출력: {out_name} ({round(out_sz/1024,1)} KB)")
    
    report = os.path.join(REPORT_DIR, f"O_COM_AllReplace_{ts}.txt")
    with open(report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\n{'='*50}")
    print(f"✅ COM AllReplace 완료!")
    print(f"   적용: {applied}건 | 스킵: {skipped}건")
    print(f"📄 {out_name} ({round(out_sz/1024,1)} KB)")
    print(f"   → 한컴오피스에서 열어보세요!")
    print(f"{'='*50}")
    
    hwp.Close()
    hwp = None

except Exception as e:
    print(f"\n❌ {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
finally:
    try: pythoncom.CoUninitialize()
    except: pass
