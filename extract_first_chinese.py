#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP 파일 처음 부분 중국어 단어 추출 및 대비 분석
"""

import re
import sys
import os

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_text_from_hwp(file_path, max_length=50000):
    """HWP 파일에서 텍스트를 추출합니다 (최대 길이 제한)."""
    text_content = []
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
            version = header[2:4].hex()
            f.seek(0)
            content = f.read()
            try:
                if len(content) % 2 == 0:
                    text_pairs = content[8:].decode('utf-16le', errors='ignore')
                else:
                    text_pairs = content[8:-1].decode('utf-16le', errors='ignore')
                text_content.append(text_pairs[:max_length])
            except:
                text_content.append(content.decode('utf-8', errors='ignore')[:max_length])
    except Exception as e:
        print(f'Error: {e}')
    return '\n'.join(text_content)

def extract_first_chinese_words(text, max_words=100):
    """텍스트의 처음 부분에서 중국어 단어를 추출합니다."""
    chinese_words = []
    chinese_pattern = re.findall(r'[\u4e00-\u9fff]{2,}', text)

    # 처음 100개 단어만 추출
    for word in chinese_pattern[:max_words]:
        chinese_words.append(word)

    return chinese_words

# 파일 경로
file1 = 'C:/Users/doris/xwechat_files/zhuchunyan331793_600e/msg/file/2026-04/【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp'
file2 = 'C:/Users/doris/Desktop/hwp_backup/【大中朝 14】J 1419-1693--275--20240920.hwp'

print("=" * 80)
print("HWP 파일 처음 부분 중국어 단어 추출")
print("=" * 80)
print()

# 텍스트 추출
print("📄 파일 1에서 텍스트 추출 중...")
text1 = extract_text_from_hwp(file1)

print("📄 파일 2에서 텍스트 추출 중...")
text2 = extract_text_from_hwp(file2)

# 처음 중국어 단어 추출
print()
print("=" * 80)
print("🔍 처음 중국어 단어 추출 (최대 100개)")
print("=" * 80)
print()

chinese1 = extract_first_chinese_words(text1, max_words=100)
chinese2 = extract_first_chinese_words(text2, max_words=100)

print(f"📁 파일 1 처음 중국어 단어 ({len(chinese1)}개):")
for i, word in enumerate(chinese1, 1):
    print(f"   {i:3d}. {word}")
print()

print(f"📁 파일 2 처음 중국어 단어 ({len(chinese2)}개):")
for i, word in enumerate(chinese2, 1):
    print(f"   {i:3d}. {word}")
print()

# 대비 분석
print("=" * 80)
print("📊 대비 분석")
print("=" * 80)
print()

# 파일 1에만 있는 단어
only_in_file1 = set(chinese1) - set(chinese2)
print(f"📝 파일 1에만 있는 단어 ({len(only_in_file1)}개):")
for word in sorted(only_in_file1):
    print(f"   • {word}")
print()

# 파일 2에만 있는 단어
only_in_file2 = set(chinese2) - set(chinese1)
print(f"📝 파일 2에만 있는 단어 ({len(only_in_file2)}개):")
for word in sorted(only_in_file2):
    print(f"   • {word}")
print()

# 공통 단어
common = set(chinese1) & set(chinese2)
print(f"✅ 공통 단어 ({len(common)}개):")
for word in sorted(common):
    print(f"   • {word}")
print()

print("=" * 80)
print("📋 요약")
print("=" * 80)
print()
print(f"파일 1 처음 100개 단어: {len(chinese1)}개")
print(f"파일 2 처음 100개 단어: {len(chinese2)}개")
print()
print(f"파일 1에만 있는 단어: {len(only_in_file1)}개")
print(f"파일 2에만 있는 단어: {len(only_in_file2)}개")
print(f"공통 단어: {len(common)}개")
print()
print("=" * 80)
