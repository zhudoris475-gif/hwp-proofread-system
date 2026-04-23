---
name: auto-config
description: This skill should be used when the user asks to "configure plugin settings", "set Ollama model path", "configure HWP settings", "change correction threshold", "customize plugin configuration", or mentions configuring the HWP Ollama autocorrect plugin.
version: 1.0.0
---

# Plugin Auto-Configuration

This skill provides configuration management for the HWP Ollama Autocorrect plugin, allowing users to customize settings for Ollama model, HWP integration, correction behavior, and report generation.

## Overview

Configure the plugin using the `.claude-plugin/config.local.md` file. This skill helps users:
- Set Ollama model paths and settings
- Configure HWP text extraction methods
- Adjust correction thresholds and behavior
- Customize report generation options
- Manage batch processing settings

## Configuration File

The plugin configuration is stored in `.claude-plugin/config.local.md`:

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

## Configuration Sections

### Ollama Settings

Configure the Ollama model and LoRA adapter:

```yaml
# Ollama settings
ollama_model: "Qwen/Qwen2.5-3B-Instruct"  # Base model path
lora_path: "C:/Users/51906/.agent-browser/round2_98percent_lora"  # LoRA adapter path
chat_template: true  # Use Qwen chat template for prompts
```

**Options:**
- `ollama_model`: Path to base model (Qwen/Qwen2.5-3B-Instruct recommended)
- `lora_path`: Path to LoRA adapter (for fine-tuned corrections)
- `chat_template`: Whether to use chat template for prompt formatting

### HWP Settings

Configure HWP file integration:

```yaml
# HWP settings
hwp_text_extraction_method: "GetTextFile(TEXT, '')"
```

**Options:**
- `hwp_text_extraction_method`: Method for extracting text from HWP files
  - `"GetTextFile(TEXT, '')"` - Plain text extraction (recommended)
  - `"GetTextFile(TEXT, 'CP949')"` - Korean encoding
  - `"GetTextFile(TEXT, '', 0, 1000)"` - Extract first 1000 characters

### Correction Settings

Configure correction behavior:

```yaml
# Correction settings
correction_threshold: 0.7  # Minimum confidence for corrections
preserve_formatting: true  # Preserve original formatting
backup_before_correction: true  # Create backup before saving
```

**Options:**
- `correction_threshold`: Minimum confidence score (0.0-1.0) for applying corrections
  - Higher values = fewer but more confident corrections
  - Lower values = more corrections (may include errors)
- `preserve_formatting`: Whether to preserve HWP formatting when saving
- `backup_before_correction`: Create timestamped backup before saving corrected file

### Report Settings

Configure report generation:

```yaml
# Report settings
report_format: "html"  # Report format (html, markdown, csv)
report_highlight_color: "#ffeb3b"  # Color for highlighting corrections
include_statistics: true  # Include statistics in reports
include_confidence_scores: true  # Include confidence scores
```

**Options:**
- `report_format`: Output format for reports
  - `"html"` - Web browser compatible (recommended)
  - `"markdown"` - Markdown documentation
  - `"csv"` - Data analysis format
- `report_highlight_color`: HTML color code for highlighting corrections (hex format)
- `include_statistics`: Include summary statistics in reports
- `include_confidence_scores`: Include confidence scores for each correction

## Configuration Management

### Loading Configuration

```python
import yaml
import os

def load_config(config_path=".claude-plugin/config.local.md"):
    """Load plugin configuration from file."""
    if not os.path.exists(config_path):
        return get_default_config()

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config

def get_default_config():
    """Get default configuration."""
    return {
        "ollama_model": "Qwen/Qwen2.5-3B-Instruct",
        "lora_path": "C:/Users/51906/.agent-browser/round2_98percent_lora",
        "chat_template": True,
        "hwp_text_extraction_method": "GetTextFile(TEXT, '')",
        "correction_threshold": 0.7,
        "preserve_formatting": True,
        "backup_before_correction": True,
        "report_format": "html",
        "report_highlight_color": "#ffeb3b",
        "include_statistics": True,
        "include_confidence_scores": True
    }
```

### Saving Configuration

```python
def save_config(config, config_path=".claude-plugin/config.local.md"):
    """Save plugin configuration to file."""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

    log_message(f"Configuration saved to {config_path}")
```

### Validating Configuration

```python
def validate_config(config):
    """Validate plugin configuration."""
    issues = []

    # Validate Ollama settings
    if "ollama_model" not in config:
        issues.append("Missing ollama_model setting")

    if "lora_path" not in config:
        issues.append("Missing lora_path setting")

    # Validate correction threshold
    if "correction_threshold" in config:
        threshold = config["correction_threshold"]
        if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 1:
            issues.append("correction_threshold must be between 0 and 1")

    # Validate report format
    if "report_format" in config:
        valid_formats = ["html", "markdown", "csv"]
        if config["report_format"] not in valid_formats:
            issues.append(f"report_format must be one of {valid_formats}")

    # Validate highlight color
    if "report_highlight_color" in config:
        color = config["report_highlight_color"]
        if not (color.startswith("#") and len(color) == 7):
            issues.append("report_highlight_color must be hex color code (e.g., #ffeb3b)")

    return issues

def apply_config(config):
    """Apply configuration settings."""
    # Validate
    issues = validate_config(config)
    if issues:
        log_error(f"Configuration validation failed: {issues}")
        return False

    # Save configuration
    save_config(config)

    # Log settings
    log_message("Configuration applied successfully:")
    log_message(f"  - Ollama model: {config.get('ollama_model', 'Not set')}")
    log_message(f"  - LoRA path: {config.get('lora_path', 'Not set')}")
    log_message(f"  - Correction threshold: {config.get('correction_threshold', 'Not set')}")
    log_message(f"  - Report format: {config.get('report_format', 'Not set')}")

    return True
```

## Configuration Examples

### Example 1: High Confidence Corrections

```yaml
# For conservative corrections (only confident changes)
correction_threshold: 0.9
backup_before_correction: true
preserve_formatting: true
```

### Example 2: Aggressive Corrections

```yaml
# For more corrections (may include some errors)
correction_threshold: 0.5
backup_before_correction: true
preserve_formatting: false
```

### Example 3: Markdown Reports

```yaml
report_format: "markdown"
report_highlight_color: "#ffff00"
include_statistics: true
include_confidence_scores: true
```

### Example 4: Batch Processing

```yaml
batch_directory: "./documents/"
output_directory: "./corrected/"
file_pattern: "*.hwp"
max_files: 50
pause_between_files: 10
```

## Additional Resources

### Reference Files

- **`references/config_validation.py`** - Configuration validation code
- **`references/config_examples.py`** - Configuration examples
- **`references/config_types.py`** - Type definitions and schemas

### Example Files

- **`examples/config_high_confidence.py`** - High confidence configuration example
- **`examples/config_batch_processing.py`** - Batch processing configuration example
- **`examples/validate_config.py`** - Configuration validation example

## Troubleshooting

### Configuration Not Loading

If configuration is not loading:
1. Check file exists at `.claude-plugin/config.local.md`
2. Verify YAML syntax is correct
3. Check file encoding (UTF-8)
4. Restart Claude Code to reload configuration

### Invalid Configuration Values

If you see validation errors:
1. Review the error messages carefully
2. Check configuration value types (int, float, string)
3. Verify ranges (e.g., threshold between 0 and 1)
4. Check format requirements (hex color code, etc.)

### Model Path Issues

If Ollama model path is incorrect:
1. Verify the path exists on your system
2. Check if the model is downloaded
3. Ensure proper permissions
4. Use absolute paths for reliability
