#!/usr/bin/env python3
"""
ISO Repacking Script for Animal Crossing e+ Translation
Repacks the translated game files into a new ISO
"""

import os
import sys
import subprocess
from pathlib import Path

class ISORepacker:
    def __init__(self):
        self.extracted_dir = Path("extracted_game")
        self.implemented_dir = Path("implemented_translations")
        self.output_dir = Path("translated_game")
        self.final_iso = Path("Animal_Crossing_E+_English.iso")
        
        # Check if wit is available
        self.wit_path = self.find_wit()
    
    def find_wit(self):
        """Find the wit executable"""
        # Check common locations
        possible_paths = [
            Path("..") / "wit-v3.05a-r8638-cygwin64" / "bin" / "wit.exe",
            Path("wit-v3.05a-r8638-cygwin64") / "bin" / "wit.exe",
            Path("wit.exe")
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        return None
    
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("=== CHECKING PREREQUISITES ===")
        
        # Check if implemented translations exist
        if not self.implemented_dir.exists():
            print("❌ Error: Implemented translations directory not found!")
            print("   Run translation_implementer.py first")
            return False
        
        # Check if extracted game exists
        if not self.extracted_dir.exists():
            print("❌ Error: Extracted game directory not found!")
            print("   Extract the ISO first using wit")
            return False
        
        # Check if wit is available
        if not self.wit_path:
            print("❌ Error: wit executable not found!")
            print("   Make sure wit is installed and accessible")
            return False
        
        print("✅ All prerequisites met!")
        return True
    
    def copy_translated_files(self):
        """Copy translated files to the extracted game directory"""
        print("\n=== COPYING TRANSLATED FILES ===")
        
        # Create output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        shutil.copytree(self.extracted_dir, self.output_dir)
        
        # Copy translated files
        game_files_dir = self.output_dir / "P-GAEJ" / "files"
        
        for translated_file in self.implemented_dir.glob("*"):
            if translated_file.is_file() and not translated_file.name.endswith('.md'):
                target_file = game_files_dir / translated_file.name
                shutil.copy2(translated_file, target_file)
                print(f"✅ Copied: {translated_file.name}")
        
        print("✅ Translated files copied successfully!")
    
    def repack_iso(self):
        """Repack the translated game into a new ISO"""
        print("\n=== REPACKING ISO ===")
        
        try:
            # Use wit to create the final ISO
            cmd = [self.wit_path, "copy", str(self.output_dir), str(self.final_iso)]
            
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ ISO repacked successfully!")
                print(f"📁 Final ISO: {self.final_iso}")
                
                # Show file size
                if self.final_iso.exists():
                    size_gb = self.final_iso.stat().st_size / (1024**3)
                    print(f"📊 File size: {size_gb:.2f} GB")
                
                return True
            else:
                print("❌ Error repacking ISO:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error during repacking: {e}")
            return False
    
    def cleanup(self):
        """Clean up temporary files"""
        print("\n=== CLEANING UP ===")
        
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
            print("✅ Temporary files cleaned up")
    
    def create_installation_guide(self):
        """Create an installation guide for users"""
        guide_path = Path("INSTALLATION_GUIDE.md")
        
        guide_content = """# Animal Crossing E+ English Translation - Installation Guide

## What This Is
This is a complete English translation of Doubutsu no Mori e+ (Animal Crossing e+), a GameCube game that was previously only available in Japanese.

## Installation Instructions

### Option 1: Dolphin Emulator (Recommended)
1. Download and install Dolphin Emulator
2. Place the translated ISO in your games directory
3. Launch the game through Dolphin
4. Enjoy Animal Crossing E+ in English!

### Option 2: Real GameCube Hardware
1. Use a modded GameCube or Wii
2. Burn the ISO to a DVD-R (may require specific media)
3. Insert and play on your console

### Option 3: Wii (Homebrew)
1. Install Homebrew Channel on your Wii
2. Use USB Loader GX or similar to load the ISO
3. Play on your Wii

## Translation Features
- **Complete UI Translation**: All menus, buttons, and interface elements
- **Full Dialogue Translation**: Character conversations and interactions
- **Items & Locations**: All game objects, buildings, and areas
- **Official Terminology**: Uses proper Animal Crossing English terms

## Credits
- **Original Game**: Nintendo - Doubutsu no Mori e+
- **Translation**: Community effort using verified Animal Crossing terminology
- **Tools**: Wii ISO Tool (wit), custom translation toolkit

## Support
If you encounter any issues or have questions about the translation, please refer to the project documentation.

---
*Enjoy Animal Crossing E+ in English!* 🎮✨
"""
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"✅ Installation guide created: {guide_path}")
    
    def run(self):
        """Main execution method"""
        print("=== ANIMAL CROSSING E+ ISO REPACKING ===")
        print("This script will repack your translated game into a new ISO")
        
        if not self.check_prerequisites():
            return False
        
        try:
            self.copy_translated_files()
            
            if self.repack_iso():
                self.create_installation_guide()
                print(f"\n🎉 SUCCESS! Your translated Animal Crossing E+ ISO is ready!")
                print(f"📁 File: {self.final_iso}")
                print(f"📖 Installation guide: INSTALLATION_GUIDE.md")
                return True
            else:
                print(f"\n❌ Failed to repack ISO")
                return False
                
        finally:
            self.cleanup()

def main():
    """Main function"""
    try:
        import shutil
    except ImportError:
        print("❌ Error: shutil module not available")
        sys.exit(1)
    
    repacker = ISORepacker()
    success = repacker.run()
    
    if success:
        print(f"\n🏆 Congratulations! You now have a fully translated Animal Crossing E+!")
        print(f"Share it with the community and enjoy playing in English!")
    else:
        print(f"\n⚠️  ISO repacking was not completed successfully")
        print(f"Check the error messages above and try again")

if __name__ == "__main__":
    main()

