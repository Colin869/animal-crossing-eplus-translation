#!/usr/bin/env python3
"""
Find Essential UI Words in Animal Crossing e+
"""

from pathlib import Path

def find_essential_ui():
    """Find the most essential UI words that should exist in Animal Crossing"""
    
    # Essential UI words that MUST exist in Animal Crossing
    essential_words = [
        # Core Menu Words
        'メニュー', '設定', '開始', '終了', 'はい', 'いいえ',
        '保存', '読み込み', '戻る', '進む', '選択', '決定',
        'キャンセル', '確認', '削除', '追加', '変更', '表示',
        '非表示', '閉じる', '開く', '検索', '並び替え', 'フィルター',
        
        # Game Core Words
        'インベントリ', 'アイテム', 'マップ', 'ステータス', 'レベル',
        '経験値', 'お金', 'ポイント', 'スコア', 'ランク', '時間',
        '日付', '曜日', '月', '年', '分', '秒', '時',
        
        # Animal Crossing Specific
        '村', '町', '家', '店', '博物館', '郵便局', '役場',
        '住民', '村長', '店員', '郵便配達', '警察官',
        '家具', '服', '道具', '魚', '虫', '化石', '絵画',
        '音楽', '花', '木', '果物', '野菜', '種', '苗',
        
        # Common Game Words
        'プレイヤー', 'キャラクター', 'NPC', '敵', '味方',
        '攻撃', '防御', '魔法', 'スキル', '装備',
        'クエスト', 'ミッション', 'タスク', '目標', '達成'
    ]
    
    japanese_file = Path("extracted_text/japanese_text.txt")
    
    found_essential = []
    
    print("Searching for essential UI words...")
    
    with open(japanese_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            if line_num % 50000 == 0:
                print(f"Processed {line_num} lines...")
            
            text = line.strip()
            if not text or len(text) < 2:
                continue
            
            # Check if text contains any essential words
            for word in essential_words:
                if word in text:
                    found_essential.append({
                        'text': text,
                        'word': word,
                        'line': line_num
                    })
                    break
    
    # Remove duplicates and sort
    unique_essential = []
    seen = set()
    
    for item in found_essential:
        if item['text'] not in seen:
            seen.add(item['text'])
            unique_essential.append(item)
    
    # Sort by word
    unique_essential.sort(key=lambda x: x['word'])
    
    # Save results
    output_file = Path("organized_translations/essential_ui_found.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Essential UI Words Found in Animal Crossing e+\n")
        f.write(f"# Total unique essential UI entries found: {len(unique_essential)}\n\n")
        
        current_word = ""
        for item in unique_essential:
            if item['word'] != current_word:
                current_word = item['word']
                f.write(f"\n# Word: {current_word}\n")
            
            f.write(f"{item['text']} | | UI - {current_word}\n")
    
    print(f"✓ Found {len(unique_essential)} unique essential UI text entries")
    print(f"✓ Saved to: {output_file}")
    
    # Show some examples
    print("\n=== Sample Essential UI Text Found ===")
    for i, item in enumerate(unique_essential[:20]):
        print(f"{i+1:2d}. {item['text']} (Contains: {item['word']})")
    
    if len(unique_essential) > 20:
        print(f"... and {len(unique_essential) - 20} more entries")
    
    return unique_essential

if __name__ == "__main__":
    find_essential_ui()
