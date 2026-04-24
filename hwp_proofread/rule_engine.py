import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class RuleEngine:
    def __init__(self, rules_dir: Optional[str] = None):
        self._rules: Dict[str, List[Tuple[str, str]]] = {}
        self._regex_rules: List[Tuple[str, re.Pattern, str]] = []
        if rules_dir:
            self.load_rules_dir(rules_dir)

    def load_rules_dir(self, rules_dir: str):
        rules_path = Path(rules_dir)
        if not rules_path.exists():
            return
        for rule_file in rules_path.glob("*.txt"):
            self.load_rule_file(str(rule_file))

    def load_rule_file(self, file_path: str, category: Optional[str] = None):
        path = Path(file_path)
        if not path.exists():
            return
        if category is None:
            category = path.stem

        rules = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "->" in line:
                    parts = line.split("->", 1)
                    src = parts[0].strip()
                    dst = parts[1].strip()
                    if src and dst:
                        rules.append((src, dst))

        if rules:
            self._rules[category] = rules

    def add_regex_rule(self, name: str, pattern: str, replacement: str):
        compiled = re.compile(pattern)
        self._regex_rules.append((name, compiled, replacement))

    def load_regex_rules(self, file_path: str):
        path = Path(file_path)
        if not path.exists():
            return
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "->" in line:
                    parts = line.split("->", 1)
                    pattern = parts[0].strip()
                    replacement = parts[1].strip()
                    if pattern and replacement:
                        try:
                            compiled = re.compile(pattern)
                            self._regex_rules.append((pattern, compiled, replacement))
                        except re.error:
                            pass

    def apply_rules(self, text: str, categories: Optional[List[str]] = None) -> Tuple[str, List[Dict]]:
        corrections = []
        result = text

        cats = categories if categories else list(self._rules.keys())
        for cat in cats:
            if cat not in self._rules:
                continue
            for src, dst in self._rules[cat]:
                count = result.count(src)
                if count > 0:
                    result = result.replace(src, dst)
                    corrections.append({
                        "category": cat,
                        "type": "replace",
                        "original": src,
                        "corrected": dst,
                        "count": count,
                    })

        for name, pattern, replacement in self._regex_rules:
            matches = list(pattern.finditer(result))
            if matches:
                new_result = pattern.sub(replacement, result)
                if new_result != result:
                    result = new_result
                    corrections.append({
                        "category": "regex",
                        "type": "regex",
                        "original": name,
                        "corrected": replacement,
                        "count": len(matches),
                    })

        return result, corrections

    def preview_rules(self, text: str, categories: Optional[List[str]] = None) -> List[Dict]:
        _, corrections = self.apply_rules(text, categories)
        return corrections

    @property
    def categories(self) -> List[str]:
        return list(self._rules.keys())

    @property
    def total_rules(self) -> int:
        count = sum(len(rules) for rules in self._rules.values())
        count += len(self._regex_rules)
        return count

    def get_rule_count(self, category: str) -> int:
        if category == "regex":
            return len(self._regex_rules)
        return len(self._rules.get(category, []))
