#!/usr/bin/env python3
"""
ROM MANAGER - Retro ROM Organization Tool
==========================================
Organize, verify, and catalog your ROM collection.
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

BANNER = """
██████╗  ██████╗ ███╗   ███╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
██╔══██╗██╔═══██╗████╗ ████║    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
██████╔╝██║   ██║██╔████╔██║    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
██╔══██╗██║   ██║██║╚██╔╝██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██║ ╚═╝ ██║    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                        [ ROM COLLECTION MANAGER | n01d-timemachine ]
"""

# ROM file extensions by platform
PLATFORMS = {
    'nes': ['.nes', '.unf', '.unif'],
    'snes': ['.sfc', '.smc', '.fig'],
    'genesis': ['.md', '.gen', '.bin', '.smd'],
    'gameboy': ['.gb', '.gbc', '.sgb'],
    'gba': ['.gba', '.agb'],
    'n64': ['.n64', '.v64', '.z64'],
    'atari2600': ['.a26', '.bin'],
    'atari7800': ['.a78'],
    'mastersystem': ['.sms'],
    'gamegear': ['.gg'],
    'c64': ['.d64', '.t64', '.prg', '.crt'],
    'amiga': ['.adf', '.dms', '.ipf'],
    'dos': ['.exe', '.com', '.bat'],
    'msx': ['.rom', '.mx1', '.mx2'],
    'zxspectrum': ['.tap', '.tzx', '.z80', '.sna'],
    'arcade': ['.zip'],  # MAME ROMs
    'psx': ['.bin', '.iso', '.img', '.cue'],
    'pce': ['.pce', '.sgx']  # PC Engine/TurboGrafx
}

class ROMManager:
    """Manage ROM collections"""
    
    def __init__(self, rom_dir):
        self.rom_dir = Path(rom_dir)
        self.catalog = {'roms': [], 'platforms': {}, 'stats': {}}
        
    def scan_directory(self, recursive=True):
        """Scan directory for ROMs"""
        pattern = '**/*' if recursive else '*'
        
        for filepath in self.rom_dir.glob(pattern):
            if filepath.is_file():
                platform = self._identify_platform(filepath)
                if platform:
                    rom_info = self._analyze_rom(filepath, platform)
                    self.catalog['roms'].append(rom_info)
                    
                    if platform not in self.catalog['platforms']:
                        self.catalog['platforms'][platform] = []
                    self.catalog['platforms'][platform].append(rom_info)
                    
        self._calculate_stats()
        return self.catalog
        
    def _identify_platform(self, filepath):
        """Identify ROM platform by extension"""
        ext = filepath.suffix.lower()
        for platform, extensions in PLATFORMS.items():
            if ext in extensions:
                return platform
        return None
        
    def _analyze_rom(self, filepath, platform):
        """Analyze individual ROM file"""
        stat = filepath.stat()
        
        # Calculate hashes
        with open(filepath, 'rb') as f:
            data = f.read()
            md5 = hashlib.md5(data).hexdigest()
            sha1 = hashlib.sha1(data).hexdigest()
            crc32 = format(hashlib.new('crc32', data).digest()[-4:].hex(), 's')
            
        return {
            'name': filepath.stem,
            'filename': filepath.name,
            'path': str(filepath),
            'platform': platform,
            'size': stat.st_size,
            'size_human': self._human_size(stat.st_size),
            'md5': md5,
            'sha1': sha1,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
        
    def _human_size(self, size):
        """Convert bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
        
    def _calculate_stats(self):
        """Calculate collection statistics"""
        total_size = sum(r['size'] for r in self.catalog['roms'])
        self.catalog['stats'] = {
            'total_roms': len(self.catalog['roms']),
            'total_size': total_size,
            'total_size_human': self._human_size(total_size),
            'platforms': len(self.catalog['platforms']),
            'by_platform': {p: len(roms) for p, roms in self.catalog['platforms'].items()}
        }
        
    def find_duplicates(self):
        """Find duplicate ROMs by hash"""
        md5_map = {}
        duplicates = []
        
        for rom in self.catalog['roms']:
            md5 = rom['md5']
            if md5 in md5_map:
                duplicates.append({
                    'original': md5_map[md5],
                    'duplicate': rom['path'],
                    'md5': md5
                })
            else:
                md5_map[md5] = rom['path']
                
        return duplicates
        
    def verify_rom(self, filepath, expected_hash):
        """Verify ROM against known good hash"""
        with open(filepath, 'rb') as f:
            data = f.read()
            
        actual_md5 = hashlib.md5(data).hexdigest()
        actual_sha1 = hashlib.sha1(data).hexdigest()
        
        if expected_hash.lower() in [actual_md5, actual_sha1]:
            return True, "Hash matches"
        return False, f"Hash mismatch. Got MD5: {actual_md5}"
        
    def organize(self, dest_dir, by='platform', dry_run=True):
        """Organize ROMs into folders"""
        dest = Path(dest_dir)
        moves = []
        
        for rom in self.catalog['roms']:
            if by == 'platform':
                target_dir = dest / rom['platform']
            elif by == 'letter':
                first_letter = rom['name'][0].upper()
                if not first_letter.isalpha():
                    first_letter = '#'
                target_dir = dest / first_letter
            else:
                target_dir = dest
                
            target_path = target_dir / rom['filename']
            moves.append({
                'source': rom['path'],
                'dest': str(target_path)
            })
            
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                Path(rom['path']).rename(target_path)
                
        return moves
        
    def export_catalog(self, output_file):
        """Export catalog to JSON"""
        with open(output_file, 'w') as f:
            json.dump(self.catalog, f, indent=2)
        return output_file


