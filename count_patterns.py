# -*- coding: utf-8 -*-
import re

with open(r'D:\ProgramData\xwechat_files\zhuchunyan331793_600e\hwp_ollama_proofread.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('PROTECT_LIST = [')
end = content.find(']', start) + 1
list_content = content[start:end]
items = re.findall(r'"[^"]+"', list_content)
print(f'hwp_ollama_proofread.py PROTECT_LIST: {len(items)} 개')

with open(r'D:\ProgramData\xwechat_files\zhuchunyan331793_600e\extract_match_context.py', 'r', encoding='utf-8') as f:
    content2 = f.read()

start2 = content2.find('suspect_patterns = [')
end2 = content2.find(']', start2) + 1
list_content2 = content2[start2:end2]
items2 = re.findall(r'"[^"]+"', list_content2)
print(f'extract_match_context.py suspect_patterns: {len(items2)} 개')