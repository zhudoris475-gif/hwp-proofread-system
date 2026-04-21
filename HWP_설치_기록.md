# HWP Ollama AI Add-In 설치 기록

## 날짜: 2026-04-12

## 1. 시스템 환경
- OS: Windows
- Python: 3.12.4
- 한컴오피스: 2024 (HOffice130)
- .NET Framework: 4.8
- Ollama: 설치됨

## 2. 설치된 항목

### 2.1 Ollama 모델
| 모델명 | 크기 | 용도 | 상태 |
|--------|------|------|------|
| korean-corrector | 6.2 GB | 한국어 맞춤법 교정 전문 | ✅ |
| qwen3b-spacing | 1.9 GB | 띄어쓰기 교정 | ✅ |
| qwen3b-korean-spacing | 1.9 GB | 한국어 띄어쓰기 | ✅ |
| qwen2.5:7b | 4.7 GB | 일반용 | ✅ |
| llama3.2:latest | 2.0 GB | 일반용 | ✅ |

### 2.2 HWP Add-In
| 파일 | 경로 | 상태 |
|------|------|------|
| HwpOllamaAddin.dll | C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\AddIn\ | ✅ |
| HwpOllamaAddin.tlb | C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\AddIn\ | ✅ |

### 2.3 COM 등록
- RegAsm.exe: /tlb /codebase 완료
- Types registered successfully

### 2.4 레지스트리
```
HKCU\SOFTWARE\Hnc\Hwp\AddIns\HwpOllama.Addin
├── (Default) = "HwpOllamaAddin"
├── ProgID = "HwpOllama.Addin"
├── Enabled = 1 (REG_DWORD)
└── LoadBehavior = 3 (REG_DWORD)
```

## 3. Python 패키지
| 패키지 | 버전 | 상태 |
|--------|------|------|
| pywin32 | 최신 | ✅ |
| py-hanspell | 1.1 | ✅ |
| requests | 2.33.1 | ✅ |

## 4. HWP 교정 자동화 도구
- 경로: C:\Users\doris\.agent-skills\HWP_교정_自动化工具\
- 규칙 파일: 1204개 교정 규칙
- 상태: setup.py 실행 완료

## 5. 사용 방법
1. 터미널에서 `ollama serve` 실행
2. HWP(한글) 실행
3. 도구 > 매크로 보안 설정 > 보통
4. 리본 메뉴에서 "Ollama AI" 탭 확인
5. 문서 열고 교정 버튼 클릭

## 6. 제거 방법
관리자 PowerShell:
```powershell
# COM 등록 해제
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\RegAsm.exe /u "C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\AddIn\HwpOllamaAddin.dll"

# DLL 삭제
Remove-Item "C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\AddIn\HwpOllamaAddin.dll"

# 레지스트리 삭제
reg delete "HKCU\SOFTWARE\Hnc\Hwp\AddIns\HwpOllama.Addin" /f
```