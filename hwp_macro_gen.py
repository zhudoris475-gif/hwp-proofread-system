# -*- coding: utf-8 -*-
import sys, os, time, re, shutil, io

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
OUT_DIR = r"C:\Users\doris\Desktop\xwechat_files\WORD"
MACRO_DIR = os.path.join(OUT_DIR, "macros")
REPORT_DIR = os.path.join(OUT_DIR, "reports")
os.makedirs(MACRO_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

ts = time.strftime("%Y%m%d_%H%M%S")
log_fh = io.StringIO()

print("=" * 60)
print("📝 HWP 교정용 JS 매크로 생성기")
print("=" * 60)

sys.path.insert(0, r"C:\Users\doris\Desktop\xwechat_files\WORD")
import hwp_ollama_proofread_detailed as mod

txt_rules, txt_dict = mod.parse_rules(mod.RULES_FILE)
china_rules, china_rules_dict = mod.load_china_place_rules()

print(f"\n📦 규칙 로드:")
print(f"   TXT: {len(txt_rules)}개 | 중한: {len(china_rules)}개")

text = mod.extract_text_from_hwp_binary(SRC, log_fh)
print(f"📝 텍스트 추출: {len(text):,}자")

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

mod.log(f"\n--- 3단계: 가운데점 (규칙) ---", log_fh)
dot_items = mod.collect_rule_based_dot_corrections(text, log_fh)
for orig, repl in dot_items:
    corrections.append((orig, repl, "가운데점", text.count(orig)))
dot_count = len(dot_items)
print(f"  ✅ 가운데점: {dot_count}건")

mod.log(f"\n--- 4단계: 따옴표 (고정명사) ---", log_fh)
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
        corrections.append((src, dst, "따옴표", text.count(src)))
qf_count = sum(1 for c in corrections if c[2] == "따옴표")
print(f"  ✅ 따옴표: {qf_count}건")

print(f"\n{'='*60}")
print(f"📊 총 교정 항목: {len(corrections)}건")
print(f"   - 중한: {len(china_corrections)} | TXT: {txt_count}")
print(f"   - 가운데점: {dot_count} | 따옴표: {qf_count}")
print(f"{'='*60}")

if not corrections:
    print("\n❌ 교정 항목 없음"); sys.exit(1)

def escape_js_string(s):
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "\\'")
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    return s

macro_file = os.path.join(MACRO_DIR, f"hwp_proofread_{ts}.js")
report_file = os.path.join(REPORT_DIR, f"JS_Macro_{ts}.txt")

js_content = []
js_content.append('/**')
js_content.append(' * HWP 자동 교정 매크로')
js_content.append(f' * 생성일시: {time.strftime("%Y-%m-%d %H:%M:%S")}')
js_content.append(f' * 대상파일: {os.path.basename(SRC)}')
js_content.append(f' * 교정항목: {len(corrections)}건')
js_content.append(' * ')
js_content.append(' * 사용법:')
js_content.append(' * 1. 한컴오피스에서 대상 HWP 파일 열기')
js_content.append(' * 2. 도구 > 매크로 > 실행 (또는 Alt+F8)')
js_content.append(' * 3. 이 파일 선택 후 실행')
js_content.append(' */')
js_content.append('')
js_content.append('function OnScriptMacro_Proofread()')
js_content.append('{')
js_content.append('\tvar totalChanges = 0;')
js_content.append('\tvar skipped = 0;')
js_content.append('')
js_content.append('\t// ===== 교정 시작 =====')

log_lines = [
    f"HWP JS 매크로 생성",
    f"시간: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    f"대상: {os.path.basename(SRC)}",
    "=" * 60,
]

done_set = set()
idx = 1
for src, dst, rule_name, count in corrections:
    if src in done_set:
        continue
    
    done_set.add(src)
    
    esc_src = escape_js_string(src)
    esc_dst = escape_js_string(dst)
    
    words = ' '.join(re.findall(r"[\uac00-\ud7af\u1100-\u11ff\u3130-\u318fA-Za-z0-9]+", src)[:4])
    
    js_content.append('')
    js_content.append(f'\t// [{idx}] {rule_name}: "{words}" x{count}')
    js_content.append(f'\ttry {{')
    js_content.append(f'\t\tHAction.GetDefault("AllReplace", HParameterSet.HFindReplace.HSet);')
    js_content.append(f'\t\twith (HParameterSet.HFindReplace) {{')
    js_content.append(f'\t\t\tFindString = "{esc_src}";')
    js_content.append(f'\t\t\tReplaceString = "{esc_dst}";')
    js_content.append(f'\t\t\tReplaceMode = 1;')
    js_content.append(f'\t\t}}')
    js_content.append(f'\t\tif (HAction.Execute("AllReplace", HParameterSet.HFindReplace.HSet)) {{')
    js_content.append(f'\t\t\ttotalChanges++;')
    js_content.append(f'\t\t}} else {{')
    js_content.append(f'\t\t\tskipped++;')
    js_content.append(f'\t\t}}')
    js_content.append(f'\t}} catch(e) {{')
    js_content.append(f'\t\tskipped++;')
    js_content.append(f'\t}}')
    
    log_lines.append(f"[{idx:3d}] ✅ '{src}' -> '{dst}' ({rule_name}) x{count}")
    
    idx += 1

js_content.append('')
js_content.append('\t// ===== 교정 완료 =====')
js_content.append('')
js_content.append('\tvar msg = "HWP 자동 교정 완료!\\n\\n";')
js_content.append('\tmsg += "적용: " + totalChanges + "건\\n";')
js_content.append('\tmsg += "스킵: " + skipped + "건\\n";')
js_content.append('\tmsg += "\\n총 " + (totalChanges + skipped) + "개 항목 처리됨";')
js_content.append('\talert(msg);')
js_content.append('}')

with open(macro_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(js_content))

log_lines.append(f"\n결과: {len(done_set)}개 항목 → JS 매크로 생성")
log_lines.append(f"매크로 파일: {macro_file}")
log_lines.append(f"\n=== 사용법 ===")
log_lines.append("1. 한컴오피스에서 대상 HWP 파일 열기")
log_lines.append("2. 도구 > 매크로 > 편집 (Alt+Shift+F11)")
log_lines.append("3. 이 매크로 내용 복사해서 붙여넣기")
log_lines.append("4. 도구 > 매크로 > 실행 (Alt+F8)")
log_lines.append("5. OnScriptMacro_Proofread 선택 후 [실행]")

with open(report_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines))

macro_size = os.path.getsize(macro_file)

print(f"\n{'='*60}")
print(f"✅ JS 매크로 생성 완료!")
print(f"{'='*60}")
print(f"\n📄 매크로 파일:")
print(f"   {macro_file}")
print(f"   크기: {round(macro_size/1024, 1)} KB")
print(f"   항목: {len(done_set)}건")
print(f"\n📋 사용법:")
print(f"   1. 한컴오피스에서 [{os.path.basename(SRC)}] 열기")
print(f"   2. 도구 > 매크로 > 편집 (Alt+Shift+F11)")
print(f"   3. 위 매크로 내용 전체 복사 > 붙여넣기")
print(f"   4. 도구 > 매크로 > 실행 (Alt+F8)")
print(f"   5. OnScriptMacro_Proofread 선택 > [실행]")
print(f"   6. 저장 (Ctrl+S)")
print(f"\n📝 리포트: {report_file}")
print(f"{'='*60}")
