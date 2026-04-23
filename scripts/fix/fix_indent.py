# -*- coding: utf-8 -*-
import os

filepath = r"C:\Users\doris\Desktop\xwechat_files\WORD\hwp_ollama_proofread_detailed.py"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

old_block = """        log(f"정규식 규칙: {len(regex_rules)}개", log_fh)
    if stage == "check":
        log("Ollama: check 모드에서는 3-4단계 생략", log_fh)
    elif ollama_ok:
            log(f"Ollama: 연결됨 (고정 모델: {resolved_ollama_model})", log_fh)
        else:
            log(f"Ollama: 미연결 또는 고정 모델 없음 ({OLLAMA_MODEL})", log_fh)
        log(f"단계: {stage}", log_fh)"""

new_block = """        log(f"정규식 규칙: {len(regex_rules)}개", log_fh)
        if stage == "check":
            log("Ollama: check 모드에서는 3-4단계 생략", log_fh)
        elif ollama_ok:
            log(f"Ollama: 연결됨 (고정 모델: {resolved_ollama_model})", log_fh)
        else:
            log(f"Ollama: 미연결 또는 고정 모델 없음 ({OLLAMA_MODEL})", log_fh)
        log(f"단계: {stage}", log_fh)"""

content = ''.join(lines)

if old_block in content:
    content = content.replace(old_block, new_block, 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ IndentationError 수정 완료! (2005번째 줄)")
else:
    print("❌ 대상 블록을 찾을 수 없음")
    for i, line in enumerate(lines[2000:2015], start=2001):
        print(f"  L{i}: {repr(line)}")
