# HWP 교정 진행상황 (PROGRESS)

> 마지막 업데이트: 2026-04-19 (세션 재개용)
> 이 파일은 작업 진행 상태를 기록합니다. 세션이 끊겨도 여기서부터 재개 가능합니다.

---

## 🚨 현재 정지 위치: 3번 항목 (fix_missing_J.py 전면 재작성) 대기 중

### 다음에 해야 할 일 (바로 시작):
1. **fix_missing_J.py가 이미 재작성 완료됨** → 코드 검토만 필요
2. **전체 교정 재실행**: `python c:\Users\doris\.agent-skills\fix_missing_J.py`
3. **결과 확인 + HWP 열기 테스트**
4. **PROGRESS.md 업데이트**

---

## 전체 작업 진행표

| # | 항목 | 상태 | 완료일 | 비고 |
|---|------|------|--------|------|
| 0 | 기존 코드/규칙 분석 | ✅ 완료 | 04-18 | hwp_ollama_proofread.py 4단계 구조 파악 |
| 1 | PROGRESS.md 생성 | ✅ 완료 | 04-19 | 이 파일 |
| 2 | 원본 파일로 복구 (J+L) | ✅ 완료 | 04-18 | fix_missing_J.py가 원본에서 새로 복사 |
| 3 | fix_missing_J.py 전면 재작성 | ✅ 완료 | 04-19 | 4단계+가운데점+쌍따옴표+누락규칙+상세로그 |
| 4 | 전체 교정 재실행 | ⏳ 대기 | - | **← 여기서부터 재개** |
| 5 | 파일 확인 + HWP 열기 테스트 | ⏳ 대기 | - | |
| 6 | Git 커밋 | ⏳ 대기 | - | |

---

## fix_missing_J.py 현재 상태 (재작성 완료)

### 파일 위치
`c:\Users\doris\.agent-skills\fix_missing_J.py` (1005줄)

### 구조 요약
```
fix_missing_J.py
├── 상수/설정
│   ├── FILES: J, L 파일 경로 (원본→출력)
│   ├── RULES_FILE: rules_documentation.txt 경로
│   └── NOSPLIT 세트: 각 의존명사별 예외 목록
│
├── 유틸리티 함수
│   ├── file_hash(): SHA-256 해시
│   ├── verify_ole(): OLE 구조 검증
│   ├── verify_decompress(): 압축해제 검증
│   ├── extract_text(): HWP 텍스트 추출
│   └── parse_records(): HWP 레코드 파싱
│
├── 규칙 로드 함수
│   ├── load_china_place_rules(): 중한 규칙 로드
│   └── parse_txt_rules(): TXT 규칙 파싱
│
├── 4단계 규칙 생성 함수
│   ├── build_step1_rules(): 나라→조 + 지명/변환
│   ├── build_step2_rules(): TXT 통합규칙
│   ├── build_step3_rules(): 의존명사/누락규칙 (정규식)
│   └── build_step4_rules(): 가운데점 + 쌍따옴표
│
├── process_single_file(): 단일 파일 처리
│   ├── 사전검증 (OLE + 압축해제)
│   ├── 4단계 규칙 생성
│   ├── 백업 + OLE 스트림 수정
│   ├── 스트림 쓰기 + 출력 검증
│   ├── 교정 결과 검증
│   ├── 교정 상세 내역
│   ├── 미적용/유지 항목 상세
│   └── HWP 파일 열기 테스트
│
└── process_all(): 전체 실행 + 로그 저장
```

### 4단계 교정 내용
| 단계 | 내용 | 규칙 소스 |
|------|------|-----------|
| 1단계 | 나라→조 + 지명/변환 | rules_china_place.txt |
| 2단계 | TXT 통합규칙 | rules_documentation.txt |
| 3단계 | 의존명사/누락규칙 | 정규식 기반 (28개 패턴) |
| 4단계 | 가운데점(·→,) + 쌍따옴표(→홑따옴표) | 정규식 기반 |

### 3단계 의존명사 패턴 (28개)
것, 수, 따위, 사이, 뿐, 고있, 척, 이상, 밑, 등, 때, 때문, 번, 데, 지, 대로, 적, 만큼, 줄, 하, 듯, 채, 바, 터, 차례, 무렵, 듬, 두발

