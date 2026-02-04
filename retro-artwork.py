#!/usr/bin/env python3
"""
RETRO ARTWORK - Box Art & Screenshot Scraper
=============================================
Download game artwork from various sources.
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

BANNER = """
██████╗ ███████╗████████╗██████╗  ██████╗      █████╗ ██████╗ ████████╗
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗    ██╔══██╗██╔══██╗╚══██╔══╝
██████╔╝█████╗     ██║   ██████╔╝██║   ██║    ███████║██████╔╝   ██║   
██╔══██╗██╔══╝     ██║   ██╔══██╗██║   ██║    ██╔══██║██╔══██╗   ██║   
██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝    ██║  ██║██║  ██║   ██║   
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                [ GAME ARTWORK MANAGER | n01d-timemachine ]
"""

# Platform mappings for various APIs
PLATFORM_IDS = {
    # TheGamesDB IDs
    'tgdb': {
        'nes': 7, 'snes': 6, 'n64': 3, 'gamecube': 2,
        'genesis': 18, 'mastersystem': 35, 'gameboy': 4,
        'gba': 5, 'psx': 10, 'ps2': 11, 'arcade': 23,
        'c64': 40, 'amiga': 4911, 'atari2600': 22
    },
    # ScreenScraper IDs
    'ss': {
        'nes': 3, 'snes': 4, 'n64': 14, 'genesis': 1,
        'gameboy': 9, 'gba': 12, 'psx': 57, 'arcade': 75,
        'c64': 66, 'amiga': 64
    }
}

class ArtworkScraper:
    """Scrape game artwork from various sources"""
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache = {}
        
    def generate_local_artwork(self, game_name, platform, style='boxart'):
        """Generate placeholder ASCII art"""
        # Create a simple text-based placeholder
        clean_name = game_name[:20].upper()
        platform_upper = platform.upper()
        
        if style == 'boxart':
            art = f"""
╔══════════════════════════════╗
║                              ║
║  ┌────────────────────────┐  ║
║  │                        │  ║
║  │   {clean_name:^20}   │  ║
║  │                        │  ║
║  │   [{platform_upper:^16}]   │  ║
║  │                        │  ║
║  └────────────────────────┘  ║
║                              ║
║      N01D TIME MACHINE       ║
╚══════════════════════════════╝
"""
        else:  # screenshot style
            art = f"""
┌──────────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
│ ▓                              ▓ │
│ ▓   {clean_name:^26}   ▓ │
│ ▓                              ▓ │
│ ▓   PRESS START TO PLAY        ▓ │
│ ▓                              ▓ │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
└──────────────────────────────────┘
         {platform_upper}
"""
        return art.strip()
        
    def search_libretro_thumbnails(self, game_name, platform):
        """Search LibRetro thumbnail database (local path format)"""
        # LibRetro uses specific naming conventions
        clean_name = game_name.replace(':', ' -').replace('/', '_')
        
        base_paths = {
            'boxart': f"Named_Boxarts/{clean_name}.png",
            'title': f"Named_Titles/{clean_name}.png",
            'snap': f"Named_Snaps/{clean_name}.png"
        }
        
        return {
            'platform': platform,
            'game': game_name,
            'paths': base_paths,
            'url_template': f"https://thumbnails.libretro.com/{platform}/{{type}}/{urllib.parse.quote(clean_name)}.png"
        }
        
    def create_artwork_manifest(self, rom_catalog):
        """Create artwork manifest from ROM catalog"""
        manifest = {
            'games': [],
            'stats': {'total': 0, 'with_art': 0, 'missing': 0}
        }
        
        for rom in rom_catalog.get('roms', []):
            game_entry = {
                'name': rom['name'],
                'platform': rom['platform'],
                'rom_path': rom['path'],
                'artwork': {
                    'boxart': None,
                    'title': None,
                    'snap': None,
                    'logo': None
                }
            }
            
            # Check for existing local artwork
            artwork_dir = self.output_dir / rom['platform'] / rom['name']
            for art_type in ['boxart', 'title', 'snap', 'logo']:
                for ext in ['.png', '.jpg', '.jpeg']:
                    art_path = artwork_dir / f"{art_type}{ext}"
                    if art_path.exists():
                        game_entry['artwork'][art_type] = str(art_path)
                        
            manifest['games'].append(game_entry)
            manifest['stats']['total'] += 1
            
            if any(game_entry['artwork'].values()):
                manifest['stats']['with_art'] += 1
            else:
                manifest['stats']['missing'] += 1
                
        return manifest
        
    def generate_html_gallery(self, manifest, output_file):
        """Generate HTML gallery of game artwork"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Retro Game Gallery</title>
    <style>
        body { 
            background: #1a1a2e; 
            color: #00ff00; 
            font-family: 'Courier New', monospace;
            padding: 20px;
        }
        h1 { 
            text-align: center; 
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }
        .gallery { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }
        .game-card {
            background: #16213e;
            border: 2px solid #00ff00;
            padding: 10px;
            text-align: center;
        }
        .game-card img {
            max-width: 100%;
            height: 150px;
            object-fit: contain;
        }
        .game-card .title {
            margin-top: 10px;
            font-size: 12px;
        }
        .game-card .platform {
            color: #888;
            font-size: 10px;
        }
        .placeholder {
            background: #0a0a0a;
            height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px dashed #00ff00;
        }
    </style>
