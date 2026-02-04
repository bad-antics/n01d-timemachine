<!--
SEO Keywords: Commodore 64 emulator, ZX Spectrum emulator, Amiga emulator, Apple II emulator,
Atari 800 emulator, TI-99 emulator, MS-DOS emulator, classic computer emulator, 
8-bit computer emulator, 16-bit computer emulator, AmigaLive, VICE, FS-UAE, bad-antics
-->

<div align="center">

```
╔═══════════════════════════════════════════════════════════════╗
║  ⏰ TIME MACHINE  ·  Authentic Classic Computing Experience   ║
╚═══════════════════════════════════════════════════════════════╝
```

[![GitHub](https://img.shields.io/badge/GitHub-bad--antics-181717?style=for-the-badge&logo=github)](https://github.com/bad-antics)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Not an emulator collection. A time portal.**

*Experience computers as they were meant to be. No filters. Just authentic hardware emulation.*

</div>

---

## ⚡ Supported Machines

| Era | Machine | Emulator Backend |
|-----|---------|------------------|
| 1977 | **Apple II** | LinApple |
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

- **Single launcher** for all machines
- **N01D aesthetics** — cyberpunk green, hacker vibes
- **Authentic boot sequences** — real BIOS/ROM boots
- **CRT shader options** — phosphor glow, scanlines, clean pixels
- **Full Amiga suite** — A500, A500+, A600, A1200, A3000, A4000, CD32

---

## 🚀 Installation

```bash
# Quick Install
curl -sL https://raw.githubusercontent.com/bad-antics/n01d-timemachine/main/install.sh | bash

# Manual Install
git clone https://github.com/bad-antics/n01d-timemachine.git
cd n01d-timemachine
pip install -r requirements.txt
python3 timemachine.py
```

### Dependencies

```bash
# Ubuntu/Debian
sudo apt install vice fsuae dosbox-x fuse-emulator-sdl atari800 linapple
```

---

## 🖥️ Usage

```bash
# Launch GUI
python3 timemachine.py

# Quick launch specific machine
python3 timemachine.py --machine c64
python3 timemachine.py --machine a500
python3 timemachine.py --machine spectrum48

# Load disk
python3 timemachine.py --machine c64 --disk game.d64
```

---

## 🎮 ROM & Disk Management

```
~/.timemachine/
├── roms/           # System ROMs
│   ├── c64/
│   ├── amiga/
│   └── spectrum/
├── disks/          # Software
│   ├── c64/        # .d64, .t64, .prg
│   ├── amiga/      # .adf, .ipf, .hdf
│   └── spectrum/   # .tzx, .tap, .z80
└── config/
    └── machines.json
```

---

## 🎨 Shader Presets

| Preset | Description |
|--------|-------------|
| `authentic` | CRT phosphor, scanlines, curvature |
| `clean` | Sharp pixels, no effects |
| `green` | Monochrome green (N01D default) |

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `F11` | Fullscreen |
| `F10` | Machine menu |
| `F5` | Reset |
| `Ctrl+Q` | Exit |

---

## 📜 Legal Notice

This is a **launcher interface only**. Supply your own legally obtained ROMs and software.

---

## 🔗 Part of the N01D Suite

| App | Description |
|-----|-------------|
| **[Time Machine](https://github.com/bad-antics/n01d-timemachine)** | Classic computing |
| **[N01D-Term](https://github.com/bad-antics/n01d-term)** | Terminal |
| **[N01D-Media](https://github.com/bad-antics/n01d-media)** | Media suite |

---

<div align="center">

**[GitHub](https://github.com/bad-antics)** • **[NullSec](https://github.com/bad-antics/nullsec)** • **[Issues](https://github.com/bad-antics/n01d-timemachine/issues)**

*Step back in time.*

</div>
