# fix_J_record.py 단일 파일 수정 플랜

## 파일 개요
- **파일**: `c:\Users\doris\.agent-skills\fix_J_record.py`
- **총 라인수**: 1250줄
- **목적**: HWP 파일(L파일) 레코드 단위 띄어쓰기 교정
- **입력**: 원본 HWP → **출력**: 교정된 HWP + 상세 로그

---

## 아키텍처 구조도

```
fix_J_record.py (1250줄)
│
├── [1] 설정 및 상수 (L1-L14)
│   ├── import (sys, os, time, re, struct, zlib, shutil, hashlib, stat, olefile, Counter)
│   ├── 경로 상수 (SRC, OUT, OUT_TMP, BACKUP_DIR, LOG_DIR, RULES_FILE)
│
├── [2] NOSPLIT 예외 사전 (L15-L479) ← 핵심 데이터 영역
│   ├── GEOT_NOSPLIT       (L16)     것 관련 합성어
│   ├── SU_NOSPLIT         (L17-L50) 수 관련 합성어 (130+개)
│   ├── TTAWI_NOSPLIT      (L52)     따위 관련
│   ├── SAI_NOSPLIT        (L53)     사이 관련
│   ├── PPUN_NOSPLIT       (L54)     뿐 관련
│   ├── CHUK_NOSPLIT_PREFIXES (L56)  척 접두사
│   ├── CHUK_NOSPLIT       (L57-L88) 척 관련 합성어 (80+개)
│   ├── ISANG_NOSPLIT      (L89)     이상 관련
│   ├── MIT_NOSPLIT        (L90)     밑 관련
│   ├── DEUNG_NOSPLIT      (L91-L110)등 관련 합성어 (60+개)
│   ├── TTE_NOSPLIT        (L111)    때 관련
│   ├── TTAE_MUN_NOSPLIT   (L112)    때문 관련
│   ├── BEON_NOSPLIT       (L113-L131)번 관련 합성어 (40+개)
│   ├── DE_NOSPLIT         (L132-L150)데 관련 합성어 (40+개)
│   ├── DAERO_NOSPLIT      (L151-L165)대로 관련 합성어 (30+개)
│   ├── MANKEUM_NOSPLIT    (L166)    만큼 관련
│   ├── JUL_NOSPLIT        (L167-L197)줄 관련 합성어 (100+개)
│   ├── TEO_NOSPLIT        (L198-L260)터 관련 합성어 (80+개)
│   ├── CHAE_NOSPLIT       (L261-L316)채 관련 합성어 (90+개)
│   ├── BA_NOSPLIT         (L261-L286)바 관련 합성어 (40+개)
│   ├── IHA_NOSPLIT        (L287-L323)이하 관련 합성어 (40+개)
│   ├── JUNG_NOSPLIT       (L324-L362)중 관련 합성어 (60+개)
│   ├── SANG_NOSPLIT       (L363-L382)상 관련 합성어 (50+개)
│   ├── U_NOSPLIT          (L383-L422)우 관련 합성어 (60+개)
│   ├── HA_NOSPLIT         (L423-L467)하 관련 합성어 (70+개)
│   ├── GAT_NOSPLIT        (L468-L471)같은 관련
│   └── GO_NOSPLIT         (L474-L479)고+동사 관련
│
├── [3] 유틸리티 함수 (L481-L600)
│   ├── file_hash()           (L481) SHA-256 해시 계산
│   ├── parse_records()       (L489) HWP 레코드 파싱 (tag_id, level, size, payload)
│   ├── rebuild_stream()      (L518) 레코드 → 바이트 스트림 재구성
│   ├── extract_text_from_records() (L533) 레코드에서 텍스트 추출 (tag_id=67)
│   ├── extract_text()        (L545) HWP 파일 → 전체 텍스트 추출
│   ├── load_china_place_rules() (L563) 중한 지명 규칙 파일 로드
│   └── parse_txt_rules()     (L583) TXT 통합규칙 파일 파싱
│
├── [4] 교정 규칙 엔진 (L602-L835) ← 핵심 로직 영역
│   ├── apply_text_corrections() (L602) 메인 교정 함수
│   │   ├── add() 내부함수 (L605) 변경사항 등록
│   │   ├── has_suitable_ending() (L616) 수 앞 종성 체크
│   │   │
│   │   ├── [4A] 개별 의존명사 규칙 (L622-L690)
│   │   │   ├── 것 규칙          (L622) GEOT_NOSPLIT 필터
│   │   │   ├── 수 규칙          (L632) 종성 체크 + SU_NOSPLIT
│   │   │   ├── 따위 규칙       (L642) TTAWI_NOSPLIT
│   │   │   ├── 사이 규칙       (L647) SAI_NOSPLIT
│   │   │   ├── 뿐 규칙         (L652) PPUN_NOSPLIT
│   │   │   ├── 뿐만 규칙       (L657) 독립 패턴
│   │   │   ├── 고있 규칙       (L662) "고있" → "고 있"
│   │   │   ├── 고+동사 규칙    (L665) "고있다/가다/하다" 패턴
│   │   │   ├── 것 같은 규칙    (L670) "것같은" 패턴
│   │   │   ├── 같은 규칙       (L682) GAT_NOSPLIT 필터
│   │   │   └── 척 규칙         (L690) CHUK_NOSPLIT + PREFIX 필터
│   │   │
│   │   ├── [4B] 통합 의존명사 루프 (L703-L732)
│   │   │   ├── 이상 (ISANG_NOSPLIT, suffix_len=2)
│   │   │   ├── 이하 (IHA_NOSPLIT, suffix_len=2) + 동사 어미 스킵
│   │   │   ├── 밑   (MIT_NOSPLIT, suffix_len=1)
│   │   │   ├── 등   (DEUNG_NOSPLIT, suffix_len=1)
│   │   │   ├── 때   (TTE_NOSPLIT, suffix_len=1)
│   │   │   ├── 때문 (TTAE_MUN_NOSPLIT, suffix_len=2)
│   │   │   ├── 번   (BEON_NOSPLIT, suffix_len=1)
│   │   │   ├── 데   (DE_NOSPLIT, suffix_len=1) + 는데/은데 스킵
│   │   │   ├── 대로 (DAERO_NOSPLIT, suffix_len=2)
│   │   │   ├── 만큼 (MANKEUM_NOSPLIT, suffix_len=2)
│   │   │   └── 중   (JUNG_NOSPLIT, suffix_len=1)
│   │   │
│   │   ├── [4C] 특수 규칙 (L733-L770)
│   │   │   ├── 하(방향) 규칙   (L733) HA_DIRECTIONAL + HA_NOSPLIT
│   │   │   ├── 줄 규칙         (L740) 종성 체크 + JUL_NOSPLIT
│   │   │   ├── 듯/차례/무렵    (L761) 통합 루프
│   │   │   └── 채 규칙         (L768) 동사 뒤 채만 교정
│   │   │
│   │   └── [4D] 문장 부호 규칙 (L773-L835)
│   │       ├── 쌍따옴표→홑따옴표 (L773) 한자/한글/혼합 패턴
│   │       └── 가운데점→쉼표    (L827) 중국어/숫자 제외
│   │
│   └── return changes
│
├── [5] 메인 실행 흐름 (L837-L1249) ← 7단계 파이프라인
│   ├── main() (L837)
│   │   ├── log() 내부함수 (L840) 출력+로그 동시 기록
│   │   │
│   │   ├── [1/7] 원본 파일 무결성 검증 (L856-L870)
│   │   │   └── OLE 구조 확인, BodyText 스트림 카운트
│   │   │
│   │   ├── [2/7] 텍스트 추출 + 교정 규칙 생성 (L872-L940)
│   │   │   ├── 텍스트 추출 (extract_text)
│   │   │   ├── 교정 전 통계 (before_stats)
│   │   │   ├── 1단계: 중한 규칙 (china_rules + dynamic_nara_rules)
│   │   │   ├── 2단계: TXT 통합규칙 (txt_rules)
│   │   │   ├── 3단계: 의존명사/누락규칙 (text_changes)
│   │   │   └── 전체 규칙 정렬 (길이 역순)
│   │   │
│   │   ├── [3/7] 백업 + 레코드 단위 수정 (L942-L1000)
│   │   │   ├── 백업 생성
│   │   │   ├── OLE 스트림 읽기
│   │   │   ├── BodyText 순회:
│   │   │   │   ├── zlib 압축해제 (wbits=-15)
│   │   │   │   ├── 레코드 파싱
│   │   │   │   ├── tag_id=67 텍스트 레코드 찾기
│   │   │   │   ├── UTF-16-LE 디코딩
│   │   │   │   ├── 규칙 적용 (str.replace)
│   │   │   │   ├── UTF-16-LE 인코딩 + 레코드 갱신
│   │   │   │   ├── 스트림 재구성 (rebuild_stream)
│   │   │   │   ├── zlib 재압축 (level=6, wbits=-15)
│   │   │   │   ├── 크기 초과시 level=1 재압축
│   │   │   │   ├── null 패딩 (원본 크기 맞춤)
│   │   │   │   └── 압축해제 검증
│   │   │   └── 수정된 스트림 수집
│   │   │
│   │   ├── [4/7] OLE 스트림 쓰기 (L1002-L1040)
│   │   │   ├── UUID 임시 파일 복사
│   │   │   ├── 쓰기 권한 설정 (chmod)
│   │   │   ├── olefile write_stream
│   │   │   ├── .bin → .hwp 이름 변경
│   │   │   └── 해시 변경 확인
│   │   │
│   │   ├── [5/7] 출력 파일 검증 (L1042-L1070)
│   │   │   ├── OLE 구조 재확인
│   │   │   ├── 압축해제 테스트
│   │   │   └── 레코드/텍스트 카운트
│   │   │
│   │   ├── [6/7] 교정 결과 검증 (L1072-L1190)
│   │   │   ├── 수정 후 텍스트 추출
│   │   │   ├── 교정 전후 통계 비교 테이블
│   │   │   ├── 남은 항목 검사
│   │   │   └── 카테고리별 상세 내역
│   │   │
│   │   └── [7/7] HWP 파일 열기 테스트 (L1192-L1210)
│   │       └── subprocess.Popen(Hwp.exe) 실행 테스트
│   │
│   └── 로그 파일 저장 (L1212-L1249)
│
└── if __name__ == "__main__": main()
```

