#!/usr/bin/env python3
"""
Find Animal Crossing Specific Dialogue Patterns
"""

from pathlib import Path

def find_ac_dialogue():
    """Find Animal Crossing specific dialogue patterns"""
    
    # Animal Crossing specific dialogue patterns
    ac_dialogue = [
        # Character names and titles
        'たぬき', 'たぬきち', 'きつね', 'きつねち', 'うさぎ', 'ねこ', 'いぬ',
        'ぶた', 'ひつじ', 'うし', 'とり', 'かえる', 'かめ', 'ぞう', 'きりん',
        
        # Animal Crossing specific phrases
        'どうぶつの森', 'どうぶつ', '森', '村', '町', '島', '海', '川',
        '釣り', '虫取り', '化石掘り', '花植え', '木植え', '家具', '服',
        
        # Game mechanics dialogue
        'お金', 'ベル', 'ポイント', 'スコア', 'ランク', 'レベル', '経験値',
        'インベントリ', 'アイテム', 'マップ', 'ステータス', '装備', 'クエスト',
        
        # Building and location names
        '博物館', '郵便局', '役場', '店', '家', '橋', '道', '広場',
        '公園', '学校', '病院', '駅', '空港', '港', '山', '森',
        
        # Time and weather
        '朝', '昼', '夜', '午前', '午後', '今日', '明日', '昨日',
        '晴れ', '雨', '雪', '曇り', '風', '雷', '虹', '夕日'
    ]
    
    japanese_file = Path("extracted_text/japanese_text.txt")
    
    found_ac_dialogue = []
    
    print("Searching for Animal Crossing specific dialogue patterns...")
    
    with open(japanese_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            if line_num % 50000 == 0:
                print(f"Processed {line_num} lines...")
            
            text = line.strip()
            if not text or len(text) < 2:
                continue
            
            # Check if text contains any AC dialogue patterns
            for word in ac_dialogue:
                if word in text:
                    found_ac_dialogue.append({
                        'text': text,
                        'word': word,
                        'line': line_num
                    })
                    break
    
    # Remove duplicates and sort
    unique_ac_dialogue = []
    seen = set()
    
    for item in found_ac_dialogue:
        if item['text'] not in seen:
            seen.add(item['text'])
            unique_ac_dialogue.append(item)
    
    # Sort by word
    unique_ac_dialogue.sort(key=lambda x: x['word'])
    
    # Save results
    output_file = Path("organized_translations/ac_dialogue_patterns.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Animal Crossing Specific Dialogue Patterns Found\n")
        f.write(f"# Total unique AC dialogue entries found: {len(unique_ac_dialogue)}\n\n")
        
        current_word = ""
        for item in unique_ac_dialogue:
            if item['word'] != current_word:
                current_word = item['word']
                f.write(f"\n# Word: {current_word}\n")
            
            f.write(f"{item['text']} | | AC Dialogue - {current_word}\n")
    
    print(f"✓ Found {len(unique_ac_dialogue)} unique Animal Crossing dialogue entries")
    print(f"✓ Saved to: {output_file}")
    
    # Show some examples
    print("\n=== Sample Animal Crossing Dialogue Patterns Found ===")
    for i, item in enumerate(unique_ac_dialogue[:20]):
        print(f"{i+1:2d}. {item['text']} (Contains: {item['word']})")
    
    if len(unique_ac_dialogue) > 20:
        print(f"... and {len(unique_ac_dialogue) - 20} more entries")
    
    return unique_ac_dialogue

if __name__ == "__main__":
    find_ac_dialogue()
