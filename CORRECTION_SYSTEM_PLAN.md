# 대중한사전 교정시스템 플랜 (Correction System Plan)

## 프로젝트 비전
대중한사전(大中朝) HWP 파일의 교정 작업을 자동화하고, 원본 내용 손실 없이 정확한 띄어쓰기/문장 교정을 수행하는 시스템 구축

---

## 1. 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    교정시스템 전체 구조                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력 계층]                                                │
│    HWP 파일 ──→ OLE 파서 ──→ 텍스트 추출 ──→ 정제           │
│                                                             │
│  [분석 계층]                                                │
│    정제 텍스트 ──→ 노이즈 필터 ──→ 변경 감지 ──→ 분류        │
│                                                             │
│  [교정 계층]                                                │
│    분류 결과 ──→ 띄어쓰기 교정 ──→ 내용 검증 ──→ 승인        │
│                                                             │
│  [출력 계층]                                                │
│    승인 결과 ──→ HWP 생성 ──→ 비교 리포트 ──→ 아카이브       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 모듈별 상세 설계

### 2.1 HWP 파서 모듈 (hwp_parser.py)

**기능**:
- OLE compound document 스트림 읽기
- BodyText/Section{N} zlib 압축 해제
- UTF-16-LE 디코딩 및 텍스트 추출
- 표제어 단위 파싱 (【...】 패턴)

**인터페이스**:
```python
class HWPParser:
    def extract_bodytext(filepath: str) -> str
    def parse_entries(text: str) -> list[DictEntry]
    def extract_section_info(text: str) -> SectionInfo
```

**처리 과정**:
1. olefile.OleFileIO로 HWP 파일 열기
2. BodyText/Section 스트림 순차 읽기
3. zlib.decompress로 압축 해제
4. UTF-16-LE 디코딩 (errors='ignore')
5. 【패턴】으로 표제어 분리

---

### 2.2 노이즈 필터 모듈 (noise_filter.py)

**기능**:
- U+XX00/U+XX04 패턴 노이즈 문자 탐지
- 빈도 기반 중국어 노이즈 문자 탐지
- 한국어 문자 화이트리스트 구축
- 알려진 노이즈 구문 제거

**인터페이스**:
```python
class NoiseFilter:
    def build_korean_whitelist(text: str) -> set[str]
    def detect_xx00_xx04_noise(text: str) -> set[str]
    def detect_chinese_noise(text: str, min_freq: int) -> set[str]
    def filter_text(text: str, noise_chars: set[str]) -> str
```

**노이즈 탐지 알고리즘**:

| 단계 | 방법 | 대상 | 임계값 |
|------|------|------|--------|
| 1 | U+XX00/XX04 | 한국어 | 화이트리스트 예외 30자 |
| 2 | 빈도 분석 | 중국어 | min_freq=100 |
| 3 | 의미 비율 | 중국어 구간 | ratio < 0.3 |
| 4 | 구문 매칭 | 전체 | KNOWN_NOISE_PHRASES |
| 5 | 단어 필터 | 한국어 | KNOWN_NOISE_WORDS |

**화이트리스트 예외 문자** (U+XX00/XX04이지만 실제 한국어):
```
가, 관, 글, 대, 밀, 쌀, 였, 저, 준, 케, 팀, 혀,
간, 누, 위, 전, 줄, 프, 현
```

---

### 2.3 변경 감지 모듈 (change_detector.py)

**기능**:
- 원본/교정본 표제어 비교
- 띄어쓰기 변경 vs 내용 변경 분류
- 중국어 단어 삭제/추가 감지
- kr_ratio 유사도 기반 노이즈 허용

**인터페이스**:
```python
class ChangeDetector:
    def classify_entry(orig: str, corr: str, heading: str) -> ChangeResult
    def compute_kr_ratio(orig: str, corr: str) -> float
    def detect_spacing_changes(orig_words: list, corr_words: list) -> list
    def detect_content_changes(orig_words: list, corr_words: list) -> list
```