---

## 데이터 흐름도

```
원본 HWP 파일
    │
    ▼
[1/7] OLE 무결성 검증
    │
    ▼
[2/7] 텍스트 추출 + 규칙 생성
    │
    ├── extract_text() → 전체 텍스트
    │       │
    │       ├── 1단계: 중한 규칙 (나라→조, 지명)
    │       ├── 2단계: TXT 통합규칙
    │       └── 3단계: 의존명사 규칙 (apply_text_corrections)
    │               │
    │               ├── [4A] 개별 규칙 (것,수,따위,사이,뿐,뿐만,고있,고+동사,것같은,같은,척)
    │               ├── [4B] 통합 루프 (이상,이하,밑,등,때,때문,번,데,대로,만큼,중)
    │               ├── [4C] 특수 규칙 (하방향,줄,듯,차례,무렵,채)
    │               └── [4D] 문장부호 (쌍따옴표,가운데점)
    │
    │   all_rules (정렬: 길이 역순)
    │
    ▼
[3/7] 레코드 단위 수정
    │
    │   for each BodyText stream:
    │       raw → zlib.decompress(-15) → records[]
    │       for tag_id==67:
    │           UTF-16-LE decode → text
    │           text.replace(모든 규칙) → new_text
    │           UTF-16-LE encode → new_payload
    │       rebuild_stream() → zlib.compress(-15) → padded
    │
    ▼
[4/7] OLE 스트림 쓰기
    │   copy(SRC→TMP) → olefile.write_stream() → rename(TMP→OUT)
    │
    ▼
[5/7] 출력 파일 검증 (OLE+압축해제+레코드)
    │
    ▼
[6/7] 교정 결과 검증 (전후 비교 + 상세 내역)
    │
    ▼
[7/7] HWP 열기 테스트 (subprocess)
    │
    ▼
출력: 교정된 HWP + 상세 로그 TXT
```

