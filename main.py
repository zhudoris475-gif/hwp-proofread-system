"""Main entry point for HWP Ollama Autocorrect."""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.hwp_extractor import HWPExtractor
from src.ollama_corrector import OllamaCorrector
from src.file_processor import FileProcessor
from src.report_generator import ReportGenerator


def correct_single_file(
    hwp_file_path: str,
    config: Config,
    output_path: str = None,
    backup: bool = True,
) -> dict:
    """Correct a single HWP file.

    Args:
        hwp_file_path: Path to HWP file.
        config: Configuration object.
        output_path: Output file path (optional).
        backup: Whether to create backup.

    Returns:
        Correction result dictionary.
    """
    print(f"Processing: {hwp_file_path}")

    # Initialize components
    extractor = HWPExtractor()
    corrector = OllamaCorrector(
        model=config.get_ollama_model(),
        lora_path=config.get_lora_path(),
        chat_template=config.get_chat_template_enabled(),
        temperature=config.get_temperature(),
        max_new_tokens=config.get_max_new_tokens(),
    )
    file_processor = FileProcessor(backup_directory=config.get_backup_directory())
    report_generator = ReportGenerator(
        highlight_color=config.get("report_highlight_color", "#ffeb3b"),
        include_statistics=config.get("include_statistics", True),
        include_confidence_scores=config.get("include_confidence_scores", True),
    )

    # Extract text
    print("  Extracting text...")
    extraction = extractor.extract_with_analysis(hwp_file_path)

    if not extraction["success"]:
        return {
            "file": hwp_file_path,
            "status": "failed",
            "error": extraction.get("error", "Extraction failed"),
        }

    text = extraction["text"]
    analysis = extraction["analysis"]

    print(f"  Text length: {analysis['character_count']} characters")

    # Preprocess text
    clean_text = extractor.preprocess_text(text)

    # Generate correction
    print("  Generating correction...")
    corrections = corrector.correct_sentences(clean_text)

    if not corrections:
        return {
            "file": hwp_file_path,
            "status": "failed",
            "error": "No corrections generated",
        }

    # Reassemble text
    corrected_text = corrector.reassemble_text(corrections)

    # Save file
    print("  Saving corrected file...")
    if backup and config.get_backup_directory() or config.get("backup_before_correction"):
        backup_path = file_processor.create_backup(hwp_file_path)
        print(f"  Backup created: {backup_path}")

    output_file = file_processor.save_corrected_existing_file(
        hwp_file_path,
        corrected_text,
        backup=False,
    )

    # Calculate statistics
    stats = {
        "original_length": len(text),
        "corrected_length": len(corrected_text),
        "corrections": len(corrections),
        "original_words": analysis["word_count"],
        "corrected_words": len(corrected_text.split()),
    }

    print(f"  Corrections: {len(corrections)}")
    print(f"  Output: {output_file}")

    return {
        "file": hwp_file_path,
        "status": "success",
        "output_file": output_file,
        "statistics": stats,
        "corrections": corrections,
    }


def correct_batch(
    directory: str,
    config: Config,
    pattern: str = "*.hwp",
    max_files: int = 100,
) -> list:
    """Correct multiple HWP files in directory.

    Args:
        directory: Directory to process.
        config: Configuration object.
        pattern: File pattern.
        max_files: Maximum files to process.

    Returns:
        List of correction results.
    """
    import glob
    import time

    # Find files
    search_pattern = Path(directory) / pattern
    files = sorted(glob.glob(str(search_pattern)))

    # Limit files
    if max_files:
        files = files[:max_files]

    if not files:
        print(f"No HWP files found in {directory}")
        return []

    print(f"Found {len(files)} HWP files to process")

    # Process each file
    results = []
    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] {Path(file_path).name}")

        result = correct_single_file(file_path, config)
        results.append(result)

        # Pause between files
        if i < len(files):
            pause = config.get("pause_between_files", 10)
            print(f"  Pausing for {pause} seconds...")
            time.sleep(pause)

    # Generate report
    report_generator = ReportGenerator()
    report_path = report_generator.generate_html_report(
        results,
        output_dir=config.get_output_directory(),
    )

    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    print(f"\nBatch complete: {success}/{len(results)} files processed")
    print(f"Report saved to: {report_path}")

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="HWP Ollama Autocorrect - Korean HWP document correction"
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Input HWP file or directory",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file or directory",
    )
    parser.add_argument(
        "-b", "--batch",
        action="store_true",
        help="Batch mode (process directory)",
    )
    parser.add_argument(
        "-p", "--pattern",
        default="*.hwp",
        help="File pattern for batch mode",
    )
    parser.add_argument(
        "-m", "--max-files",
        type=int,
        default=100,
        help="Maximum files to process",
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to config file",
    )

    args = parser.parse_args()

    # Load configuration
    config = Config(args.config)

    if args.batch or (args.input and Path(args.input).is_dir()):
        # Batch mode
        correct_batch(
            directory=args.input or config.get_batch_directory() or ".",
            config=config,
            pattern=args.pattern,
            max_files=args.max_files,
        )
    elif args.input:
        # Single file mode
        result = correct_single_file(
            hwp_file_path=args.input,
            config=config,
            output_path=args.output,
        )

        if result["status"] == "success":
            print("\n✓ Correction complete!")
        else:
            print(f"\n✗ Failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
