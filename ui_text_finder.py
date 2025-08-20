#!/usr/bin/env python3
"""
UI Text Finder for Animal Crossing e+
Finds UI-related text in the extracted Japanese text
"""

import re
from pathlib import Path

def find_ui_text():
    """Find UI-related text in the extracted Japanese text"""
    
    # Common UI patterns in Japanese games
    ui_patterns = [
        # Menu items
        r'メニュー', r'設定', r'開始', r'終了', r'はい', r'いいえ',
        r'保存', r'読み込み', r'戻る', r'進む', r'選択', r'決定',
        r'キャンセル', r'確認', r'削除', r'追加', r'変更', r'表示',
        r'非表示', r'閉じる', r'開く', r'検索', r'並び替え', r'フィルター',
        
        # Game-specific UI
        r'インベントリ', r'アイテム', r'マップ', r'ステータス', r'レベル',
        r'経験値', r'お金', r'ポイント', r'スコア', r'ランク', r'時間',
        r'日付', r'曜日', r'月', r'年', r'分', r'秒', r'時', r'分',
        
        # Common UI words
        r'ボタン', r'タブ', r'ウィンドウ', r'ダイアログ', r'メッセージ',
        r'エラー', r'警告', r'情報', r'ヘルプ', r'説明', r'詳細',
        r'名前', r'タイトル', r'サブタイトル', r'説明文', r'コメント',
        
        # Game mechanics UI
        r'プレイヤー', r'キャラクター', r'NPC', r'敵', r'味方',
        r'攻撃', r'防御', r'魔法', r'スキル', r'アイテム', r'装備',
        r'クエスト', r'ミッション', r'タスク', r'目標', r'達成',
        
        # Animal Crossing specific
        r'村', r'町', r'家', r'店', r'博物館', r'郵便局', r'役場',
        r'住民', r'村長', r'店員', r'郵便配達', r'警察官',
        r'家具', r'服', r'道具', r'魚', r'虫', r'化石', r'絵画',
        r'音楽', r'花', r'木', r'果物', r'野菜', r'種', r'苗',
        
        # Common particles and connectors that appear in UI
        r'の', r'を', r'に', r'へ', r'から', r'まで', r'より',
        r'と', r'や', r'または', r'および', r'について', r'に関して'
    ]
    
    # Load Japanese text
    japanese_file = Path("extracted_text/japanese_text.txt")
    if not japanese_file.exists():
        print("Error: japanese_text.txt not found!")
        return
    
    print("Searching for UI text patterns...")
    
    ui_text_found = []
    
    with open(japanese_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            if line_num % 10000 == 0:
                print(f"Processed {line_num} lines...")
            
            text = line.strip()
            if not text or len(text) < 2:
                continue
            
            # Check if text contains any UI patterns
            for pattern in ui_patterns:
                if re.search(pattern, text):
                    ui_text_found.append({
                        'text': text,
                        'pattern': pattern,
                        'line': line_num
                    })
                    break
    
    # Remove duplicates and sort
    unique_ui_text = []
    seen = set()
    
    for item in ui_text_found:
        if item['text'] not in seen:
            seen.add(item['text'])
            unique_ui_text.append(item)
    
    # Sort by pattern type
    unique_ui_text.sort(key=lambda x: x['pattern'])
    
    # Save results
    output_file = Path("organized_translations/ui_text_extended.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Extended UI Text Found in Animal Crossing e+\n")
        f.write(f"# Total unique UI entries found: {len(unique_ui_text)}\n\n")
        
        current_pattern = ""
        for item in unique_ui_text:
            if item['pattern'] != current_pattern:
                current_pattern = item['pattern']
                f.write(f"\n# Pattern: {current_pattern}\n")
            
            f.write(f"{item['text']} | | UI - {current_pattern}\n")
    
    print(f"✓ Found {len(unique_ui_text)} unique UI text entries")
    print(f"✓ Saved to: {output_file}")
    
    # Show some examples
    print("\n=== Sample UI Text Found ===")
    for i, item in enumerate(unique_ui_text[:20]):
        print(f"{i+1:2d}. {item['text']} (Pattern: {item['pattern']})")
    
    if len(unique_ui_text) > 20:
        print(f"... and {len(unique_ui_text) - 20} more entries")
    
    return unique_ui_text

if __name__ == "__main__":
    find_ui_text()
