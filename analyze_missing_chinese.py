#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP 파일 한자 손실 분석 스크립트
원본과 수정본의 한자를 비교하여 손실된 한자를 찾아냅니다.
"""

import sys
import os
import re
import struct
import zlib
from collections import defaultdict
from typing import List, Dict, Tuple, Set

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class HWPTextExtractor:
    """HWP 파일에서 텍스트를 추출하는 클래스"""

    def __init__(self):
        self.olefile = None

    def extract_text(self, filepath: str) -> Tuple[str, List[Dict]]:
        """
        HWP 파일에서 텍스트 추출

        Args:
            filepath: HWP 파일 경로

        Returns:
            (추출된 텍스트, 한자 위치 정보 리스트)
        """
        try:
            import olefile
            self.olefile = olefile
        except ImportError:
            raise RuntimeError("olefile 모듈이 필요합니다. pip install olefile")

        texts = []
        chinese_locations = []

        ole = None
        try:
            ole = olefile.OleFileIO(filepath, write_mode=False)
            streams = ole.listdir()

            # BodyText 스트림 찾기
            body_streams = [s for s in streams if s and s[0] == "BodyText"]

            for stream_path in body_streams:
                stream_name = '/'.join(stream_path)
                raw = ole.openstream(stream_name).read()

                try:
                    dec = zlib.decompress(raw, -15)
                    records = self._parse_records(dec)

                    parts = []
                    for rec in records:
                        if rec.get("tag_id") != 67:  # Tag ID 67: 텍스트 레코드
                            continue

                        try:
                            payload = rec["payload"].decode("utf-16-le", errors="replace")
                            parts.append(payload)

                            # 한자 위치 추적
                            chinese_words = self._extract_chinese_with_location(payload, rec.get("level", 0))
                            chinese_locations.extend(chinese_words)

                        except Exception:
                            continue

                    if parts:
                        texts.append('
'.join(parts))
'.join(parts))
'.join(parts))

        except Exception:
            print(f"❌ HWP 파일 추출 오류")
            return "", []

        finally:
            if ole:
                ole.close()

        return '\n'.join(texts), chinese_locations

    def _parse_records(self, data: bytes) -> List[Dict]:
        """HWP 레코드 파싱"""
        records = []
        offset = 0

        while offset < len(data) - 4:
            try:
                raw = struct.unpack_from('<I', data, offset)[0]
                tag_id = raw & 0x3FF
                level = (raw >> 10) & 0x3FF
                size = (raw >> 20) & 0xFFF

                if size == 0xFFF:
                    if offset + 8 > len(data):
                        break
                    size = struct.unpack_from('<I', data, offset + 4)[0]
                    header_size = 8
                else:
                    header_size = 4

                if offset + header_size + size > len(data):
                    break

                payload = data[offset + header_size:offset + header_size + size]

                records.append({
                    "tag_id": tag_id,
                    "level": level,
                    "payload": payload,
                })

                offset += header_size + size

            except Exception:
                break

        return records

    def _extract_chinese_with_location(self, text: str, level: int) -> List[Dict]:
        """텍스트에서 한자와 위치 정보 추출"""
        chinese_words = []

        # 한자 패턴: \u4e00-\u9fff (2자 이상)
        chinese_pattern = re.finditer(r'[\u4e00-\u9fff]{2,}', text)

        for match in chinese_pattern:
            chinese_word = match.group()
            start_pos = match.start()
            end_pos = match.end()

            # 전체 텍스트에서의 위치 계산
            char_index = text[:start_pos].count('\x00') + start_pos

            chinese_words.append({
                "word": chinese_word,
                "start_pos": start_pos,
                "end_pos": end_pos,
                "char_index": char_index,
                "level": level,
            })

        return chinese_words


class ChineseAnalyzer:
    """한자 분석 클래스"""

    def __init__(self):
        # 한자 범위: \u4e00-\u9fff (CJK 통합 한자)
        self.CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]{2,}')

    def extract_chinese(self, text: str) -> Set[str]:
        """텍스트에서 모든 한자 추출"""
        return set(self.CHINESE_PATTERN.findall(text))

    def extract_chinese_with_details(self, text: str) -> List[Dict]:
        """텍스트에서 한자와 상세 정보 추출"""
        chinese_words = []

        for match in self.CHINESE_PATTERN.finditer(text):
            chinese_word = match.group()
            chinese_words.append({
                "word": chinese_word,
                "start": match.start(),
                "end": match.end(),
            })

        return chinese_words


def compare_chinese_files(original_file: str, modified_file: str) -> Dict:
    """
    원본과 수정본의 한자 비교

    Args:
        original_file: 원본 HWP 파일 경로
        modified_file: 수정본 HWP 파일 경로

    Returns:
        비교 결과 딕셔너리
    """
    print("=" * 80)
    print("HWP 파일 한자 손실 분석")
    print("=" * 80)
    print(f"\n원본 파일: {original_file}")
    print(f"수정본 파일: {modified_file}")
    print()

    # 텍스트 추출
    print("📂 원본 파일에서 텍스트 추출 중...")
    extractor = HWPTextExtractor()
    original_text, original_locations = extractor.extract_text(original_file)

    print("📂 수정본 파일에서 텍스트 추출 중...")
    modified_text, modified_locations = extractor.extract_text(modified_file)

    if not original_text:
        print("❌ 원본 파일에서 텍스트 추출 실패!")
        return {}

    if not modified_text:
        print("❌ 수정본 파일에서 텍스트 추출 실패!")
        return {}

    # 한자 추출
    analyzer = ChineseAnalyzer()
    original_chinese = analyzer.extract_chinese(original_text)
    modified_chinese = analyzer.extract_chinese(modified_text)

    print(f"\n📊 원본 파일: {len(original_text):,}자, {len(original_chinese):,}개 한자")
    print(f"📊 수정본 파일: {len(modified_text):,}자, {len(modified_chinese):,}개 한자")
    print()

    # 비교 분석
    result = {
        "original_text": original_text,
        "modified_text": modified_text,
        "original_chinese": original_chinese,
        "modified_chinese": modified_chinese,
        "missing_chinese": original_chinese - modified_chinese,
        "added_chinese": modified_chinese - original_chinese,
        "common_chinese": original_chinese & modified_chinese,
    }

    # 결과 출력
    print("=" * 80)
    print("🔍 한자 손실 분석 결과")
    print("=" * 80)
    print()

    # 누락된 한자
    missing = result["missing_chinese"]
    if missing:
        print(f"❌ 누락된 한자 ({len(missing)}개):")
        for i, word in enumerate(sorted(missing), 1):
            print(f"   {i:3d}. {word}")
        print()
    else:
        print("✅ 누락된 한자: 없음")
        print()

    # 추가된 한자
    added = result["added_chinese"]
    if added:
        print(f"➕ 추가된 한자 ({len(added)}개):")
        for i, word in enumerate(sorted(added), 1):
            print(f"   {i:3d}. {word}")
        print()
    else:
        print("✅ 추가된 한자: 없음")
        print()

    # 공통 한자
    common = result["common_chinese"]
    print(f"✅ 공통 한자 ({len(common):,}개)")
    print()

    # 통계
    print("=" * 80)
    print("📊 통계")
    print("=" * 80)
    print(f"원본 한자: {len(original_chinese):,}개")
    print(f"수정본 한자: {len(modified_chinese):,}개")
    print(f"누락된 한자: {len(missing):,}개")
    print(f"추가된 한자: {len(added):,}개")
    print(f"공통 한자: {len(common):,}개")
    print()

    # 한자 손실 비율
    if original_chinese:
        loss_rate = len(missing) / len(original_chinese) * 100
        print(f"한자 손실 비율: {loss_rate:.2f}%")
        print()

    return result


def save_report(result: Dict, output_file: str):
    """분석 결과를 파일로 저장"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("HWP 파일 한자 손실 분석 보고서\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"원본 한자: {len(result['original_chinese']):,}개\n")
        f.write(f"수정본 한자: {len(result['modified_chinese']):,}개\n")
        f.write(f"누락된 한자: {len(result['missing_chinese']):,}개\n")
        f.write(f"추가된 한자: {len(result['added_chinese']):,}개\n")
        f.write(f"공통 한자: {len(result['common_chinese']):,}개\n\n")

        if result['missing_chinese']:
            f.write("=" * 80 + "\n")
            f.write("❌ 누락된 한자 목록\n")
            f.write("=" * 80 + "\n\n")
            for i, word in enumerate(sorted(result['missing_chinese']), 1):
                f.write(f"{i:3d}. {word}\n")
            f.write("\n")

        if result['added_chinese']:
            f.write("=" * 80 + "\n")
            f.write("➕ 추가된 한자 목록\n")
            f.write("=" * 80 + "\n\n")
            for i, word in enumerate(sorted(result['added_chinese']), 1):
                f.write(f"{i:3d}. {word}\n")
            f.write("\n")

        if result['common_chinese']:
            f.write("=" * 80 + "\n")
            f.write("✅ 공통 한자 목록 (최상위 50개)\n")
            f.write("=" * 80 + "\n\n")
            for i, word in enumerate(sorted(result['common_chinese'])[:50], 1):
                f.write(f"{i:3d}. {word}\n")
            f.write("\n")

    print(f"\n📄 보고서 저장: {output_file}")


def main():
    """메인 함수"""
    if len(sys.argv) < 3:
        print("사용법: python analyze_missing_chinese.py <원본파일.hwp> <수정본파일.hwp> [출력파일.txt]")
        print()
        print("예시:")
        print("  python analyze_missing_chinese.py original.hwp modified.hwp")
        print("  python analyze_missing_chinese.py original.hwp modified.hwp report.txt")
        sys.exit(1)

    original_file = sys.argv[1]
    modified_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "missing_chinese_report.txt"

    # 파일 존재 확인
    if not os.path.exists(original_file):
        print(f"❌ 원본 파일을 찾을 수 없습니다: {original_file}")
        sys.exit(1)

    if not os.path.exists(modified_file):
        print(f"❌ 수정본 파일을 찾을 수 없습니다: {modified_file}")
        sys.exit(1)

    # 비교 실행
    result = compare_chinese_files(original_file, modified_file)

    if result:
        # 보고서 저장
        save_report(result, output_file)

        print()
        print("=" * 80)
        print("✅ 분석 완료")
        print("=" * 80)
    else:
        print()
        print("=" * 80)
        print("❌ 분석 실패")
        print("=" * 80)


if __name__ == "__main__":
    main()
