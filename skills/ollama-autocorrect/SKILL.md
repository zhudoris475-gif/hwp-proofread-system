---
name: ollama-autocorrect
description: This skill should be used when the user asks to "correct sentences in HWP file", "autocorrect HWP document", "fix Korean sentences", "use Ollama to correct text", "autonomous sentence correction", or mentions HWP document correction with qwen2.5:3b model.
version: 1.0.0
---

# Ollama Autonomous Sentence Correction

This skill provides autonomous sentence correction for Korean text using the Ollama qwen2.5:3b model with LoRA fine-tuning.

## Overview

The skill automates the correction workflow:
1. Extract text from HWP file
2. Send text to Ollama qwen2.5:3b model
3. Process corrections with confidence scoring
4. Reassemble corrected text
5. Generate correction report

## Configuration

Load plugin configuration from `.claude-plugin/config.local.md`:

```python
config = {
    "ollama_model": "Qwen/Qwen2.5-3B-Instruct",
    "lora_path": "C:/Users/51906/.agent-browser/round2_98percent_lora",
    "chat_template": True,
    "correction_threshold": 0.7,
    "preserve_formatting": True,
    "backup_before_correction": True
}
```

## Workflow

### Step 1: Load Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load tokenizer (base model for chat template)
tokenizer = AutoTokenizer.from_pretrained(
    config["ollama_model"],
    trust_remote_code=True
)

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    config["ollama_model"],
    torch_dtype=torch.float32,
    device_map="cpu",
    trust_remote_code=True
)

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, config["lora_path"])
model.eval()
```

### Step 2: Prepare Correction Prompt

```python
messages = [
    {
        "role": "system",
        "content": "당신은 한국어 문장 교정 전문가입니다. 띄어쓰기, 맞춤법, 문법 오류를 자동으로 수정합니다."
    },
    {
        "role": "user",
        "content": f"다음 문장의 띄여쓰기 오류를 수정하라.\n{text}"
    }
]

# Apply chat template
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
```

### Step 3: Generate Correction

```python
inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
outputs = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.7,
    do_sample=True
)

# Extract corrected text
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
correction = generated_text[len(prompt):].strip()
```

### Step 4: Process Corrections

```python
def calculate_confidence(original, corrected):
    """Calculate confidence score for correction."""
    # Simple confidence calculation based on length difference
    original_len = len(original)
    corrected_len = len(corrected)

    # More corrections = potentially more errors
    length_diff = abs(corrected_len - original_len)
    correction_ratio = length_diff / max(original_len, 1)

    # Higher ratio = more changes = lower confidence
    confidence = 1.0 - min(correction_ratio, 0.5)

    return round(confidence, 2)

def generate_correction(sentence):
    """Generate correction for a single sentence using Ollama."""
    messages = [
        {
            "role": "system",
            "content": "당신은 한국어 문장 교정 전문가입니다. 띄어쓰기, 맞춤법, 문법 오류를 자동으로 수정합니다."
        },
        {
            "role": "user",
            "content": f"다음 문장의 띄여쓰기 오류를 수정하라.\n{sentence}"
        }
    ]

    # Apply chat template
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Generate correction
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True
    )

    # Extract corrected text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    correction = generated_text[len(prompt):].strip()

    return correction

# Split into sentences
sentences = text.split(".")

# Process each sentence
corrections = []
for sentence in sentences:
    if len(sentence.strip()) < 5:  # Skip short sentences
        continue

    # Generate correction for this sentence
    corrected_sentence = generate_correction(sentence)

    # Calculate confidence
    confidence = calculate_confidence(sentence, corrected_sentence)

    # Apply only if confidence above threshold
    if confidence >= config["correction_threshold"]:
        corrections.append({
            "original": sentence.strip(),
            "corrected": corrected_sentence.strip(),
            "confidence": confidence
        })

# Reassemble corrected text
corrected_text = ". ".join([c["corrected"] for c in corrections])
```

### Step 5: Save Corrected HWP

```python
import win32com.client as win32

hwp = win32.Dispatch("HwpBasic.HwpObject")
hwp.Open(hwp_file_path)

# Apply corrections using AllReplace API
hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
hwp.HParameterSet.HFindReplace.FindString = original_text
hwp.HParameterSet.HFindReplace.ReplaceString = corrected_text
hwp.HParameterSet.HFindReplace.Direction = 0
hwp.HParameterSet.HFindReplace.ReplaceMode = 2
hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)

# Save with backup if enabled
if config["backup_before_correction"]:
    backup_path = create_backup(hwp_file_path)
    log_message(f"Created backup: {backup_path}")

hwp.Save()
hwp.Close()
```

## Additional Resources

### Reference Files

- **`references/model_loading.py`** - Complete model loading code
- **`references/prompt_formatting.py`** - Prompt template examples
- **`references/correction_processing.py`** - Correction processing logic

### Example Files

- **`examples/correct_single_file.py`** - Complete single file correction workflow
- **`examples/correct_batch.py`** - Batch processing example

## Error Handling

Handle common errors:
- **Model loading errors**: Check LoRA path and Python libraries
- **Text extraction errors**: Verify HWP file is accessible
- **Generation errors**: Retry with lower temperature
- **Save errors**: Check file permissions and HWP installation

## Performance Notes

- CPU mode is slower (~2-5 seconds per file)
- For large files, consider processing in batches
- Model memory usage: ~6GB (float32)
