import sys
import argparse
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))

from hwp_proofread import ProofreadPipeline


def main():
    parser = argparse.ArgumentParser(
        description="HWP 교정 시스템 v3.0 - 한글 문서 자동 교정",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예:
  python main.py document.hwpx                    # 단일 파일 교정
  python main.py document.hwpx --preview          # 미리보기 (저장 안 함)
  python main.py document.hwpx --report html      # HTML 리포트 생성
  python main.py ./documents/ --batch             # 배치 교정
  python main.py document.hwpx --rules ./rules/   # 규칙 디렉토리 지정
        """,
    )
    parser.add_argument("input", help="입력 HWP/HWPX 파일 또는 디렉토리")
    parser.add_argument("-o", "--output", help="출력 파일 경로")
    parser.add_argument("--batch", action="store_true", help="배치 모드 (디렉토리 처리)")
    parser.add_argument("--pattern", default="*.hwp", help="배치 파일 패턴 (기본: *.hwp)")
    parser.add_argument("--preview", action="store_true", help="미리보기 (저장 안 함)")
    parser.add_argument("--report", choices=["text", "html", "json"], default="text", help="리포트 형식")
    parser.add_argument("--rules", help="규칙 파일 디렉토리")
    parser.add_argument("--no-middle-dot", action="store_true", help="가운데점 교정 비활성화")
    parser.add_argument("--no-quotes", action="store_true", help="따옴표 교정 비활성화")
    parser.add_argument("--no-place-names", action="store_true", help="지명 변환 비활성화")
    parser.add_argument("--no-spacing", action="store_true", help="띄어쓰기 교정 비활성화")
    parser.add_argument("--no-rules", action="store_true", help="규칙 파일 교정 비활성화")
    parser.add_argument("--no-backup", action="store_true", help="백업 생성 안 함")

    args = parser.parse_args()

    pipeline = ProofreadPipeline(
        rules_dir=args.rules,
        enable_middle_dot=not args.no_middle_dot,
        enable_quotes=not args.no_quotes,
        enable_place_names=not args.no_place_names,
        enable_spacing=not args.no_spacing,
        enable_rules=not args.no_rules,
        backup=not args.no_backup,
    )

    input_path = Path(args.input)
    if not input_path.exists():
        abs_input = Path(args.input).resolve()
        if abs_input.exists():
            input_path = abs_input
        else:
            print(f"Input path not found: {args.input}")
            sys.exit(1)

    if args.batch or input_path.is_dir():
        results = pipeline.batch_proofread(
            directory=str(input_path),
            pattern=args.pattern,
            save=not args.preview,
            report_format=args.report,
        )

        success = sum(1 for r in results if r.get("success"))
        total_corrections = sum(r.get("total_corrections", 0) for r in results)

        print(f"\n배치 완료: {success}/{len(results)} 파일 처리")
        print(f"총 교정 건수: {total_corrections}")

        if args.report == "json":
            import json
            print(json.dumps(results, ensure_ascii=False, indent=2, default=str))

    elif input_path.is_file():
        if args.preview:
            result = pipeline.preview(str(input_path))
        else:
            result = pipeline.proofread(
                str(input_path),
                output_path=args.output,
                save=True,
                report_format=args.report,
            )

        if not result.get("success"):
            print(f"오류: {result.get('error', '알 수 없는 오류')}")
            sys.exit(1)

        print(f"\n파일: {result['file']}")
        print(f"형식: {result['format']}")
        print(f"총 교정 건수: {result['total_corrections']}")

        if result.get("category_summary"):
            print("\n교정 유형별:")
            for cat, count in result["category_summary"].items():
                print(f"  {cat}: {count}건")

        if result.get("save_result", {}).get("success"):
            print(f"\n저장: {result['save_result']['output_file']}")

        if args.report != "text" and "report" in result:
            report_path = str(input_path.parent / f"{input_path.stem}_report.{args.report}")
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(result["report"])
            print(f"리포트: {report_path}")
        elif "report" in result:
            print(f"\n{result['report']}")

    else:
        print(f"입력 경로를 찾을 수 없습니다: {args.input}")
        sys.exit(1)


if __name__ == "__main__":
    main()