### NOSPLIT 예외 목록 (각 패턴별)
| 패턴 | 주요 예외 |
|------|-----------|
| 것 | 이것, 그것, 저것 |
| 수 | 장수, 교수, 척수, 실수, 침수, 할수록, 어쩔수, 얻을수, 볼수 등 (150+개) |
| 따위 | 따위의, 따위로, 따위를 |
| 사이 | 강사이, 수사이, 두사이 |
| 뿐 | 뿐만, 뿐이다 |
| 척 | 배척하다, 무척, 인척, 세척, 개척 (접두어 15개) |
| 이상 | 이상의, 이상하다 |
| 밑 | 밑바닥, 밑면 |
| 등 | 균등, 고등, 등산, 등록, 신호등 (70+개) |
| 때 | 제때, 그때, 한때 |
| 때문 | 때문에, 때문이다 |
| 번 | 이번, 한번, 순번, 빈번 (40+개) |
| 데 | 가운데, 포름알데, 한데 |
| 지 | 간지, 한지, 산지 |
| 대로 | 뜻대로, 마음대로, 그대로 |
| 적 | 간적, 본적 |
| 만큼 | 그만큼, 이만큼 |
| 줄 | 줄밖 |
| 하 | 산하, 강하 |
| 두발 | 두발 (머리카락 의미) |

---

## 대상 파일

| 라벨 | 원본 (src) | 출력 (out) |
|------|-----------|-----------|
| J | `C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_1st_copy.hwp` | `C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp` |
| L | `C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp` | `C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920_교정.hwp` |

### 백업 위치
`C:\Users\doris\Desktop\hwp_backup\`

### 로그 저장 위치
`C:\Users\doris\Desktop\한국어_문장_수정본_최종결과\교정로그_YYYYMMDD_HHMMSS.txt`

---

## 파일 열림 문제 원인 및 해결

### 원인
- 이전 출력파일: J trailing_nulls=622,028 / L trailing_nulls=364,156
- 원본파일: J trailing_nulls=1 / L trailing_nulls=1
- 압축 후 패딩한 null 바이트가 너무 많아 HWP가 파일을 손상으로 인식

### 해결방안 (현재 코드에 반영됨)
1. 압축 후 원본 스트림 크기에 맞게 null 패딩
2. 패딩 후 압축해제 검증 (verify_dec == new_dec 확인)
3. OLE 구조 검증 + 압축해제 검증 수행
4. 파일 해시 비교로 무결성 확인

---

## 과거 오류 이력

### 1. ValueError: write_stream data size mismatch
- **원인**: OLE 스트림 크기와 쓰는 데이터 크기 불일치
- **해결**: null 패딩으로 원본 스트림 크기에 맞춤 + 검증

### 2. COM 자동화 실패 (-2147024770)
- **원인**: HWP COM 모듈 로드 실패
- **해결**: subprocess.Popen으로 HWP 실행 파일 직접 호출 (fallback)

### 3. 파일 손상 (null 패딩 과다)
- **원인**: 압축 데이터 뒤에 너무 많은 null 바이트 패딩
- **해결**: 패딩 후 압축해제 검증 추가

---

## 실행 명령어

### 교정 실행 (4번 항목)
```powershell
cd c:\Users\doris\.agent-skills
python fix_missing_J.py
```

### 사전 확인 (olefile 설치 여부)
```powershell
pip install olefile
```

### 결과 확인
```powershell
# 로그 파일 확인
Get-ChildItem "C:\Users\doris\Desktop\한국어_문장_수정본_최종결과\교정로그_*.txt" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { Get-Content $_.FullName }
```

---

## 재시작 시 절차

1. **이 파일(PROGRESS.md)을 먼저 읽기**
2. "🚨 현재 정지 위치" 확인 → 현재는 **4번 항목 (전체 교정 재실행)**
3. "실행 명령어" 섹션의 명령어 실행
4. 실행 결과 확인:
   - OLE 구조 ✅ 인지 확인
   - 압축해제 ✅ 인지 확인
   - 교정 결과 검증 ✅ 인지 확인
   - HWP 열기 테스트 결과 확인
5. 로그 파일에서 상세 내용 확인
6. 각 항목 완료 후 이 파일의 진행표 업데이트
7. 문제 발생 시 "과거 오류 이력" 참고

---

## 의존성

### Python 패키지
- `olefile`: OLE 파일 조작 (필수)
- `zlib`: 압축/해제 (표준 라이브러리)
- `struct`: 바이너리 파싱 (표준 라이브러리)
- `hashlib`: 해시 계산 (표준 라이브러리)
- `re`: 정규식 (표준 라이브러리)
- `shutil`: 파일 복사 (표준 라이브러리)

### 외부 파일
- `C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt`: 중한 규칙
- `C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt`: 통합 규칙 (6425개)
- `C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\Hwp.exe`: HWP 실행 파일
