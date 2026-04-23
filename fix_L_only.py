# -*- coding: utf-8 -*-
import sys, os, time, shutil, hashlib, re
from datetime import datetime

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

import win32com.client
import pythoncom

SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"
RULES_FILE = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"

NARA_RULES = [
    ("나라때", "조 때"), ("나라말기", "조 말기"), ("나라시기", "조 시기"),
    ("나라중기", "조 중기"), ("나라초기", "조 초기"),
]

SPACING_RULES = [
    ("고있다", "고 있다"), ("고있는", "고 있는"), ("고있었", "고 있었"),
    ("고있어", "고 있어"), ("고있겠", "고 있겠"), ("고있지", "고 있지"),
    ("고있고", "고 있고"), ("고있음", "고 있음"),
    ("해보다", "해 보다"), ("해본", "해 본"), ("해봐", "해 봐"),
    ("해봤", "해 봤"), ("해보려", "해 보려"), ("해보고", "해 보고"),
    ("살펴보다", "살펴 보다"), ("살펴본", "살펴 본"), ("살펴봐", "살펴 봐"),
    ("생각해보다", "생각해 보다"), ("생각해본", "생각해 본"), ("생각해봐", "생각해 봐"),
    ("먹어보다", "먹어 보다"), ("읽어보다", "읽어 보다"),
    ("흥정해본", "흥정해 본"), ("시탐해보다", "시탐해 보다"),
    ("조사해보다", "조사해 보다"), ("검사해보다", "검사해 보다"),
    ("역할따위", "역할 따위"), ("갈등따위", "갈등 따위"),
    ("넘어질번", "넘어질 번"), ("한번도", "한 번도"),
    ("한번은", "한 번은"), ("두번다시", "두 번 다시"),
    ("세번째", "세 번째"), ("첫번째", "첫 번째"), ("몇번", "몇 번"),
    ("수있다", "수 있다"), ("수있는", "수 있는"), ("수있었", "수 있었"),
    ("것같다", "것 같다"), ("것같은", "것 같은"), ("것같이", "것 같이"),
    ("척했다", "척했다"), ("척하는", "척하는"),
]

QUOTE_RULES = [
    ("\u201c", "\u2018"),
    ("\u201d", "\u2019"),
]

def load_rules(fpath):
    rules = []
    with open(fpath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" in line:
                parts = line.split("->")
                if len(parts) == 2:
                    src = parts[0].strip()
                    dst = parts[1].strip()
                    rules.append((src, dst))
    return rules

def kill_hwp():
    import subprocess
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(5)

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = rf"C:\Users\doris\Desktop\L파일_교정로그_{timestamp}.txt"

    china_rules = load_rules(RULES_FILE)

    text = extract_text_from_hwp_binary(SRC)
    print(f"원본 텍스트: {len(text):,}자")

    all_fixes = []

    for src, dst in NARA_RULES:
        cnt = text.count(src)
        if cnt > 0:
            all_fixes.append((src, dst, cnt, "나라→조"))

    for src, dst in china_rules:
        cnt = text.count(src)
        if cnt > 0:
            all_fixes.append((src, dst, cnt, "중한규칙"))

    for src, dst in SPACING_RULES:
        cnt = text.count(src)
        if cnt > 0:
            all_fixes.append((src, dst, cnt, "띄어쓰기"))

    for src, dst in QUOTE_RULES:
        cnt = text.count(src)
        if cnt > 0:
            all_fixes.append((src, dst, cnt, "따옴표"))

    print(f"수정 항목: {len(all_fixes)}종")
    for src, dst, cnt, cat in all_fixes:
        print(f"  [{cat}] '{src}' → '{dst}' ({cnt}건)")

    if not all_fixes:
        print("수정 불필요")
        return

    backup_path = SRC.replace(".hwp", f"_백업2_{timestamp}.hwp")
    shutil.copy2(SRC, backup_path)
    print(f"백업: {backup_path}")

    kill_hwp()
    pythoncom.CoInitialize()
    hwp = None
    try:
        hwp = win32com.client.dynamic.Dispatch("HWPFrame.HwpObject")
        try:
            hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        except Exception:
            pass
        try:
            hwp.SetMessageBoxMode(0x00020000)
        except Exception:
            pass

        hwp.Open(SRC, "HWP", "forceopen:true")
        print(f"파일 열기 성공")

        applied = 0
        skipped = 0

        for src, dst, cnt, cat in all_fixes:
            try:
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = src
                hwp.HParameterSet.HFindReplace.ReplaceString = dst
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 0x0100
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HParameterSet.HFindReplace.FindType = 0
                result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                if result:
                    applied += 1
                    print(f"  [OK] [{cat}] '{src}' → '{dst}' ({cnt}건)")
                else:
                    skipped += 1
                    print(f"  [SKIP] [{cat}] '{src}' → '{dst}'")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [FAIL] [{cat}] '{src}' ({e})")

        print(f"\n적용: {applied}종, 건너뜀: {skipped}종")

        out_path = SRC.replace(".hwp", f"_v2_{timestamp}.hwp")
        print(f"\n새 이름으로 저장: {out_path}")

        try:
            hwp.SaveAs(out_path, "HWP", "")
            print(f"SaveAs 메서드 성공")
        except Exception as e:
            print(f"SaveAs 메서드 오류: {e}")
            try:
                hwp.HAction.GetDefault("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
                hwp.HParameterSet.HFileOpenSave.filename = out_path
                hwp.HParameterSet.HFileOpenSave.Format = "HWP"
                result = hwp.HAction.Execute("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
                print(f"SaveAs Action 성공")
            except Exception as e2:
                print(f"SaveAs Action 오류: {e2}")

        try:
            hwp.Quit()
        except Exception:
            pass
        hwp = None

    except Exception as e:
        print(f"COM 오류: {e}")
        if hwp:
            try:
                hwp.Quit()
            except Exception:
                pass
        return
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

    time.sleep(3)

    if os.path.exists(out_path):
        new_text = extract_text_from_hwp_binary(out_path)
        print(f"\n교정 후 텍스트: {len(new_text):,}자")
        print(f"텍스트 변화: {len(new_text) - len(text):+,}자")

        remaining_nara = sum(1 for src, dst in NARA_RULES if new_text.count(src) > 0)
        remaining_spacing = sum(1 for src, dst in SPACING_RULES if new_text.count(src) > 0)
        remaining_quote_open = new_text.count('\u201c')
        remaining_quote_close = new_text.count('\u201d')

        print(f"잔여 나라→조: {remaining_nara}종")
        print(f"잔여 띄어쓰기: {remaining_spacing}종")
        print(f"잔여 따옴표: 열기={remaining_quote_open}, 닫기={remaining_quote_close}")

        if remaining_nara == 0 and remaining_spacing == 0 and remaining_quote_open == 0 and remaining_quote_close == 0:
            print("\n✅ L파일 모든 규칙 완전 적용!")
        else:
            print("\n⚠️ 일부 규칙 잔여")
    else:
        print(f"\n❌ 출력 파일 없음: {out_path}")

if __name__ == "__main__":
    main()
