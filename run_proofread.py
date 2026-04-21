import sys, os
sys.path.insert(0, r"C:\Users\doris\Desktop\xwechat_files\hwp_proofreading_package")
os.chdir(r"C:\Users\doris\Desktop\xwechat_files\hwp_proofreading_package")

import hwp_ollama_proofread as hp

hp.HWP_DIR = r"C:\사전"

target = r"C:\사전\【20】O 2179-2182排版页수4-金花顺-.backup"

txt_rules = hp.parse_rules(hp.RULES_FILE)
china_rules = hp.load_china_place_rules()
regex_rules = hp.load_regex_rules()
ollama_ok = hp.ollama_is_available()

print(f"TXT rules: {len(txt_rules)}")
print(f"China place rules: {len(china_rules)}")
print(f"Regex rules: {len(regex_rules)}")
print(f"Ollama: {'connected' if ollama_ok else 'not available'}")
print(f"Target: {target}")
print(f"File exists: {os.path.exists(target)}")

with open(hp.LOG_FILE, 'a', encoding='utf-8') as log_fh:
    hp.log(f"\n\n{'#' * 60}", log_fh)
    hp.log(f"HWP proofread: {target}", log_fh)
    hp.log(f"TXT rules: {len(txt_rules)}, China: {len(china_rules)}, Regex: {len(regex_rules)}", log_fh)
    hp.log(f"Ollama: {'connected' if ollama_ok else 'not available'}", log_fh)
    hp.log(f"{'#' * 60}\n", log_fh)

    applied, corrections = hp.process_hwp_file(target, txt_rules, regex_rules, china_rules, log_fh)
    hp.log(f"\nApplied: {applied} changes", log_fh)
    hp.log(f"Total corrections: {len(corrections)}", log_fh)

    report_path = hp.save_report(target, corrections, applied, log_fh)
    if report_path:
        print(f"\nReport saved: {report_path}")

print(f"\nDone! Applied: {applied} changes, {len(corrections)} correction items")
print(f"Log: {hp.LOG_FILE}")
