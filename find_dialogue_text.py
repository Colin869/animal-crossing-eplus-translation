#!/usr/bin/env python3
"""
Find Dialogue Text in Animal Crossing e+
"""

from pathlib import Path

def find_dialogue():
    """Find dialogue and character interaction text"""
    
    # Dialogue and character interaction words
    dialogue_words = [
        # Greetings and basic dialogue
        'こんにちは', 'さようなら', 'ありがとう', 'おはよう', 'おやすみ',
        'すみません', 'どういたしまして', 'お疲れ様', 'お元気ですか',
        'はじめまして', 'よろしく', 'さようなら', 'またね', 'バイバイ',
        
        # Character interactions
        '話す', '聞く', '教える', '質問', '答え', '説明', '紹介',
        '挨拶', '会話', '相談', '約束', '約束する', '待つ', '待って',
        
        # Emotions and reactions
        '嬉しい', '悲しい', '怒る', '驚く', '困る', '心配', '安心',
        '楽しい', '面白い', '大変', '大丈夫', '頑張る', '応援',
        
        # Common phrases
        'そうですね', 'そうですか', '本当ですか', '本当に', '確かに',
        'もちろん', 'もちろんです', 'いえいえ', 'いえ', 'はい',
        '分かりました', '分かります', '分からない', '知らない',
        
        # Game-specific dialogue
        '村長', '住民', '友達', '隣人', '店員', '郵便配達',
        '博物館', '役場', '郵便局', '店', '家', '村', '町'
    ]
    
    japanese_file = Path("extracted_text/japanese_text.txt")
    
    found_dialogue = []
    
    print("Searching for dialogue and character interaction text...")
    
    with open(japanese_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            if line_num % 50000 == 0:
                print(f"Processed {line_num} lines...")
            
            text = line.strip()
            if not text or len(text) < 2:
                continue
            
            # Check if text contains any dialogue words
            for word in dialogue_words:
                if word in text:
                    found_dialogue.append({
                        'text': text,
                        'word': word,
                        'line': line_num
                    })
                    break
    
    # Remove duplicates and sort
    unique_dialogue = []
    seen = set()
    
    for item in found_dialogue:
        if item['text'] not in seen:
            seen.add(item['text'])
            unique_dialogue.append(item)
    
    # Sort by word
    unique_dialogue.sort(key=lambda x: x['word'])
    
    # Save results
    output_file = Path("organized_translations/dialogue_found.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Dialogue and Character Interaction Text Found\n")
        f.write(f"# Total unique dialogue entries found: {len(unique_dialogue)}\n\n")
        
        current_word = ""
        for item in unique_dialogue:
            if item['word'] != current_word:
                current_word = item['word']
                f.write(f"\n# Word: {current_word}\n")
            
            f.write(f"{item['text']} | | Dialogue - {current_word}\n")
    
    print(f"✓ Found {len(unique_dialogue)} unique dialogue text entries")
    print(f"✓ Saved to: {output_file}")
    
    # Show some examples
    print("\n=== Sample Dialogue Text Found ===")
    for i, item in enumerate(unique_dialogue[:20]):
        print(f"{i+1:2d}. {item['text']} (Contains: {item['word']})")
    
    if len(unique_dialogue) > 20:
        print(f"... and {len(unique_dialogue) - 20} more entries")
    
    return unique_dialogue

if __name__ == "__main__":
    find_dialogue()
