"""Configuration management for HWP Ollama Autocorrect."""

import os
import json
from pathlib import Path
from typing import Optional


class Config:
    """Central configuration manager for the autocorrect system."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.

        Args:
            config_path: Path to config.local.md file. Defaults to
                        .claude-plugin/config.local.md in project root.
        """
        if config_path is None:
            project_root = Path(__file__).parent.parent
            config_path = project_root / ".claude-plugin" / "config.local.md"

        self.config_path = Path(config_path)
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from config.local.md file.

        Returns:
            Dictionary containing all configuration values.
        """
        config = {
            # Ollama settings
            "ollama_model": "Qwen/Qwen2.5-3B-Instruct",
            "lora_path": None,
            "chat_template": True,
            "temperature": 0.7,
            "max_new_tokens": 512,

            # HWP settings
            "hwp_text_extraction_method": "GetTextFile(TEXT, '')",

            # Correction settings
            "correction_threshold": 0.7,
            "preserve_formatting": True,
            "backup_before_correction": True,
            "backup_directory": None,

            # Report settings
            "report_format": "html",
            "report_highlight_color": "#ffeb3b",
            "include_statistics": True,
            "include_confidence_scores": True,

            # Batch settings
            "batch_directory": None,
            "output_directory": None,
            "file_pattern": "*.hwp",
            "max_files": 100,
            "pause_between_files": 10,
        }

        if not self.config_path.exists():
            return config

        # Parse config.local.md file
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                content = f.read()

            for line in content.split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")

                    # Parse value types
                    if value.isdigit():
                        config[key] = int(value)
                    elif value.replace(".", "").isdigit():
                        config[key] = float(value)
                    elif value.lower() == "true":
                        config[key] = True
                    elif value.lower() == "false":
                        config[key] = False
                    else:
                        config[key] = value

        except Exception as e:
            print(f"Warning: Could not load config from {self.config_path}: {e}")

        return config

    def get(self, key: str, default=None):
        """Get configuration value.

        Args:
            key: Configuration key.
            default: Default value if key not found.

        Returns:
            Configuration value or default.
        """
        return self._config.get(key, default)

    def get_ollama_model(self) -> str:
        """Get Ollama model name."""
        return self._config.get("ollama_model", "Qwen/Qwen2.5-3B-Instruct")

    def get_lora_path(self) -> Optional[str]:
        """Get LoRA model path."""
        return self._config.get("lora_path")

    def get_chat_template_enabled(self) -> bool:
        """Check if chat template is enabled."""
        return self._config.get("chat_template", True)

    def get_temperature(self) -> float:
        """Get generation temperature."""
        return self._config.get("temperature", 0.7)

    def get_max_new_tokens(self) -> int:
        """Get maximum new tokens."""
        return self._config.get("max_new_tokens", 512)

    def get_correction_threshold(self) -> float:
        """Get correction confidence threshold."""
        return self._config.get("correction_threshold", 0.7)

    def get_backup_directory(self) -> Optional[str]:
        """Get backup directory path."""
        return self._config.get("backup_directory")

    def get_batch_directory(self) -> Optional[str]:
        """Get batch processing directory."""
        return self._config.get("batch_directory")

    def get_output_directory(self) -> Optional[str]:
        """Get output directory for corrected files."""
        return self._config.get("output_directory")

    def save(self):
        """Save configuration to file."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write("# HWP Ollama Autocorrect Configuration\n\n")

            for key, value in self._config.items():
                if isinstance(value, bool):
                    f.write(f"{key}: {str(value).lower()}\n")
                elif isinstance(value, str) and " " in value:
                    f.write(f'{key}: "{value}"\n')
                else:
                    f.write(f"{key}: {value}\n")

    def update(self, **kwargs):
        """Update configuration values.

        Args:
            **kwargs: Key-value pairs to update.
        """
        self._config.update(kwargs)
        self.save()
