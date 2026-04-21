@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   한컴오피스 2024 - 호환성 모드 설치
echo   (Win11 24H2 호환 문제 해결)
echo ============================================
echo.

set "SRC=C:\Users\doris\Downloads\한컴 오피스 2024 교육기관용_자동인증(1)"
set LOG=%USERPROFILE%\Desktop\compat_install_log.txt

echo [시작] %date% %time% > "%LOG%"

echo [1/5] 관리자 권한 확인...
net session >nul 2>&1
if errorlevel 1 (
    echo [오류] 관리자 권한으로 실행하세요!
    pause
    exit /b 1
)

echo.
echo [2/5] 이전 설치 흔적 완전 삭제...
taskkill /F /IM Hwp.exe 2>nul
taskkill /F /IM HCell.exe 2>nul
taskkill /F /IM HShow.exe 2>nul
rd /s /q "C:\Program Files (x86)\HNC" 2>nul
rd /s /q "%APPDATA%\Hnc" 2>nul
rd /s /q "%APPDATA%\Hancom" 2>nul
for %%i in (Hnc Hwp96 HCell96 HShow96) do rd /s /q "%TEMP%\%%i" 2>nul
echo ✅ 삭제 완료 >> "%LOG%"

echo.
echo [3/5] Windows Installer 서비스 재시작...
net stop msiserver /y >nul 2>&1
ping -n 3 127.0.0.1 >nul
net start msiserver >nul 2>&1
echo ✅ 재시작 완료 >> "%LOG%"

echo.
echo [4/5] Setup.exe 실행 (호환성 모드)...
echo    방법: Install.exe 직접 실행

pushd "%SRC%"
Install.exe /silent /norestart /log "%USERPROFILE%\Desktop\setup_compat.log"
set SETUP_ERR=%errorlevel%
popd

echo    Setup.exe 종료 코드: %SETUP_ERR% >> "%LOG%"

if %SETUP_ERR% equ 0 (
    echo ✅ Setup.exe 성공!
    goto SUCCESS
)

echo.
echo [5/5] MSI 직접 실행 (추가 옵션)...
echo    msiexec with IGNOREPLATFORMCHECK...

msiexec /i "%SRC%\Install\HOffice130.msi" ^
    ALLOWDOWNLEVEL=1 ^
    IGNOREPLATFORMCHECK=1 ^
    REINSTALLMODE=amus ^
    RUNFROMSETUP=1 ^
    ECDATA=F5ZUS8LU3GAS9EQB1Y9S ^
    MSIFASTINSTALL=7 ^
    /L*v "%USERPROFILE%\Desktop\hwp_compat.log" ^
    /norestart

set MSI_ERR=%errorlevel%
echo MSI 종료 코드: %MSI_ERR% >> "%LOG%"

:SUCCESS
echo.
echo ============================================
if exist "C:\Program Files (x86)\HNC\Office 2024\HOffice130\Bin\Hwp.exe" (
    echo   ✅✅✅ 한컴오피스 2024 설치 성공! ✅✅✅
    echo   경로: C:\Program Files (x86)\HNC\Office 2024\HOffice130\Bin\Hwp.exe
) else (
    echo   ⚠ 설치 확인 필요
    echo   로그 파일들을 확인하세요:
    echo   - %USERPROFILE%\Desktop\setup_compat.log
    echo   - %USERPROFILE%\Desktop\hwp_compat.log
    echo   - %LOG%
)
echo ============================================
pause