**분류 로직**:

```
원본 텍스트 == 교정본 텍스트
    → 변경 없음

한국어 문자 유사도(kr_ratio) >= 0.94
    → 띄어쓰기 변경 (노이즈 허용)

한국어 문자 유사도(kr_ratio) < 0.94
    → 단어 분할 후 비교
        분할 결과 연결 문자열이 동일 → 띄어쓰기 변경
        분할 결과 연결 문자열이 다름 → 내용 변경
```

**kr_ratio 임계값 근거**:
- 0.94: HWP 노이즈로 인한 1~5개 문자 차이 허용
- 200자 기준 3개 노이즈 문자 = ratio ≈ 0.948
- 실제 내용 변경은 ratio < 0.90에서 발생

---

### 2.4 교정 엔진 모듈 (correction_engine.py)

**기능**:
- 띄어쓰기 규칙 기반 자동 교정
- 한국어 맞춤법 검사
- 교정 제안 생성
- 교정 이력 관리

**인터페이스**:
```python
class CorrectionEngine:
    def apply_spacing_rules(text: str) -> str
    def suggest_corrections(text: str) -> list[Correction]
    def validate_correction(orig: str, corrected: str) -> ValidationResult
    def generate_correction_report(results: list) -> str
```

**띄어쓰기 규칙 (한국어)**:

| 규칙 | 예시 | 설명 |
|------|------|------|
| 조사는 붙여 쓰기 | 사이에 → 사이에 | 조사는 앞 단어에 붙임 |
| 보조 용언은 띄어 쓰기 | 도와 주다 → 도와 주다 | 본용언+보조용언 |
| 의존 명사는 띄어 쓰기 | 것 이다 → 것이다 | 보조사는 붙임 |
| 단위 명사는 띄어 쓰기 | 두 개 → 두개 (명사) | 합성어는 붙임 |
| 전문 용어 | 데서, 가운데서 | 관용 표현은 붙임 |

---

### 2.5 리포트 생성 모듈 (report_generator.py)

**기능**:
- 복구 목록 생성 (우선순위별)
- 띄어쓰기 변경 상세 분석
- 중국어 삭제/추가 리포트
- 교정 이력 리포트

**출력 형식**:
- TXT: 상세 복구 목록
- JSON: 기계 판독용 결과
- HTML: 시각화 리포트

---

## 3. 교정 워크플로우

```
[1] HWP 파일 입력
    │
    ▼
[2] 텍스트 추출 및 정제
    │  ├── OLE 스트림 파싱
    │  ├── zlib 압축 해제
    │  └── 노이즈 필터링
    │
    ▼
[3] 표제어 단위 분리
    │  └── 【패턴】 매칭
    │
    ▼
[4] 원본-교정본 비교
    │  ├── kr_ratio 유사도 계산
    │  ├── 띄어쓰기 변경 감지
    │  ├── 내용 변경 감지
    │  └── 중국어 변경 감지
    │
    ▼
[5] 교정 제안 생성
    │  ├── 띄어쓰기 자동 교정
    │  ├── 내용 변경 검토 요청
    │  └── 중국어 복구 제안
    │
    ▼
[6] 승인 프로세스
    │  ├── 자동 승인 (띄어쓰기, kr_ratio >= 0.98)
    │  ├── 검토 필요 (내용 변경, 0.94 <= kr_ratio < 0.98)
    │  └── 수동 승인 (kr_ratio < 0.94)
    │
    ▼
[7] 결과 출력
    ├── 복구 목록 (hwp_recovery_list.txt)
    ├── 교정 리포트 (JSON/HTML)
    └── 아카이브 (Git 커밋)
```

---

## 4. 자동화 파이프라인

### 4.1 CI/CD 파이프라인