---

## 교정 규칙 분류 체계

### 1단계: 중한 전용명사 규칙
| 규칙 | 소스 | 설명 |
|------|------|------|
| 나라→조 | 동적 생성 | 당나라→당조, 송나라→송조 등 |
| 지명 변환 | rules_china_place.txt | 중국 지명 한국어 표기 |

### 2단계: TXT 통합규칙
| 규칙 | 소스 | 설명 |
|------|------|------|
| 일반 교정 | rules_documentation.txt | 오탈자, 표기 통일 |

### 3단계: 의존명사 띄어쓰기 규칙
| 카테고리 | 형식 | NOSPLIT | 특수 로직 |
|----------|------|---------|-----------|
| 것 | X것 → X 것 | GEOT_NOSPLIT | - |
| 수 | X수 → X 수 | SU_NOSPLIT | 종성 체크 (ㄹ 받침) |
| 따위 | X따위 → X 따위 | TTAWI_NOSPLIT | - |
| 사이 | X사이 → X 사이 | SAI_NOSPLIT | - |
| 뿐 | X뿐 → X 뿐 | PPUN_NOSPLIT | - |
| 뿐만 | X뿐만 → X 뿐만 | - | 독립 패턴 |
| 고있 | 고있 → 고 있 | - | 단순 치환 |
| 고+동사 | 고V → 고 V | GO_NOSPLIT | 정규식 매칭 |
| 것 같은 | 것같X → 것 같X | GEOT_NOSPLIT | 정규식 매칭 |
| 같은 | X같X → X 같X | GAT_NOSPLIT | - |
| 척 | X척 → X 척 | CHUK_NOSPLIT | PREFIX 필터 |
| 이상 | X이상 → X 이상 | ISANG_NOSPLIT | 통합 루프 |
| 이하 | X이하 → X 이하 | IHA_NOSPLIT | 동사 어미 스킵 |
| 밑 | X밑 → X 밑 | MIT_NOSPLIT | 통합 루프 |
| 등 | X등 → X 등 | DEUNG_NOSPLIT | 통합 루프 |
| 때 | X때 → X 때 | TTE_NOSPLIT | 통합 루프 |
| 때문 | X때문 → X 때문 | TTAE_MUN_NOSPLIT | 통합 루프 |
| 번 | X번 → X 번 | BEON_NOSPLIT | 통합 루프 |
| 데 | X데 → X 데 | DE_NOSPLIT | 는데/은데 스킵 |
| 대로 | X대로 → X 대로 | DAERO_NOSPLIT | 통합 루프 |
| 만큼 | X만큼 → X 만큼 | MANKEUM_NOSPLIT | 통합 루프 |
| 중 | X중 → X 중 | JUNG_NOSPLIT | 통합 루프 |
| 하(방향) | 위하 → 위 하 | HA_NOSPLIT | 방향성만 적용 |
| 줄 | X줄 → X 줄 | JUL_NOSPLIT | 종성 체크 |
| 듯 | X듯 → X 듯 | DEUT_NOSPLIT | 통합 루프 |
| 차례 | X차례 → X 차례 | CHARYE_NOSPLIT | 통합 루프 |
| 무렵 | X무렵 → X 무렵 | - | 통합 루프 |
| 채 | X채 → X 채 | CHAE_NOSPLIT | 동사 뒤만 |
| 쌍따옴표 | "X" → 'X' | - | 한자/한글/혼합 |
| 가운데점 | X·Y → X, Y | - | 중국어/숫자 제외 |

