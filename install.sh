#!/bin/bash
#╔════════════════════════════════════════════════════════════════════════════════╗
#║                           TIME MACHINE INSTALLER                               ║
#║              Authentic Classic Computing Experience | bad-antics              ║
#╚════════════════════════════════════════════════════════════════════════════════╝

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
DIM='\033[0;90m'

echo -e "${GREEN}"
cat << 'BANNER'
 ████████╗██╗███╗   ███╗███████╗    ███╗   ███╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗
 ╚══██╔══╝██║████╗ ████║██╔════╝    ████╗ ████║██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝
    ██║   ██║██╔████╔██║█████╗      ██╔████╔██║███████║██║     ███████║██║██╔██╗ ██║█████╗  
    ██║   ██║██║╚██╔╝██║██╔══╝      ██║╚██╔╝██║██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝  
    ██║   ██║██║ ╚═╝ ██║███████╗    ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗
    ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
BANNER
echo -e "${NC}"
echo -e "${DIM}                   [ INSTALLER | bad-antics ]${NC}"
echo ""

INSTALL_DIR="${HOME}/.local/share/timemachine"
BIN_DIR="${HOME}/.local/bin"

echo -e "[*] Installing Time Machine..."

# Clone or update repo
if [ -d "$INSTALL_DIR" ]; then
    echo "[*] Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "[*] Cloning repository..."
    git clone https://github.com/bad-antics/n01d-timemachine.git "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# Install Python dependencies
echo "[*] Installing Python dependencies..."
pip3 install --user -r requirements.txt 2>/dev/null || pip install --user -r requirements.txt

# Create directories
echo "[*] Creating configuration directories..."
mkdir -p ~/.timemachine/{roms,disks,config}
mkdir -p ~/.timemachine/roms/{c64,amiga,spectrum,apple2,atari800,dos}
mkdir -p ~/.timemachine/disks/{c64,amiga,spectrum,apple2,atari800,dos}

# Create symlink
mkdir -p "$BIN_DIR"
ln -sf "$INSTALL_DIR/timemachine.py" "$BIN_DIR/timemachine"
chmod +x "$BIN_DIR/timemachine"

# Check for emulators
echo ""
echo -e "${GREEN}[✓] Time Machine installed!${NC}"
echo ""
echo "Checking for emulators..."
echo ""

check_emu() {
    if command -v "$1" &> /dev/null; then
        echo -e "  ${GREEN}●${NC} $2 ($1)"
    else
        echo -e "  ${RED}○${NC} $2 - Install: $3"
    fi
}

check_emu "x64sc" "Commodore 64" "sudo apt install vice"
check_emu "fs-uae" "Amiga" "sudo apt install fs-uae"
check_emu "fuse" "ZX Spectrum" "sudo apt install fuse-emulator-sdl"
check_emu "dosbox-x" "MS-DOS" "sudo apt install dosbox-x"
check_emu "atari800" "Atari 800" "sudo apt install atari800"
check_emu "linapple" "Apple II" "sudo apt install linapple"

echo ""
echo -e "Run: ${GREEN}timemachine${NC} to start"
echo -e "Or:  ${GREEN}timemachine --help${NC} for options"
echo ""
