<!--
SEO Keywords: Commodore 64 emulator, ZX Spectrum emulator, Amiga emulator, Apple II emulator,
Atari 800 emulator, TI-99 emulator, MS-DOS emulator, classic computer emulator, 
8-bit computer emulator, 16-bit computer emulator, vintage computer emulator,
AmigaLive, VICE, FS-UAE, UAE, retro computing, classic gaming, bad-antics
-->

<div align="center">

```
 ████████╗██╗███╗   ███╗███████╗    ███╗   ███╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗
 ╚══██╔══╝██║████╗ ████║██╔════╝    ████╗ ████║██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝
    ██║   ██║██╔████╔██║█████╗      ██╔████╔██║███████║██║     ███████║██║██╔██╗ ██║█████╗  
    ██║   ██║██║╚██╔╝██║██╔══╝      ██║╚██╔╝██║██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝  
    ██║   ██║██║ ╚═╝ ██║███████╗    ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗
    ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
                    [ AUTHENTIC CLASSIC COMPUTING EXPERIENCE | bad-antics ]
```

### ⏰ Step Back in Time — Run Classic Computers in Their Full Glory

[![GitHub](https://img.shields.io/badge/GitHub-bad--antics-181717?style=for-the-badge&logo=github)](https://github.com/bad-antics)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Not an emulator collection. A time portal.**

*Experience computers as they were meant to be. No filters. No nostalgia goggles. Just raw, authentic hardware emulation.*

</div>

---

## ⚡ The Experience

Time Machine isn't about "vintage" or "retro". It's about stepping into 1985 and feeling what it was like to boot a Commodore 64, or experiencing the Amiga's revolutionary graphics for the first time.

**This is a unified launcher** that gives you instant access to:

| Era | Machine | Emulator Backend |
|-----|---------|------------------|
| 1977 | **Apple II** | LinApple / AppleWin |
| 1979 | **Atari 800** | Atari800 |
| 1981 | **ZX Spectrum** | FUSE |
| 1981 | **TI-99/4A** | MAME |
| 1982 | **Commodore 64** | VICE (x64sc) |
| 1985 | **Amiga 500** | FS-UAE |
| 1987 | **MS-DOS** | DOSBox-X |
| 1992 | **Amiga 1200** | FS-UAE |
| 1993 | **Amiga CD32** | FS-UAE |
| 1994 | **Amiga 4000** | FS-UAE |

---

## 🎯 Features

### Unified Experience
- **Single launcher** for all machines
- **N01D aesthetics** — cyberpunk green, hacker vibes
- **Authentic boot sequences** — experience real BIOS/ROM boots
- **CRT shader options** — phosphor glow, scanlines, or clean pixels
- **Sound chip emulation** — SID, Paula, AY-3-8910, all authentic

### The Amiga Suite
Full Amiga family support with **AmigaLive** integration:

| Machine | Chipset | RAM | Special Features |
|---------|---------|-----|-----------------|
| **A500** | OCS/ECS | 512K-2MB | Classic gaming, demos |
| **A500+** | ECS | 1MB | Enhanced chip RAM |
| **A600** | ECS | 1-2MB | Compact, HDD support |
| **A1200** | AGA | 2MB | 256 colors, faster CPU |
| **A3000** | ECS | 2MB | 030 CPU, autovector |
| **A4000** | AGA | 2-16MB | 040/060 CPU, high-end |
| **CD32** | AGA | 2MB | Console, Akiko chip |

### 8-Bit Legends

| Machine | CPU | Specialty |
|---------|-----|-----------|
| **C64** | 6510 @ 1MHz | SID sound, sprites |
| **ZX Spectrum** | Z80 @ 3.5MHz | ULA graphics, beeper |
| **Apple II** | 6502 @ 1MHz | Hi-res graphics, disk II |
| **Atari 800** | 6502 @ 1.79MHz | ANTIC/GTIA, POKEY sound |
| **TI-99** | TMS9900 | Speech synthesis |

### DOS Era

| System | Features |
|--------|----------|
| **MS-DOS** | 286-Pentium emulation, SoundBlaster, VGA |

---

## 🚀 Installation

### Quick Install (Linux/macOS)

```bash
curl -sL https://raw.githubusercontent.com/bad-antics/n01d-timemachine/main/install.sh | bash
```

### Manual Install

```bash
git clone https://github.com/bad-antics/n01d-timemachine.git
cd n01d-timemachine
pip install -r requirements.txt
python3 timemachine.py
```

### Dependencies

The installer will prompt to install emulator backends:

```bash
# Ubuntu/Debian
sudo apt install vice fsuae dosbox-x fuse-emulator-sdl atari800 linapple

# Fedora
sudo dnf install vice fsuae dosbox-x fuse-emulator-sdl atari800

# macOS (Homebrew)
brew install vice fs-uae dosbox-x fuse-emulator atari800
```

---

## 🖥️ Usage

### Launch the Time Machine

```bash
python3 timemachine.py
```

### Quick Launch Specific Machine

```bash
# Commodore 64
python3 timemachine.py --machine c64

# Amiga 500
python3 timemachine.py --machine a500

# ZX Spectrum 48K
python3 timemachine.py --machine spectrum48

# MS-DOS
python3 timemachine.py --machine dos

# Load specific disk/tape
python3 timemachine.py --machine c64 --disk game.d64
```

### GUI Mode

The launcher provides a full GUI with:
- Machine selection carousel
- ROM/disk/tape browser
- Configuration per machine
- Shader/CRT effects toggle
- Screenshot/recording

---

## 🎮 ROM & Disk Management

```
~/.timemachine/
├── roms/
│   ├── c64/           # Kernal, BASIC, Chargen
│   ├── amiga/         # Kickstart ROMs (1.3, 2.05, 3.1)
│   ├── spectrum/      # 48K, 128K ROMs
│   ├── apple2/        # Apple II+, //e ROMs
│   ├── atari800/      # OS ROMs, BASIC
│   └── dos/           # DOS boot disks
├── disks/
│   ├── c64/           # .d64, .t64, .prg
│   ├── amiga/         # .adf, .ipf, .hdf
│   ├── spectrum/      # .tzx, .tap, .z80
│   └── dos/           # .img, directories
└── config/
    └── machines.json  # Per-machine settings
```

---

## 🎨 Shader Presets

| Preset | Description |
|--------|-------------|
| `authentic` | CRT phosphor, scanlines, curvature |
| `clean` | Sharp pixels, no effects |
| `aperture` | RGB aperture grille |
| `composite` | Composite video artifacts |
| `amber` | Monochrome amber phosphor |
| `green` | Monochrome green (N01D default) |

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `F11` | Toggle fullscreen |
| `F10` | Machine menu |
| `F9` | Disk/tape swap |
| `F8` | Screenshot |
| `F5` | Reset machine |
| `Pause` | Pause emulation |
| `Ctrl+Q` | Exit to launcher |

---

## 🔧 Configuration

Edit `~/.timemachine/config/machines.json`:

```json
{
  "c64": {
    "model": "c64sc",
    "sid": "6581",
    "shader": "authentic",
    "autoload": true
  },
  "amiga": {
    "model": "A500",
    "kickstart": "1.3",
    "chip_ram": "512K",
    "fast_ram": "0K"
  }
}
```

---

## 🔗 Part of the N01D Suite

| App | Description |
|-----|-------------|
| **[Time Machine](https://github.com/bad-antics/n01d-timemachine)** | Classic computing (you are here) |
| **[N01D-Term](https://github.com/bad-antics/n01d-term)** | Terminal emulator |
| **[N01D-Notes](https://github.com/bad-antics/n01d-notes)** | Markdown notes |
| **[N01D-SysMon](https://github.com/bad-antics/n01d-sysmon)** | System monitor |
| **[N01D-Media](https://github.com/bad-antics/n01d-media)** | Media suite |

---

## 📜 Legal Notice

This project provides a **launcher interface only**. You must supply your own legally obtained:
- ROM files (Kickstart, Kernal, etc.)
- Software/games
- Emulator backends

Emulators themselves are open source. System ROMs are copyrighted by their respective owners.

---

<div align="center">

**[GitHub](https://github.com/bad-antics)** • **[NullSec](https://github.com/bad-antics/nullsec)** • **[Issues](https://github.com/bad-antics/n01d-timemachine/issues)**

*Step back in time. Experience computing as it was.*

**Time Machine** — *Part of the NullSec Framework*

</div>
