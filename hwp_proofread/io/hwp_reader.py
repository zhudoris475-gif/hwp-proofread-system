import zipfile
import xml.etree.ElementTree as ET
import os
import struct
import zlib
from pathlib import Path
from typing import Optional, Dict, Any, List


class HWPReader:
    HWPX_NS = "http://www.hancom.co.kr/hwpml/2011/paragraph"

    def __init__(self):
        self._text_cache: Dict[str, str] = {}

    def read(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            return {"success": False, "error": f"파일을 찾을 수 없습니다: {file_path}"}

        ext = path.suffix.lower()
        if ext == ".hwpx":
            return self._read_hwpx(path)
        elif ext == ".hwp":
            return self._read_hwp(path)
        else:
            return {"success": False, "error": f"지원하지 않는 형식: {ext}"}

    def _read_hwpx(self, path: Path) -> Dict[str, Any]:
        try:
            zf = zipfile.ZipFile(str(path), "r")
            paragraphs = []
            section_count = 0

            section_files = sorted(
                [n for n in zf.namelist() if n.startswith("Contents/section") and n.endswith(".xml")]
            )

            for section_file in section_files:
                section_count += 1
                content = zf.read(section_file).decode("utf-8")
                root = ET.fromstring(content)
                ns = self.HWPX_NS

                for p in root.iter(f"{{{ns}}}p"):
                    para_text = []
                    for t_elem in p.iter(f"{{{ns}}}t"):
                        if t_elem.text:
                            para_text.append(t_elem.text)
                    if para_text:
                        paragraphs.append("".join(para_text))

            preview_text = ""
            try:
                preview_text = zf.read("Preview/PrvText.txt").decode("utf-8")
            except Exception:
                pass

            zf.close()

            full_text = "\n".join(paragraphs)
            return {
                "success": True,
                "format": "hwpx",
                "text": full_text,
                "paragraphs": paragraphs,
                "section_count": section_count,
                "preview_text": preview_text,
                "analysis": self._analyze(full_text),
            }
        except Exception as e:
            return {"success": False, "error": f"HWPX 읽기 오류: {e}"}

    def _read_hwp(self, path: Path) -> Dict[str, Any]:
        try:
            texts = self._extract_hwp_binary(str(path))
            if not texts:
                return self._read_hwp_fallback(str(path))
            full_text = "\n\n".join(texts)
            paragraphs = []
            for section_text in texts:
                paragraphs.extend(section_text.split("\n"))
            return {
                "success": True,
                "format": "hwp",
                "text": full_text,
                "paragraphs": [p for p in paragraphs if p.strip()],
                "section_count": len(texts),
                "analysis": self._analyze(full_text),
            }
        except Exception as e:
            return self._read_hwp_fallback(str(path))

    def _extract_hwp_binary(self, path: str) -> List[str]:
        try:
            import olefile
        except ImportError:
            return []

        ole = olefile.OleFileIO(path, write_mode=False)
        texts = []
        try:
            streams = ole.listdir()
            body_streams = sorted(
                [s for s in streams if s and s[0] == "BodyText"],
                key=lambda s: int(s[1]) if len(s) > 1 and s[1].isdigit() else 0,
            )
            for stream_path in body_streams:
                stream_name = "/".join(stream_path)
                raw = ole.openstream(stream_name).read()
                dec = self._decompress_chain(raw)
                if dec is None:
                    continue
                records = self._parse_records(dec)
                parts = []
                for rec in records:
                    if rec.get("tag_id") == 67:
                        try:
                            parts.append(rec["payload"].decode("utf-16-le", errors="replace"))
                        except Exception:
                            continue
                if parts:
                    texts.append("".join(parts))
        finally:
            ole.close()
        return texts

    def _decompress_chain(self, raw: bytes) -> Optional[bytes]:
        for wbits in [-15, 15, 31]:
            try:
                return zlib.decompress(raw, wbits)
            except Exception:
                pass
        buf = bytearray()
        off = 0
        while off < len(raw):
            chunk = 65536
            end = min(off + chunk, len(raw))
            for wbits in [-15, 15, 31]:
                try:
                    buf.extend(zlib.decompress(raw[off:end], wbits))
                    off = end
                    break
                except Exception:
                    continue
            else:
                off = end
        return bytes(buf) if buf else None

    def _parse_records(self, data: bytes) -> List[Dict]:
        records = []
        offset = 0
        while offset < len(data) - 4:
            raw = struct.unpack_from("<I", data, offset)[0]
            tag_id = raw & 0x3FF
            level = (raw >> 10) & 0x3FF
            size = (raw >> 20) & 0xFFF
            if size == 0xFFF:
                if offset + 8 > len(data):
                    break
                size = struct.unpack_from("<I", data, offset + 4)[0]
                header_size = 8
            else:
                header_size = 4
            if offset + header_size + size > len(data):
                break
            payload = data[offset + header_size : offset + header_size + size]
            records.append({"tag_id": tag_id, "level": level, "payload": payload})
            offset += header_size + size
        return records

    def _read_hwp_fallback(self, path: str) -> Dict[str, Any]:
        try:
            import win32com.client as win32

            abs_path = Path(path).resolve()
            path_str = str(abs_path)
            if not path_str.startswith("\\\\?\\"):
                path_str = "\\\\?\\" + path_str

            hwp = win32.Dispatch("HwpBasic.HwpObject")
            try:
                hwp.Open(path_str)
                text = hwp.GetTextFile("TEXT", "")
                return {
                    "success": True,
                    "format": "hwp-com",
                    "text": text or "",
                    "paragraphs": [p for p in (text or "").split("\n\n") if p.strip()],
                    "section_count": 1,
                    "analysis": self._analyze(text or ""),
                }
            finally:
                try:
                    hwp.Close(0)
                except Exception:
                    pass
        except Exception as e:
            return {"success": False, "error": f"HWP 읽기 실패 (OLE + COM 모두 실패): {e}"}

    def _analyze(self, text: str) -> Dict[str, Any]:
        korean_chars = sum(1 for c in text if "\uAC00" <= c <= "\uD7A3")
        chinese_chars = sum(1 for c in text if "\u4E00" <= c <= "\u9FFF")
        english_chars = sum(1 for c in text if c.isalpha() and ord(c) < 0x4E00)
        return {
            "character_count": len(text),
            "korean_characters": korean_chars,
            "chinese_characters": chinese_chars,
            "english_characters": english_chars,
            "line_count": len(text.splitlines()),
            "word_count": len(text.split()),
        }
