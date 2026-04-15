@echo off
setlocal

REM 各種テストをまとめて実行する
call "%~dp0run_unittest.bat"
if not "%ERRORLEVEL%"=="0" exit /b %ERRORLEVEL%

call "%~dp0run_dry_run.bat"
if not "%ERRORLEVEL%"=="0" exit /b %ERRORLEVEL%

call "%~dp0run_boundary_checks.bat"
if not "%ERRORLEVEL%"=="0" exit /b %ERRORLEVEL%

echo [OK] all checks passed
exit /b 0

