@echo off
setlocal

REM dry-runの基本動作を確認する
set "PYTHON_EXE=python"
if exist "%~dp0..\.venv\Scripts\python.exe" set "PYTHON_EXE=%~dp0..\.venv\Scripts\python.exe"

pushd "%~dp0.." >nul
"%PYTHON_EXE%" -m mc_command_paster ".\examples\smoke_commands.txt" --dry-run --countdown 10 --delay-ms 500
set "EXIT_CODE=%ERRORLEVEL%"
popd >nul

if not "%EXIT_CODE%"=="0" (
  echo [NG] dry-run failed with exit code %EXIT_CODE%
  exit /b %EXIT_CODE%
)

echo [OK] dry-run passed
exit /b 0

