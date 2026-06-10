import csv
import json
import os

INPUT_CSV = r"C:\KAMON\archive_projects\research_projects\surname_project\core\archive\original_exports\A-1.csv"
OUTPUT_JSON = r"C:\KAMON\development\tools_dv3\A1_clean.json"

def convert():
    output = []

    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # 1行目: 英語ヘッダー
    # 2行目: 日本語ヘッダー
    # 3行目以降: データ
    for row in rows[2:]:
        if not row or len(row) < 6:
            continue

        rank = row[0]
        kanji = row[4]
        stable_id = row[5]
        yomi = row[6]          # Furigana-1
        romaji = row[7]        # Latin alphabet-1

        entry = {
            "rank": int(rank) if rank.isdigit() else None,
            "kanji": kanji,
            "yomi": yomi,
            "romaji": romaji,
            "stable_id": stable_id
        }
        output.append(entry)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✓ A1_clean.json を生成しました（{len(output)} 件）")


if __name__ == "__main__":
    convert()
