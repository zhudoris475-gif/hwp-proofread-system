import zipfile
import xml.etree.ElementTree as ET
import shutil
import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class HWPWriter:
    HWPX_NS = "http://www.hancom.co.kr/hwpml/2011/paragraph"

    def __init__(self, backup: bool = True):
        self.backup = backup

    def save(
        self,
        original_path: str,
        corrected_text: str,
        output_path: Optional[str] = None,
        corrections: Optional[list] = None,
    ) -> Dict[str, Any]:
        path = Path(original_path)
        ext = path.suffix.lower()

        if ext == ".hwpx":
            return self._save_hwpx(path, corrected_text, output_path, corrections)
        elif ext == ".hwp":
            return self._save_hwp(str(path), corrected_text, output_path)
        else:
            return {"success": False, "error": f"지원하지 않는 형식: {ext}"}

    def _save_hwpx(
        self,
        original_path: Path,
        corrected_text: str,
        output_path: Optional[str],
        corrections: Optional[list],
    ) -> Dict[str, Any]:
        try:
            if output_path:
                out = Path(output_path)
            else:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                out = original_path.parent / f"{original_path.stem}_corrected_{timestamp}{original_path.suffix}"

            if self.backup:
                self._create_backup(original_path)

            shutil.copy2(str(original_path), str(out))

            paragraphs = corrected_text.split("\n")

            zf = zipfile.ZipFile(str(original_path), "r")
            section_files = sorted(
                [n for n in zf.namelist() if n.startswith("Contents/section") and n.endswith(".xml")]
            )
            zf.close()

            if section_files and corrections:
                self._apply_hwpx_corrections(str(out), corrections)

            return {"success": True, "output_file": str(out), "format": "hwpx"}
        except Exception as e:
            return {"success": False, "error": f"HWPX 저장 오류: {e}"}

    def _apply_hwpx_corrections(self, hwpx_path: str, corrections: list):
        try:
            import tempfile
            import os

            temp_dir = tempfile.mkdtemp()
            zf = zipfile.ZipFile(hwpx_path, "r")
            zf.extractall(temp_dir)
            zf.close()

            section_files = sorted(
                [f for f in Path(temp_dir, "Contents").glob("section*.xml")]
            )

            for section_file in section_files:
                content = section_file.read_text(encoding="utf-8")
                modified = content
                for corr in corrections:
                    if corr.get("type") == "replace":
                        src = corr["original"]
                        dst = corr["corrected"]
                        if src in modified:
                            modified = modified.replace(src, dst)
                section_file.write_text(modified, encoding="utf-8")

            out_zf = zipfile.ZipFile(hwpx_path, "w", zipfile.ZIP_DEFLATED)
            for root_dir, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    out_zf.write(file_path, arcname)
            out_zf.close()

            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

    def _save_hwp(
        self,
        original_path: str,
        corrected_text: str,
        output_path: Optional[str],
    ) -> Dict[str, Any]:
        try:
            import win32com.client as win32

            if output_path:
                out = Path(output_path)
            else:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                p = Path(original_path)
                out = p.parent / f"{p.stem}_corrected_{timestamp}{p.suffix}"

            if self.backup:
                self._create_backup(Path(original_path))

            hwp = win32.Dispatch("HwpBasic.HwpObject")
            try:
                hwp.Open(str(original_path))
                hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.HParameterSet.HFindReplace.FindString = hwp.GetTextFile("TEXT", "")
                hwp.HParameterSet.HFindReplace.ReplaceString = corrected_text
                hwp.HParameterSet.HFindReplace.Direction = 0
                hwp.HParameterSet.HFindReplace.ReplaceMode = 2
                hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
                hwp.SaveAs(str(out))
            finally:
                try:
                    hwp.Close(0)
                except Exception:
                    pass

            return {"success": True, "output_file": str(out), "format": "hwp-com"}
        except ImportError:
            return {"success": False, "error": "HWP 파일 쓰기는 win32com이 필요합니다. 한글 프로그램을 설치하세요."}
        except Exception as e:
            return {"success": False, "error": f"HWP 저장 오류: {e}"}

    def _create_backup(self, original_path: Path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = original_path.parent / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / f"{original_path.stem}_backup_{timestamp}{original_path.suffix}"
        shutil.copy2(str(original_path), str(backup_path))
