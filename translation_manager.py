#!/usr/bin/env python3
"""
Translation Manager for Animal Crossing e+
Helps organize and prioritize the massive amount of Japanese text for translation
"""

import os
import json
from pathlib import Path
import re

class TranslationManager:
    def __init__(self):
        self.extracted_dir = Path("extracted_text")
        self.translation_dir = Path("translation_files")
        self.priority_dir = Path("priority_translations")
        
        # Create directories
        for directory in [self.priority_dir]:
            directory.mkdir(exist_ok=True)
    
    def categorize_text(self):
        """Categorize text by importance and frequency"""
        print("=== Categorizing Text by Importance ===")
        
        # Load all extracted text
        json_file = self.extracted_dir / "all_extracted_text.json"
        if not json_file.exists():
            print("Error: all_extracted_text.json not found!")
            return
        
        print("Loading extracted text...")
        with open(json_file, 'r', encoding='utf-8') as f:
            all_text = json.load(f)
        
        # Categorize text
        categories = {
            'ui_text': [],      # User interface text
            'dialogue': [],     # Character dialogue
            'items': [],        # Item names
            'locations': [],    # Location names
            'common_phrases': [], # Frequently used phrases
            'other': []         # Everything else
        }
        
        # Common UI patterns
        ui_patterns = [
            r'メニュー', r'設定', r'開始', r'終了', r'はい', r'いいえ',
            r'保存', r'読み込み', r'戻る', r'進む', r'選択', r'決定'
        ]
        
        # Common dialogue patterns
        dialogue_patterns = [
            r'こんにちは', r'さようなら', r'ありがとう', r'おはよう',
            r'おやすみ', r'すみません', r'どういたしまして'
        ]
        
        # Common item patterns
        item_patterns = [
            r'リンゴ', r'オレンジ', r'魚', r'虫', r'花', r'木',
            r'家具', r'服', r'道具', r'種'
        ]
        
        # Common location patterns
        location_patterns = [
            r'森', r'海', r'川', r'山', r'村', r'町', r'店',
            r'家', r'橋', r'道'
        ]
        
        print("Categorizing text...")
        for item in all_text:
            text = item.get('text', '')
            if not text or len(text) < 3:
                continue
            
            categorized = False
            
            # Check UI patterns
            for pattern in ui_patterns:
                if re.search(pattern, text):
                    categories['ui_text'].append(item)
                    categorized = True
                    break
            
            if categorized:
                continue
            
            # Check dialogue patterns
            for pattern in dialogue_patterns:
                if re.search(pattern, text):
                    categories['dialogue'].append(item)
                    categorized = True
                    break
            
            if categorized:
                continue
            
            # Check item patterns
            for pattern in item_patterns:
                if re.search(pattern, text):
                    categories['items'].append(item)
                    categorized = True
                    break
            
            if categorized:
                continue
            
            # Check location patterns
            for pattern in location_patterns:
                if re.search(pattern, text):
                    categories['locations'].append(item)
                    categorized = True
                    break
            
            if categorized:
                continue
            
            # Check for common phrases (frequently repeated)
            if text in [item['text'] for item in all_text if item != item]:
                categories['common_phrases'].append(item)
            else:
                categories['other'].append(item)
        
        # Save categorized text
        for category, items in categories.items():
            if items:
                output_file = self.priority_dir / f"{category}_text.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {category.replace('_', ' ').title()} Text\n")
                    f.write(f"# Total entries: {len(items)}\n\n")
                    
                    # Get unique text
                    unique_text = set()
                    for item in items:
                        text = item['text']
                        if text not in unique_text and len(text) > 2:
                            unique_text.add(text)
                            f.write(f"{text}\n")
                
                print(f"✓ {category}: {len(items)} entries, {len(unique_text)} unique")
        
        return categories
    
    def create_priority_translation_template(self):
        """Create a prioritized translation template"""
        print("\n=== Creating Priority Translation Template ===")
        
        # Load categorized text
        categories = self.categorize_text()
        
        # Create priority template
        template_content = "# Animal Crossing e+ Priority Translation Template\n"
        template_content += "# Focus on these categories in order:\n\n"
        
        priority_order = ['ui_text', 'dialogue', 'items', 'locations', 'common_phrases']
        
        for category in priority_order:
            if category in categories and categories[category]:
                template_content += f"## {category.replace('_', ' ').title()}\n"
                template_content += f"# Priority: High - These appear frequently in the game\n\n"
                
                # Get sample text
                sample_items = categories[category][:20]  # First 20 items
                unique_text = set()
                
                for item in sample_items:
                    text = item['text']
                    if text not in unique_text and len(text) > 2:
                        unique_text.add(text)
                        template_content += f"{text} | | {category}\n"
                
                template_content += f"\n# ... and {len(categories[category]) - len(unique_text)} more entries\n\n"
        
        # Save priority template
        priority_file = self.priority_dir / "priority_translation_template.txt"
        with open(priority_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"✓ Priority translation template created: {priority_file}")
        
        return priority_file
    
    def create_translation_workflow(self):
        """Create a translation workflow guide"""
        workflow_content = """# Animal Crossing e+ Translation Workflow

## Overview
You have successfully extracted 209,856 Japanese text entries from the game.
This is a massive undertaking that requires careful organization.

## Translation Priority Order

### 1. UI Text (High Priority)
- Menu items, buttons, settings
- These appear constantly and are essential for gameplay
- Start with: メニュー, 設定, 開始, 終了, はい, いいえ

### 2. Dialogue (High Priority)
- Character conversations and greetings
- Core to the Animal Crossing experience
- Start with: こんにちは, さようなら, ありがとう

### 3. Items (Medium Priority)
- Item names, tools, furniture
- Important for inventory management
- Start with: common items like fruits, fish, tools

### 4. Locations (Medium Priority)
- Place names, areas, buildings
- Important for navigation
- Start with: 森 (forest), 海 (sea), 村 (village)

### 5. Common Phrases (Medium Priority)
- Frequently repeated text
- Good for building translation consistency

## Recommended Tools

### Translation Tools
- **Google Translate**: Good for initial rough translations
- **DeepL**: Better for Japanese to English
- **Jisho.org**: Excellent Japanese dictionary
- **Translation memory tools**: To maintain consistency

### File Management
- Use the priority_translation_template.txt for high-priority items
- Keep backups of all original files
- Use version control for translation progress

## Translation Process

1. **Start with UI text** - Translate menu items first
2. **Move to dialogue** - Focus on common greetings
3. **Work on items** - Translate essential game objects
4. **Handle locations** - Translate place names
5. **Review and refine** - Ensure consistency

## Quality Guidelines

- Maintain original text length when possible
- Keep Animal Crossing's friendly, casual tone
- Use consistent terminology (e.g., always translate 森 as "forest")
- Test translations in context when possible

## File Structure
```
extracted_text/
├── all_extracted_text.json (88MB) - All extracted text
├── japanese_text.txt (17MB) - Japanese text only
├── english_text.txt (422KB) - English text found
└── translation_template.txt (17MB) - Full template

priority_translations/
├── ui_text_text.txt - UI elements
├── dialogue_text.txt - Character dialogue
├── items_text.txt - Item names
├── locations_text.txt - Location names
└── priority_translation_template.txt - This guide
```

## Next Steps
1. Start with the priority_translation_template.txt
2. Focus on UI text first
3. Build a glossary of common terms
4. Work systematically through each category
5. Test translations in the game when possible

## Estimated Time
- UI text: 1-2 weeks
- Dialogue: 2-4 weeks  
- Items: 2-3 weeks
- Locations: 1-2 weeks
- Total: 6-11 weeks for basic translation
- Polish and testing: Additional 2-4 weeks

Remember: This is a marathon, not a sprint. Take your time and maintain quality!
"""
        
        workflow_file = self.priority_dir / "translation_workflow.md"
        with open(workflow_file, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        
        print(f"✓ Translation workflow guide created: {workflow_file}")
        return workflow_file
    
    def run(self):
        """Main execution method"""
        print("=== Animal Crossing e+ Translation Manager ===")
        print("Organizing the massive amount of extracted text...")
        
        # Create priority translation template
        priority_file = self.create_priority_translation_template()
        
        # Create workflow guide
        workflow_file = self.create_translation_workflow()
        
        print(f"\n=== Translation Manager Complete ===")
        print(f"✓ Priority template: {priority_file}")
        print(f"✓ Workflow guide: {workflow_file}")
        print(f"✓ All files organized in: {self.priority_dir}")
        print(f"\nYou now have:")
        print(f"- 209,856 Japanese text entries to translate")
        print(f"- Prioritized translation template")
        print(f"- Complete workflow guide")
        print(f"- Organized text by category")
        print(f"\nStart with the priority template and work systematically!")

if __name__ == "__main__":
    manager = TranslationManager()
    manager.run()


