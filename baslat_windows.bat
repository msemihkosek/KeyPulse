@echo off
title KeyPulse Baslatici
echo KeyPulse baslatiliyor... Lutfen bekleyin.

:: Python yüklü mü kontrol et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [HATA] Python bulunamadi! Lutfen Python yukleyin ve PATH'e ekleyin.
    pause
    exit /b
)

:: Sanal ortam var mı kontrol et, yoksa kur
if not exist ".venv\Scripts\activate.bat" (
    echo Ilk kurulum yapiliyor (Bu islem birkac dakika surebilir)...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

:: Uygulamayı başlat
start pythonw main.py
exit