</head>
<body>
    <h1>🎮 N01D TIME MACHINE - GAME GALLERY</h1>
    <p style="text-align:center">
        Total: """ + str(manifest['stats']['total']) + """ | 
        With Art: """ + str(manifest['stats']['with_art']) + """ | 
        Missing: """ + str(manifest['stats']['missing']) + """
    </p>
    <div class="gallery">
"""
        
        for game in manifest['games'][:100]:  # Limit to 100 for performance
            boxart = game['artwork'].get('boxart')
            if boxart:
                img_html = f'<img src="{boxart}" alt="{game["name"]}">'
            else:
                img_html = f'<div class="placeholder">No Art</div>'
                
            html += f"""
        <div class="game-card">
            {img_html}
            <div class="title">{game['name'][:30]}</div>
            <div class="platform">{game['platform']}</div>
        </div>
"""
        
        html += """
    </div>
</body>
</html>"""
        
        with open(output_file, 'w') as f:
            f.write(html)
        return output_file


def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="Retro Game Artwork Manager")
    parser.add_argument("-o", "--output", default="./artwork",
                       help="Output directory for artwork")
    parser.add_argument("--catalog", help="ROM catalog JSON file")
    parser.add_argument("--generate", nargs=2, metavar=('GAME', 'PLATFORM'),
                       help="Generate placeholder art for game")
    parser.add_argument("--manifest", action="store_true",
                       help="Create artwork manifest from catalog")
    parser.add_argument("--gallery", metavar="OUTPUT",
                       help="Generate HTML gallery")
    parser.add_argument("--search", nargs=2, metavar=('GAME', 'PLATFORM'),
                       help="Search for game artwork URLs")
    
    args = parser.parse_args()
    
    scraper = ArtworkScraper(args.output)
    
    if args.generate:
        game, platform = args.generate
        print(f"[*] Generating placeholder for: {game} ({platform})")
        
        boxart = scraper.generate_local_artwork(game, platform, 'boxart')
        print("\n[BOXART]")
        print(boxart)
        
        snap = scraper.generate_local_artwork(game, platform, 'screenshot')
        print("\n[SCREENSHOT]")
        print(snap)
        
    if args.search:
        game, platform = args.search
        print(f"[*] Searching artwork for: {game} ({platform})")
        
        result = scraper.search_libretro_thumbnails(game, platform)
        print(f"\n[LibRetro Thumbnails]")
        for art_type, path in result['paths'].items():
            url = result['url_template'].replace('{type}', path.split('/')[0])
            print(f"  {art_type}: {url}")
            
    if args.catalog and args.manifest:
        print(f"[*] Loading catalog: {args.catalog}")
        with open(args.catalog) as f:
            catalog = json.load(f)
            
        manifest = scraper.create_artwork_manifest(catalog)
        
        manifest_file = Path(args.output) / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"[*] Manifest saved: {manifest_file}")
        
        print(f"\n[STATS]")
        print(f"  Total Games: {manifest['stats']['total']}")
        print(f"  With Artwork: {manifest['stats']['with_art']}")
        print(f"  Missing: {manifest['stats']['missing']}")
        
        if args.gallery:
            gallery_file = scraper.generate_html_gallery(manifest, args.gallery)
            print(f"[*] Gallery saved: {gallery_file}")
            
    if not any([args.generate, args.search, args.manifest]):
        print("[*] Use --generate, --search, or --manifest")
        print("[*] Example: retro-artwork.py --generate 'Super Mario Bros' nes")


if __name__ == "__main__":
    main()
