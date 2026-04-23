# HWP 교정 시스템 - 발견 사항 & 연구 노트

## 📅 최종 업데이트: 2026-04-22

---

## 🔧 기술적 발견

### 1. Ollama 타임아웃 원인 (2026-04-22)

**문제:**
```
Retrying in 18 seconds… (attempt 10/10)
API_TIMEOUT_MS=600000ms (10분 x 10회 = 총 100분 대기)
```

**원인 분석:**
| 항목 | 값 |
|------|-----|
| Ollama 프로세스 | 실행 중 (PID 37228) |
| 포트 11434 | LISTENING |
| API 응답 | ❌ 응답 없음 |
| 모델 크기 | korean-corrector (6.2 GB) |
| **원인** | **메모리 부족 / 모델 로딩 멈춤** |

**해결:** 규칙 기반 스크립트로 우회 (Ollama 불필요)

---

### 2. HWP COM API Find() 매칭 문제

**문제:**
- COM Find() 메서드가 UTF-16 텍스트를 정확히 매칭하지 못함
- 31건 분석했으나 0건 적용

**해결 방안 (3가지):**

| 우선순위 | 방식 | 효과 |
|----------|------|------|
| ⭐ 1등 | **JS 매크로 AllReplace** | 한컴 내부 실행, 호환성 100% |
| 2등 | HWPX 변환 | XML 기반 수정 가능 |
| 3등 | COM Find() 디버깅 | 인코딩 문제 해결 필요 |

---

### 3. HWP 압축 포맷 호환성

**발견:**
- 원본 HWP: **HWP 전용 LZ77 압축** (0xA4 헤더)
- Python zlib: **표준 zlib** (0x78 헤더)
- 결과: 유효한 OLE2 파일이지만 한컴오피스에서 열리지 않음

**해결:** COM Automation으로 한컴 SaveAs 사용 → 원본 압축 유지

---

## 📋 규칙파일 구조 이해

### 규칙 함수 반환값

```python
# parse_rules(rules_file)
return rules, {src: dst for src, dst in rules}  # (list, dict)

# load_china_place_rules()
rules, rules_dict = parse_rules(CHINA_PLACE_FILE)
return rules, rules_dict  # (dict, dict)
```

> ⚠️ 주의: 튜플 언패킹 시 항상 2개 변수로 받아야 함!

---

## ✅ 교정 로직 검증 기준

### 삭제 vs 수정 구분

| 구분 | 조건 | 예시 | 판단 |
|------|------|------|------|
| **삭제 (정상)** | 규칙파일에 있음 + 원본에도 있음 | `저장성(절강성·浙江省)` → `절강성(浙江)` | ✅ |
| **수정 (정상)** | 규칙파일에 없음 → 다른 내용 변경 | `한것` → `한 것` | ✅ |
| **❌ 버그** | 규칙없이 내용이 사라짐 | - | 해당 없음 |

---

## 📊 성능 비교

| 방식 | 실행 시간 | 교정 건수 | 의존성 |
|------|----------|----------|--------|
| Ollama + COM | ~10분+ (타임아웃) | 27건 | Ollama 필수 |
| 규칙 + COM | ~30초 | 31건 (0건 적용) | Ollama 불필요 |
| **JS 매크로** | **~30초 (생성)** | **31건** | **Ollama 불필요** ⭐ |

---

## 🔗 관련 리소스

### 중요 경로
```
C:\Users\doris\Desktop\新词典\          # 원본 HWP
C:\Users\doris\Desktop\xwechat_files\WORD\  # 출력/리포트
C:\AMD\AJ\hwp_proofreading_package\      # 패키지
C:\Users\doris\.agent-skills\            # 작업 디렉토리
```

### 설정 파일
```
C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config\
├── rules.txt                    # TXT 규칙 (6889개)
├── rules_china_place.txt        # 중한 지명 규칙 (273개)
└── ...
```
