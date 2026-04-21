# -*- coding: utf-8 -*-
import re

filepath = r"C:\Users\doris\Desktop\xwechat_files\WORD\hwp_ollama_proofread_detailed.py"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
count = 0

for i, line in enumerate(lines):
    new_lines.append(line)
    
    stripped = line.strip()
    
    if '[CHECK-중한' in stripped and '->' in stripped:
        indent = line[:len(line) - len(line.lstrip())]
        new_lines.append(f'{indent}log(f"    📝 단어(2): " + " ".join(re.findall(r"[\\uac00-\\ud7af\\u1100-\\u11ff\\u3130-\\u318fA-Za-z0-9]+", src)[:2]), log_fh)\n')
        new_lines.append(f'{indent}log(f"    📝 단어(3): " + " ".join(re.findall(r"[\\uac00-\\ud7af\\u1100-\\u11ff\\u3130-\\u318fA-Za-z0-9]+", src)[:3]), log_fh)\n')
        new_lines.append(f'{indent}log(f"    📝 단어(4): " + " ".join(re.findall(r"[\\uac00-\\ud7af\\u1100-\\u11ff\\u3130-\\u318fA-Za-z0-9]+", src)[:4]), log_fh)\n')
        count += 1
    
    elif '[CHECK-TXT]' in stripped and '->' in stripped:
        indent = line[:len(line) - len(line.lstrip())]
        new_lines.append(f'{indent}log(f"    📝 단어(2): " + " ".join(re.findall(r"[\\uac00-\\ud7af\\u1100-\\u11ff\\u3130-\\u318fA-Za-z0-9]+", src)[:2]), log_fh)\n')
        new_lines.append(f'{indent}log(f"    📝 단어(3): " + " ".join(re.findall(r"[\\uac00-\\ud7af\\u1100-\\u11ff\\u3130-\\u318fA-Za-z0-9]+", src)[:3]), log_fh)\n')
        new_lines.append(f'{indent}log(f"    📝 단어(4): " + " ".join(re.findall(r"[\\uac00-\\ud7af\\u1100-\\u11ff\\u3130-\\u318fA-Za-z0-9]+", src)[:4]), log_fh)\n')
        count += 1
    
    elif '[가운데점-병렬 후보' in stripped:
        indent = line[:len(line) - len(line.lstrip())]
        new_lines.append(f'{indent}log(f"    📝 추출단어: {{orig}}", log_fh)\n')
        count += 1
    
    elif '[가운데점-규칙 교정]:' in stripped:
        indent = line[:len(line) - len(line.lstrip())]
        new_lines.append(f'{indent}log(f"    📝 원본단어: {{orig}}", log_fh)\n')
        new_lines.append(f'{indent}log(f"    📝 교정단어: {{corr}}", log_fh)\n')
        count += 1
    
    elif '[가운데점-규칙 유지]:' in stripped:
        indent = line[:len(line) - len(line.lstrip())]
        new_lines.append(f'{indent}log(f"    📝 유지단어: {{orig}}", log_fh)\n')
        count += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"✅ {count}处 로그에 단어 명시 추가 완료!")
