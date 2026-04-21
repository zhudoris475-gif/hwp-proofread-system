#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP 파일 텍스트 내용 비교 스크립트
중국어 단어 차이점을 상세히 분석합니다.
"""

import os
import sys
import re
import hashlib
from datetime import datetime

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_text_from_hwp(file_path):
    """HWP 파일에서 텍스트를 추출합니다."""
    text_content = []

    try:
        with open(file_path, 'rb') as f:
            # HWP 파일 구조 파악
            header = f.read(8)

            # 버전 확인
            version = header[2:4].hex()
            print(f"📄 버전: 0x{version}")

            # 파일 위치 복원
            f.seek(0)

            # HWP 파일에서 텍스트 영역 찾기 (간단한 방법)
            # 실제 HWP 파싱은 복잡하므로, 바이너리에서 텍스트 패턴 검색

            # 텍스트 패턴 검색 (한자, 한글, 영문)
            f.seek(8)
            content = f.read()

            # 유니코드 텍스트 패턴 추출 (UTF-16LE 인코딩된 텍스트)
            unicode_pattern = b'[\x20-\x7e\x80-\xff]{2,}'

            # UTF-16LE로 디코딩 시도
            try:
                # 파일 크기가 2의 배수인지 확인
                if len(content) % 2 == 0:
                    text_pairs = content[8:].decode('utf-16le', errors='ignore')
                    text_content.append(text_pairs)
                else:
                    # 홀수 바이트 제거
                    text_pairs = content[8:-1].decode('utf-16le', errors='ignore')
                    text_content.append(text_pairs)
            except:
                # 디코딩 실패 시 바이너리 패턴 사용
                text_content.append(content.decode('utf-8', errors='ignore'))

    except Exception as e:
        print(f"❌ 텍스트 추출 실패: {e}")
        return ""

    return "\n".join(text_content)

def analyze_chinese_difference(text1, text2):
    """중국어 차이점을 분석합니다."""
    print("=" * 80)
    print("중국어 차이점 상세 분석")
    print("=" * 80)
    print()

    # 텍스트 전처리
    def clean_text(text):
        # 공백 및 특수문자 정리
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        return text.strip()

    text1_clean = clean_text(text1)
    text2_clean = clean_text(text2)

    print(f"📄 파일 1 길이: {len(text1_clean):,} 문자")
    print(f"📄 파일 2 길이: {len(text2_clean):,} 문자")
    print()

    # 중국어 단어 추출 (2자 이상의 한자)
    def extract_chinese(text):
        # 2자 이상의 한자 추출 (연속된 한자)
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', text)
        return set(chinese_words)

    chinese1 = extract_chinese(text1_clean)
    chinese2 = extract_chinese(text2_clean)

    print(f"📚 파일 1 중국어 단어: {len(chinese1):,}개")
    print(f"📚 파일 2 중국어 단어: {len(chinese2):,}개")
    print()

    # 차이점 분석
    only_in_file1 = chinese1 - chinese2
    only_in_file2 = chinese2 - chinese1
    common = chinese1 & chinese2

    print("=" * 80)
    print("🔍 차이점 분석")
    print("=" * 80)
    print()

    # 파일 1에만 있는 단어
    if only_in_file1:
        print(f"📝 파일 1에만 있는 단어 ({len(only_in_file1)}개):")
        for word in sorted(only_in_file1):
            print(f"   • {word}")
        print()
    else:
        print("✅ 파일 1에만 있는 단어: 없음")
        print()

    # 파일 2에만 있는 단어
    if only_in_file2:
        print(f"📝 파일 2에만 있는 단어 ({len(only_in_file2)}개):")
        for word in sorted(only_in_file2):
            print(f"   • {word}")
        print()
    else:
        print("✅ 파일 2에만 있는 단어: 없음")
        print()

    # 공통 단어
    print(f"✅ 공통 단어: {len(common):,}개")
    print()

    # 빈도 분석
    print("=" * 80)
    print("📊 빈도 분석")
    print("=" * 80)
    print()

    def count_frequency(text, words):
        freq = {}
        for word in words:
            count = text.count(word)
            if count > 0:
                freq[word] = count
        return freq

    freq1 = count_frequency(text1_clean, common)
    freq2 = count_frequency(text2_clean, common)

    if freq1:
        print("📄 파일 1 빈도 (공통 단어):")
        for word, count in sorted(freq1.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"   • {word}: {count}회")
        print()

    if freq2:
        print("📄 파일 2 빈도 (공통 단어):")
        for word, count in sorted(freq2.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"   • {word}: {count}회")
        print()

    # 주요 차이점 요약
    print("=" * 80)
    print("📋 주요 차이점 요약")
    print("=" * 80)
    print()

    total_diff = len(only_in_file1) + len(only_in_file2)

    if total_diff == 0:
        print("✅ 두 파일의 중국어 단어가 완전히 동일합니다.")
    else:
        print(f"⚠️  총 {total_diff}개의 단어 차이가 있습니다.")
        print()
        print("💡 팁:")
        if only_in_file1:
            print(f"   • 파일 1에 있는 {len(only_in_file1)}개 단어는 파일 2에서 제거된 것입니다.")
        if only_in_file2:
            print(f"   • 파일 2에 있는 {len(only_in_file2)}개 단어는 파일 1에 없는 것입니다.")

    print()
    print("=" * 80)

def main():
    if len(sys.argv) != 3:
        print("사용법: python compare_chinese.py <파일1.hwp> <파일2.hwp>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if not os.path.exists(file1):
        print(f"❌ 파일 1을 찾을 수 없습니다: {file1}")
        sys.exit(1)

    if not os.path.exists(file2):
        print(f"❌ 파일 2를 찾을 수 없습니다: {file2}")
        sys.exit(1)

    print()
    print("=" * 80)
    print("HWP 텍스트 내용 비교 및 중국어 차이점 분석")
    print("=" * 80)
    print()

    # 텍스트 추출
    print("📄 파일 1에서 텍스트 추출 중...")
    text1 = extract_text_from_hwp(file1)

    print("📄 파일 2에서 텍스트 추출 중...")
    text2 = extract_text_from_hwp(file2)

    # 차이점 분석
    analyze_chinese_difference(text1, text2)

if __name__ == "__main__":
    main()
