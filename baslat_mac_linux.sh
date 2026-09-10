#!/bin/bash

echo "KeyPulse baslatiliyor..."

# Komut kontrolü
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "[HATA] Python bulunamadi! Lutfen Python yukleyin."
    exit 1
fi

# Sanal ortam kontrolü ve kurulum
if [ ! -d ".venv" ]; then
    echo "Ilk kurulum yapiliyor (Bu islem birkac dakika surebilir)..."
    $PYTHON_CMD -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Uygulamayı başlat
$PYTHON_CMD main.py &
