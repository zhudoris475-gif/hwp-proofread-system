import os
import json
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / '.claude-plugin'
CONFIG_FILE = CONFIG_DIR / 'config.local.md'


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = cls._instance._load_defaults()
            cls._instance._load_from_file()
        return cls._instance

    @staticmethod
    def _load_defaults():
        return {
            'ollama_model': 'Qwen/Qwen2.5-3B-Instruct',
            'lora_path': None,
            'chat_template': True,
            'temperature': 0.7,
            'max_new_tokens': 512,
            'ollama_api_url': 'http://localhost:11434/api',
            'hwp_text_extraction_method': 'GetTextFile(TEXT, "")',
            'correction_threshold': 0.7,
            'preserve_formatting': True,
            'backup_before_correction': True,
            'backup_directory': None,
            'report_format': 'html',
            'report_highlight_color': '#ffeb3b',
            'include_statistics': True,
            'include_confidence_scores': True,
            'batch_directory': None,
            'output_directory': None,
            'file_pattern': '*.hwp',
            'max_files': 100,
            'pause_between_files': 10,
            'kr_ratio_threshold': 0.94,
            'chinese_noise_min_freq': 100,
            'log_directory': str(PROJECT_ROOT),
        }

    def _load_from_file(self):
        if not CONFIG_FILE.exists():
            return
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if value.lower() in ('true', 'false'):
                        value = value.lower() == 'true'
                    elif value.isdigit():
                        value = int(value)
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                    self._config[key] = value
        except Exception:
            pass

    def get(self, key, default=None):
        return self._config.get(key, default)

    def set(self, key, value):
        self._config[key] = value

    @property
    def ollama_model(self):
        return self._config['ollama_model']

    @property
    def ollama_api_url(self):
        return self._config['ollama_api_url']

    @property
    def kr_ratio_threshold(self):
        return self._config['kr_ratio_threshold']

    @property
    def log_directory(self):
        return self._config['log_directory']

    def get_ollama_model(self):
        return self._config['ollama_model']

    def get_lora_path(self):
        return self._config.get('lora_path')

    def get_chat_template_enabled(self):
        return self._config.get('chat_template', True)

    def get_temperature(self):
        return self._config.get('temperature', 0.7)

    def get_max_new_tokens(self):
        return self._config.get('max_new_tokens', 512)

    def get_backup_directory(self):
        return self._config.get('backup_directory')
