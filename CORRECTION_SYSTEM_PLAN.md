# 대중한사전 교정시스템 플랜 (Correction System Plan)

## 프로젝트 비전
대중한사전(大中朝) HWP 파일의 교정 작업을 자동화하고, 원본 내용 손실 없이 정확한 띄어쓰기/문장 교정을 수행하는 시스템 구축

---

## 1. 시스템 아키텍처 (v2 — 모듈 구조화 완료)

```
┌──────────────────────────────────────────────────────────────────┐
│                    교정시스템 전체 구조 (v2)                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [진입점]                                                        │
│    run.py ── CLI 인터페이스 (compare / test / config)             │
│                                                                  │
│  [핵심 모듈: hwp_proofread/]                                     │
│    constants.py  ── 상수/설정 (COMMON_CHINESE, SECTIONS 등)       │
│    config.py     ── 싱글톤 설정 관리자                            │
│    hwp_io.py     ── HWP 파싱 + 텍스트 정제 + 노이즈 탐지          │
│    noise_filter.py ── 노이즈 필터 유틸리티                        │
│    change_detector.py ── 변경 감지 및 분류                        │
│                                                                  │
│  [AI 교정: ollama_editor/]                                       │
│    hwp_4stage_proofread.py ── 4단계 AI 교정                      │
│    src/app.py              ── Ollama 문서 편집기                  │
│    src/ollama_client.py    ── Ollama API 클라이언트               │
│                                                                  │
│  [레거시 스크립트: 루트 디렉토리]                                  │
│    compare_hwp.py ~ v8_final.py ── 비교 스크립트 발전 과정        │
│    generate_recovery_list.py ── 복구 목록 생성기                  │
│    final_correction_program.py ── 최종 교정 프로그램              │
│    modify_P_original.py ── P편 전용 교정                          │
│    system_test_all_sections.py ── 전체 섹션 테스트                │
│                                                                  │
│  [소스 모듈: src/]                                                │
│    config.py, file_processor.py, hwp_extractor.py                │
│    ollama_corrector.py, report_generator.py                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. 모듈 구조 (hwp_proofread/)

### 2.1 constants.py — 상수 정의

| 상수 | 설명 | 크기 |
|------|------|------|
| COMMON_CHINESE | 상위 500 빈도 중국어 문자 | 500자 |
| PINYIN_TONES | 병음 성조 기호 | 60자 |
| NOISE_WORDS | 알려진 노이즈 단어 | 7개 |
| KNOWN_NOISE_WORDS | 한국어 노이즈 단어 | 2개 |
| KR_XX00_XX04_WHITELIST | U+XX00/XX04 예외 문자 | 19자 |
| NOISE_PHRASES | 노이즈 구문 목록 | 10개 |
| CJK_RANGE | CJK 유니코드 범위 | (0x4E00, 0x9FFF) |
| KR_SYLLABLE | 한국어 음절 범위 | (0xAC00, 0xD7AF) |
| CONTENT_CHARS | 내용 문자 집합 | 50자 |
| SECTIONS | J~R편 파일 경로 정보 | 9섹션 |

### 2.2 hwp_io.py — HWP 파싱 및 텍스트 정제

**핵심 함수**:

| 함수 | 설명 |
|------|------|
| extract_bodytext_raw(filepath) | OLE→zlib→UTF-16-LE 텍스트 추출 |
| extract_meaningful_text(raw, noise, kr_wl, kr_noise) | 화이트리스트 기반 정제 |
| build_char_whitelist_from_words(orig, corr, min_freq) | 단어 빈도 기반 한국어 화이트리스트 |
| build_valid_word_set(orig, corr, min_freq) | 유효 한국어 단어 집합 |
| build_noise_char_set(text, threshold) | 빈도 기반 중국어 노이즈 탐지 |
| build_korean_noise_char_set(text, min_freq) | U+XX00/XX04 노이즈 탐지 |
| parse_entries(cleaned) | 【패턴】 표제어 분리 |
| is_real_chinese_word(word) | 중국어 단어 유효성 검증 |
| extract_chinese_words(text) | 유효 중국어 단어 추출 |
| extract_korean_words(text) | 유효 한국어 단어 추출 |

**정제 파이프라인**:
```
raw_text
  → 1차 중국어 노이즈 제거 (threshold=20)
  → 한국어 화이트리스트 필터링
  → U+XX00/XX04 노이즈 제거
  → 중국어 meaningful ratio 검사 (ratio >= 0.15)
  → 노이즈 구문 제거
  → 2차 중국어 노이즈 제거 (threshold=30)
  → 공백 정규화
