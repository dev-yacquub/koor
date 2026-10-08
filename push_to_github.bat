@echo off
title Push Koor to GitHub
echo ==================================================
echo   PUSHING KOOR TO GITHUB (dev-yacquub/koor)
echo ==================================================
echo.
git push -u origin main
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==================================================
    echo   SUCCESSFULLY PUSHED TO GITHUB!
    echo ==================================================
) else (
    echo.
    echo If GitHub returned 'Repository not found', please make sure
    echo you created the repository 'koor' at https://github.com/new
)
echo.
pause
