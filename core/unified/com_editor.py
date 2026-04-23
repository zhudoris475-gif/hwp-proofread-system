# -*- coding: utf-8 -*-
import os, time, shutil, hashlib, subprocess

try:
    import win32com.client
    import pythoncom
    HAS_COM = True
except ImportError:
    HAS_COM = False


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


class COMEditor:
    def __init__(self, log_func=None):
        self.log = log_func or print
        self.hwp = None

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.log(f"[{ts}] {msg}")

    def open(self, filepath):
        if not HAS_COM:
            self._log("[오류] win32com 미설치")
            return False

        kill_hwp()
        pythoncom.CoInitialize()
        try:
            self.hwp = win32com.client.dynamic.Dispatch("HWPFrame.HwpObject")
            try:
                self.hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
            except Exception:
                pass
            try:
                self.hwp.SetMessageBoxMode(0x00020000)
            except Exception:
                pass
            self.hwp.Open(filepath, "HWP", "forceopen:true")
            self._log(f"파일 열기 성공: {filepath}")
            return True
        except Exception as e:
            self._log(f"COM 열기 오류: {e}")
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass
            return False

    def replace_all(self, src, dst):
        if not self.hwp:
            return False
        try:
            self.hwp.HAction.GetDefault("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)
            self.hwp.HParameterSet.HFindReplace.FindString = src
            self.hwp.HParameterSet.HFindReplace.ReplaceString = dst
            self.hwp.HParameterSet.HFindReplace.Direction = 0
            self.hwp.HParameterSet.HFindReplace.ReplaceMode = 0x0100
            self.hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
            self.hwp.HParameterSet.HFindReplace.FindType = 0
            result = self.hwp.HAction.Execute("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)
            return result
        except Exception as e:
            self._log(f"  [FAIL] '{src}' ({e})")
            return False

    def save(self, out_path):
        if not self.hwp:
            return False
        try:
            self.hwp.SaveAs(out_path, "HWP", "")
            self._log(f"SaveAs 성공: {out_path}")
            return True
        except Exception as e:
            self._log(f"SaveAs 메서드 오류: {e}")

        try:
            self.hwp.HAction.GetDefault("SaveAs", self.hwp.HParameterSet.HFileOpenSave.HSet)
            self.hwp.HParameterSet.HFileOpenSave.filename = out_path
            self.hwp.HParameterSet.HFileOpenSave.Format = "HWP"
            result = self.hwp.HAction.Execute("SaveAs", self.hwp.HParameterSet.HFileOpenSave.HSet)
            self._log(f"SaveAs Action 성공: {out_path}")
            return True
        except Exception as e:
            self._log(f"SaveAs Action 오류: {e}")

        return False

    def close(self):
        if self.hwp:
            try:
                self.hwp.Quit()
            except Exception:
                pass
            self.hwp = None
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

    def apply_rules(self, rules, label=""):
        applied = 0
        skipped = 0
        for item in rules:
            if len(item) == 3:
                src, dst, cnt = item
            elif len(item) == 4:
                src, dst, cat, cnt = item
            else:
                continue
            result = self.replace_all(src, dst)
            if result:
                applied += 1
                self._log(f"  [OK] '{src}' → '{dst}' ({cnt}건)")
            else:
                skipped += 1
            time.sleep(0.2)
        self._log(f"  적용: {applied}종, 건너뜀: {skipped}종")
        return applied, skipped

    def proofread_file(self, filepath, all_fixes, context_fixes=None, timestamp=""):
        if not os.path.exists(filepath):
            self._log(f"파일 없음: {filepath}")
            return False

        backup_path = filepath.replace(".hwp", f"_백업_{timestamp}.hwp")
        shutil.copy2(filepath, backup_path)
        self._log(f"백업: {backup_path}")

        if not self.open(filepath):
            return False

        try:
            applied, skipped = self.apply_rules(all_fixes)

            context_applied = 0
            if context_fixes:
                seen = set()
                for src, dst in context_fixes:
                    if src in seen:
                        continue
                    seen.add(src)
                    result = self.replace_all(src, dst)
                    if result:
                        context_applied += 1
                    time.sleep(0.2)
                self._log(f"  문맥띄어쓰기 적용: {context_applied}종")

            saved = self.save(filepath)
            if not saved:
                self._log("파일 저장 실패!")
                return False

            return True
        finally:
            self.close()
