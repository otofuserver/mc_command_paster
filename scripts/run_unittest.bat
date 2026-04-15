@echo off
setlocal

REM unittestを実行する
set "PYTHON_EXE=python"
if exist "%~dp0..\.venv\Scripts\python.exe" set "PYTHON_EXE=%~dp0..\.venv\Scripts\python.exe"

pushd "%~dp0.." >nul
"%PYTHON_EXE%" -m unittest discover -s tests -v
set "EXIT_CODE=%ERRORLEVEL%"
popd >nul

if not "%EXIT_CODE%"=="0" (
  echo [NG] unittest failed with exit code %EXIT_CODE%
  exit /b %EXIT_CODE%
)

echo [OK] unittest passed
exit /b 0

