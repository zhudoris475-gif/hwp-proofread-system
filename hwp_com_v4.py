# -*- coding: utf-8 -*-
import sys, os, time, re, shutil

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")

SRC = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
WORK_DIR = r"C:\Users\doris\.agent-skills"
REPORT_DIR = r"C:\Users\doris\Desktop\xwechat_files\WORD\reports"
os.makedirs(REPORT_DIR, exist_ok=True)

ts = time.strftime("%Y%m%d_%H%M%S")
WORK_FILE = os.path.join(WORK_DIR, f"O_work_{ts}.hwp")

shutil.copy2(SRC, WORK_FILE)
print(f"✅ 복사: {WORK_FILE}")

try:
    import win32com.client
    import pythoncom
except ImportError:
    print("❌ win32com"); sys.exit(1)

pythoncom.CoInitialize()

try:
    hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=4)
    print("✅ COM 연결!")
    
    hwp.SetMessageBoxMode(0x00020000)
    
    hwp.Open(WORK_FILE, "HWP", "")
    time.sleep(2)
    print("✅ 파일 열림!")
    
    hwp.Run("MoveDocBegin")
    
    lines = []
    for i in range(100000):
        try:
            lt = hwp.GetLine()
            if lt is None or (lt == "" and i > 10):
                break
            if lt:
                lines.append(lt)
        except: break
        try:
            hwp.Run("MoveLineEnd")
            hwp.Run("MoveNext")
        except: break
    
    full_text = '\n'.join(lines)
    print(f"📝 추출: {len(lines)}줄 / {len(full_text)}자")
    print(f"   {full_text[:150]}...")
    
    from proofread import (
        collect_chinese_korean_corrections,
        collect_txt_corrections,
        collect_middle_dot_corrections,
        collect_quote_corrections,
    )
    
    config_dir = r"C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config"
    corrections = []
    
    for fn, label in [
        (collect_chinese_korean_corrections, "중한규칙"),
        (collect_txt_corrections, "TXT규칙"),
        (collect_middle_dot_corrections, "가운데점"),
        (collect_quote_corrections, "따옴표"),
    ]:
        try:
            c = fn(full_text, config_dir)
            corrections.extend(c)
            print(f"  ✅ {label}: {len(c)}개")
        except Exception as e:
            print(f"  ⚠️ {label}: {e}")
    
    print(f"\n📊 총 교정: {len(corrections)}개")
    
    if not corrections:
        print("→ 없음"); hwp.Close(); sys.exit(0)
    
    applied = skipped = 0
    log_lines = [f"HWP COM 교정 - {time.strftime('%Y-%m-%d %H:%M:%S')}", "="*50]
    
    for src, dst, rule_name, count in corrections:
        if src not in full_text:
            skipped += 1; continue
        
        words = ' '.join(re.findall(r"[\uac00-\ud7af\u1100-\u11ff\u3130-\u318fA-Za-z0-9]+", src)[:4])
        
        try:
            hwp.Run("MoveDocBegin")
            
            fr = hwp.Find(src, False, False, False)
            
            if fr > 0:
                ct = hwp.GetSelectedCtrlType()
                if ct == 0:
                    hwp.Delete()
                    hwp.Insert(dst)
                    applied += 1
                    log_lines.append(f"✅ '{src}' -> '{dst}' ({rule_name}) | {words}")
                    full_text = full_text.replace(src, dst, 1)
                else:
                    skipped += 1; log_lines.append(f"⏭ '{src}' (ctrl)")
            else:
                skipped += 1; log_lines.append(f"⏭ '{src}' (not found)")
        except Exception as e:
            skipped += 1; log_lines.append(f"❌ '{src}' -> {e}")
    
    out_name = f"O_COM_교정본_{ts}.hwp"
    out_path = os.path.join(r"C:\Users\doris\Desktop\xwechat_files\WORD", out_name)
    
    hwp.SaveAs(out_path, "HWP", "")
    time.sleep(1)
    
    out_sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    
    log_lines.append(f"\n결과: {applied}건 / 스킵 {skipped}건")
    log_lines.append(f"출력: {out_name} ({round(out_sz/1024,1)} KB)")
    
    report = os.path.join(REPORT_DIR, f"O_COM_{ts}.txt")
    with open(report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\n{'='*50}")
    print(f"✅ 완료! {applied}건 적용 / {skipped}건 스킵")
    print(f"📄 {out_name} ({round(out_sz/1024,1)} KB)")
    print(f"{'='*50}")
    
    hwp.Close()
    hwp = None

except Exception as e:
    print(f"\n❌ {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
finally:
    try: pythoncom.CoUninitialize()
    except: pass
