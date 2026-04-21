@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   C:\사전\ HWP 전체 교정 v17.0
echo   패키지: C:\AMD\AJ\hwp_proofreading_package
echo ============================================
echo.

set PY=C:\Users\doris\AppData\Local\Programs\Python\Python312\python.exe
set SCRIPT=C:\AMD\AJ\hwp_proofreading_package\hwp_ollama_proofread.py
set SADIR=C:\사전

if not exist "%PY%" (
    echo [오류] Python 3.12 없음
    pause
    exit /b 1
)

if not exist "%SCRIPT%" (
    echo [오류] 스크립트 없음: %SCRIPT%
    pause
    exit /b 1
)

if not exist "%SADIR%" (
    echo [오류] 사전 디렉토리 없음: %SADIR%
    pause
    exit /b 1
)

echo [대상 파일]
for %%f in ("%SADIR%\*.hwp") do (
    echo   📄 %%~nxf (%%~zf bytes)
)

echo.
echo [Ollama 상태]
ollama list 2>nul | findstr "korean-corrector"
if errorlevel 1 (
    echo ⚠ Ollama 실행 안됨 - 가운데점/따옴표 교정 제외
)

echo.
set /p STAGE="모드 선택 (check=검사 only, all=교정적용): "
if "%STAGE%"=="" set STAGE=check

echo.
echo ============================================
echo   실행: --stage=%STAGE%
echo   대상: %SADIR%
echo ============================================
echo.

"%PY%" "%SCRIPT%" --stage=%STAGE% "%SADIR%"

echo.
echo ============================================
echo   완료! 로그: C:\AMD\AJ\hwp_proofreading_package\hwp_ollama_proofread_log.txt
echo   리포트: C:\AMD\AJ\hwp_proofreading_package\reports\
echo ============================================
pause