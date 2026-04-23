# HWP 전반 교정 시스템 통합 플랜

## 목표
분산된 교정 모듈을 하나의 고품질 통합 시스템으로 병합하여,
J/L/K 파일 모두에 대해 **바이너리 수준 + COM 자동화** 이중 교정 파이프라인 구축

## 현재 상태 분석

### 핵심 모듈 (3개 분산)
1. **fix_J_record.py** (~1200줄) - 바이너리 레코드 수준 교정 (OLE/레코드 파싱)
   - NOSPLIT 세트 28종 (1573개 항목)
   - 의존명사 문맥 교정 로직
   - 나라→조 동적 규칙
   - 따옴표 변환
   - 가운데점→쉼표 변환

2. **JLK_완전교정_시스템.py** (~450줄) - COM 자동화 교정
   - SPACING_RULES (고정 규칙)
   - CONTEXT_SPACING_RULES (정규식)
   - QUOTE_RULES
   - NARA_RULES
   - SPACING_NOSPLIT
   - COM 기반 Find/Replace

3. **fix_rules_extra.py** (~50줄) - 규칙 파일 보조 스크립트

### 중복/불일치 문제
- NOSPLIT 세트가 fix_J_record.py와 JLK_완전교정_시스템.py에 분산
- SPACING_RULES가 JLK_완전교정_시스템.py에만 있고 fix_J_record.py에는 없음
- 규칙 파일 경로가 하드코딩 (rules_china_place.txt, rules_documentation.txt)
- 두 시스템 간 NOSPLIT 불일치 가능성

## 통합 아키텍처

```
hwp_proofread_unified.py (단일 진입점)
├── config/
│   ├── nosplit_sets.py     ← 모든 NOSPLIT 통합 (1573+ 항목)
│   ├── spacing_rules.py    ← SPACING_RULES + CONTEXT_RULES 통합
│   └── paths.py            ← 파일 경로 설정
├── core/
│   ├── text_analyzer.py    ← 텍스트 추출 + 교정 규칙 생성
│   ├── binary_editor.py    ← OLE/레코드 파싱 + 바이너리 수정
│   └── com_editor.py       ← COM 자동화 Find/Replace
├── pipeline.py             ← 전체 교정 파이프라인 오케스트레이션
└── main.py                 ← CLI 진입점
```

## Phase별 작업

### Phase 1: 통합 설정 모듈 작성
- [x] 모든 NOSPLIT 세트를 단일 파일로 통합
- [x] SPACING_RULES + CONTEXT_RULES 통합
- [x] 파일 경로 설정 중앙화

### Phase 2: 핵심 교정 엔진 작성
- [x] text_analyzer: 텍스트 추출 + 의존명사 교정 규칙 생성
- [x] binary_editor: OLE 레코드 파싱/수정/재구성
- [x] com_editor: COM 자동화 교정 (백업/저장/검증)

### Phase 3: 파이프라인 통합
- [x] 1단계: 바이너리 수준 교정 (나라→조, 의존명사, 따옴표)
- [x] 2단계: COM 수준 교정 (정규식 규칙, 복잡 패턴)
- [x] 3단계: 교정 결과 검증 (전후 비교)

### Phase 4: 테스트 + Git 반영
- [x] 종합 검증 테스트
- [x] Git 커밋 + 원격 동기화

## 의존명사 교정 규칙 요약 (28종)
것/수/따위/사이/뿐/뿐만/고있/고+동사/척/이상/이하/밑/등/때/때문/번/데/대로/만큼/줄/듯/채/바/터/차례/무렵/중/상/우/하/같은/것같은/적/지/앞/게/가운데/안/밖/뒤/나라