```

### 2.3 noise_filter.py — 노이즈 필터 유틸리티

| 함수 | 설명 |
|------|------|
| is_common_cjk(ch) | 상위 500 중국어 문자 여부 |
| is_cjk(ch) | CJK 범위 문자 여부 |
| is_korean(ch) | 한국어 음절 여부 |
| detect_xx00_xx04_noise(text) | U+XX00/XX04 패턴 탐지 |
| detect_chinese_noise_chars(text, min_freq) | 빈도 기반 중국어 노이즈 |
| build_korean_whitelist(text) | 한국어 문자 화이트리스트 |
| filter_noise_text(text, noise_chars) | 노이즈 문자 제거 |

### 2.4 change_detector.py — 변경 감지

**분류 로직**:
```
원본 == 교정본 → 변경 없음

kr_ratio >= 0.94:
  → 한국어 단어 비교
  → 유효 단어만 추출 (valid_word_set)
  → SequenceMatcher로 띄어쓰기 변경 감지

kr_ratio < 0.94:
  → 단어 분할 (최장 일치)
  → 분할 결과 연결 문자열 비교
  → 동일 → 띄어쓰기 변경
  → 상이 → 내용 변경 (삭제/추가/수정)
```

### 2.5 config.py — 설정 관리

**싱글톤 패턴**으로 전역 설정 관리. `.claude-plugin/config.local.md`에서 사용자 설정 로드.

| 설정 키 | 기본값 | 설명 |
|---------|--------|------|
| ollama_model | Qwen/Qwen2.5-3B-Instruct | AI 모델 |
| ollama_api_url | http://localhost:11434/api | API 엔드포인트 |
| kr_ratio_threshold | 0.94 | 한국어 유사도 임계값 |
| chinese_noise_min_freq | 100 | 중국어 노이즈 최소 빈도 |
| temperature | 0.7 | 생성 온도 |
| max_new_tokens | 512 | 최대 토큰 수 |

---

## 3. CLI 인터페이스 (run.py)

```bash
# 단일 섹션 비교
python run.py compare J
python run.py compare L -o ./reports

# 전체 시스템 테스트
python run.py test

# 설정 확인
python run.py config
```

**compare 명령 처리 과정**:
```
[1/8] BodyText 원본 추출
[2/8] 단어 기반 한국어 문자 화이트리스트 구축
[3/8] 유효 한국어 단어 집합 구축
[4/8] U+XX00/XX04 노이즈 문자 탐지
[5/8] 중국어 노이즈 문자 탐지
[6/8] 텍스트 정제 (화이트리스트 기반 한국어 필터링)
[7/8] 사전 표제어 파싱 및 비교 분석
[8/8] 통계 집계
```

---

## 4. 교정 워크플로우

```
[1] HWP 파일 입력
    │
    ▼
[2] 텍스트 추출 및 정제
    │  ├── OLE 스트림 파싱 (hwp_io.extract_bodytext_raw)
    │  ├── 1차 노이즈 필터링 (hwp_io.build_noise_char_set)
    │  ├── 한국어 화이트리스트 구축 (hwp_io.build_char_whitelist_from_words)
    │  ├── U+XX00/XX04 노이즈 제거 (hwp_io.build_korean_noise_char_set)
    │  ├── 의미 비율 검사 (hwp_io.extract_meaningful_text)
    │  └── 2차 노이즈 필터링
    │
    ▼
