@echo off
setlocal

REM 下限バリデーションが効いているかを確認する
set "PYTHON_EXE=python"
if exist "%~dp0..\.venv\Scripts\python.exe" set "PYTHON_EXE=%~dp0..\.venv\Scripts\python.exe"

set "FAILED=0"

pushd "%~dp0.." >nul

REM delay-ms=99は失敗(非0)が期待
"%PYTHON_EXE%" -m mc_command_paster ".\examples\smoke_commands.txt" --dry-run --countdown 10 --delay-ms 99 >nul 2>&1
if "%ERRORLEVEL%"=="0" (
  echo [NG] expected failure: --delay-ms 99
  set "FAILED=1"
) else (
  echo [OK] expected failure confirmed: --delay-ms 99
)

REM countdown=9は失敗(非0)が期待
"%PYTHON_EXE%" -m mc_command_paster ".\examples\smoke_commands.txt" --dry-run --countdown 9 --delay-ms 500 >nul 2>&1
if "%ERRORLEVEL%"=="0" (
  echo [NG] expected failure: --countdown 9
  set "FAILED=1"
) else (
  echo [OK] expected failure confirmed: --countdown 9
)

popd >nul

if "%FAILED%"=="1" exit /b 1

echo [OK] boundary checks passed
exit /b 0

