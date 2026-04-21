@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   한컴오피스 2024 - 수동 설치 (CAB 추출)
echo ============================================
echo.

set SRC=C:\Users\doris\Downloads\한컴 오피스 2024 교육기관용_자동인증(1)\Install
set TMPDIR=%TEMP%\HWP_Install
set LOG=%USERPROFILE%\Desktop\manual_install_log.txt

echo [시작] %date% %time% > "%LOG%"

echo [1/6] 임시 디렉토리 생성...
if exist "%TMPDIR%" rd /s /q "%TMPDIR%"
mkdir "%TMPDIR%\CAB"
mkdir "%TMPDIR%\Files"
echo ✅ 생성 완료 >> "%LOG%"

echo.
echo [2/6] CAB 파일 복사 (한글 경로 문제 회피)...
copy "%SRC%\cab*.cab" "%TMPDIR%\CAB\" >> "%LOG%" 2>&1
echo CAB 파일 수:
dir /b "%TMPDIR%\CAB\*.cab" 2>nul | find /c /v "" >> "%LOG%"

echo.
echo [3/6] expand.exe로 CAB 압축 해제...
for %%f in ("%TMPDIR%\CAB\*.cab") do (
    echo   추출 중: %%~nxf
    expand.exe -r "%%f" -F:* "%TMPDIR%\Files\" >> "%LOG%" 2>&1
)

echo.
echo [4/6] 추출 결과 확인...
for /d %%d in ("%TMPDIR%\Files\*") do (
    set /a count=0
    for %%f in ("%%d\*.*") do set /a count+=1
    echo   %%~nxd: !count! 개 파일
)
echo 총 파일:
dir /s /b "%TMPDIR%\Files\*.*" 2>nul | find /c /v ""

echo.
echo [5/6] 설치 대상 준비...
set "TARGET=C:\Program Files (x86)\HNC\Office 2024\HOffice130"
if not exist "%TARGET%" mkdir "%TARGET%"
echo ✅ 대상: %TARGET%

echo.
echo [6/6] 파일 복사...
xcopy "%TMPDIR%\Files\*" "%TARGET%\" /E /Y /I >> "%LOG%" 2>&1

echo.
echo ============================================
if exist "%TARGET%\Hwp.exe" (
    echo   ✅✅✅ 파일 복사 성공!
    echo   Hwp.exe 위치: %TARGET%\Hwp.exe
) else (
    echo   ⚠ Hwp.exe 없음 - 추가 작업 필요
    dir "%TARGET%" /b | head -20
)
echo ============================================
echo.
echo 로그: %LOG%
pause