def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="ROM Collection Manager")
    parser.add_argument("directory", nargs='?', default='.',
                       help="ROM directory to scan")
    parser.add_argument("-s", "--scan", action="store_true",
                       help="Scan and catalog ROMs")
    parser.add_argument("-d", "--duplicates", action="store_true",
                       help="Find duplicate ROMs")
    parser.add_argument("-o", "--organize", metavar="DEST",
                       help="Organize ROMs into destination folder")
    parser.add_argument("--by", choices=['platform', 'letter'],
                       default='platform', help="Organization method")
    parser.add_argument("--export", metavar="FILE",
                       help="Export catalog to JSON")
    parser.add_argument("-v", "--verify", nargs=2, metavar=('FILE', 'HASH'),
                       help="Verify ROM against hash")
    parser.add_argument("--no-recursive", action="store_true",
                       help="Don't scan subdirectories")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be done without doing it")
    
    args = parser.parse_args()
    
    if args.verify:
        filepath, expected_hash = args.verify
        print(f"[*] Verifying: {filepath}")
        valid, msg = ROMManager('.').verify_rom(filepath, expected_hash)
        if valid:
            print(f"[✓] {msg}")
        else:
            print(f"[✗] {msg}")
        sys.exit(0 if valid else 1)
        
    manager = ROMManager(args.directory)
    
    if args.scan or args.duplicates or args.organize or args.export:
        print(f"[*] Scanning: {args.directory}")
        manager.scan_directory(not args.no_recursive)
        
        stats = manager.catalog['stats']
        print(f"\n[COLLECTION STATS]")
        print(f"  Total ROMs: {stats['total_roms']}")
        print(f"  Total Size: {stats['total_size_human']}")
        print(f"  Platforms: {stats['platforms']}")
        
        print(f"\n[BY PLATFORM]")
        for platform, count in sorted(stats['by_platform'].items(), 
                                       key=lambda x: x[1], reverse=True):
            print(f"  {platform:15} {count:5} ROMs")
            
    if args.duplicates:
        dups = manager.find_duplicates()
        print(f"\n[DUPLICATES] Found {len(dups)}")
        for dup in dups[:10]:
            print(f"  {dup['original']}")
            print(f"    ↳ {dup['duplicate']}")
            
    if args.organize:
        moves = manager.organize(args.organize, args.by, args.dry_run)
        action = "Would move" if args.dry_run else "Moving"
        print(f"\n[ORGANIZE] {action} {len(moves)} files")
        for move in moves[:5]:
            print(f"  {move['source']} → {move['dest']}")
        if len(moves) > 5:
            print(f"  ... and {len(moves) - 5} more")
            
    if args.export:
        manager.export_catalog(args.export)
        print(f"\n[*] Catalog exported: {args.export}")
        
    if not any([args.scan, args.duplicates, args.organize, args.export, args.verify]):
        print("[*] Use --scan, --duplicates, --organize, --export, or --verify")
        print("[*] Example: rom-manager.py ~/roms --scan --export catalog.json")


if __name__ == "__main__":
    main()
