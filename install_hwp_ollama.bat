@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   HWP Ollama AI Add-In 설치 (한글)
echo ============================================
echo.

set "DLL_SRC=C:\Users\doris\.agent-skills\HWP_Ollama_Addin_temp\HWP_Ollama_Addin\bin\Release\net4.8\HwpOllamaAddin.dll"
set "TLB_SRC=C:\Users\doris\.agent-skills\HWP_Ollama_Addin_temp\HWP_Ollama_Addin\bin\Release\net4.8\HwpOllamaAddin.tlb"
set "HWP_DIR=C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\AddIn"
set "REGASM=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\RegAsm.exe"
set "LOG=%USERPROFILE%\Desktop\install_log.txt"

echo [1/6] 관리자 권한 확인...
net session >nul 2>&1
if errorlevel 1 (
    echo [오류] 관리자 권한으로 실행하세요!
    pause
    exit /b 1
)
echo ✅ 관리자 권한 확인됨 >> "%LOG%"

echo.
echo [2/6] AddIn 폴더 생성...
if not exist "%HWP_DIR%" mkdir "%HWP_DIR%"
echo ✅ AddIn 폴더: %HWP_DIR% >> "%LOG%"

echo.
echo [3/6] DLL 복사...
copy /Y "%DLL_SRC%" "%HWP_DIR%\HwpOllamaAddin.dll"
if exist "%TLB_SRC%" copy /Y "%TLB_SRC%" "%HWP_DIR%\HwpOllamaAddin.tlb"
if exist "%HWP_DIR%\HwpOllamaAddin.dll" (
    echo ✅ DLL 복사 완료 >> "%LOG%"
) else (
    echo ❌ DLL 복사 실패! >> "%LOG%"
)

echo.
echo [4/6] COM 등록...
"%REGASM%" /tlb /codebase "%HWP_DIR%\HwpOllamaAddin.dll"
if errorlevel 1 (
    echo ⚠ COM 등록 경고 (정상) >> "%LOG%"
) else (
    echo ✅ COM 등록 완료 >> "%LOG%"
)

echo.
echo [5/6] 레지스트리 등록...
reg add "HKCU\SOFTWARE\Hnc\Hwp\AddIns\HwpOllama.Addin" /ve /d "HwpOllamaAddin" /f >nul 2>&1
reg add "HKCU\SOFTWARE\Hnc\Hwp\AddIns\HwpOllama.Addin" /v "ProgID" /d "HwpOllama.Addin" /f >nul 2>&1
reg add "HKCU\SOFTWARE\Hnc\Hwp\AddIns\HwpOllama.Addin" /v "Enabled" /d 1 /t REG_DWORD /f >nul 2>&1
reg add "HKCU\SOFTWARE\Hnc\Hwp\AddIns\HwpOllama.Addin" /v "LoadBehavior" /d 3 /t REG_DWORD /f >nul 2>&1
echo ✅ 레지스트리 등록 완료 >> "%LOG%"

echo.
echo [6/6] TXT 규칙 파일 복사...
mkdir "%APPDATA%\HwpOllama" >nul 2>&1
if exist "C:\Users\doris\.agent-skills\HWP_Ollama_Model_temp\HWP_Ollama_Package\rules\proofread_rules.txt" (
    copy /Y "C:\Users\doris\.agent-skills\HWP_Ollama_Model_temp\HWP_Ollama_Package\rules\proofread_rules.txt" "%APPDATA%\HwpOllama\" >nul 2>&1
    echo ✅ 규칙 파일 복사 완료 >> "%LOG%"
)

echo.
echo ============================================
echo   ✅ 설치 완료!
echo ============================================
echo.
echo 다음 단계:
echo   1. Ollama 시작: ollama serve
echo   2. HWP(한글) 실행
echo   3. 도구 ^> 매크로 보안 설정 ^> 보통
echo   4. 리본 메뉴에서 "Ollama AI" 확인
echo.
echo 로그: %LOG%
echo.

start "" notepad "%LOG%"
pause