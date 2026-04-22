"""Ollama-based text correction using LoRA fine-tuned model."""

import time
import torch
from typing import Optional, List, Dict, Any
from pathlib import Path


class OllamaCorrector:
    """Correct Korean text using Ollama qwen2.5:3b with LoRA."""

    def __init__(
        self,
        model: str = "Qwen/Qwen2.5-3B-Instruct",
        lora_path: Optional[str] = None,
        chat_template: bool = True,
        temperature: float = 0.7,
        max_new_tokens: int = 512,
    ):
        """Initialize Ollama corrector.

        Args:
            model: Base model name.
            lora_path: Path to LoRA adapter.
            chat_template: Whether to use chat template.
            temperature: Generation temperature.
            max_new_tokens: Maximum tokens to generate.
        """
        self.model_name = model
        self.lora_path = lora_path
        self.chat_template = chat_template
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens

        self._model = None
        self._tokenizer = None

    def load_model(self) -> bool:
        """Load the model and tokenizer.

        Returns:
            True if loading successful, False otherwise.
        """
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            from peft import PeftModel

            # Load tokenizer (base model for chat template)
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
            )

            # Load base model
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True,
            )

            # Load LoRA adapter if provided
            if self.lora_path and Path(self.lora_path).exists():
                lora_config_path = Path(self.lora_path) / "adapter_config.json"
                if lora_config_path.exists():
                    # It's a LoRA adapter
                    self._model = PeftModel.from_pretrained(
                        self._model,
                        self.lora_path,
                    )
                    print(f"Loaded LoRA adapter from {self.lora_path}")
                else:
                    # It's a full model, try to load it directly
                    print(f"Loading full model from {self.lora_path}")
                    self._model = AutoModelForCausalLM.from_pretrained(
                        self.lora_path,
                        torch_dtype="auto",
                        device_map="auto",
                        trust_remote_code=True,
                    )

            self._model.eval()
            return True

        except Exception as e:
            print(f"Failed to load model: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_correction(self, text: str) -> str:
        """Generate correction for text using v2 extraction method.

        Args:
            text: Input text to correct.

        Returns:
            Corrected text.
        """
        return self.generate_correction_v2(text)

    def generate_correction_v2(self, text: str) -> str:
        """Generate correction for text (v2 - more robust extraction).

        Args:
            text: Input text to correct.

        Returns:
            Corrected text.
        """
        # Ensure model is loaded
        if self._model is None:
            if not self.load_model():
                return text

        # Prepare prompt
        messages = [
            {
                "role": "system",
                "content": "당신은 한국어 문장 교정 전문가입니다. 띄어쓰기, 맞춤법, 문법 오류를 자동으로 수정합니다.",
            },
            {
                "role": "user",
                "content": f"다음 문장의 띄어쓰기 오류를 수정하라.\n{text}",
            },
        ]

        # Apply chat template
        if self.chat_template and self._tokenizer:
            prompt = self._tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        else:
            prompt = f"System: 당신은 한국어 문장 교정 전문가입니다.\n\nUser: 다음 문장의 띄어쓰기 오류를 수정하라.\n{text}\n\nAssistant:"

        # Generate input
        inputs = self._tokenizer(prompt, return_tensors="pt")

        # Move to device
        device = self._model.device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Get prompt token length
        prompt_len = inputs["input_ids"].shape[1]

        # Generate correction
        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self._tokenizer.eos_token_id,
            )

        # Extract only the new tokens (after prompt)
        new_tokens = outputs[0, prompt_len:]
        correction = self._tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

        return correction

    def is_model_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._model is not None and self._tokenizer is not None

    def unload_model(self):
        """Unload model to free memory."""
        if self._model is not None:
            del self._model
            self._model = None
        if self._tokenizer is not None:
            del self._tokenizer
            self._tokenizer = None
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

    def correct_sentences(self, text: str) -> List[Dict[str, Any]]:
        """Correct text sentence by sentence.

        Args:
            text: Input text.

        Returns:
            List of correction results.
        """
        # Split into sentences (Korean uses . and ...)
        import re

        sentences = re.split(r"([.。]+)", text)

        # Pair sentences with delimiters
        pairs = []
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i].strip()
            delimiter = sentences[i + 1] if i + 1 < len(sentences) else "."
            if sentence:
                pairs.append((sentence, delimiter))

        results = []

        for sentence, delimiter in pairs:
            if len(sentence) < 5:  # Skip short sentences
                continue

            corrected = self.generate_correction(sentence)
            confidence = self._calculate_confidence(sentence, corrected)

            results.append({
                "original": sentence,
                "corrected": corrected,
                "delimiter": delimiter,
                "confidence": confidence,
            })

        return results

    def _calculate_confidence(self, original: str, corrected: str) -> float:
        """Calculate confidence score for correction.

        Uses multiple factors:
        - Length difference ratio
        - Character overlap
        - Correction patterns

        Args:
            original: Original text.
            corrected: Corrected text.

        Returns:
            Confidence score between 0 and 1.
        """
        # Length difference ratio
        original_len = len(original)
        corrected_len = len(corrected)

        if original_len == 0:
            return 1.0

        length_diff = abs(corrected_len - original_len)
        length_ratio = length_diff / original_len

        # Character overlap (simple Jaccard-like)
        original_chars = set(original)
        corrected_chars = set(corrected)
        intersection = len(original_chars & corrected_chars)
        union = len(original_chars | corrected_chars)
        overlap_ratio = intersection / union if union > 0 else 0

        # Confidence calculation
        # Penalize large changes, reward high overlap
        length_penalty = min(length_ratio * 2, 0.5)  # Max 0.5 penalty
        confidence = (1.0 - length_penalty) * overlap_ratio

        return round(max(0.0, min(1.0, confidence)), 2)

    def reassemble_text(self, corrections: List[Dict[str, Any]]) -> str:
        """Reassemble corrected sentences into text.

        Args:
            corrections: List of correction results.

        Returns:
            Assembled corrected text.
        """
        parts = []
        for correction in corrections:
            parts.append(correction["corrected"] + correction["delimiter"])

        return "".join(parts)

    def close(self):
        """Release model resources."""
        self._model = None
        self._tokenizer = None
