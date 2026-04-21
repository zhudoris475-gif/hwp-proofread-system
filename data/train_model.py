# -*- coding: utf-8 -*-
"""
띄어쓰기 교정 모델 훈련 스크립트
조선어 규범집 기반 훈련 데이터

사용법:
1. Ollama로 훈련: ollama create spacing-model -f Modelfile
2. 또는 LoRA 파인튜닝 사용
"""

import json
import os

# 데이터 경로
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TRAIN_FILE = os.path.join(DATA_DIR, "spacing_correction_train.jsonl")
VALID_FILE = os.path.join(DATA_DIR, "spacing_correction_valid.jsonl")

def load_data(filepath):
    """JSONL 파일 로드"""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def create_modelfile():
    """Ollama Modelfile 생성"""
    modelfile = '''FROM llama3.2

# 띄어쓰기 교정 모델
# 조선어 규범집 기반

SYSTEM """당신은 조선어(한국어) 띄어쓰기 교정 전문가입니다.
주어진 문장의 띄어쓰기 오류를 수정하고, 필요시 규칙을 설명합니다.

규칙:
1. 고유명사는 붙여쓴다 (중화인민공화국, 연변대학)
2. 의존명사는 띄어쓴다 (것, 수, 바, 데, 줄, 만, 등)
3. 단위명사는 띄어쓴다 (개, 명, 마리, 권, 그루)
4. 보조용언은 띄어쓴다 (있다, 하다, 되다)
5. 조사는 앞말에 붙여쓴다
"""

PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
'''
    return modelfile

def create_ollama_training_data():
    """Ollama 훈련용 데이터 변환"""
    train_data = load_data(TRAIN_FILE)

    output_path = os.path.join(DATA_DIR, "ollama_training_data.jsonl")
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in train_data:
            ollama_item = {
                "system": "당신은 조선어 띄어쓰기 교정 전문가입니다.",
                "messages": [
                    {"role": "user", "content": item["instruction"] + "\n" + item.get("input", "")},
                    {"role": "assistant", "content": item["output"]}
                ]
            }
            f.write(json.dumps(ollama_item, ensure_ascii=False) + '\n')

    print(f"Ollama 훈련 데이터 생성: {len(train_data)}개")
    return output_path

def print_sample_data(n=5):
    """샘플 데이터 출력"""
    train_data = load_data(TRAIN_FILE)
    print(f"\n=== 훈련 데이터 샘플 ({n}개) ===\n")
    for i, item in enumerate(train_data[:n]):
        print(f"[{i+1}] 지시: {item['instruction']}")
        print(f"    입력: {item.get('input', '(없음)')}")
        print(f"    출력: {item['output'][:100]}...")
        print()

def main():
    print("=" * 60)
    print("띄어쓰기 교정 훈련 데이터 요약")
    print("=" * 60)

    # 데이터 로드
    train_data = load_data(TRAIN_FILE)
    valid_data = load_data(VALID_FILE)

    print(f"\n훈련 데이터: {len(train_data)}개")
    print(f"검증 데이터: {len(valid_data)}개")

    # 카테고리별 통계
    categories = {}
    for item in train_data:
        cat = item.get('metadata', {}).get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\n카테고리별 분포:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  - {cat}: {count}개")

    # 샘플 출력
    print_sample_data(3)

    # Ollama 훈련 데이터 생성
    ollama_path = create_ollama_training_data()
    print(f"\nOllama 훈련 데이터: {ollama_path}")

    # Modelfile 저장
    modelfile_path = os.path.join(DATA_DIR, "Modelfile")
    with open(modelfile_path, 'w', encoding='utf-8') as f:
        f.write(create_modelfile())
    print(f"Modelfile 저장: {modelfile_path}")

    print("\n" + "=" * 60)
    print("훈련 방법:")
    print("=" * 60)
    print("""
1. Ollama로 모델 생성:
   ollama create spacing-model -f Modelfile

2. 모델 테스트:
   ollama run spacing-model
   >>> 학교가다

3. LoRA 파인튜닝 (고급):
   unsloth 또는 transformers 라이브러리 사용
""")

if __name__ == "__main__":
    main()
