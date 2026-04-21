@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   한컴오피스 2024 강제 삭제 스크립트
echo ============================================
echo.

set LOG=%USERPROFILE%\Desktop\cleanup_log.txt
echo [시작] %date% %time% > "%LOG%"

echo [1/8] 관리자 권한 확인...
net session >nul 2>&1
if errorlevel 1 (
    echo [오류] 관리자 권한으로 실행하세요!
    pause
    exit /b 1
)
echo ✅ 관리자 권한 확인됨 >> "%LOG%"

echo.
echo [2/8] HWP Converter 제거...
msiexec /x {90150000-2009-0412-1000-0000000FF1CE} /quiet /norestart >> "%LOG%" 2>&1
if errorlevel 1 (
    echo ⚠ HWP Converter 제거 실패 (무시 가능) >> "%LOG%"
) else (
    echo ✅ HWP Converter 제거됨 >> "%LOG%"
)

echo.
echo [3/8] 프로그램 폴더 삭제...
rd /s /q "C:\Program Files (x86)\HNC" 2>nul & echo ✅ ProgramFiles(x86)\HNC >> "%LOG%"
rd /s /q "C:\Program Files\HNC" 2>nul & echo ✅ ProgramFiles\HNC >> "%LOG%"

echo.
echo [4/8] AppData 삭제...
rd /s /q "%APPDATA%\Hnc" 2>nul & echo ✅ AppData\Hnc >> "%LOG%"
rd /s /q "%APPDATA%\HWP" 2>nul & echo ✅ AppData\HWP >> "%LOG%"
rd /s /q "%APPDATA%\Hancom" 2>nul & echo ✅ AppData\Hancom >> "%LOG%"
rd /s /q "%LOCALAPPDATA%\Hnc" 2>nul & echo ✅ LocalAppData\Hnc >> "%LOG%"
rd /s /q "%LOCALAPPDATA%\HWP" 2>nul & echo ✅ LocalAppData\HWP >> "%LOG%"
rd /s /q "%LOCALAPPDATA%\Hancom" 2>nul & echo ✅ LocalAppData\Hancom >> "%LOG%"

echo.
echo [5/8] ProgramData 삭제...
rd /s /q "%ProgramData%\HNC" 2>nul & echo ✅ ProgramData\HNC >> "%LOG%"
rd /s /q "%ProgramData%\Hancom" 2>nul & echo ✅ ProgramData\Hancom >> "%LOG%"

echo.
echo [6/8] Temp 폴더 정리...
for %%i in (Hnc Hwp96 HCell96 HShow96 HOffice Hancom HNCDownload) do (
    rd /s /q "%TEMP%\%%i" 2>nul
)
echo ✅ Temp 정리 완료 >> "%LOG%"

echo.
echo [7/8] 레지스트리 정리...
reg delete "HKCU\SOFTWARE\Hnc" /f 2>nul & echo ✅ HKCU\Hnc >> "%LOG%"
reg delete "HKCU\SOFTWARE\Hancom" /f 2>nul & echo ✅ HKCU\Hancom >> "%LOG%"
reg delete "HKLM\SOFTWARE\Hnc" /f 2>nul & echo ✅ HKLM\Hnc >> "%LOG%"
reg delete "HKLM\SOFTWARE\Hancom" /f 2>nul & echo ✅ HKLM\Hancom >> "%LOG%"
reg delete "HKLM\SOFTWARE\WOW6432Node\Hnc" /f 2>nul & echo ✅ WOW64\Hnc >> "%LOG%"
reg delete "HKLM\SOFTWARE\WOW6432Node\Hancom" /f 2>nul & echo ✅ WOW64\Hancom >> "%LOG%"

echo.
echo [8/8] Windows Installer 재등록...
msiexec /unreg >nul 2>&1
ping -n 3 127.0.0.1 >nul
msiexec /regserver >nul 2>&1
echo ✅ Windows Installer 재등록 완료 >> "%LOG%"

echo.
echo ============================================
echo   ✅ 강제 삭제 완료!
echo ============================================
echo.
echo 로그 파일: %LOG%
echo.
echo 이제 컴퓨터를 **재시작**하고
echo 한컴오피스 2024를 다시 설치하세요!
echo.
pause