# -*- coding: utf-8 -*-
import sys, os, time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET = r"C:\Users\doris\Desktop\xwechat_files\WORD\hwp_ollama_proofread_detailed.py"

sys.path.insert(0, os.path.dirname(TARGET))

import importlib.util
spec = importlib.util.spec_from_file_location("proofread", TARGET)
mod = importlib.util.module_from_spec(spec)

mod.OLLAMA_DOT_TIMEOUT = 30
mod.OLLAMA_QUOTE_TIMEOUT = 30

spec.loader.exec_module(mod)

def fast_collect_dot(text, log_fh=None):
    import re as _re
    
    corrections = []
    t_start = time.time()
    
    dot_contexts = []
    for dot in ["·", "•", "・"]:
        for m in _re.finditer(r'.{0,20}' + _re.escape(dot) + r'.{0,20}', text):
            ctx = m.group().strip()
            if ctx and ctx not in dot_contexts:
                dot_contexts.append(ctx)
    
    if not dot_contexts:
        mod.log("  [가운데점] 대상 없음", log_fh)
        return corrections
    
    phonetic_pattern = _re.compile(r'[a-z]\d*[·•・]|[·•\-][a-z]\d*', _re.IGNORECASE)
    filtered = [c for c in dot_contexts if not phonetic_pattern.search(c)]
    
    mod.log(f"  [가운데점] 총 {len(dot_contexts)}개 발견 (발음기호 제외: {len(filtered)}개)", log_fh)
    
    two_word_rules = []
    three_word_rules = []
    four_word_rules = []
    ollama_candidates = []
    
    china_place_pattern = _re.compile(r'[\u4e00-\u9fff]{1,3}[·•][省市区县]')
    
    for ctx in filtered[:100]:
        if china_place_pattern.search(ctx):
            ollama_candidates.append(ctx)
            continue
            
        clean = ctx.replace("·", "").replace("•", "").replace("・", "")
        hangul_words = _re.findall(r'[가-힣]{2,}', clean)
        
        has_chinese_only = bool(_re.match(r'^[\u4e00-\u9fff·•・]+$', ctx.strip()))
        has_number_unit = bool(_re.search(r'\d+[·•]', ctx))
        has_book_mark = bool(_re.search(r'[《》]', ctx))
        
        if has_chinese_only or has_number_unit or has_book_mark:
            ollama_candidates.append(ctx)
            continue
        
        is_parallel = (
            2 <= len(hangul_words) <= 4 and
            all(1 <= len(w) <= 8 for w in hangul_words) and
            not any(p in ctx for p in ["(", ")", "[", "]", "{", "}", ".", ",", ";", ":", "!", "?"])
        )
        
        if is_parallel:
            word_count = len(hangul_words)
            if word_count == 2:
                two_word_rules.append(ctx)
            elif word_count == 3:
                three_word_rules.append(ctx)
            elif word_count == 4:
                four_word_rules.append(ctx)
        else:
            ollama_candidates.append(ctx)
    
    mod.log(f"  [가운데점-규칙분류] 2단어병렬: {len(two_word_rules)}개 / 3단어병렬: {len(three_word_rules)}개 / 4단어병렬: {len(four_word_rules)}개 / Ollama후보: {len(ollama_candidates)}개", log_fh)
    
    if two_word_rules:
        mod.log(f"  [가운데점-2단어병렬규칙] 총 {len(two_word_rules)}건 처리 시작", log_fh)
        for i, ctx in enumerate(two_word_rules, 1):
            clean = ctx.replace("·", ", ").replace("•", ", ").replace("・", ", ")
            original = ctx.strip()
            corrected = clean.strip()
            if original != corrected:
                corrections.append((original, corrected))
                mod.log(f"    [2단어-{i}] '{original}' -> '{corrected}'", log_fh)
            else:
                mod.log(f"    [2단어-{i}] '{original}' (변경없음)", log_fh)
        mod.log(f"  [가운데점-2단어병렬규칙] 완료: {len([c for c in corrections])}건 교정", log_fh)
    
    if three_word_rules:
        mod.log(f"  [가운데점-3단어병렬규칙] 총 {len(three_word_rules)}건 처리 시작", log_fh)
        for i, ctx in enumerate(three_word_rules, 1):
            clean = ctx.replace("·", ", ").replace("•", ", ").replace("・", ", ")
            original = ctx.strip()
            corrected = clean.strip()
            if original != corrected:
                corrections.append((original, corrected))
                mod.log(f"    [3단어-{i}] '{original}' -> '{corrected}'", log_fh)
            else:
                mod.log(f"    [3단어-{i}] '{original}' (변경없음)", log_fh)
        mod.log(f"  [가운데점-3단어병렬규칙] 완료: {len([c for c in corrections])}건 교정", log_fh)
    
    if four_word_rules:
        mod.log(f"  [가운데점-4단어병렬규칙] 총 {len(four_word_rules)}건 처리 시작", log_fh)
        for i, ctx in enumerate(four_word_rules, 1):
            clean = ctx.replace("·", ", ").replace("•", ", ").replace("・", ", ")
            original = ctx.strip()
            corrected = clean.strip()
            if original != corrected:
                corrections.append((original, corrected))
                mod.log(f"    [4단어-{i}] '{original}' -> '{corrected}'", log_fh)
            else:
                mod.log(f"    [4단어-{i}] '{original}' (변경없음)", log_fh)
        mod.log(f"  [가운데점-4단어병렬규칙] 완료: {len([c for c in corrections])}건 교정", log_fh)
    
    if ollama_candidates and len(ollama_candidates) <= 20:
        mod.log(f"  [가운데점-Ollama] {len(ollama_candidates)}건 Ollama 처리 (규칙으로 판단불가)", log_fh)
        
        batch_size = 10
        for batch_idx, start in enumerate(range(0, len(ollama_candidates), batch_size), 1):
            batch = ollama_candidates[start:start+batch_size]
            
            dot_list = "\n".join([f'  {i+1}. {c}' for i, c in enumerate(batch)])
            dot_prompt = f"""가운데점(·) 교정: 병렬나열은 쉼표(, )로 변경, 중국지명/발음기호/책제목은 유지.
{dot_list}
JSON 출력: [{{"id":1,"action":"keep|correct","original":"원문","corrected":"교정문"}}]"""
            
            payload = {
                "model": mod.resolve_ollama_model(),
                "messages": [{"role": "user", "content": dot_prompt}],
                "stream": False,
                "options": {"num_predict": 200, "temperature": 0}
            }
            
            try:
                resp = mod.post_ollama_chat(payload, timeout=30)
                resp_text = ""
                if isinstance(resp, dict):
                    if "message" in resp and isinstance(resp["message"], dict):
                        resp_text = resp["message"].get("content", "")
                
                items = mod.parse_ollama_json_array(resp_text)
                
                for item in items:
                    action = item.get("action", "")
                    original = item.get("original", "").strip()
                    corrected = item.get("corrected", "").strip()
                    
                    if action == "correct" and original and corrected and original != corrected:
                        corrections.append((original, corrected))
                        mod.log(f"    [Ollama-{batch_idx}] '{original}' -> '{corrected}'", log_fh)
                    elif action == "keep":
                        mod.log(f"    [Ollama-{batch_idx}] '{original}' (유지)", log_fh)
                        
            except Exception as e:
                mod.log(f"    [Ollama-{batch_idx}] 오류: {e}", log_fh)
    elif ollama_candidates:
        mod.log(f"  [가운데점-Ollama SKIP] {len(ollama_candidates)}건은 규칙으로 처리불가능하나 시간관계로 건너뜀 (필요시 개별확인)", log_fh)
        for i, ctx in enumerate(ollama_candidates[:10], 1):
            mod.log(f"    [SKIP-{i}] '{ctx}'", log_fh)
        if len(ollama_candidates) > 10:
            mod.log(f"    ... 외 {len(ollama_candidates) - 10}건 생략", log_fh)
    else:
        mod.log(f"  [가운데점-Ollama] 모든 항목 규칙으로 처리됨 - Ollama 불필요", log_fh)
    
    t_elapsed = time.time() - t_start
    mod.log(f"  [가운데점-완료] 총 {len(corrections)}건 교정 ({t_elapsed:.1f}초) [2단어:{len(two_word_rules)}/3단어:{len(three_word_rules)}/4단어:{len(four_word_rules)}/Ollama:{min(len(ollama_candidates),20)}]", log_fh)
    return corrections

