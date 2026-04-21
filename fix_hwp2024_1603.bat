@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   HWP2024 Fix - 1603 Error Resolution
echo   Copy to ASCII path + Reinstall
echo ============================================
echo.

set LOG=%USERPROFILE%\Desktop\hwp2024_fix_log.txt
echo [Fix Start] %date% %time% > "%LOG%"

set SRC=C:\Users\doris\Downloads\한컴 오피스 2024 교육기관용_자동인증(1)
set DST=C:\HWP2024_Install

echo [1/5] Copying install files to ASCII path...
echo    Source: %SRC%
echo    Target: %DST%
if exist "%DST%" rd /s /q "%DST%"
xcopy "%SRC%" "%DST%\" /E /I /H /Y >> "%LOG%" 2>&1
if errorlevel 1 (
    echo   ❌ Copy failed!
    pause
    exit /b 1
)
echo   ✅ Files copied to C:\HWP2024_Install >> "%LOG%"
echo   ✅ Copy complete!

echo.
echo [2/5] Cleaning old installations...
rd /s /q "C:\Program Files (x86)\HNC" 2>nul
rd /s /q "C:\Program Files\HNC" 2>nul
rd /s /q "%APPDATA%\Hnc" 2>nul
rd /s /q "%APPDATA%\Hancom" 2>nul
reg delete "HKCU\SOFTWARE\Hnc" /f 2>nul
reg delete "HKCU\SOFTWARE\Hancom" /f 2>nul
reg delete "HKLM\SOFTWARE\Hnc" /f 2>nul
reg delete "HKLM\SOFTWARE\Hancom" /f 2>nul
reg delete "HKLM\SOFTWARE\WOW6432Node\Hnc" /f 2>nul
reg delete "HKLM\SOFTWARE\WOW6432Node\Hancom" /f 2>nul
echo   ✅ Cleaned old files >> "%LOG%"

echo.
echo [3/5] Restarting Windows Installer service...
net stop msiserver /y >nul 2>&1
ping -n 3 127.0.0.1 >nul
net start msiserver >nul 2>&1
echo   ✅ Service restarted >> "%LOG%"

echo.
echo [4/5] Installing VC++ Redistributable...
"%DST%\install\VC_redist.x86.exe" /quiet /norestart >> "%LOG%" 2>&1
echo   ✅ VC++ installed >> "%LOG%"

echo.
echo [5/5] Starting HWP2024 Installation...
echo ============================================
echo    Installing from: %DST%\Install.exe
echo    Please click '설치' in the popup window!
echo ============================================
start /wait "" "%DST%\Install.exe"

if errorlevel 1 (
    echo.
    echo ============================================
    echo   ❌ Installation failed! Error code: %errorlevel%
    echo ============================================
    echo Failed with errorlevel %errorlevel% >> "%LOG%"
) else (
    echo.
    echo ============================================
    echo   ✅✅✅ HWP2024 Installed Successfully! ✅✅✅
    echo ============================================
    echo Success >> "%LOG%"
)

echo.
echo Log file: %LOG%
pause