### 제거된 규칙 (과교정 방지)
| 규칙 | 제거 사유 | 기존 건수 |
|------|-----------|-----------|
| 하 (일반) | 하다 동사 과교정 | 3311건 |
| 우 | 합성어 과교정 | 120건 |
| 상 | 합성어 과교정 | 225건 |
| 바 | 합성어 과교정 | 68건 |
| 터 | 부터 과교정 | - |

---

## 수정 시 체크리스트

### NOSPLIT 추가 시
1. [ ] 해당 합성어가 실제로 문서에 존재하는지 확인 (로그에서 검색)
2. [ ] NOSPLIT 세트에 추가 (명사구 + 조사 형태 포함)
3. [ ] 재실행 후 로그에서 해당 항목 교정 제외 확인

### 새 규칙 추가 시
1. [ ] 개별 규칙인지 통합 루프 규칙인지 결정
2. [ ] NOSPLIT 세트 생성 (최소 합성어 포함)
3. [ ] 과교정 가능성 분석 (의존명사 vs 합성어 비율)
4. [ ] 과교정이 심하면 규칙 제외 검토

### HWP 파일 수정 시
1. [ ] zlib 압축해제: wbits=-15 (raw deflate)
2. [ ] 레코드 파싱: tag_id=67 (텍스트 레코드)
3. [ ] 텍스트 인코딩: UTF-16-LE
4. [ ] 재압축 후 원본 크기 이내인지 확인
5. [ ] null 패딩으로 크기 맞춤
6. [ ] 압축해제 검증 필수

### 파일 권한 처리
1. [ ] UUID 기반 임시 파일 (.bin) 사용
2. [ ] os.chmod로 쓰기 권한 추가
3. [ ] .bin → .hwp 이름 변경
4. [ ] 기존 파일 삭제 실패시 타임스탬프 fallback

---

## 최신 교정 결과 (2026-04-20 01:45)

| 규칙 | 교정 건수 | 상태 |
|------|-----------|------|
| 1단계-중한(동적) | 다수 | ✅ |
| 2단계-TXT | 다수 | ✅ |
| 것 같은 | 3건 | ✅ |
| 고+동사 | 10건 | ✅ |
| 대로 | 21건 | ✅ |
| 데 | 8건 | ✅ |
| 등 | 39건 | ✅ |
| 때 | 20건 | ✅ |
| 만큼 | 3건 | ✅ |
| 번 | 11건 | ✅ |
| 뿐 | 6건 | ✅ |
| 뿐만 | 1건 | ✅ |
| 사이 | 36건 | ✅ |
| 수 | 11건 | ✅ |
| 쌍따옴표 | 348건 | ✅ |
| 이상 | 17건 | ✅ |
| 이하 | 0건 | ✅ (NOSPLIT 완비) |
| 줄 | 3건 | ✅ |
| 중 | 1건 | ✅ |
| 차례 | 12건 | ✅ |
| 채 | 3건 | ✅ |
| 하(방향) | 16건 | ✅ |
| **총계** | **885건** | **과교정 83.7% 감소** |
