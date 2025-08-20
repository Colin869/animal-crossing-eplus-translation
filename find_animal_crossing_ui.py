#!/usr/bin/env python3
"""
Find Animal Crossing Specific UI Words
"""

from pathlib import Path

def find_ac_ui():
    """Find Animal Crossing specific UI words"""
    
    # Animal Crossing specific UI words
    ac_words = [
        # Core Animal Crossing
        '村', '町', '家', '店', '博物館', '郵便局', '役場',
        '住民', '村長', '店員', '郵便配達', '警察官',
        '家具', '服', '道具', '魚', '虫', '化石', '絵画',
        '音楽', '花', '木', '果物', '野菜', '種', '苗',
        
        # Game mechanics
        'お金', 'ポイント', 'スコア', 'ランク', '時間',
        '日付', '曜日', '月', '年', '分', '秒', '時',
        
        # Common UI
        'メニュー', '設定', '開始', '終了', 'はい', 'いいえ',
        '保存', '読み込み', '戻る', '進む', '選択', '決定',
        'キャンセル', '確認', '削除', '追加', '変更', '表示',
        '非表示', '閉じる', '開く', '検索', '並び替え', 'フィルター'
    ]
    
    japanese_file = Path("extracted_text/japanese_text.txt")
    
    found_ac = []
    
    print("Searching for Animal Crossing specific UI words...")
    
    with open(japanese_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            if line_num % 50000 == 0:
                print(f"Processed {line_num} lines...")
            
            text = line.strip()
            if not text or len(text) < 2:
                continue
            
            # Check if text contains any AC words
            for word in ac_words:
                if word in text:
                    found_ac.append({
                        'text': text,
                        'word': word,
                        'line': line_num
                    })
                    break
    
    # Remove duplicates and sort
    unique_ac = []
    seen = set()
    
    for item in found_ac:
        if item['text'] not in seen:
            seen.add(item['text'])
            unique_ac.append(item)
    
    # Sort by word
    unique_ac.sort(key=lambda x: x['word'])
    
    # Save results
    output_file = Path("organized_translations/ac_ui_found.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Animal Crossing Specific UI Words Found\n")
        f.write(f"# Total unique AC UI entries found: {len(unique_ac)}\n\n")
        
        current_word = ""
        for item in unique_ac:
            if item['word'] != current_word:
                current_word = item['word']
                f.write(f"\n# Word: {current_word}\n")
            
            f.write(f"{item['text']} | | AC UI - {current_word}\n")
    
    print(f"✓ Found {len(unique_ac)} unique Animal Crossing UI text entries")
    print(f"✓ Saved to: {output_file}")
    
    # Show some examples
    print("\n=== Sample Animal Crossing UI Text Found ===")
    for i, item in enumerate(unique_ac[:20]):
        print(f"{i+1:2d}. {item['text']} (Contains: {item['word']})")
    
    if len(unique_ac) > 20:
        print(f"... and {len(unique_ac) - 20} more entries")
    
    return unique_ac

if __name__ == "__main__":
    find_ac_ui()
