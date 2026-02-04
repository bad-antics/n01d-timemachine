#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                              TIME MACHINE                                       ║
║              Authentic Classic Computing Experience | bad-antics               ║
╚════════════════════════════════════════════════════════════════════════════════╝

Unified launcher for classic computer emulation.
Step back in time. Experience computing as it was.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List
import argparse

try:
    import customtkinter as ctk
    from PIL import Image
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

# N01D Color Scheme
N01D_BG = "#0a0a0a"
N01D_FG = "#00ff41"
N01D_ACCENT = "#00cc33"
N01D_DIM = "#004d00"
N01D_HIGHLIGHT = "#33ff66"

# Configuration paths
CONFIG_DIR = Path.home() / ".timemachine"
ROMS_DIR = CONFIG_DIR / "roms"
DISKS_DIR = CONFIG_DIR / "disks"
CONFIG_FILE = CONFIG_DIR / "config" / "machines.json"

@dataclass
class Machine:
    """Classic computer definition"""
    id: str
    name: str
    year: int
    cpu: str
    emulator: str
    emulator_cmd: List[str]
    extensions: List[str]
    description: str
    
# Machine definitions
MACHINES: Dict[str, Machine] = {
    "c64": Machine(
        id="c64",
        name="Commodore 64",
        year=1982,
        cpu="MOS 6510 @ 1 MHz",
        emulator="x64sc",
        emulator_cmd=["x64sc"],
        extensions=[".d64", ".t64", ".prg", ".tap", ".crt"],
        description="The best-selling home computer. SID sound, sprites, BASIC V2."
    ),
    "c128": Machine(
        id="c128",
        name="Commodore 128",
        year=1985,
        cpu="MOS 8502 @ 2 MHz",
        emulator="x128",
        emulator_cmd=["x128"],
        extensions=[".d64", ".d71", ".d81", ".prg"],
        description="C64 compatibility plus 80-column mode and CP/M."
    ),
    "vic20": Machine(
        id="vic20",
        name="VIC-20",
        year=1980,
        cpu="MOS 6502 @ 1 MHz",
        emulator="xvic",
        emulator_cmd=["xvic"],
        extensions=[".prg", ".crt", ".tap"],
        description="First computer to sell one million units."
    ),
    "a500": Machine(
        id="a500",
        name="Amiga 500",
        year=1987,
        cpu="Motorola 68000 @ 7.09 MHz",
        emulator="fs-uae",
        emulator_cmd=["fs-uae", "--amiga-model=A500"],
        extensions=[".adf", ".ipf", ".hdf", ".lha"],
        description="The people's Amiga. OCS chipset, incredible for its time."
    ),
    "a500plus": Machine(
        id="a500plus",
        name="Amiga 500+",
        year=1991,
        cpu="Motorola 68000 @ 7.09 MHz",
        emulator="fs-uae",
        emulator_cmd=["fs-uae", "--amiga-model=A500+"],
        extensions=[".adf", ".ipf", ".hdf"],
        description="Enhanced A500 with ECS chipset and 1MB chip RAM."
    ),
    "a600": Machine(
        id="a600",
        name="Amiga 600",
        year=1992,
        cpu="Motorola 68000 @ 7.09 MHz",
        emulator="fs-uae",
        emulator_cmd=["fs-uae", "--amiga-model=A600"],
        extensions=[".adf", ".ipf", ".hdf"],
        description="Compact Amiga with IDE hard drive support."
    ),
    "a1200": Machine(
        id="a1200",
        name="Amiga 1200",
        year=1992,
        cpu="Motorola 68EC020 @ 14 MHz",
        emulator="fs-uae",
        emulator_cmd=["fs-uae", "--amiga-model=A1200"],
        extensions=[".adf", ".ipf", ".hdf", ".lha"],
        description="AGA chipset, 256 colors, the enthusiast's Amiga."
    ),
    "a3000": Machine(
        id="a3000",
        name="Amiga 3000",
        year=1990,
        cpu="Motorola 68030 @ 25 MHz",
        emulator="fs-uae",
        emulator_cmd=["fs-uae", "--amiga-model=A3000"],
        extensions=[".adf", ".hdf"],
        description="Professional workstation with 68030 CPU."
    ),
    "a4000": Machine(
        id="a4000",
        name="Amiga 4000",
        year=1992,
        cpu="Motorola 68040 @ 25 MHz",
        emulator="fs-uae",
        emulator_cmd=["fs-uae", "--amiga-model=A4000"],
        extensions=[".adf", ".hdf"],
        description="High-end Amiga with 68040 and AGA."
    ),
    "cd32": Machine(
        id="cd32",
        name="Amiga CD32",
        year=1993,
        cpu="Motorola 68EC020 @ 14 MHz",
        emulator="fs-uae",
        emulator_cmd=["fs-uae", "--amiga-model=CD32"],
        extensions=[".iso", ".cue", ".bin"],
        description="32-bit game console. AGA chipset, Akiko chip."
    ),
    "spectrum48": Machine(
        id="spectrum48",
        name="ZX Spectrum 48K",
        year=1982,
        cpu="Zilog Z80 @ 3.5 MHz",
        emulator="fuse",
        emulator_cmd=["fuse", "--machine=48"],
        extensions=[".tzx", ".tap", ".z80", ".sna"],
        description="Sir Clive Sinclair's masterpiece. UK gaming icon."
    ),
    "spectrum128": Machine(
        id="spectrum128",
        name="ZX Spectrum 128K",
        year=1986,
        cpu="Zilog Z80 @ 3.5 MHz",
        emulator="fuse",
        emulator_cmd=["fuse", "--machine=128"],
        extensions=[".tzx", ".tap", ".z80", ".sna"],
        description="128K RAM, AY sound chip, enhanced graphics."
    ),
    "apple2": Machine(
        id="apple2",
        name="Apple II",
        year=1977,
        cpu="MOS 6502 @ 1 MHz",
        emulator="linapple",
        emulator_cmd=["linapple"],
        extensions=[".dsk", ".nib", ".po", ".do"],
        description="The machine that started Apple. Integer BASIC, hi-res graphics."
    ),
    "apple2e": Machine(
        id="apple2e",
        name="Apple //e",
        year=1983,
        cpu="MOS 6502 @ 1 MHz",
        emulator="linapple",
        emulator_cmd=["linapple"],
        extensions=[".dsk", ".nib", ".po", ".do"],
        description="Enhanced Apple II with 64K, better keyboard."
    ),
    "atari800": Machine(
        id="atari800",
        name="Atari 800",
        year=1979,
        cpu="MOS 6502 @ 1.79 MHz",
        emulator="atari800",
        emulator_cmd=["atari800"],
        extensions=[".atr", ".xex", ".xfd", ".cas"],
        description="ANTIC, GTIA, POKEY. Advanced graphics and sound for 1979."
    ),
    "atari800xl": Machine(
        id="atari800xl",
        name="Atari 800XL",
        year=1983,
        cpu="MOS 6502C @ 1.79 MHz",
        emulator="atari800",
        emulator_cmd=["atari800", "-xl"],
        extensions=[".atr", ".xex", ".xfd"],
        description="64K RAM, built-in BASIC, the popular Atari 8-bit."
    ),
    "ti99": Machine(
        id="ti99",
        name="TI-99/4A",
        year=1981,
        cpu="TMS9900 @ 3 MHz",
        emulator="mame",
        emulator_cmd=["mame", "ti99_4a"],
        extensions=[".rpk", ".dsk"],
        description="16-bit CPU in a home computer. Speech synthesis optional."
    ),
    "dos": Machine(
        id="dos",
        name="MS-DOS PC",
        year=1981,
        cpu="Intel 8086-Pentium",
        emulator="dosbox-x",
        emulator_cmd=["dosbox-x"],
        extensions=[".exe", ".com", ".bat", ".img"],
        description="IBM PC compatible. From CGA to VGA, PC speaker to SoundBlaster."
    ),
}

