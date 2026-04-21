# -*- coding: utf-8 -*-
import sys, os, time, re, shutil, io

sys.stdout.reconfigure(encoding='utf-8', errors='repeat')

SRC = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
WORK_DIR = r"C:\Users\doris\.agent-skills"
OUT_DIR = r"C:\Users\doris\Desktop\xwechat_files\WORD"
REPORT_DIR = os.path.join(OUT_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

ts = time.strftime("%Y%m%d_%H%M%S")
WORK_FILE = os.path.join(WORK_DIR, f"O_rule_{ts}.hwp")

shutil.copy2(SRC, WORK_FILE)
print(f"✅ 복사: {WORK_FILE}")

sys.path.insert(0, r"C:\Users\doris\Desktop\xwechat_files\WORD")
import hwp_ollama_proofread_detailed as mod

config_dir = r"C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config"
log_fh = io.StringIO()

txt_rules, txt_dict = mod.parse_rules(mod.RULES_FILE)
china_rules, china_rules_dict = mod.load_china_place_rules()

print(f"\n📦 규칙 로드:")
print(f"   TXT: {len(txt_rules)}개 | 중한: {len(china_rules)}개")

text = mod.extract_text_from_hwp_binary(WORK_FILE, log_fh)
print(f"📝 텍스트: {len(text):,}자")

corrections = []

mod.log(f"\n--- 1단계: 중한 규칙 ---", log_fh)
china_corrections = mod.collect_china_korean_corrections(text, china_rules, log_fh)
for orig, repl in china_corrections:
    cnt = text.count(orig)
    corrections.append((orig, repl, "중한규칙", cnt))
print(f"  ✅ 중한: {len(china_corrections)}건")

mod.log(f"\n--- 2단계: TXT 규칙 ---", log_fh)
china_matched_srcs = set(orig for orig, repl in china_corrections)
for src, dst in txt_rules:
    if src not in text:
        continue
    skip = False
    for cms in china_matched_srcs:
        if src in cms or cms in src:
            skip = True; break
    if skip:
        continue
    cnt = text.count(src)
    corrections.append((src, dst, "TXT규칙", cnt))
txt_count = sum(1 for c in corrections if c[2] == "TXT규칙")
print(f"  ✅ TXT: {txt_count}건")

mod.log(f"\n--- 3단계: 가운데점 (규칙만) ---", log_fh)
dot_items = mod.collect_rule_based_dot_corrections(text, log_fh)
for orig, repl in dot_items:
    corrections.append((orig, repl, "가운데점-규칙", text.count(orig)))
dot_count = len(dot_items)
print(f"  ✅ 가운데점(규칙): {dot_count}건")

mod.log(f"\n--- 4단계: 따옴표 (고정명사만) ---", log_fh)
quote_fixed = [
    ('"欧洲联盟"', "'欧洲联盟'"),
    ('"欧洲共同体"', "'欧洲共同体'"),
    ('"欧洲共同市场"', "'欧洲共同市场'"),
    ('"欧洲大战"', "'欧洲大战'"),
    ('"欧洲煤钢联营"', "'欧洲煤钢联营'"),
    ('"欧洲原子能联营"', "'欧洲原子能联营'"),
    ('"欧洲经济共同体(共同市场)"', "'欧洲经济共同体(共同市场)'"),
    ('"欧洲安全和合作会议"', "'欧洲安全和合作会议'"),
]
for src, dst in quote_fixed:
    if src in text:
        corrections.append((src, dst, "따옴표-고정명사", text.count(src)))
qf_count = sum(1 for c in corrections if c[2] == "따옴표-고정명사")
print(f"  ✅ 따옴표(고정명사): {qf_count}건")

print(f"\n{'='*50}")
print(f"📊 총 교정 후보: {len(corrections)}건 (Ollama 없이)")
print(f"   - 중한: {len(china_corrections)} | TXT: {txt_count}")
print(f"   - 가운데점: {dot_count} | 따옴표: {qf_count}")
print(f"{'='*50}")

if not corrections:
    print("→ 교정 항목 없음"); sys.exit(0)

try:
    import win32com.client
    import pythoncom
except ImportError:
    print("❌ win32com 필요"); sys.exit(1)

pythoncom.CoInitialize()

try:
    hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=4)
    print("\n✅ COM 연결!")
    
    hwp.SetMessageBoxMode(0x00020000)
    
    hwp.Open(WORK_FILE, "HWP", "")
    time.sleep(1)
    print("✅ 파일 열림!")
    
    applied = skipped = 0
    log_lines = [f"HWP 규칙기반 교정 (No Ollama)", f"시간: {time.strftime('%Y-%m-%d %H:%M:%S')}", "="*50]
    
    done = set()
    
    for src, dst, rule_name, count in corrections:
        if src in done:
            continue
        
        words = ' '.join(re.findall(r"[\uac00-\ud7af\u1100-\u11ff\u3130-\u318fA-Za-z0-9]+", src)[:4])
        
        try:
            hwp.Run("MoveDocBegin")
            
            result = hwp.Find(src, False, False, False)
            
            total_found = 0
            
            while result > 0:
                sel_type = hwp.GetSelectedCtrlType()
                
                if sel_type == 0:
                    hwp.Delete()
                    hwp.Insert(dst)
                    total_found += 1
                
                result = hwp.Find(src, False, False, False)
                
                if total_found >= count or total_found > 100:
                    break
            
            if total_found > 0:
                applied += 1
                log_lines.append(f"✅ '{src}' -> '{dst}' ({rule_name}) x{total_found} | {words}")
                done.add(src)
            else:
                skipped += 1
                log_lines.append(f"⏭ '{src}' (미발견)")
                
        except Exception as e:
            skipped += 1
            log_lines.append(f"❌ '{src}' -> {e}")
    
    out_name = f"O_규칙교정본_{ts}.hwp"
    out_path = os.path.join(OUT_DIR, out_name)
    
    hwp.SaveAs(out_path, "HWP", "")
    time.sleep(1)
    
    out_sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    
    log_lines.append(f"\n결과: {applied}건 적용 / {skipped}건 스킵")
    log_lines.append(f"출력: {out_name} ({round(out_sz/1024,1)} KB)")
    log_lines.append(f"\n방식: 규칙 기반 (Ollama 미사용)")
    
    report = os.path.join(REPORT_DIR, f"O_RuleOnly_{ts}.txt")
    with open(report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\n{'='*50}")
    print(f"✅ 규칙 기반 교정 완료! (Ollama 없이)")
    print(f"   적용: {applied}건 | 스킵: {skipped}건")
    print(f"📄 {out_name} ({round(out_sz/1024,1)} KB)")
    print(f"   → 한컴오피스에서 열어보세요!")
    print(f"{'='*50}")

except Exception as e:
    print(f"\n❌ {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
finally:
    try: pythoncom.CoUninitialize()
    except: pass
