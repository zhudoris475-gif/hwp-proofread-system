# 발견 사항

## 2026-04-16
- 프로젝트 루트: `C:\Users\doris\Desktop\xwechat_files\WORD`
- 주요 실행 파일: `hwp_ollama_proofread_detailed.py`
- 대상 파일: `【20】O 2179-2182排版页수4-金花顺-.backup.hwp`
- 백업 파일: `【20】O 2179-2182排版页수4-金花顺-.backup.hwp.bak`
- 규칙 파일은 최신 기준으로 `C:\AMD\AJ\hwp_proofreading_package`에서 확보 가능했다.
- 현재 작업 폴더에는 `rules_documentation.txt`, `rules_china_place.txt`, `rules_regex.txt`를 복사해 두었다.
- 32비트 Python 3.13 환경에서 `pythoncom`, `win32com.client`, `requests`, `olefile` 모두 정상이다.
- `--stage=check` 실행 시 텍스트 추출 자수는 `11,896자`였다.
- `--stage=check` 실행 시 매치 합계는 `9개`였고 실제 적용은 하지 않았다.
- `--stage=all` 실행 시 총 `10개 항목 / 12건 적용`으로 완료되었다.
- 실제 적용 결과는 `reports\【20】O 2179-2182排版页수4-金花顺-.backup_교정결과_20260416_235254.txt`에 저장되었다.
- LocalServer 경로는 `DistributedCOM 10010`으로 불안정하므로 현재 실무 경로는 `64비트 시작 -> 32비트 자동 재실행`이다.
- 운영/구조/오류/업데이트 정리 문서로 `system_review_20260416.md`를 생성했다.
- 기본 대상 폴더는 고정 경로 대신 `HWP_DIR 환경변수 -> 현재 작업 폴더 -> 스크립트 폴더 -> 레거시 경로` 순으로 자동 해석되도록 수정했다.
