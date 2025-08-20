#!/usr/bin/env python3
"""
Text Extractor for Animal Crossing e+ (Doubutsu no Mori e+)
Extracts Japanese text from game files for translation
"""

import os
import sys
import struct
import re
from pathlib import Path
import json

class AnimalCrossingTextExtractor:
    def __init__(self, extracted_dir):
        self.extracted_dir = Path(extracted_dir)
        self.text_output_dir = Path("extracted_text")
        self.text_output_dir.mkdir(exist_ok=True)
        
        # Common Japanese text encodings
        self.encodings = ['shift_jis', 'utf-8', 'euc-jp']
        
        # Text patterns to look for
        self.text_patterns = [
            rb'[\x80-\xff]{2,}',  # Japanese characters
            rb'[A-Za-z\s]{3,}',   # English text
            rb'[0-9]{1,}',        # Numbers
        ]
    
    def extract_arc_file(self, arc_path):
        """Extract text from .arc files"""
        print(f"Analyzing ARC file: {arc_path.name}")
        
        try:
            with open(arc_path, 'rb') as f:
                data = f.read()
                
                # Look for text patterns
                extracted_text = []
                
                for pattern in self.text_patterns:
                    matches = re.findall(pattern, data)
                    for match in matches:
                        # Try different encodings
                        for encoding in self.encodings:
                            try:
                                decoded = match.decode(encoding, errors='ignore')
                                if len(decoded.strip()) > 2:  # Filter out very short strings
                                    extracted_text.append({
                                        'text': decoded.strip(),
                                        'encoding': encoding,
                                        'offset': data.find(match)
                                    })
                                break
                            except:
                                continue
                
                return extracted_text
                
        except Exception as e:
            print(f"Error reading {arc_path.name}: {e}")
            return []
    
    def extract_szs_file(self, szs_path):
        """Extract text from .szs files (compressed archives)"""
        print(f"Analyzing SZS file: {szs_path.name}")
        
        try:
            with open(szs_path, 'rb') as f:
                data = f.read()
                
                # SZS files are compressed, but we can still look for text patterns
                extracted_text = []
                
                for pattern in self.text_patterns:
                    matches = re.findall(pattern, data)
                    for match in matches:
                        for encoding in self.encodings:
                            try:
                                decoded = match.decode(encoding, errors='ignore')
                                if len(decoded.strip()) > 2:
                                    extracted_text.append({
                                        'text': decoded.strip(),
                                        'encoding': encoding,
                                        'offset': data.find(match)
                                    })
                                break
                            except:
                                continue
                
                return extracted_text
                
        except Exception as e:
            print(f"Error reading {szs_path.name}: {e}")
            return []
    
    def analyze_forest_msg(self):
        """Special analysis for the main message file"""
        msg_path = self.extracted_dir / "P-GAEJ" / "files" / "forest_msg.arc"
        
        if not msg_path.exists():
            print("forest_msg.arc not found!")
            return []
        
        print(f"\n=== Analyzing Main Message File: {msg_path.name} ===")
        
        try:
            with open(msg_path, 'rb') as f:
                data = f.read()
                
                # Look for message structures
                messages = []
                
                # Common message delimiters in games
                delimiters = [b'\x00', b'\x0A', b'\x0D', b'\x1F', b'\x1E']
                
                for delimiter in delimiters:
                    parts = data.split(delimiter)
                    for part in parts:
                        if len(part) > 10:  # Reasonable length for a message
                            for encoding in self.encodings:
                                try:
                                    decoded = part.decode(encoding, errors='ignore')
                                    if any(ord(c) > 127 for c in decoded):  # Contains non-ASCII
                                        if len(decoded.strip()) > 5:
                                            messages.append({
                                                'text': decoded.strip(),
                                                'encoding': encoding,
                                                'type': 'message'
                                            })
                                    break
                                except:
                                    continue
                
                return messages
                
        except Exception as e:
            print(f"Error analyzing forest_msg.arc: {e}")
            return []
    
    def extract_all_text(self):
        """Extract text from all relevant game files"""
        print("=== Animal Crossing e+ Text Extraction ===")
        
        all_text = []
        files_dir = self.extracted_dir / "P-GAEJ" / "files"
        
        # Priority files to analyze
        priority_files = [
            "forest_msg.arc",
            "forest_1st_script.arc",
            "forest_1st.arc",
            "forest_2nd.arc"
        ]
        
        # Analyze priority files first
        for filename in priority_files:
            file_path = files_dir / filename
            if file_path.exists():
                if filename.endswith('.arc'):
                    text = self.extract_arc_file(file_path)
                elif filename.endswith('.szs'):
                    text = self.extract_szs_file(file_path)
                else:
                    text = []
                
                all_text.extend(text)
                print(f"Extracted {len(text)} text entries from {filename}")
        
        # Analyze other .arc files
        for file_path in files_dir.glob("*.arc"):
            if file_path.name not in priority_files:
                text = self.extract_arc_file(file_path)
                all_text.extend(text)
                print(f"Extracted {len(text)} text entries from {file_path.name}")
        
        # Analyze .szs files
        for file_path in files_dir.glob("*.szs"):
            if file_path.name not in priority_files:
                text = self.extract_szs_file(file_path)
                all_text.extend(text)
                print(f"Extracted {len(text)} text entries from {file_path.name}")
        
        # Special analysis for main message file
        msg_text = self.analyze_forest_msg()
        all_text.extend(msg_text)
        
        return all_text
    
    def save_extracted_text(self, text_data):
        """Save extracted text to files"""
        print(f"\n=== Saving Extracted Text ===")
        
        # Save all text
        with open(self.text_output_dir / "all_extracted_text.json", 'w', encoding='utf-8') as f:
            json.dump(text_data, f, indent=2, ensure_ascii=False)
        
        # Save Japanese text only
        japanese_text = [item for item in text_data if any(ord(c) > 127 for c in item.get('text', ''))]
        
        with open(self.text_output_dir / "japanese_text.txt", 'w', encoding='utf-8') as f:
            for item in japanese_text:
                f.write(f"{item['text']}\n")
        
        # Save English text only
        english_text = [item for item in text_data if all(ord(c) <= 127 for c in item.get('text', '')) and len(item.get('text', '')) > 3]
        
        with open(self.text_output_dir / "english_text.txt", 'w', encoding='utf-8') as f:
            for item in english_text:
                f.write(f"{item['text']}\n")
        
        # Create translation template
        translation_template = "# Animal Crossing e+ Translation Template\n"
        translation_template += "# Format: Japanese | English | Context\n\n"
        
        # Add some common phrases
        common_phrases = [
            "こんにちは | Hello | Greeting",
            "さようなら | Goodbye | Farewell", 
            "ありがとう | Thank you | Gratitude",
            "おはよう | Good morning | Morning greeting",
            "おやすみ | Good night | Night greeting"
        ]
        
        for phrase in common_phrases:
            translation_template += f"{phrase}\n"
        
        translation_template += "\n# Extracted text from game files:\n"
        
        # Add unique Japanese text
        unique_japanese = set()
        for item in japanese_text:
            text = item['text']
            if len(text) > 3 and text not in unique_japanese:
                unique_japanese.add(text)
                translation_template += f"{text} | | \n"
        
        with open(self.text_output_dir / "translation_template.txt", 'w', encoding='utf-8') as f:
            f.write(translation_template)
        
        print(f"✓ Saved {len(text_data)} total text entries")
        print(f"✓ Saved {len(japanese_text)} Japanese text entries")
        print(f"✓ Saved {len(english_text)} English text entries")
        print(f"✓ Created translation template with {len(unique_japanese)} unique Japanese phrases")
        
        return len(japanese_text)
    
    def run(self):
        """Main execution method"""
        print("Starting text extraction from Animal Crossing e+...")
        
        if not self.extracted_dir.exists():
            print(f"Error: Extracted game directory not found: {self.extracted_dir}")
            return
        
        # Extract text from all files
        text_data = self.extract_all_text()
        
        if not text_data:
            print("No text data extracted!")
            return
        
        # Save extracted text
        japanese_count = self.save_extracted_text(text_data)
        
        print(f"\n=== Extraction Complete ===")
        print(f"Total text entries: {len(text_data)}")
        print(f"Japanese text entries: {japanese_count}")
        print(f"Output saved to: {self.text_output_dir}")
        print(f"\nNext steps:")
        print(f"1. Review extracted text in {self.text_output_dir}")
        print(f"2. Use translation_template.txt to start translating")
        print(f"3. Focus on forest_msg.arc and script files first")

if __name__ == "__main__":
    extractor = AnimalCrossingTextExtractor("extracted_game")
    extractor.run()