class TimeMachineConfig:
    """Configuration management"""
    
    def __init__(self):
        self.ensure_dirs()
        self.config = self.load_config()
    
    def ensure_dirs(self):
        """Create necessary directories"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        ROMS_DIR.mkdir(parents=True, exist_ok=True)
        DISKS_DIR.mkdir(parents=True, exist_ok=True)
        (CONFIG_DIR / "config").mkdir(parents=True, exist_ok=True)
        
        # Create machine-specific dirs
        for machine_id in MACHINES:
            (ROMS_DIR / machine_id).mkdir(exist_ok=True)
            (DISKS_DIR / machine_id).mkdir(exist_ok=True)
    
    def load_config(self) -> dict:
        """Load configuration file"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                return json.load(f)
        return self.default_config()
    
    def default_config(self) -> dict:
        """Generate default configuration"""
        return {
            "default_machine": "c64",
            "shader": "authentic",
            "fullscreen": False,
            "machines": {
                "c64": {"sid": "6581", "model": "c64sc"},
                "a500": {"kickstart": "1.3", "chip_ram": "512K"},
                "spectrum48": {"joystick": "kempston"},
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)

def check_emulator(emulator: str) -> bool:
    """Check if emulator is installed"""
    return shutil.which(emulator) is not None

def get_available_machines() -> List[Machine]:
    """Return list of machines with available emulators"""
    available = []
    for machine in MACHINES.values():
        if check_emulator(machine.emulator):
            available.append(machine)
    return available

def launch_machine(machine: Machine, disk: Optional[str] = None, config: Optional[dict] = None):
    """Launch emulator for specified machine"""
    cmd = machine.emulator_cmd.copy()
    
    # Add disk/tape if specified
    if disk:
        if machine.emulator == "x64sc":
            cmd.extend(["-autostart", disk])
        elif machine.emulator == "fs-uae":
            cmd.extend([f"--floppy-drive-0={disk}"])
        elif machine.emulator == "fuse":
            cmd.append(disk)
        elif machine.emulator == "dosbox-x":
            cmd.extend(["-c", f"mount c {disk}", "-c", "c:"])
        else:
            cmd.append(disk)
    
    print(f"\n{'='*60}")
    print(f"  LAUNCHING: {machine.name} ({machine.year})")
    print(f"  CPU: {machine.cpu}")
    print(f"  Emulator: {machine.emulator}")
    print(f"{'='*60}\n")
    
    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        print(f"Error: Emulator '{machine.emulator}' not found.")
        print(f"Install with: sudo apt install {machine.emulator}")
        return False
    return True

def print_banner():
    """Display Time Machine banner"""
    banner = """
\033[32m
 ████████╗██╗███╗   ███╗███████╗    ███╗   ███╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗
 ╚══██╔══╝██║████╗ ████║██╔════╝    ████╗ ████║██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝
    ██║   ██║██╔████╔██║█████╗      ██╔████╔██║███████║██║     ███████║██║██╔██╗ ██║█████╗  
    ██║   ██║██║╚██╔╝██║██╔══╝      ██║╚██╔╝██║██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝  
    ██║   ██║██║ ╚═╝ ██║███████╗    ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗
    ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
\033[0m
                   \033[90m[ AUTHENTIC CLASSIC COMPUTING | bad-antics ]\033[0m
"""
    print(banner)

def list_machines():
    """Display available machines"""
    print("\n  AVAILABLE TIME MACHINES:")
    print("  " + "="*56)
    
    available = get_available_machines()
    all_machines = list(MACHINES.values())
    
    for m in sorted(all_machines, key=lambda x: x.year):
        status = "\033[32m●\033[0m" if m in available else "\033[31m○\033[0m"
        print(f"  {status} {m.id:12} {m.year}  {m.name:20} [{m.emulator}]")
    
    print()
    print(f"  \033[32m●\033[0m = Emulator available    \033[31m○\033[0m = Emulator not installed")
    print()

def interactive_menu():
    """Interactive CLI menu"""
    config = TimeMachineConfig()
    
    while True:
        print_banner()
        list_machines()
        
        print("  OPTIONS:")
        print("  [machine-id]  Launch machine (e.g., 'c64', 'a500')")
        print("  [l]           List machines")
        print("  [q]           Quit")
        print()
        
        choice = input("  \033[32m>\033[0m ").strip().lower()
        
        if choice == 'q':
            print("\n  Returning to the present...\n")
            break
        elif choice == 'l':
            continue
        elif choice in MACHINES:
            machine = MACHINES[choice]
            if not check_emulator(machine.emulator):
                print(f"\n  \033[31mError:\033[0m Emulator '{machine.emulator}' not installed.")
                print(f"  Install: sudo apt install {machine.emulator}\n")
                input("  Press Enter to continue...")
            else:
                launch_machine(machine)
        else:
            print(f"\n  Unknown machine: {choice}")
            input("  Press Enter to continue...")

# GUI Application
if GUI_AVAILABLE:
    class TimeMachineGUI(ctk.CTk):
        """Time Machine GUI Application"""
        
        def __init__(self):
            super().__init__()
            
            self.title("Time Machine")
            self.geometry("900x700")
            self.configure(fg_color=N01D_BG)
            
            ctk.set_appearance_mode("dark")
            
            self.config = TimeMachineConfig()
            self.selected_machine = None
            
            self.create_ui()
        
        def create_ui(self):
            # Header
            header = ctk.CTkLabel(
                self,
                text="⏰ TIME MACHINE",
                font=ctk.CTkFont(family="Courier", size=32, weight="bold"),
                text_color=N01D_FG
            )
            header.pack(pady=20)
            
            subtitle = ctk.CTkLabel(
                self,
                text="Authentic Classic Computing Experience",
                font=ctk.CTkFont(size=14),
                text_color=N01D_DIM
            )
            subtitle.pack()
            
            # Machine list frame
            list_frame = ctk.CTkScrollableFrame(
                self,
                fg_color="#111111",
                width=800,
                height=400
            )
            list_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Add machines
            for machine in sorted(MACHINES.values(), key=lambda x: x.year):
                self.add_machine_card(list_frame, machine)
            
            # Launch button
            self.launch_btn = ctk.CTkButton(
                self,
                text="LAUNCH TIME MACHINE",
                font=ctk.CTkFont(size=18, weight="bold"),
                fg_color=N01D_DIM,
                hover_color=N01D_ACCENT,
                text_color=N01D_BG,
                height=50,
                command=self.launch_selected
            )
            self.launch_btn.pack(pady=20)
            
            # Status
            self.status = ctk.CTkLabel(
                self,
                text="Select a machine to begin your journey",
                font=ctk.CTkFont(size=12),
                text_color=N01D_DIM
            )
            self.status.pack(pady=10)
        
        def add_machine_card(self, parent, machine: Machine):
            available = check_emulator(machine.emulator)
            
            card = ctk.CTkFrame(
                parent,
                fg_color="#1a1a1a" if available else "#0d0d0d",
                corner_radius=10
            )
            card.pack(pady=5, padx=10, fill="x")
            
            # Year badge
            year_label = ctk.CTkLabel(
                card,
                text=str(machine.year),
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=N01D_ACCENT if available else N01D_DIM,
                width=60
            )
            year_label.pack(side="left", padx=10, pady=10)
            
            # Machine info
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10)
            
            name_label = ctk.CTkLabel(
                info_frame,
                text=machine.name,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=N01D_FG if available else N01D_DIM,
                anchor="w"
            )
            name_label.pack(anchor="w")
            
            desc_label = ctk.CTkLabel(
                info_frame,
                text=f"{machine.cpu} • {machine.description[:50]}...",
                font=ctk.CTkFont(size=11),
                text_color="#666666",
                anchor="w"
            )
            desc_label.pack(anchor="w")
            
            # Status indicator
            status_text = "● Ready" if available else "○ Install: " + machine.emulator
            status_color = N01D_ACCENT if available else "#cc0000"
            
            status_label = ctk.CTkLabel(
                card,
                text=status_text,
                font=ctk.CTkFont(size=11),
                text_color=status_color,
                width=150
            )
            status_label.pack(side="right", padx=10)
            
            # Make clickable
            if available:
                card.bind("<Button-1>", lambda e, m=machine: self.select_machine(m))
                for child in card.winfo_children():
                    child.bind("<Button-1>", lambda e, m=machine: self.select_machine(m))
        
        def select_machine(self, machine: Machine):
            self.selected_machine = machine
            self.status.configure(
                text=f"Selected: {machine.name} ({machine.year})",
                text_color=N01D_FG
            )
            self.launch_btn.configure(fg_color=N01D_ACCENT)
        
        def launch_selected(self):
            if self.selected_machine:
                self.status.configure(text=f"Launching {self.selected_machine.name}...")
                self.update()
                launch_machine(self.selected_machine)
                self.status.configure(text="Select a machine to begin your journey")

def main():
    parser = argparse.ArgumentParser(
        description="Time Machine - Authentic Classic Computing Experience"
    )
    parser.add_argument(
        "--machine", "-m",
        help="Machine to launch (c64, a500, spectrum48, etc.)"
    )
    parser.add_argument(
        "--disk", "-d",
        help="Disk/tape image to load"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available machines"
    )
    parser.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Launch GUI mode"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Force CLI mode"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print_banner()
        list_machines()
        return
    
    if args.machine:
        if args.machine not in MACHINES:
            print(f"Unknown machine: {args.machine}")
            print(f"Available: {', '.join(MACHINES.keys())}")
            sys.exit(1)
        
        machine = MACHINES[args.machine]
        launch_machine(machine, args.disk)
        return
    
    # Default behavior
    if args.gui or (GUI_AVAILABLE and not args.cli):
        app = TimeMachineGUI()
        app.mainloop()
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
