# -*- coding: utf-8 -*-
import sys, os, time, re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")

TARGET_FILE = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
OUTPUT_DIR = r"C:\Users\doris\Desktop\xwechat_files\WORD"
REPORT_DIR = os.path.join(OUTPUT_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

try:
    import win32com.client
    import pythoncom
except ImportError:
    print("❌ win32com 필요")
    sys.exit(1)

print("=" * 60)
print("🔧 HWP COM 교정 - 한컴오피스 직접 수정 방식")
print("=" * 60)
print(f" 대상: {os.path.basename(TARGET_FILE)}")

pythoncom.CoInitialize()

try:
    hwp = win32com.client.DispatchEx("HWPFrame.HwpObject", clsctx=4)
    print("✅ 한컴오피스 COM 연결 성공!")
    
    hwp.SetMessageBoxMode(0x00020000)
    try:
        hwp.Visible = False
    except:
        pass
    
    hwp.Open(TARGET_FILE, "HWP", "")
    time.sleep(1)
    
    total_chars = hwp.GetLineCount()
    total_len = 0
    
    text_parts = []
    for i in range(1, min(total_chars + 1, 50000)):
        try:
            line_text = hwp.GetTextByLine(i)
            if line_text:
                text_parts.append(line_text)
                total_len += len(line_text)
        except:
            break
    
    full_text = '\n'.join(text_parts)
    
    print(f"\n 📄 텍스트 추출:")
    print(f"   줄 수: {len(text_parts)}")
    print(f"   총 길이: {total_len}자")
    print(f"   미리보기: {full_text[:150]}...")
    
    from proofread import (
        collect_chinese_korean_corrections,
        collect_txt_corrections,
        collect_middle_dot_corrections,
        collect_quote_corrections,
    )
    
    config_dir = r"C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config"
    
    corrections = []
    
    try:
        ck = collect_chinese_korean_corrections(full_text, config_dir)
        corrections.extend(ck)
        print(f"\n ✅ 중한규칙: {len(ck)}개")
    except Exception as e:
        print(f" ⚠️ 중한규칙: {e}")
    
    try:
        txt = collect_txt_corrections(full_text, config_dir)
        corrections.extend(txt)
        print(f" ✅ TXT규칙: {len(txt)}개")
    except Exception as e:
        print(f" ⚠️ TXT규칙: {e}")
    
    try:
        md = collect_middle_dot_corrections(full_text, config_dir)
        corrections.extend(md)
        print(f" ✅ 가운데점: {len(md)}개")
    except Exception as e:
        print(f" ⚠️ 가운데점: {e}")
    
    try:
        qt = collect_quote_corrections(full_text, config_dir)
        corrections.extend(qt)
        print(f" ✅ 따옴표: {len(qt)}개")
    except Exception as e:
        print(f" ⚠️ 따옴표: {e}")
    
    print(f"\n 📊 총 교정 후보: {len(corrections)}개")
    
    if not corrections:
        print("   → 교정 항목 없음, 저장 없음")
        hwp.Close()
        hwp = None
        sys.exit(0)
    
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_name = f"【20】O 2179-2182排版页数4-金花顺_COM교정본_{ts}.hwp"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    
    applied = 0
    skipped = 0
    
    log_lines = []
    log_lines.append(f"{'='*60}")
    log_lines.append(f"HWP COM 교정 결과")
    log_lines.append(f"파일: {out_path}")
    log_lines.append(f"시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"{'='*60}\n")
    
    for src, dst, rule_name, count in corrections:
        if full_text.count(src) > 0:
            try:
                result = hwp.Replace(src, dst, 0, 0, 0, 0, 0, 0)
                
                if result:
                    applied += 1
                    status = "✅ 적용"
                    words = re.findall(r"[\uac00-\ud7af\u1100-\u11ff\u3130-\u318fA-Za-z0-9]+", src)[:4]
                    log_lines.append(f"[{status}] '{src}' -> '{dst}' ({rule_name})")
                    log_lines.append(f"         단어: {' '.join(words)}")
                else:
                    skipped += 1
                    log_lines.append(f"[⏭️ 건너뜀] '{src}' (찾지 못함 또는 이미 변경됨)")
            except Exception as e:
                skipped += 1
                log_lines.append(f"[❌ 오류] '{src}' -> {e}")
        else:
            skipped += 1
    
    hwp.SaveAs(out_path, "HWP", "")
    time.sleep(0.5)
    
    log_lines.append(f"\n{'='*60}")
    log_lines.append(f"결과: {applied}건 적용 / {skipped}건 스킵")
    log_lines.append(f"출력: {out_path}")
    log_lines.append(f"{'='*60}")
    
    report_name = f"O_COM_교정결과_{ts}.txt"
    report_path = os.path.join(REPORT_DIR, report_name)
    
    with open(report_path, 'w', encoding='utf-8') as lf:
        lf.write('\n'.join(log_lines))
    
    print(f"\n{'='*60}")
    print(f"✅ COM 교정 완료!")
    print(f"   적용: {applied}건 | 스킵: {skipped}건")
    print(f"   출력: {out_path}")
    print(f"   리포트: {report_path}")
    print(f"{'='*60}")
    
    hwp.Close()
    hwp = None

except Exception as e:
    print(f"\n❌ 오류: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        pythoncom.CoUninitialize()
    except:
        pass
