@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   한컴오피스 2024 MSI 직접 설치
echo ============================================
echo.

set MSI_PATH=C:\Users\doris\Downloads\한컴 오피스 2024 교육기관용_자동인증(1)\Install\HOffice130.msi
set LOG_PATH=%USERPROFILE%\Desktop\msi_install.log

echo [1/5] 관리자 권한 확인...
net session >nul 2>&1
if errorlevel 1 (
    echo [오류] 관리자 권한으로 실행하세요!
    pause
    exit /b 1
)

echo.
echo [2/5] 기존 설치 폴더 삭제...
rd /s /q "C:\Program Files (x86)\HNC\Office 2024" 2>nul
rd /s /q "C:\Program Files (x86)\HNC\Office 2022" 2>nul
echo ✅ 기존 폴더 삭제 완료

echo.
echo [3/5] AppData 로그 정리...
del /q "%APPDATA%\Hnc\*.log" 2>nul
del /q "%APPDATA%\Hnc\*Exception*.txt" 2>nul
echo ✅ 로그 정리 완료

echo.
echo [4/5] MSI 직접 설치 시작...
echo 로그: %LOG_PATH%
echo.

msiexec /i "%MSI_PATH%" /L*v "%LOG_PATH%" /norestart

if errorlevel 1 (
    echo.
    echo ============================================
    echo   ❌ 설치 실패!
    echo   로그 파일을 확인하세요:
    echo   %LOG_PATH%
    echo ============================================
) else (
    echo.
    echo ============================================
    echo   ✅ 한컴오피스 2024 설치 완료!
    echo ============================================
)

pause