# HWP Ollama Autonomous Correction Plugin

## Overview

This plugin provides autonomous sentence correction for Korean HWP (Hangul Word Processor) documents using the Ollama qwen2.5:3b model. The plugin automatically extracts text from HWP files, corrects sentences using AI, and generates detailed HTML reports.

## Features

- **Autonomous Correction**: Ollama automatically corrects sentences without manual intervention
- **HWP Integration**: Extract text from HWP files using OLE parsing
- **Batch Processing**: Process multiple HWP files automatically
- **HTML Reports**: Detailed reports showing corrections with highlighting
- **qwen2.5:3b Model**: Uses the trained LoRA model for high-accuracy corrections

## Installation

### Local Testing

```bash
cc --plugin-dir /path/to/hwp-ollama-autocorrect
```

### Project Testing

Copy the plugin to your project's `.claude-plugin/` directory.

## Prerequisites

- HWP (Hangul Word Processor) installed
- Ollama installed with qwen2.5:3b model
- Python 3.13 with required libraries:
  - pywin32 (win32com.client)
  - transformers
  - peft
  - torch

## Usage

### Skills

The plugin provides the following skills:

1. **ollama-autocorrect** - Main skill for autonomous sentence correction
2. **hwp-integration** - Extract text from HWP files
3. **batch-autocorrect** - Process multiple HWP files
4. **correction-report** - Generate HTML reports
5. **auto-config** - Configure plugin settings

### Example Usage

**Correct a single HWP file:**

```
Use the ollama-autocorrect skill to correct sentences in [filename.hwp]
```

**Batch process multiple files:**

```
Use the batch-autocorrect skill to process all HWP files in [directory]
```

**Generate a report:**

```
Use the correction-report skill to generate an HTML report for [filename.hwp]
```

## Configuration

Plugin settings are stored in `.claude-plugin/config.local.md`. Default configuration:

```markdown
# HWP Ollama Autocorrect Configuration

# Ollama settings
ollama_model: "Qwen/Qwen2.5-3B-Instruct"
lora_path: "C:/Users/51906/.agent-browser/round2_98percent_lora"
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
```

## Workflow

1. **Extract text** from HWP file using HWP COM automation
2. **Send text** to Ollama qwen2.5:3b model for correction
3. **Process corrections** with confidence scoring
4. **Reassemble** corrected text with original formatting
5. **Generate** HTML report with correction details

## Technical Details

### Text Extraction

Uses `GetTextFile("TEXT", "")` method to extract text from HWP files.

### Model Loading

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    trust_remote_code=True
)

base_model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    torch_dtype=torch.float32,
    device_map="cpu",
    trust_remote_code=True
)

model = PeftModel.from_pretrained(base_model, lora_path)
model.eval()
```

### Chat Template

Uses Qwen chat template for prompt formatting:

```python
messages = [
    {"role": "system", "content": "당신은 한국어 문장 교정 전문가입니다."},
    {"role": "user", "content": f"다음 문장의 띄어쓰기 오류를 수정하라.\n{text}"}
]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
```

## Troubleshooting

### SSL Errors

If you encounter SSL errors with Ollama:
1. Use VPN connection
2. Configure proxy settings
3. Use local cache

### Text Extraction Issues

If text extraction returns 0 characters:
- Verify HWP file is not password protected
- Check file path is correct
- Ensure HWP is installed and accessible

### Model Loading Issues

If model fails to load:
- Verify LoRA path is correct
- Check Python libraries are installed
- Ensure sufficient memory (CPU mode)

## Development

### Project Structure

```
hwp-ollama-autocorrect/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── ollama-autocorrect/
│   │   └── SKILL.md
│   ├── hwp-integration/
│   │   └── SKILL.md
│   ├── batch-autocorrect/
│   │   └── SKILL.md
│   ├── correction-report/
│   │   └── SKILL.md
│   └── auto-config/
│       └── SKILL.md
└── README.md
```

### Contributing

Contributions are welcome! Please follow these guidelines:
- Use kebab-case for all file names
- Include clear descriptions in SKILL.md files
- Test thoroughly before submitting
- Document any changes in this README

## License

MIT License - see LICENSE file for details
