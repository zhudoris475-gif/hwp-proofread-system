# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")

from core.unified.pipeline import ProofreadPipeline
from core.unified.config.paths import FILES


def main():
    import argparse
    parser = argparse.ArgumentParser(description="HWP 전반 교정 시스템 (통합판)")
    parser.add_argument("--files", nargs="+", choices=list(FILES.keys()), default=None,
                        help="교정할 파일 라벨 (J, L, K)")
    parser.add_argument("--no-binary", action="store_true", help="바이너리 교정 건너뛰기")
    parser.add_argument("--no-com", action="store_true", help="COM 교정 건너뛰기")
    parser.add_argument("--analyze-only", action="store_true", help="분석만 수행")
    args = parser.parse_args()

    pipeline = ProofreadPipeline()

    if args.analyze_only:
        from core.unified.text_analyzer import analyze_text, load_china_rules
        from core.unified.binary_editor import extract_text
        from core.unified.config.paths import RULES_CHINA_PLACE

        china_rules = load_china_rules(RULES_CHINA_PLACE)
        labels = args.files or list(FILES.keys())
        for label in labels:
            if label in FILES:
                paths = FILES[label]
                work_path = paths.get("work", paths.get("orig"))
                if os.path.exists(work_path):
                    text = extract_text(work_path)
                    analysis = analyze_text(text, china_rules)
                    print(f"\n[{label}] 텍스트: {analysis['text_len']:,}자")
                    print(f"  한자: {analysis['cn_total']:,}개")
                    print(f"  나라→조: {len(analysis['nara_rules'])}종")
                    print(f"  띄어쓰기: {len(analysis['spacing_needed'])}종")
                    print(f"  따옴표: {len(analysis['quote_needed'])}종")
                    print(f"  중한규칙: {len(analysis['china_needed'])}종")
                    print(f"  문맥띄어쓰기: {len(analysis['context_expanded'])}건")
        return

    pipeline.run(args.files)


if __name__ == "__main__":
    main()
