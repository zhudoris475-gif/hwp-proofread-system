# HWP Ollama Autocorrect Configuration

# Ollama settings
ollama_model: "Qwen/Qwen2.5-3B-Instruct"
# lora_path: null  # No compatible LoRA available
chat_template: true

# HWP settings
hwp_text_extraction_method: "GetTextFile(TEXT, '')"

# Correction settings
correction_threshold: 0.7  # Minimum confidence for corrections
preserve_formatting: true
backup_before_correction: true

# Report settings
report_format: "html"
report_highlight_color: "#ffeb3b"  # Yellow for corrections
include_statistics: true
include_confidence_scores: true
