---
name: "hwp-proofread"
description: "HWP 문서 교정(지명변환, 왕조명교정, 띄어쓰기/붙여쓰기 통합규칙) 실행. Invoke when user asks to proofread HWP files, apply rules to HWP documents, or run correction on HWP files."
---

# HWP 문서 교정 스킬

HWP 한글 문서에 교정 규칙(지명 변환, 왕조명 교정, 띄어쓰기/붙여쓰기 통합 규칙)을 일괄 적용하는 스킬입니다.

## 규칙 파일 위치

| 규칙 | 파일 경로 | 내용 |
|------|-----------|------|
| 중국 지명 변환 | `C:\Users\51906\Desktop\rules_china_place.txt` | 중국 지명 현지음→한자음 변환 (베이징→북경 등) |
| 왕조명 교정 | `C:\Users\51906\Desktop\rules_dynasty.txt` | 왕조명 나라→조 변환 (당나라→당조 등, 66개) |
| 통합 규칙 | `C:\Users\51906\Desktop\rules_integrated.txt` | 띄어쓰기/붙여쓰기, 의존명사 것 등 (1,455개) |

## 대상 HWP 파일

기본 대상 폴더: `C:\Users\51906\Desktop\사전`

HWP 파일 목록:
- 【20】O 2179-2182排版页수4-金花顺-.hwp
- 【21】P 2183-2268排版页数86-金花顺.hwp
- 【大中朝 14】J 1419-1693--275--20240920.hwp
- 【大中朝 15】K 1694-1786--93--20240920.hwp
- 【大中朝 16】L 1787-1958--172--20240920-gaowm.hwp
- 【大中朝 17】M 1959-2093--135--20240920.hwp
- 【大中朝 18】N 2094-2178--85--20240920.hwp

## 실행 방법

### 방법 1: 보고서 생성 (pyhwp 기반 - 읽기 전용, 안전)

pyhwp 라이브러리로 HWP 텍스트를 추출하여 규칙 매칭 결과만 보고서로 출력합니다. **원본 파일을 수정하지 않습니다.**

```bash
cd "D:\ProgramData\xwechat_files"
python _dynasty_convert.py        # 왕조명 교정 보고서
python _china_place_convert.py    # 지명 변환 보고서 (win32com - 실제 수정)
python _integrated_convert.py     # 통합 규칙 교정 보고서
```

**pyhwp 기반 보고서 스크립트 구조** (`_dynasty_convert.py`, `_integrated_convert.py`):
1. `from hwp5.hwp5txt import Hwp5File, TextTransform` 로 텍스트 추출
2. 규칙 파일에서 `->` 구분으로 규칙 로드
3. `text.count(src)` 로 매칭 건수 확인
4. `text.replace(src, dst)` 로 텍스트 치환 (메모리상)
5. 결과를 `_보고서.txt` 파일로 저장

### 방법 2: 실제 HWP 파일 수정 (win32com 기반 - 주의!)

win32com으로 한글 프로그램을 제어하여 HWP 파일을 직접 수정합니다.

**사전 준비**:
1. 한글(HWP) 프로그램이 설치되어 있어야 함
2. `pywin32` 패키지 필요: `pip install pywin32`
3. **반드시 백업 먼저 실행**

**실행 순서**:
```bash
# 1. 백업 (최초 1회)
# _백업_원본 폴더에 원본 복사

# 2. 교정 실행
cd "D:\ProgramData\xwechat_files"
python _china_place_convert.py    # 지명 변환 (win32com 직접 수정)
python _proofread_all.py          # 전체 파일 교정 (win32com)
python _proofread_batch.py        # 배치 교정 (서브프로세스 방식)
python run_proofread_v17.py       # 단일 파일 교정 (v17)
```

**win32com 교정 스크립트 핵심 구조**:
1. `pythoncom.CoInitialize()` - COM 초기화
2. `hwp = win32com.client.Dispatch("HWPFrame.HwpObject")` - 한글 연결
3. `hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")` - 보안 모듈
4. `hwp.Open(filepath, "HWP", "forceopen:true")` - 파일 열기
5. `hwp.GetTextFile("UNICODE", "")` - 텍스트 추출 (변경 전/후 비교)
6. 규칙 적용:
   ```python
   hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
   hwp.HParameterSet.HFindReplace.FindString = orig
   hwp.HParameterSet.HFindReplace.ReplaceString = repl
   hwp.HParameterSet.HFindReplace.Direction = 0
   hwp.HParameterSet.HFindReplace.ReplaceMode = 2
   hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
   hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
   ```
7. `hwp.Save()` 또는 `hwp.SaveAs(temp_path, "HWP", "")` - 저장
8. `hwp.Quit()` - 종료
9. `pythoncom.CoUninitialize()` - COM 해제

### 방법 3: 따옴표 내용 추출 (pyhwp 기반)

HWP 파일에서 따옴표 내용을 추출하여 언어별(중문/한글/혼합/기타)로 분류합니다.

```bash
cd "D:\ProgramData\xwechat_files\zhuchunyan331793_600e"
python _extract_detailed_quotes.py
```

## 규칙 파일 형식

```
# 주석
원본 -> 변경
```

예시:
```
베이징 -> 북경
당(唐)나라 -> 당(唐)조
두 개 -> 두개
가난한것 -> 가난한 것
```

## 주의사항

1. **백업 필수**: 실제 수정 전 반드시 `_백업_원본` 폴더에 백업
2. **한글 프로그램**: win32com 방식은 한글(HWP) 프로그램이 실행 중이면 안 됨
3. **대화상자**: v17 스크립트는 `_dialog_closer.py` 로 자동 대화상자 닫기 기능 포함
4. **검증**: 수정 후 텍스트 비교로 변경 사항 검증
5. **보고서**: 모든 교정 결과는 `_보고서.txt` 파일로 저장됨

## 출력 파일

| 스크립트 | 출력 파일 | 위치 |
|----------|-----------|------|
| _dynasty_convert.py | _왕조명_교정_보고서.txt | 대상 폴더 |
| _china_place_convert.py | _지명변환_결과.txt | 대상 폴더 |
| _integrated_convert.py | _통합규칙_교정_보고서.txt | 대상 폴더 |
| _extract_detailed_quotes.py | _따옴표_상세결과.txt | 스크립트 폴더 |
| run_proofread_v17.py | *_report.txt | 대상 파일 폴더 |
