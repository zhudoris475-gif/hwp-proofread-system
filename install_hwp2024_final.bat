@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   한컴오피스 2024 - 최종 설치 스크립트
echo   (UAC 수정 + 완전 삭제 + MSI 직접 설치)
echo ============================================
echo.

set LOG=%USERPROFILE%\Desktop\final_install_log.txt
echo [시작] %date% %time% > "%LOG%"

echo [1/8] 관리자 권한 확인...
net session >nul 2>&1
if errorlevel 1 (
    echo [오류] 관리자 권한으로 실행하세요!
    pause
    exit /b 1
)
echo ✅ 관리자 권한 >> "%LOG%"

echo.
echo [2/8] UAC 설정 확인 및 수정...
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA | find "0x0" >nul 2>&1
if not errorlevel 1 (
    echo ⚠ UAC가 비활성화되어 있습니다!
    echo    한컴오피스 설치를 위해 UAC를 활성화합니다...
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 1 /f >> "%LOG%" 2>&1
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 5 /f >> "%LOG%" 2>&1
    echo ✅ UAC 활성화됨 (재시작 필요 없음) >> "%LOG%"
) else (
    echo ✅ UAC 정상 >> "%LOG%"
)

echo.
echo [3/8] Windows Installer 서비스 재시작...
net stop msiserver /y >nul 2>&1
ping -n 2 127.0.0.1 >nul
net start msiserver >nul 2>&1
if errorlevel 1 (
    echo ⚠ 서비스 시작 실패 (무시 가능) >> "%LOG%"
) else {
    echo ✅ Windows Installer 재시작됨 >> "%LOG%"
}

echo.
echo [4/8] 기존 파일 강제 삭제...
rd /s /q "C:\Program Files (x86)\HNC" 2>nul
rd /s /q "C:\Program Files\HNC" 2>nul
rd /s /q "%APPDATA%\Hnc" 2>nul
rd /s /q "%APPDATA%\Hancom" 2>nul
rd /s /q "%LOCALAPPDATA%\Hnc" 2>nul
rd /s /q "%LOCALAPPDATA%\Hancom" 2>nul
rd /s /q "%ProgramData%\HNC" 2>nul
rd /s /q "%ProgramData%\Hancom" 2>nul
for %%i in (Hnc Hwp96 HCell96 HShow96 HOffice Hancom HNCDownload) do rd /s /q "%TEMP%\%%i" 2>nul
del /q "%USERPROFILE%\Documents\welcome*" 2>nul
echo ✅ 파일 삭제 완료 >> "%LOG%"

echo.
echo [5/8] 레지스트리 정리...
reg delete "HKCU\SOFTWARE\Hnc" /f 2>nul
reg delete "HKCU\SOFTWARE\Hancom" /f 2>nul
reg delete "HKLM\SOFTWARE\Hnc" /f 2>nul
reg delete "HKLM\SOFTWARE\Hancom" /f 2>nul
reg delete "HKLM\SOFTWARE\WOW6432Node\Hnc" /f 2>nul
reg delete "HKLM\SOFTWARE\WOW6432Node\Hancom" /f 2>nul
reg delete "HKLM\SOFTWARE\Classes\Installer\Features\2A390EF0DD114267A38710DA12D9CAA8" /f 2>nul
reg delete "HKLM\SOFTWARE\Classes\Installer\Products\2A390EF0DD114267A38710DA12D9CAA8" /f 2>nul
echo ✅ 레지스트리 정리 완료 >> "%LOG%"

echo.
echo [6/8] 임시 파일 정리...
del /q "%TEMP%\*.tmp" 2>nul
del /q "%TEMP%\*.msi" 2>nul
echo ✅ 임시 파일 정리 완료 >> "%LOG%"

echo.
echo [7/8] VC++ Redist 사전 설치...
echo    VC++ Redistributable x86 설치 중...
"C:\Users\doris\Downloads\한컴 오피스 2024 교육기관용_자동인증(1)\Install\VC_redist.x86.exe" /quiet /norestart >> "%LOG%" 2>&1
echo ✅ VC++ 완료 >> "%LOG%"

echo.
echo [8/8] 한컴오피스 2024 설치 (GUI 모드)...
echo ============================================
echo    ⚠ 설치 창이 열리면 '설치' 버튼을 클릭하세요!
echo    창이 닫릴 때까지 기다려주세요...
del /q "%USERPROFILE%\Desktop\hwp2024_final.log" 2>nul
start /wait "" "C:\Users\doris\Downloads\한컴 오피스 2024 교육기관용_자동인증(1)\Install.exe"

if errorlevel 1 (
    echo.
    echo ============================================
    echo   ❌ 설치 실패!
    echo ============================================
    echo 실패 >> "%LOG%"
) else (
    echo.
    echo ============================================
    echo   ✅✅✅ 한컴오피스 2024 설치 완료! ✅✅✅
    echo ============================================
    echo 성공 >> "%LOG%"
)

echo.
echo ============================================
echo   로그: %LOG%
echo ============================================
pause