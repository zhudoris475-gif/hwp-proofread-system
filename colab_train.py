# Colab에서 실행하세요

# 1. 필요한 라이브러리 설치
!pip install transformers datasets torch -q

# 2. Google Drive 마운트 (파일 위치)
from google.colab import drive
drive.mount('/content/drive')

# 3. 훈련데이터 로드
import json

data_path = '/content/drive/MyDrive/spacing_train_data.jsonl'
with open(data_path, 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]

print(f'총 데이터: {len(data)}개')

# 4. 데이터 전처리
from transformers import BertTokenizerFast

tokenizer = BertTokenizerFast.from_pretrained('klue/bert-base')

# 훈련용 데이터 생성
train_texts = [item['original'] for item in data]
train_labels = [item['corrected'] for item in data]

# 5. 간단한 띄어쓰기 교정 모델 학습
# (여기서는 MLM로 사전학습 후 간단히演示)
from transformers import BertForMaskedLM, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from datasets import Dataset
import torch

# Dataset 생성
dataset = Dataset.from_dict({'text': train_texts})

def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, padding='max_length', max_length=128)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# 모델 준비
model = BertForMaskedLM.from_pretrained('klue/bert-base')

# 훈련 인자
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=2e-5,
    save_total_limit=1,
    logging_steps=100,
    report_to='none'
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# 훈련 시작
print('훈련 시작...')
trainer.train()

# 6. 모델 저장
model.save_pretrained('/content/drive/MyDrive/spacing_model')
tokenizer.save_pretrained('/content/drive/MyDrive/spacing_model')
print('모델 저장 완료!')
