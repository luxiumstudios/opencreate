#!/usr/bin/env bash

set -e

echo "Welcome to the openCreate launcher installer!"

echo "Which Linux distro are you using?"
echo "1) Arch (including Manjaro, EndeavourOS)"
echo "2) Debian/Ubuntu (including Mint, Pop!_OS, etc)"
echo "3) Fedora"
echo "4) Other"
read -rp "Enter the number: " DISTRO

INSTALL_DIR="/usr/local/share/opencreate"
BIN_DIR="/usr/local/bin"
REPO_URL="https://github.com/luxiumstudios/opencreate.git"
REPO_DIR="opencreate-tmp-$$"

install_pkgs_arch() {
    sudo pacman -Sy --needed python python-pyqt5 gimp inkscape blender kdenlive shotcut git
}

install_pkgs_debian() {
    sudo apt update
    sudo apt install -y python3 python3-pyqt5 gimp inkscape blender kdenlive shotcut git
}

install_pkgs_fedora() {
    sudo dnf install -y python3 python3-qt5 gimp inkscape blender kdenlive shotcut git
}

install_pkgs_other() {
    echo "Please install Python 3, PyQt5, GIMP, Inkscape, Blender, Kdenlive, and Shotcut using your package manager."
    echo "Press Enter to continue once done."
    read
}

PYQT_INSTALLED=0

case "$DISTRO" in
    1)
        install_pkgs_arch
        if pacman -Q python-pyqt5 &>/dev/null; then
            PYQT_INSTALLED=1
        fi
        ;;
    2)
        install_pkgs_debian
        if dpkg -l | grep python3-pyqt5 &>/dev/null; then
            PYQT_INSTALLED=1
        fi
        ;;
    3)
        install_pkgs_fedora
        if rpm -q python3-qt5 &>/dev/null; then
            PYQT_INSTALLED=1
        fi
        ;;
    4)
        install_pkgs_other
        ;;
    *)
        echo "Invalid option"; exit 1 ;;
esac

echo "Downloading the openCreate launcher repository..."
git clone --depth=1 "$REPO_URL" "$REPO_DIR"

# Or, if you prefer not to require git, use:
# curl -L "$REPO_URL/archive/refs/heads/main.zip" -o repo.zip
# unzip repo.zip
# REPO_DIR=$(find . -maxdepth 1 -type d -name "YOUR_REPO-*")

if [ "$PYQT_INSTALLED" -eq 1 ]; then
    echo "PyQt5 installed via package manager."
    sudo mkdir -p "$INSTALL_DIR"
    sudo cp "$REPO_DIR/opencreate_launcher.py" "$INSTALL_DIR/"
    sudo cp "$REPO_DIR"/*.png "$INSTALL_DIR/"
    sudo tee "$BIN_DIR/opencreate" > /dev/null <<EOF
#!/usr/bin/env bash
python3 "$INSTALL_DIR/opencreate_launcher.py"
EOF
    sudo chmod +x "$BIN_DIR/opencreate"

    # Add .desktop file with icon.png as the icon
    DESKTOP_FILE="/usr/share/applications/opencreate.desktop"
    ICON_PATH="$INSTALL_DIR/icon.png"
    sudo tee "$DESKTOP_FILE" > /dev/null <<EOF
[Desktop Entry]
Type=Application
Name=openCreate
Comment=Launcher for the openCreate suite of FOSS creative applications
Exec=$BIN_DIR/opencreate
Icon=$ICON_PATH
Terminal=false
Categories=Graphics;AudioVideo;Utility;
EOF
    sudo update-desktop-database || true

    echo "Installed opencreate system-wide. Run 'opencreate' to launch."
else
    echo "PyQt5 not found in package manager. Installing with pipx..."
    if ! command -v pipx &>/dev/null; then
        echo "pipx not found, installing..."
        python3 -m pip install --user pipx
        python3 -m pipx ensurepath
        export PATH="$HOME/.local/bin:$PATH"
    fi
    pipx install --force "$REPO_DIR/opencreate_launcher.py" --python python3 --include-deps
    echo "Installed opencreate with pipx. Run 'opencreate-launcher' to launch."
fi

# Clean up
rm -rf "$REPO_DIR"

echo "Installation complete!" 