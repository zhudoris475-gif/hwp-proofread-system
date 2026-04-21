# -*- coding: utf-8 -*-
import sys, os, time, re, shutil

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")

SRC = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
WORK_DIR = r"C:\Users\doris\Desktop\xwechat_files\WORD"
REPORT_DIR = os.path.join(WORK_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

WORK_FILE = os.path.join(WORK_DIR, "O_COM_work.hwp")

shutil.copy2(SRC, WORK_FILE)
print(f"✅ 작업 파일 복사: {WORK_FILE}")

try:
    import win32com.client
    import pythoncom
except ImportError:
    print("❌ win32com 필요"); sys.exit(1)

pythoncom.CoInitialize()

try:
    hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=4)
    print("✅ COM 연결 성공!")
    
    hwp.SetMessageBoxMode(0x00020000)
    try: hwp.Visible = False
    except: pass
    
    print(f"📂 열기: {WORK_FILE}")
    hwp.Open(WORK_FILE, "HWP", "")
    time.sleep(2)
    
    total_len = hwp.GetLength()
    print(f"📄 문서 길이: {total_len}자")
    
    full_text = ""
    pos = 0
    chunk_size = 10000
    while pos < total_len:
        end = min(pos + chunk_size, total_len)
        try:
            text = hwp.GetText(pos, end)
            if text:
                full_text += text
        except:
            pass
        pos = end
    
    if not full_text:
        print("⚠️ GetText 실패, GetLineCount로 재시도...")
        lines = []
        for i in range(1, min(50000, hwp.GetLineCount() + 1)):
            try:
                t = hwp.GetTextByLine(i)
                if t: lines.append(t)
            except: break
        full_text = '\n'.join(lines)
    
    print(f"📝 추출 텍스트: {len(full_text)}자")
    print(f"   미리보기: {full_text[:200]}...")
    
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
    
    print(f"\n📊 총 교정 후보: {len(corrections)}개")
    
    if not corrections:
        print("→ 교정 없음"); hwp.Close(); sys.exit(0)
    
    applied = 0; skipped = 0
    log_lines = [f"HWP COM 교정 - {time.strftime('%Y-%m-%d %H:%M:%S')}", f"대상: {os.path.basename(SRC)}", "="*50]
    
    for src, dst, rule_name, count in corrections:
        if src not in full_text:
            skipped += 1; continue
        
        words = ' '.join(re.findall(r"[\uac00-\ud7af\u1100-\u11ff\u3130-\u318fA-Za-z0-9]+", src)[:4])
        
        try:
            hwp.Find(src)
            found_pos = hwp.GetPos()
            
            if found_pos >= 0:
                hwp.Replace(src, dst, 0, 0, 0, 0, 0, 0)
                applied += 1
                log_lines.append(f"✅ '{src}' -> '{dst}' ({rule_name}) | 단어:{words}")
                full_text = full_text.replace(src, dst, 1)
            else:
                skipped += 1
                log_lines.append(f"⏭️ '{src}' (찾지 못함)")
        except Exception as e:
            skipped += 1
            log_lines.append(f"❌ '{src}' -> {e}")
    
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_name = f"O_COM_교정본_{ts}.hwp"
    out_path = os.path.join(WORK_DIR, out_name)
    
    hwp.SaveAs(out_path, "HWP", "")
    time.sleep(1)
    
    out_size = os.path.getsize(out_path)
    
    log_lines.append(f"\n결과: {applied}건 적용 / {skipped}건 스킵")
    log_lines.append(f"출력: {out_name} ({round(out_size/1024,1)} KB)")
    
    report = os.path.join(REPORT_DIR, f"O_COM_교정_{ts}.txt")
    with open(report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\n{'='*50}")
    print(f"✅ COM 교정 완료!")
    print(f"   적용: {applied}건 | 스킵: {skipped}건")
    print(f"   출력: {out_name} ({round(out_size/1024,1)} KB)")
    print(f"{'='*50}")
    
    hwp.Close()
    hwp = None

except Exception as e:
    print(f"\n❌ 오류: {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
finally:
    try: pythoncom.CoUninitialize()
    except: pass
