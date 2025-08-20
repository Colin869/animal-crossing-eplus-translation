#!/usr/bin/env python3
"""
Find Meaningful UI Text
"""

from pathlib import Path

def find_meaningful_ui():
    """Find meaningful UI text that we can actually translate"""
    
    # Meaningful UI words to look for
    meaningful_words = [
        # Essential UI
        'メニュー', '設定', '開始', '終了', 'はい', 'いいえ',
        '保存', '読み込み', '戻る', '進む', '選択', '決定',
        'キャンセル', '確認', '削除', '追加', '変更', '表示',
        '非表示', '閉じる', '開く', '検索', '並び替え', 'フィルター',
        
        # Game UI
        'インベントリ', 'アイテム', 'マップ', 'ステータス', 'レベル',
        '経験値', 'お金', 'ポイント', 'スコア', 'ランク', '時間',
        '日付', '曜日', '月', '年', '分', '秒', '時',
        
        # Common UI
        'ボタン', 'タブ', 'ウィンドウ', 'ダイアログ', 'メッセージ',
        'エラー', '警告', '情報', 'ヘルプ', '説明', '詳細',
        '名前', 'タイトル', 'サブタイトル', '説明文', 'コメント',
        
        # Game mechanics
        'プレイヤー', 'キャラクター', 'NPC', '敵', '味方',
        '攻撃', '防御', '魔法', 'スキル', '装備',
        'クエスト', 'ミッション', 'タスク', '目標', '達成',
        
        # Animal Crossing specific
        '村', '町', '家', '店', '博物館', '郵便局', '役場',
        '住民', '村長', '店員', '郵便配達', '警察官',
        '家具', '服', '道具', '魚', '虫', '化石', '絵画',
        '音楽', '花', '木', '果物', '野菜', '種', '苗'
    ]
    
    japanese_file = Path("extracted_text/japanese_text.txt")
    
    meaningful_found = []
    
    print("Searching for meaningful UI text...")
    
    with open(japanese_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            if line_num % 50000 == 0:
                print(f"Processed {line_num} lines...")
            
            text = line.strip()
            if not text or len(text) < 2:
                continue
            
            # Check if text contains any meaningful words
            for word in meaningful_words:
                if word in text:
                    meaningful_found.append({
                        'text': text,
                        'word': word,
                        'line': line_num
                    })
                    break
    
    # Remove duplicates and sort
    unique_meaningful = []
    seen = set()
    
    for item in meaningful_found:
        if item['text'] not in seen:
            seen.add(item['text'])
            unique_meaningful.append(item)
    
    # Sort by word
    unique_meaningful.sort(key=lambda x: x['word'])
    
    # Save results
    output_file = Path("organized_translations/meaningful_ui.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Meaningful UI Text Found in Animal Crossing e+\n")
        f.write(f"# Total unique meaningful UI entries found: {len(unique_meaningful)}\n\n")
        
        current_word = ""
        for item in unique_meaningful:
            if item['word'] != current_word:
                current_word = item['word']
                f.write(f"\n# Word: {current_word}\n")
            
            f.write(f"{item['text']} | | UI - {current_word}\n")
    
    print(f"✓ Found {len(unique_meaningful)} unique meaningful UI text entries")
    print(f"✓ Saved to: {output_file}")
    
    # Show some examples
    print("\n=== Sample Meaningful UI Text Found ===")
    for i, item in enumerate(unique_meaningful[:20]):
        print(f"{i+1:2d}. {item['text']} (Contains: {item['word']})")
    
    if len(unique_meaningful) > 20:
        print(f"... and {len(unique_meaningful) - 20} more entries")
    
    return unique_meaningful

if __name__ == "__main__":
    find_meaningful_ui()
