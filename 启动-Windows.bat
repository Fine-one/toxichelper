@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul

rem Clear broken proxy settings so pip and DeepSeek connect directly.
set "HTTP_PROXY="
set "HTTPS_PROXY="
set "ALL_PROXY="
set "http_proxy="
set "https_proxy="
set "all_proxy="

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found. Please install Python 3.10+ first.
  pause
  exit /b 1
)

if not exist .venv (
  echo [1/3] Creating .venv ...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create .venv
    pause
    exit /b 1
  )
)

echo [2/3] Installing requirements ...
".venv\Scripts\python.exe" -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --disable-pip-version-check
if errorlevel 1 (
  echo [ERROR] pip install failed.
  pause
  exit /b 1
)

if not exist .streamlit mkdir .streamlit
if not exist .streamlit\secrets.toml (
  echo DEEPSEEK_API_KEY = "sk-REPLACE_ME"> .streamlit\secrets.toml
  echo [INFO] Created .streamlit\secrets.toml. Paste your real key, then restart.
)

echo [3/3] Starting http://localhost:8501 ...
".venv\Scripts\streamlit.exe" run app.py
pause