[3] 표제어 단위 분리
    │  └── 【패턴】 매칭 (hwp_io.parse_entries)
    │
    ▼
[4] 원본-교정본 비교
    │  ├── kr_ratio 유사도 계산 (change_detector.classify_entry)
    │  ├── 띄어쓰기 변경 감지
    │  ├── 내용 변경 감지
    │  └── 중국어 변경 감지 (is_real_chinese_word)
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
    ├── 비교 리포트 (comparison_report_{section}.txt)
    ├── 교정 이력 (JSON)
    └── 아카이브 (Git 커밋)
```

---

## 5. J편 검증 결과 (2026-04-23)

| 항목 | 결과 |
|------|------|
| 원본 텍스트 | 3,019,159자 |
| 교정본 텍스트 | 3,018,544자 |
| 한국어 화이트리스트 | 1,023문자 |
| 유효 한국어 단어 | 8,616개 |
| U+XX00/XX04 노이즈 | 33개 |
| 1차 중국어 노이즈 | 1,305개 |
| 원본 표제어 | 4,257개 |
| 교정본 표제어 | 4,257개 |
| 완전 삭제된 표제어 | 0개 |
| 새로 추가된 표제어 | 0개 |
| 내용 변경된 표제어 | 2,321개 |
| 변경 없는 표제어 | 1,934개 |
| 띄어쓰기 변경 | 559개 |
| 실제 내용 변경 | 74개 |
| 삭제된 실제 중국어 단어 | 0개 |

---

## 6. 확장 계획

### Phase 1 (완료) — 기본 비교 시스템
- [x] HWP 텍스트 추출
- [x] 노이즈 필터링 (다단계)
- [x] 띄어쓰기/내용 변경 분류
- [x] 복구 목록 생성
- [x] 모듈 구조화 (hwp_proofread/)
- [x] CLI 인터페이스 (run.py)
- [x] 설정 관리 (config.py)

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
- [ ] 4단계 교정 시스템 (ollama_editor/hwp_4stage_proofread.py)

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
| 레거시 스크립트 | 루트 디렉토리 산재 | hwp_proofread/로 완전 통합 |
| src/ 모듈 | 독립 서브시스템 | hwp_proofread/와 통합 |

---

## 8. 파일 구조

```
c:\Users\doris\Desktop\text\
├── run.py                          # CLI 진입점
├── main.py                         # 레거시 메인 (src/ 기반)
├── hwp_proofread/                  # ★ 핵심 모듈 패키지
│   ├── __init__.py                 # 패키지 초기화
│   ├── constants.py                # 상수 정의
│   ├── config.py                   # 설정 관리 (싱글톤)
│   ├── hwp_io.py                   # HWP 파싱 + 텍스트 정제
│   ├── noise_filter.py             # 노이즈 필터 유틸리티
│   └── change_detector.py          # 변경 감지 및 분류
├── ollama_editor/                  # AI 교정 서브시스템
│   ├── hwp_4stage_proofread.py     # 4단계 교정
│   └── src/                        # Ollama 문서 편집기
├── src/                            # 레거시 소스 모듈
│   ├── config.py
│   ├── file_processor.py
│   ├── hwp_extractor.py
│   ├── ollama_corrector.py
│   └── report_generator.py
├── compare_hwp.py ~ v8_final.py    # 비교 스크립트 발전 과정
├── generate_recovery_list.py       # 복구 목록 생성기
├── final_correction_program.py     # 최종 교정 프로그램
├── modify_P_original.py            # P편 전용 교정
├── system_test_all_sections.py     # 전체 섹션 테스트
├── CORRECTION_SYSTEM_PLAN.md       # 본 문서
├── PROCESS_LOG.md                  # 과정 로그
└── .gitignore                      # Git 무시 규칙
```
