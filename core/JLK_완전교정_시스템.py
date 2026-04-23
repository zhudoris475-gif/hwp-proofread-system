# -*- coding: utf-8 -*-
import sys, os, io, time, shutil, subprocess, hashlib, re, json
from datetime import datetime

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

import win32com.client
import pythoncom

FILES = {
    "J": {
        "orig": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp",
        "work": r"C:\Users\doris\Desktop\J_spacing_fixed.hwp",
    },
    "L": {
        "orig": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp",
        "work": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp",
    },
    "K": {
        "orig": r"C:\Users\doris\Desktop\新词典\【大中朝 15】K 1694-1786--93--20240920.hwp",
        "work": r"C:\Users\doris\Desktop\xwechat_files\WORD\K 1694-1786--93--20240920_교정본_상세로그_20260418_재실행_작업본_최근규칙_작업본_20260418_3차.hwp",
    },
}

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

def file_md5(fpath):
    h = hashlib.md5()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

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
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(5)

class JLKProofreader:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = rf"C:\Users\doris\Desktop\JLK_완전교정_상세로그_{self.timestamp}.txt"
        self.log_fh = None
        self.china_rules = load_rules(RULES_FILE)
        self.all_results = {}

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        if self.log_fh:
            try:
                self.log_fh.write(line + "\n")
                self.log_fh.flush()
            except Exception:
                pass

    def com_replace_all(self, hwp, src, dst):
        try:
            hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
            hwp.HParameterSet.HFindReplace.FindString = src
            hwp.HParameterSet.HFindReplace.ReplaceString = dst
            hwp.HParameterSet.HFindReplace.Direction = 0
            hwp.HParameterSet.HFindReplace.ReplaceMode = 0x0100
            hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
            hwp.HParameterSet.HFindReplace.FindType = 0
            result = hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
            return result
        except Exception as e:
            self.log(f"    [FAIL] '{src}' ({e})")
            return False

    def com_save(self, hwp, out_path):
        try:
            hwp.SaveAs(out_path, "HWP", "")
            self.log(f"  SaveAs 메서드 성공: {out_path}")
            return True
        except Exception as e:
            self.log(f"  SaveAs 메서드 오류: {e}")

        try:
            hwp.HAction.GetDefault("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
            hwp.HParameterSet.HFileOpenSave.filename = out_path
            hwp.HParameterSet.HFileOpenSave.Format = "HWP"
            result = hwp.HAction.Execute("SaveAs", hwp.HParameterSet.HFileOpenSave.HSet)
            self.log(f"  SaveAs Action 성공: {out_path}")
            return True
        except Exception as e:
            self.log(f"  SaveAs Action 오류: {e}")

        return False

    def analyze_before(self, label, fpath):
        text = extract_text_from_hwp_binary(fpath)
        cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
        cn_words = cn_pattern.findall(text)

        nara_needed = []
        for src, dst in NARA_RULES:
            cnt = text.count(src)
            if cnt > 0:
                nara_needed.append((src, dst, cnt))

        spacing_needed = []
        for src, dst in SPACING_RULES:
            cnt = text.count(src)
            if cnt > 0:
                spacing_needed.append((src, dst, cnt))

        quote_needed = []
        for src, dst in QUOTE_RULES:
            cnt = text.count(src)
            if cnt > 0:
                quote_needed.append((src, dst, cnt))

        china_needed = []
        for src, dst in self.china_rules:
            cnt = text.count(src)
            if cnt > 0:
                china_needed.append((src, dst, cnt))

        return {
            "text_len": len(text),
            "cn_total": len(cn_words),
            "nara_needed": nara_needed,
            "spacing_needed": spacing_needed,
            "quote_needed": quote_needed,
            "china_needed": china_needed,
        }

    def proofread_file(self, label, work_path):
        self.log(f"\n{'=' * 70}")
        self.log(f"  [{label}파일] 완전교정 시작")
        self.log(f"{'=' * 70}")

        if not os.path.exists(work_path):
            self.log(f"  파일 없음: {work_path}")
            return None

        backup_path = work_path.replace(".hwp", f"_백업_{self.timestamp}.hwp")
        shutil.copy2(work_path, backup_path)
        backup_md5 = file_md5(backup_path)
        self.log(f"  백업: {backup_path} (MD5={backup_md5[:8]})")

        before = self.analyze_before(label, work_path)
        self.log(f"  교정 전 텍스트: {before['text_len']:,}자")
        self.log(f"  교정 전 한자: {before['cn_total']:,}개")
        self.log(f"  나라→조 필요: {len(before['nara_needed'])}종")
        self.log(f"  띄어쓰기 필요: {len(before['spacing_needed'])}종")
        self.log(f"  따옴표 필요: {len(before['quote_needed'])}종")
        self.log(f"  중한규칙 필요: {len(before['china_needed'])}종")

        all_fixes = []
        all_fixes.extend(before['nara_needed'])
        all_fixes.extend(before['china_needed'])
        all_fixes.extend(before['spacing_needed'])
        all_fixes.extend(before['quote_needed'])

        if not all_fixes:
            self.log(f"  수정 불필요 - 모든 규칙 이미 적용됨")
            self.all_results[label] = {"status": "no_change", "before": before, "after": before}
            return before

        self.log(f"\n  총 수정 항목: {len(all_fixes)}종")

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

            hwp.Open(work_path, "HWP", "forceopen:true")
            self.log(f"  파일 열기 성공")

            applied = 0
            skipped = 0
            failed = 0

            for src, dst, cnt in all_fixes:
                result = self.com_replace_all(hwp, src, dst)
                if result:
                    applied += 1
                    self.log(f"    [OK] '{src}' → '{dst}' ({cnt}건)")
                else:
                    skipped += 1
                    self.log(f"    [SKIP] '{src}' → '{dst}'")
                time.sleep(0.2)

            self.log(f"\n  적용: {applied}종, 건너뜀: {skipped}종, 실패: {failed}종")

            saved = self.com_save(hwp, work_path)
            if not saved:
                self.log(f"  ❌ 파일 저장 실패!")
                return before

            try:
                hwp.Quit()
            except Exception:
                pass
            hwp = None

        except Exception as e:
            self.log(f"  COM 오류: {e}")
            if hwp:
                try:
                    hwp.Quit()
                except Exception:
                    pass
            return before
        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass

        time.sleep(3)

        after = self.analyze_after(label, work_path)
        self.log(f"\n  교정 후 텍스트: {after['text_len']:,}자")
        self.log(f"  교정 후 한자: {after['cn_total']:,}개")

        remaining_nara = sum(1 for src, dst in NARA_RULES if after['text'].count(src) > 0)
        remaining_spacing = sum(1 for src, dst in SPACING_RULES if after['text'].count(src) > 0)
        remaining_quote_open = after['text'].count('\u201c')
        remaining_quote_close = after['text'].count('\u201d')

        self.log(f"\n  잔여 나라→조: {remaining_nara}종")
        self.log(f"  잔여 띄어쓰기: {remaining_spacing}종")
        self.log(f"  잔여 따옴표: 열기={remaining_quote_open}, 닫기={remaining_quote_close}")

        self.all_results[label] = {
            "status": "completed",
            "before": before,
            "after": after,
            "applied": applied,
            "skipped": skipped,
            "remaining_nara": remaining_nara,
            "remaining_spacing": remaining_spacing,
            "remaining_quote_open": remaining_quote_open,
            "remaining_quote_close": remaining_quote_close,
        }

        return after

    def analyze_after(self, label, fpath):
        text = extract_text_from_hwp_binary(fpath)
        cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
        cn_words = cn_pattern.findall(text)

        return {
            "text_len": len(text),
            "cn_total": len(cn_words),
            "text": text,
        }

    def generate_final_report(self):
        self.log(f"\n\n{'=' * 70}")
        self.log(f"  JLK 세파일 완전교정 최종 보고서")
        self.log(f"{'=' * 70}")
        self.log(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"  Git 사용자: zhudoris475-gif <zhudoris475@gmail.com>")
        self.log(f"")

        for label, result in self.all_results.items():
            self.log(f"\n  [{label}파일]")
            self.log(f"  {'-' * 50}")

            if result['status'] == 'no_change':
                self.log(f"    상태: 수정 불필요 (이미 모든 규칙 적용됨)")
                self.log(f"    텍스트: {result['before']['text_len']:,}자")
                self.log(f"    한자: {result['before']['cn_total']:,}개")
                continue

            before = result['before']
            self.log(f"    교정 전 텍스트: {before['text_len']:,}자")
            self.log(f"    교정 전 한자: {before['cn_total']:,}개")
            self.log(f"    나라→조 필요: {len(before['nara_needed'])}종")
            self.log(f"    띄어쓰기 필요: {len(before['spacing_needed'])}종")
            self.log(f"    따옴표 필요: {len(before['quote_needed'])}종")
            self.log(f"    중한규칙 필요: {len(before['china_needed'])}종")

            self.log(f"")
            self.log(f"    적용: {result['applied']}종")
            self.log(f"    건너뜀: {result['skipped']}종")
            self.log(f"    잔여 나라→조: {result['remaining_nara']}종")
            self.log(f"    잔여 띄어쓰기: {result['remaining_spacing']}종")
            self.log(f"    잔여 따옴표: 열기={result['remaining_quote_open']}, 닫기={result['remaining_quote_close']}")

            after = result['after']
            self.log(f"    교정 후 텍스트: {after['text_len']:,}자")
            self.log(f"    교정 후 한자: {after['cn_total']:,}개")

            text_diff = after['text_len'] - before['text_len']
            cn_diff = after['cn_total'] - before['cn_total']
            self.log(f"    텍스트 변화: {text_diff:+,}자")
            self.log(f"    한자 변화: {cn_diff:+,}개")

        self.log(f"\n\n  최종 판정")
        self.log(f"  {'-' * 50}")

        all_ok = True
        for label, result in self.all_results.items():
            if result['status'] == 'no_change':
                continue
            if result['remaining_nara'] > 0:
                self.log(f"  ⚠️ [{label}] 나라→조 {result['remaining_nara']}종 남음")
                all_ok = False
            if result['remaining_spacing'] > 0:
                self.log(f"  ⚠️ [{label}] 띄어쓰기 {result['remaining_spacing']}종 남음")
                all_ok = False
            if result['remaining_quote_open'] > 0 or result['remaining_quote_close'] > 0:
                self.log(f"  ⚠️ [{label}] 따옴표 열기={result['remaining_quote_open']}, 닫기={result['remaining_quote_close']} 남음")
                all_ok = False

        if all_ok:
            self.log(f"  ✅ 세파일 모든 규칙 완전 적용 확인!")
        else:
            self.log(f"  ⚠️ 일부 규칙 잔여 - COM 방식 한계로 수동 확인 필요")

    def run(self):
        self.log_fh = open(self.log_path, "w", encoding="utf-8")
        self.log(f"JLK 세파일 완전교정 시스템")
        self.log(f"시작일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Git 사용자: zhudoris475-gif <zhudoris475@gmail.com>")
        self.log(f"규칙파일: {RULES_FILE}")
        self.log(f"중한규칙: {len(self.china_rules)}개")
        self.log(f"나라→조 규칙: {len(NARA_RULES)}개")
        self.log(f"띄어쓰기 규칙: {len(SPACING_RULES)}개")
        self.log(f"따옴표 규칙: {len(QUOTE_RULES)}개")

        try:
            for label, paths in FILES.items():
                work_path = paths["work"]
                self.proofread_file(label, work_path)

            self.generate_final_report()

        except Exception as e:
            self.log(f"시스템 오류: {e}")
        finally:
            self.log(f"\n완료일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.log_fh.close()

        print(f"\n상세로그 저장: {self.log_path}")
        return self.log_path

if __name__ == "__main__":
    proofreader = JLKProofreader()
    proofreader.run()
