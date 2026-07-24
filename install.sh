#!/bin/bash

# ============================================================
# HN DDOS V2 - AUTO INSTALLER (TERMUX/LINUX)
# ============================================================

echo "🔥 HN DDOS V2 - Installing requirements..."
echo "=========================================="

# Update packages (Termux)
if command -v pkg &> /dev/null; then
    echo "[*] Updating Termux packages..."
    pkg update -y && pkg upgrade -y
    pkg install python -y
    pkg install python-pip -y
fi

# Update packages (Linux)
if command -v apt &> /dev/null; then
    echo "[*] Updating Linux packages..."
    sudo apt update -y
    sudo apt install python3 python3-pip -y
fi

# Install Python packages
echo "[*] Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Extra dependencies for Termux
if command -v pkg &> /dev/null; then
    echo "[*] Installing Termux-specific dependencies..."
    pkg install openssl -y
    pkg install libxml2 -y
    pkg install libxslt -y
fi

# Success message
echo "=========================================="
echo "✅ ALL REQUIREMENTS INSTALLED SUCCESSFULLY!"
echo "🔥 Run: python cloudddos.py"
echo "=========================================="
