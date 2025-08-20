#!/usr/bin/env python3
"""
Simple Translation Organizer for Animal Crossing e+
Efficiently organizes the massive amount of extracted text
"""

import os
from pathlib import Path

class SimpleTranslationOrganizer:
    def __init__(self):
        self.extracted_dir = Path("extracted_text")
        self.organized_dir = Path("organized_translations")
        self.organized_dir.mkdir(exist_ok=True)
    
    def create_simple_categories(self):
        """Create simple text categories"""
        print("=== Creating Simple Text Categories ===")
        
        # Load Japanese text file
        japanese_file = self.extracted_dir / "japanese_text.txt"
        if not japanese_file.exists():
            print("Error: japanese_text.txt not found!")
            return
        
        print("Reading Japanese text file...")
        
        # Simple categorization
        ui_text = []
        dialogue = []
        items = []
        locations = []
        other = []
        
        # Common patterns to look for
        ui_keywords = ['メニュー', '設定', '開始', '終了', 'はい', 'いいえ', '保存', '読み込み', '戻る', '進む', '選択', '決定']
        dialogue_keywords = ['こんにちは', 'さようなら', 'ありがとう', 'おはよう', 'おやすみ', 'すみません', 'どういたしまして']
        item_keywords = ['リンゴ', 'オレンジ', '魚', '虫', '花', '木', '家具', '服', '道具', '種']
        location_keywords = ['森', '海', '川', '山', '村', '町', '店', '家', '橋', '道']
        
        print("Categorizing text...")
        with open(japanese_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f):
                if line_num % 10000 == 0:
                    print(f"Processed {line_num} lines...")
                
                text = line.strip()
                if not text or len(text) < 3:
                    continue
                
                # Simple categorization
                categorized = False
                
                # Check UI keywords
                for keyword in ui_keywords:
                    if keyword in text:
                        ui_text.append(text)
                        categorized = True
                        break
                
                if categorized:
                    continue
                
                # Check dialogue keywords
                for keyword in dialogue_keywords:
                    if keyword in text:
                        dialogue.append(text)
                        categorized = True
                        break
                
                if categorized:
                    continue
                
                # Check item keywords
                for keyword in item_keywords:
                    if keyword in text:
                        items.append(text)
                        categorized = True
                        break
                
                if categorized:
                    continue
                
                # Check location keywords
                for keyword in location_keywords:
                    if keyword in text:
                        locations.append(text)
                        categorized = True
                        break
                
                if not categorized:
                    other.append(text)
        
        # Save categorized text
        categories = {
            'ui_text': ui_text,
            'dialogue': dialogue,
            'items': items,
            'locations': locations,
            'other': other
        }
        
        for category, texts in categories.items():
            if texts:
                output_file = self.organized_dir / f"{category}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {category.replace('_', ' ').title()} Text\n")
                    f.write(f"# Total entries: {len(texts)}\n\n")
                    
                    # Get unique text
                    unique_texts = list(set(texts))
                    for text in unique_texts[:100]:  # Limit to first 100 for readability
                        f.write(f"{text}\n")
                    
                    if len(unique_texts) > 100:
                        f.write(f"\n# ... and {len(unique_texts) - 100} more entries\n")
                
                print(f"✓ {category}: {len(texts)} entries, {len(unique_texts)} unique")
        
        return categories
    
    def create_priority_template(self):
        """Create a priority translation template"""
        print("\n=== Creating Priority Translation Template ===")
        
        template_content = """# Animal Crossing e+ Priority Translation Template
# Focus on these categories in order of importance

## 1. UI Text (HIGH PRIORITY)
# These appear constantly and are essential for gameplay
# Start with these common UI elements:

メニュー | Menu |
設定 | Settings |
開始 | Start |
終了 | End/Exit |
はい | Yes |
いいえ | No |
保存 | Save |
読み込み | Load |
戻る | Back |
進む | Next |
選択 | Select |
決定 | Confirm/OK |

## 2. Dialogue (HIGH PRIORITY)
# Character conversations and greetings
# Core to the Animal Crossing experience

こんにちは | Hello |
さようなら | Goodbye |
ありがとう | Thank you |
おはよう | Good morning |
おやすみ | Good night |
すみません | Excuse me/Sorry |
どういたしまして | You're welcome |

## 3. Items (MEDIUM PRIORITY)
# Item names, tools, furniture
# Important for inventory management

リンゴ | Apple |
オレンジ | Orange |
魚 | Fish |
虫 | Bug/Insect |
花 | Flower |
木 | Tree |
家具 | Furniture |
服 | Clothing |
道具 | Tool |
種 | Seed |

## 4. Locations (MEDIUM PRIORITY)
# Place names, areas, buildings
# Important for navigation

森 | Forest |
海 | Sea |
川 | River |
山 | Mountain |
村 | Village |
町 | Town |
店 | Shop/Store |
家 | House/Home |
橋 | Bridge |
道 | Road/Path |

## Translation Guidelines:
# - Keep Animal Crossing's friendly, casual tone
# - Maintain similar text length when possible
# - Use consistent terminology
# - Test in context when possible

# Add your translations in the format: Japanese | English | Notes
"""
        
        template_file = self.organized_dir / "priority_translation_template.txt"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"✓ Priority template created: {template_file}")
        return template_file
    
    def create_workflow_guide(self):
        """Create a simple workflow guide"""
        workflow_content = """# Animal Crossing e+ Translation Workflow

## What You Have
- **209,856 Japanese text entries** extracted from the game
- **Organized by category** for easier translation
- **Priority template** to get started

## Translation Order (Recommended)

### Phase 1: Essential UI (Week 1-2)
- Menu items, buttons, settings
- These appear constantly during gameplay
- **Goal**: Make the game playable in English

### Phase 2: Basic Dialogue (Week 3-4)
- Common greetings and responses
- Character conversations
- **Goal**: Understand basic interactions

### Phase 3: Game Items (Week 5-6)
- Item names, tools, furniture
- **Goal**: Navigate inventory and crafting

### Phase 4: Locations & Navigation (Week 7-8)
- Place names, areas, buildings
- **Goal**: Navigate the game world

### Phase 5: Polish & Testing (Week 9-10)
- Review consistency
- Test translations in game
- **Goal**: Professional quality

## Tools You'll Need

### Translation Tools
- **Google Translate**: Quick rough translations
- **DeepL**: Better Japanese→English quality
- **Jisho.org**: Japanese dictionary
- **Translation memory**: Maintain consistency

### File Management
- Use the organized category files
- Keep backups of all original files
- Track progress systematically

## Getting Started
1. Open `priority_translation_template.txt`
2. Start with UI text (メニュー, 設定, etc.)
3. Work through each category systematically
4. Build a glossary of common terms
5. Test translations when possible

## Estimated Timeline
- **Basic translation**: 8-10 weeks
- **Polish & testing**: 2-4 weeks
- **Total**: 10-14 weeks

## Tips
- Focus on quality over speed
- Maintain consistent terminology
- Keep Animal Crossing's friendly tone
- Test frequently in the game
- This is a marathon, not a sprint!

Good luck with your translation project!
"""
        
        workflow_file = self.organized_dir / "translation_workflow.md"
        with open(workflow_file, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        
        print(f"✓ Workflow guide created: {workflow_file}")
        return workflow_file
    
    def run(self):
        """Main execution method"""
        print("=== Simple Translation Organizer ===")
        print("Organizing the massive amount of extracted text...")
        
        # Create simple categories
        categories = self.create_simple_categories()
        
        # Create priority template
        template_file = self.create_priority_template()
        
        # Create workflow guide
        workflow_file = self.create_workflow_guide()
        
        print(f"\n=== Organization Complete ===")
        print(f"✓ Categories created in: {self.organized_dir}")
        print(f"✓ Priority template: {template_file}")
        print(f"✓ Workflow guide: {workflow_file}")
        print(f"\nYou now have:")
        print(f"- Text organized by category")
        print(f"- Priority translation template")
        print(f"- Complete workflow guide")
        print(f"\nStart with the priority template and work systematically!")

if __name__ == "__main__":
    organizer = SimpleTranslationOrganizer()
    organizer.run()


