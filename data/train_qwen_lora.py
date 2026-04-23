# -*- coding: utf-8 -*-
"""
Qwen 2.5 7B 띄어쓰기 교정 모델 LoRA 파인튜닝
GPU 훈련 스크립트

요구사항:
- CUDA 지원 GPU (VRAM 16GB+ 권장)
- Python 3.10+
- PyTorch 2.0+

설치:
pip install torch transformers peft accelerate bitsandbytes datasets
"""

import json
import os
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)
from peft import LoraConfig, get_peft_model, TaskType

# 설정
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUTPUT_DIR = os.path.join(DATA_DIR, "qwen_spacing_model")
MAX_LENGTH = 512

def load_training_data():
    """훈련 데이터 로드"""
    train_path = os.path.join(DATA_DIR, "spacing_correction_train.jsonl")
    valid_path = os.path.join(DATA_DIR, "spacing_correction_valid.jsonl")

    def load_jsonl(path):
        data = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data

    train_data = load_jsonl(train_path)
    valid_data = load_jsonl(valid_path)

    print(f"훈련 데이터: {len(train_data)}개")
    print(f"검증 데이터: {len(valid_data)}개")

    return train_data, valid_data

def format_prompt(item):
    """프롬프트 포맷팅"""
    instruction = item["instruction"]
    input_text = item.get("input", "")

    if input_text:
        prompt = f"""<|im_start|>system
당신은 조선어(한국어) 띄어쓰기 교정 전문가입니다.<|im_end|>
<|im_start|>user
{instruction}
{input_text}<|im_end|>
<|im_start|>assistant
{item["output"]}<|im_end|>"""
    else:
        prompt = f"""<|im_start|>system
당신은 조선어(한국어) 띄어쓰기 교정 전문가입니다.<|im_end|>
<|im_start|>user
{instruction}<|im_end|>
<|im_start|>assistant
{item["output"]}<|im_end|>"""

    return prompt

def prepare_dataset(data, tokenizer):
    """데이터셋 준비"""
    prompts = [format_prompt(item) for item in data]

    def tokenize(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
            return_tensors="pt"
        )

    dataset = Dataset.from_dict({"text": prompts})
    tokenized_dataset = dataset.map(tokenize, batched=True, remove_columns=["text"])

    return tokenized_dataset

def main():
    print("=" * 60)
    print("Qwen 2.5 7B 띄어쓰기 교정 모델 파인튜닝")
    print("=" * 60)

    # GPU 확인
    print(f"\nCUDA 사용 가능: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

    # 토크나이저 로드
    print("\n토크나이저 로딩...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
        padding_side="right"
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 모델 로드 (4-bit 양자화)
    print("\n모델 로딩 (4-bit 양자화)...")
    from transformers import BitsAndBytesConfig

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )

    # LoRA 설정
    print("\nLoRA 설정...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"],
        bias="none",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # 데이터 로드
    print("\n데이터 로딩...")
    train_data, valid_data = load_training_data()

    train_dataset = prepare_dataset(train_data, tokenizer)
    valid_dataset = prepare_dataset(valid_data, tokenizer)

    # 훈련 설정
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        logging_steps=10,
        eval_steps=100,
        save_steps=500,
        learning_rate=2e-4,
        fp16=True,
        optim="paged_adamw_8bit",
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
    )

    # 트레이너 생성
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        tokenizer=tokenizer,
    )

    # 훈련 시작
    print("\n훈련 시작...")
    trainer.train()

    # 모델 저장
    print("\n모델 저장...")
    model.save_pretrained(os.path.join(OUTPUT_DIR, "lora_adapter"))
    tokenizer.save_pretrained(OUTPUT_DIR)

    print(f"\n완료! 모델 저장 위치: {OUTPUT_DIR}")
    print("\n사용법:")
    print("""
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# 기본 모델 로드
base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")

# LoRA 어댑터 로드
model = PeftModel.from_pretrained(base_model, "path/to/lora_adapter")

# 추론
prompt = "다음 문장의 띄어쓰기 오류를 수정하라.\\n학교가다"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=100)
print(tokenizer.decode(outputs[0]))
""")

if __name__ == "__main__":
    main()