mod.collect_dot_corrections_with_ollama = fast_collect_dot

def fast_collect_quote(text, log_fh=None):
    import re as _re
    
    corrections = []
    t_start = time.time()
    
    ldq, rdq = '\u201c', '\u201d'
    lsq, rsq = '\u2018', '\u2019'
    
    quote_pairs = []
    for m in _re.finditer(_re.escape(ldq) + r'(?:[^' + _re.escape(rdq) + r']{1,50})' + _re.escape(rdq), text):
        quote_pairs.append(m.group())
    
    if not quote_pairs:
        mod.log("  [따옴표] 대상 없음", log_fh)
        return corrections
    
    mod.log(f"  [따옴표] 총 {len(quote_pairs)}쌍 발견", log_fh)
    
    simple_terms = {
        "欧洲安全和合作会议", "欧洲共同体", "欧洲联盟", "欧洲共同市场",
        "欧洲大战", "欧洲煤钢联营", "欧洲原子能联营",
        "欧洲经济共同体", "欧洲经济共同体(共同市场)",
    }
    
    kept_korean = []
    kept_chinese = []
    converted = []
    kept_other = []
    
    for i, q in enumerate(quote_pairs, 1):
        inner = q[1:-1]
        has_hangul = bool(_re.search(r'[가-힣]', inner))
        has_chinese = bool(_re.search(r'[\u4e00-\u9fff]', inner))
        has_newline = bool(_re.search(r'[\n\r]', inner))
        ends_particle = bool(_re.search(r'(吗|呢|吧|啊|呀|啦|嘛|么)$', inner))
        
        is_chinese_term = (
            len(inner) >= 2 and
            (has_chinese or not has_hangul) and
            not has_newline and
            not ends_particle and
            not _re.search(r'[·•\-]', inner)
        )
        
        if is_chinese_term:
            if any(t in inner for t in simple_terms):
                new_q = lsq + inner + rsq
                corrections.append((q, new_q))
                converted.append((i, q, new_q))
                mod.log(f"    [따옴표-{i} 변환] '{q}' -> '{new_q}'", log_fh)
            else:
                kept_chinese.append((i, q))
                mod.log(f"    [따옴표-{i} 유지-중문] '{q}'", log_fh)
        elif has_hangul:
            kept_korean.append((i, q))
            mod.log(f"    [따옴표-{i} 유지-한글] '{q}'", log_fh)
        else:
            kept_other.append((i, q))
            mod.log(f"    [따옴표-{i} 유지-기타] '{q}'", log_fh)
    
    t_elapsed = time.time() - t_start
    mod.log(f"  [따옴표-완료] 변환:{len(converted)}건 / 한글유지:{len(kept_korean)}건 / 중문유지:{len(kept_chinese)}건 / 기타유지:{len(kept_other)}건 ({t_elapsed:.1f}초)", log_fh)
    return corrections

mod.collect_quote_corrections_with_ollama = fast_collect_quote

if __name__ == "__main__":
    mod.main()
