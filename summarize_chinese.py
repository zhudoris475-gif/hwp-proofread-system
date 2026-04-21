#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP 중국어 차이점 핵심 요약
"""

import re
import sys
import os

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_text_from_hwp(file_path):
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
                    text_content.append(text_pairs)
                else:
                    text_pairs = content[8:-1].decode('utf-16le', errors='ignore')
                    text_content.append(text_pairs)
            except:
                text_content.append(content.decode('utf-8', errors='ignore'))
    except Exception as e:
        print(f'Error: {e}')
    return '\n'.join(text_content)

text1 = extract_text_from_hwp('C:/Users/doris/xwechat_files/zhuchunyan331793_600e/msg/file/2026-04/【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp')
text2 = extract_text_from_hwp('C:/Users/doris/Desktop/hwp_backup/【大中朝 14】J 1419-1693--275--20240920.hwp')

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
    return text.strip()

text1_clean = clean_text(text1)
text2_clean = clean_text(text2)

chinese1 = set(re.findall(r'[\u4e00-\u9fff]{2,}', text1_clean))
chinese2 = set(re.findall(r'[\u4e00-\u9fff]{2,}', text2_clean))

only_in_file1 = chinese1 - chinese2
only_in_file2 = chinese2 - chinese1

print('=' * 80)
print('중국어 차이점 핵심 요약')
print('=' * 80)
print()
print(f'📄 파일 1 중국어 단어: {len(chinese1):,}개')
print(f'📄 파일 2 중국어 단어: {len(chinese2):,}개')
print()
print(f'📝 파일 1에만 있는 단어: {len(only_in_file1):,}개')
print(f'📝 파일 2에만 있는 단어: {len(only_in_file2):,}개')
print()

# 파일 1에만 있는 단어 중 일부 표시
if only_in_file1:
    print('🔍 파일 1에만 있는 주요 단어 (상위 30개):')
    for word in sorted(only_in_file1)[:30]:
        print(f'   • {word}')
    print()

# 파일 2에만 있는 단어 중 일부 표시
if only_in_file2:
    print('🔍 파일 2에만 있는 주요 단어 (상위 30개):')
    for word in sorted(only_in_file2)[:30]:
        print(f'   • {word}')
    print()

# 결론
print('=' * 80)
print('📋 결론')
print('=' * 80)
print()
if len(only_in_file1) > 0:
    print(f'⚠️  파일 1에 {len(only_in_file1):,}개의 단어가 추가되었습니다.')
    print('   → 파일 2에서 제거된 단어들입니다.')
if len(only_in_file2) > 0:
    print(f'⚠️  파일 2에 {len(only_in_file2):,}개의 단어가 추가되었습니다.')
    print('   → 파일 1에 없는 새로운 단어들입니다.')
print()
print('=' * 80)