```yaml
# .github/workflows/correction-pipeline.yml
name: HWP Correction Pipeline

on:
  push:
    paths:
      - '*.hwp'
      - 'scripts/*.py'

jobs:
  extract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Extract HWP text
        run: python scripts/hwp_parser.py

  compare:
    needs: extract
    runs-on: ubuntu-latest
    steps:
      - name: Compare versions
        run: python scripts/change_detector.py

  report:
    needs: compare
    runs-on: ubuntu-latest
    steps:
      - name: Generate report
        run: python scripts/report_generator.py
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
```

### 4.2 품질 검증

| 검증 항목 | 방법 | 기준 |
|-----------|------|------|
| 노이즈 필터 정확도 | 수동 검증 | FP < 1% |
| 띄어쓰기 분류 정확도 | kr_ratio 검증 | 정확도 > 99% |
| 중국어 삭제 감지 | 전수 확인 | FN = 0 |
| 내용 변경 감지 | 수동 검토 | FP < 5% |

---

## 5. 데이터 관리

### 5.1 버전 관리 전략

```
main ──── 안정 버전 (검증 완료)
  │
  ├── develop ──── 개발 버전
  │     │
  │     ├── feature/noise-filter ──── 노이즈 필터 개선
  │     ├── feature/spacing-rules ──── 띄어쓰기 규칙 추가
  │     └── feature/chinese-detect ──── 중국어 감지 개선
  │
  └── hotfix ──── 긴급 수정
```

### 5.2 교정 이력 관리

```json
{
  "correction_id": "CORR-2026-0422-001",
  "timestamp": "2026-04-22T01:42:50",
  "original_file": "【大中朝 14】J 1419-1693--275--20240920.hwp",
  "corrected_file": "【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp",
  "total_entries": 4257,
  "spacing_changes": 279,
  "content_changes": 0,
  "deleted_chinese": 0,
  "approved_by": "zhudoris475-gif",
  "status": "verified"
}
```

---

## 6. 확장 계획

### Phase 1 (현재) — 기본 비교 시스템
- [x] HWP 텍스트 추출
- [x] 노이즈 필터링
- [x] 띄어쓰기/내용 변경 분류
- [x] 복구 목록 생성

### Phase 2 — 자동 교정 시스템
- [ ] 띄어쓰기 규칙 엔진 구현
- [ ] 한국어 맞춤법 검사 연동
- [ ] 자동 교정 제안 생성
- [ ] 승인/거부 워크플로우

### Phase 3 — AI 기반 교정
- [ ] LLM 기반 교정 제안 (Qwen/LoRA)
- [ ] 띄어쓰기 교정 모델 훈련
- [ ] 중국어-한국어 번역 검증
- [ ] 맞춤법 자동 교정

### Phase 4 — 통합 플랫폼
- [ ] 웹 기반 교정 인터페이스
- [ ] 실시간 협업 교정
- [ ] 버전 간 diff 시각화
- [ ] 교정 품질 대시보드

---

## 7. 기술 부채 및 개선 사항

| 항목 | 현재 상태 | 개선 방향 |
|------|----------|----------|
| kr_ratio 임계값 | 하드코딩 0.94 | 적응형 임계값 (텍스트 길이 기반) |
| 단어 분할 | 사전 기반 최장 일치 | 형태소 분석기 연동 (Mecab) |
| 노이즈 탐지 | 규칙 기반 | 머신러닝 기반 이상 탐지 |
| HWP 파싱 | 텍스트만 추출 | 서식/스타일 정보 보존 |
| 중국어 검증 | 빈도 기반 | 중국어 사전 연동 |

---

## 8. 참고 자료

- [HWP 파일 형식 분석](https://github.com/mete0r/pyhwp)
- [한국어 띄어쓰기 규정](https://korean.go.kr/kornorms/mainMain.do)
- [OLE Compound Document Format](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-cfb/)
- [SequenceMatcher 알고리즘](https://docs.python.org/3/library/difflib.html)
