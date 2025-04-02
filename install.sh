#!/bin/bash

install_package() {
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y "$1"
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y "$1"
    elif command -v pacman &> /dev/null; then
        sudo pacman -Sy --noconfirm "$1"
    elif command -v zypper &> /dev/null; then
        sudo zypper install -y "$1"
    else
        echo "Gerenciador de pacotes não suportado. Instale '$1' manualmente."
        exit 1
    fi
}

if ! command -v python3 &> /dev/null; then
    install_package python3
else
    echo "Python3 já instalado."
fi

if ! command -v pip3 &> /dev/null; then
    install_package python3-pip
else
    echo "pip já instalado."
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME/.tuxgate"

if [ "$PROJECT_DIR" != "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
    cp -r "$PROJECT_DIR"/* "$TARGET_DIR"
    PROJECT_DIR="$TARGET_DIR"
fi

if [ ! -d "$PROJECT_DIR/venv" ]; then
    python3 -m venv "$PROJECT_DIR/venv"
fi

source "$PROJECT_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r "$PROJECT_DIR/resources/requirements.txt"

DESKTOP_FILE="$HOME/.local/share/applications/tuxgate.desktop"

cat > "$DESKTOP_FILE" <<EOL
[Desktop Entry]
Version=1.0
Name=TuxGate
Comment=Gerenciador de Acesso SSH
Exec=bash -c "source $HOME/.tuxgate/venv/bin/activate && python3 $HOME/.tuxgate/main.py"
Icon=$HOME/.tuxgate/resources/logo.svg
Terminal=true
Type=Application
Categories=Utility;
EOL

chmod +x "$DESKTOP_FILE"
echo "Instalação concluída. Use o atalho gráfico (TuxGate) para iniciar."
