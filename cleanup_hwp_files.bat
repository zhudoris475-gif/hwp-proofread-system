@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   HWP 교정 파일 정리 (중복/임시 삭제)
echo ============================================
echo.

set BASE=C:\AMD\AJ\hwp_proofreading_package
set XW=C:\Users\doris\Desktop\xwechat_files
set LOG=%USERPROFILE%\Desktop\cleanup_hwp_%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%.txt

echo [시작] %date% %time% > "%LOG%"

echo [1/3] 임시/박업 파일 삭제...
set /a TMP_CNT=0

for /r "%BASE%" %%f in (*.bak *.broken_* *.tmp) do (
    del /q "%%f" 2>nul
    if not exist "%%f" (
        echo   🗑 %%~nxf >> "%LOG%"
        set /a TMP_CNT+=1
    )
)

for /r "%BASE%" %%d in (__pycache__) do (
    rd /s /q "%%d" 2>nul
    if not exist "%%d" (
        echo   🗑 %%~nxd >> "%LOG%"
        set /a TMP_CNT+=1
    )
)
echo ✅ %TMP_CNT%개 임시 파일 삭제 완료 >> "%LOG%"
echo ✅ 임시 파일 %TMP_CNT%개 삭제 완료

echo.
echo [2/3] xwechat_files 중복 .py 삭제 (AMD/AJ 보존)...
set /a DUP_CNT=0

for /r "%XW%" %%f in (*.py) do (
    if exist "%BASE%\%%~nxf" (
        del /q "%%f" 2>nul
        if not exist "%%f" (
            echo   🗑 %%~nxf (xwechat) >> "%LOG%"
            set /a DUP_CNT+=1
        )
    )
)
echo ✅ %DUP_CNT%개 중복 파일 삭제 완료 >> "%LOG%"
echo ✅ 중복 파일 %DUP_CNT%개 삭제 완료

echo.
echo [3/3] 결과 확인...
echo.
echo ============================================
echo   ✅ 정리 완료!
echo   임시 파일: %TMP_CNT%개
echo   중복 파일: %DUP_CNT%개
echo   로그: %LOG%
echo ============================================

pause