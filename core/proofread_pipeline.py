# -*- coding: utf-8 -*-
import os, sys, io, time, shutil, subprocess, hashlib, json, re
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

import win32com.client
import pythoncom

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PIPELINE_DIR, "logs")
BACKUP_DIR = os.path.join(PIPELINE_DIR, "backups")
SNAPSHOT_DIR = os.path.join(PIPELINE_DIR, "snapshots")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

NARA_RULES = [
    ("省", ""), ("市", ""), ("县", ""), ("区", ""),
    ("镇", ""), ("乡", ""), ("村", ""),
]

NARA_RULES_FROM_FILE = []

SPACING_RULES = [
    ("고있다", "고 있다"), ("고있는", "고 있는"), ("고있었", "고 있었"),
    ("고있겠", "고 있겠"), ("고있지", "고 있지"), ("고있고", "고 있고"),
    ("고있어", "고 있어"), ("고있음", "고 있음"),
    ("해보다", "해 보다"), ("해본", "해 본"), ("해봐", "해 봐"),
    ("살펴보다", "살펴 보다"), ("생각해보다", "생각해 보다"),
    ("생각해봐", "생각해 봐"), ("먹어보다", "먹어 보다"),
    ("읽어보다", "읽어 보다"), ("흥정해본", "흥정해 본"),
    ("시탐해보다", "시탐해 보다"), ("조사해보다", "조사해 보다"),
    ("검사해보다", "검사해 보다"),
    ("역할따위", "역할 따위"), ("갈등따위", "갈등 따위"),
    ("넘어질번", "넘어질 번"), ("한번도", "한 번도"),
    ("한번은", "한 번은"), ("두번다시", "두 번 다시"),
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

def kill_hwp():
    try:
        subprocess.run(["powershell", "-Command",
            "Stop-Process -Name 'Hwp' -Force -ErrorAction SilentlyContinue; "
            "Stop-Process -Name 'HwpApi' -Force -ErrorAction SilentlyContinue"],
            timeout=10)
    except Exception:
        pass
    time.sleep(5)

def load_nara_rules_from_file():
    global NARA_RULES_FROM_FILE
    rules_path = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"
    if not os.path.exists(rules_path):
        return
    with open(rules_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" in line:
                parts = line.split("->")
                if len(parts) == 2:
                    src = parts[0].strip()
                    dst = parts[1].strip()
                    NARA_RULES_FROM_FILE.append((src, dst))

load_nara_rules_from_file()

class ProofreadPipeline:
    def __init__(self, input_path, output_path=None):
        self.input_path = input_path
        self.output_path = output_path or input_path
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(LOG_DIR, f"pipeline_{self.timestamp}.log")
        self.snapshot_base = os.path.join(SNAPSHOT_DIR, self.timestamp)
        os.makedirs(self.snapshot_base, exist_ok=True)
        self.log_fh = None
        self.steps = []
        self.results = []

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

    def snapshot(self, label):
        ext = os.path.splitext(self.input_path)[1]
        snap_path = os.path.join(self.snapshot_base, f"{label}{ext}")
        shutil.copy2(self.input_path, snap_path)
        md5 = file_md5(snap_path)
        self.log(f"스냅샷: {label} → {snap_path} (MD5={md5[:8]})")
        return snap_path, md5

    def extract_text(self, fpath):
        return extract_text_from_hwp_binary(fpath)

    def step_backup(self):
        self.log(f"\n{'=' * 60}")
        self.log(f"STEP 0: 원본 백업")
        self.log(f"{'=' * 60}")

        backup_path = os.path.join(BACKUP_DIR, f"original_{self.timestamp}.hwp")
        shutil.copy2(self.input_path, backup_path)
        md5 = file_md5(backup_path)
        self.log(f"백업: {backup_path} (MD5={md5})")

        text = self.extract_text(self.input_path)
        self.log(f"원본 텍스트: {len(text):,}자")

        cn = re.findall(r'[\u4e00-\u9fff]+', text)
        self.log(f"원본 한자: {len(cn):,}개")

        self.results.append({
            "step": "backup",
            "backup_path": backup_path,
            "md5": md5,
            "text_len": len(text),
            "cn_count": len(cn),
        })

        return True

    def step_nara(self):
        self.log(f"\n{'=' * 60}")
        self.log(f"STEP 1: 나라→조 규칙 적용")
        self.log(f"{'=' * 60}")

        text = self.extract_text(self.input_path)

        all_rules = NARA_RULES + NARA_RULES_FROM_FILE
        needed = []
        for src, dst in all_rules:
            cnt = text.count(src)
            if cnt > 0:
                needed.append((src, dst, cnt))
                self.log(f"  '{src}' → '{dst}' ({cnt}건)")

        if not needed:
            self.log("수정 불필요")
            self.results.append({"step": "nara", "applied": 0, "total": 0})
            return True

        self.log(f"총 {len(needed)}종 수정")

        kill_hwp()
        pythoncom.CoInitialize()
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

            hwp.Open(self.input_path, "HWP", "forceopen:true")
            self.log("파일 열기 성공")

            applied = 0
            for src, dst, cnt in needed:
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
                        self.log(f"  [OK] '{src}' → '{dst}'")
                    else:
                        self.log(f"  [SKIP] '{src}' → '{dst}'")
                    time.sleep(0.2)
                except Exception as e:
                    self.log(f"  [FAIL] '{src}' ({e})")

            out_path = self.output_path if self.output_path != self.input_path else self.input_path
            try:
                hwp.SaveAs(out_path, "HWP", "")
                self.log(f"저장 성공: {out_path}")
            except Exception as e:
                self.log(f"SaveAs 오류: {e}")

            try:
                hwp.Quit()
            except Exception:
                pass

            self.results.append({
                "step": "nara",
                "applied": applied,
                "total": len(needed),
            })

            return applied > 0

        except Exception as e:
            self.log(f"COM 오류: {e}")
            try:
                hwp.Quit()
            except Exception:
                pass
            return False
        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass

    def step_spacing(self):
        self.log(f"\n{'=' * 60}")
        self.log(f"STEP 2: 띄어쓰기 규칙 적용")
        self.log(f"{'=' * 60}")

        text = self.extract_text(self.input_path)

        needed = []
        for src, dst in SPACING_RULES:
            cnt = text.count(src)
            if cnt > 0:
                needed.append((src, dst, cnt))
                self.log(f"  '{src}' → '{dst}' ({cnt}건)")

        if not needed:
            self.log("수정 불필요")
            self.results.append({"step": "spacing", "applied": 0, "total": 0})
            return True

        self.log(f"총 {len(needed)}종 수정")

        kill_hwp()
        pythoncom.CoInitialize()
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

            hwp.Open(self.input_path, "HWP", "forceopen:true")
            self.log("파일 열기 성공")

            applied = 0
            for src, dst, cnt in needed:
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
                        self.log(f"  [OK] '{src}' → '{dst}'")
                    else:
                        self.log(f"  [SKIP] '{src}' → '{dst}'")
                    time.sleep(0.2)
                except Exception as e:
                    self.log(f"  [FAIL] '{src}' ({e})")

            out_path = self.output_path if self.output_path != self.input_path else self.input_path
            try:
                hwp.SaveAs(out_path, "HWP", "")
                self.log(f"저장 성공: {out_path}")
            except Exception as e:
                self.log(f"SaveAs 오류: {e}")

            try:
                hwp.Quit()
            except Exception:
                pass

            self.results.append({
                "step": "spacing",
                "applied": applied,
                "total": len(needed),
            })

            return applied > 0

        except Exception as e:
            self.log(f"COM 오류: {e}")
            try:
                hwp.Quit()
            except Exception:
                pass
            return False
        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass

    def step_quotes(self):
        self.log(f"\n{'=' * 60}")
        self.log(f"STEP 3: 따옴표 규칙 적용")
        self.log(f"{'=' * 60}")

        text = self.extract_text(self.input_path)

        needed = []
        for src, dst in QUOTE_RULES:
            cnt = text.count(src)
            if cnt > 0:
                needed.append((src, dst, cnt))
                self.log(f"  U+{ord(src):04X} → U+{ord(dst):04X} ({cnt}건)")

        if not needed:
            self.log("수정 불필요")
            self.results.append({"step": "quotes", "applied": 0, "total": 0})
            return True

        kill_hwp()
        pythoncom.CoInitialize()
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

            hwp.Open(self.input_path, "HWP", "forceopen:true")
            self.log("파일 열기 성공")

            applied = 0
            for src, dst, cnt in needed:
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
                        self.log(f"  [OK] U+{ord(src):04X} → U+{ord(dst):04X}")
                    else:
                        self.log(f"  [SKIP] U+{ord(src):04X} → U+{ord(dst):04X}")
                    time.sleep(0.2)
                except Exception as e:
                    self.log(f"  [FAIL] U+{ord(src):04X} ({e})")

            out_path = self.output_path if self.output_path != self.input_path else self.input_path
            try:
                hwp.SaveAs(out_path, "HWP", "")
                self.log(f"저장 성공: {out_path}")
            except Exception as e:
                self.log(f"SaveAs 오류: {e}")

            try:
                hwp.Quit()
            except Exception:
                pass

            self.results.append({
                "step": "quotes",
                "applied": applied,
                "total": len(needed),
            })

            return applied > 0

        except Exception as e:
            self.log(f"COM 오류: {e}")
            try:
                hwp.Quit()
            except Exception:
                pass
            return False
        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass

    def step_verify(self):
        self.log(f"\n{'=' * 60}")
        self.log(f"STEP 4: 최종 검증")
        self.log(f"{'=' * 60}")

        text = self.extract_text(self.input_path)
        self.log(f"교정 텍스트: {len(text):,}자")

        cn = re.findall(r'[\u4e00-\u9fff]+', text)
        self.log(f"한자: {len(cn):,}개")

        all_ok = True

        for src, dst in NARA_RULES:
            cnt = text.count(src)
            if cnt > 0 and dst == "":
                self.log(f"  ⚠️ 나라→조 '{src}' {cnt}건 남음")
                all_ok = False

        for src, dst in SPACING_RULES:
            cnt = text.count(src)
            if cnt > 0:
                self.log(f"  ⚠️ 띄어쓰기 '{src}' {cnt}건 남음")
                all_ok = False

        if all_ok:
            self.log("✅ 모든 규칙 적용 완료!")

        self.results.append({
            "step": "verify",
            "text_len": len(text),
            "cn_count": len(cn),
            "all_ok": all_ok,
        })

        return all_ok

    def run(self, steps=None):
        self.log_fh = open(self.log_path, "w", encoding="utf-8")
        self.log(f"HWP 교정 파이프라인 시작")
        self.log(f"입력: {self.input_path}")
        self.log(f"출력: {self.output_path}")
        self.log(f"시간: {self.timestamp}")

        if steps is None:
            steps = ["backup", "nara", "spacing", "quotes", "verify"]

        try:
            for step in steps:
                if step == "backup":
                    self.step_backup()
                elif step == "nara":
                    self.step_nara()
                elif step == "spacing":
                    self.step_spacing()
                elif step == "quotes":
                    self.step_quotes()
                elif step == "verify":
                    self.step_verify()
        except Exception as e:
            self.log(f"파이프라인 오류: {e}")
        finally:
            self.log(f"\n{'=' * 60}")
            self.log(f"파이프라인 완료")
            self.log(f"결과: {json.dumps(self.results, ensure_ascii=False, indent=2)}")
            self.log_fh.close()

        return self.results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python proofread_pipeline.py <입력.hwp> [출력.hwp]")
        print("  steps: backup, nara, spacing, quotes, verify")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    pipeline = ProofreadPipeline(input_path, output_path)
    results = pipeline.run()

    print(f"\n결과 요약:")
    for r in results:
        print(f"  {r}")
