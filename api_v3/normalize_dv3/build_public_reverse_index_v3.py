import json
import os

INPUT_PATH = os.path.join(os.path.dirname(__file__), "public_surname_v3.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "public_reverse_index_v3.json")


def load_input():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_public_reverse_index():
    rows = load_input()
    reverse_index = {}

    for row in rows:
        sid = row["stable_id"]

        # 公開用は canonical のみ
        kanji = row["kanji"]
        yomi = row["yomi"]
        romaji = row["romaji"]

        reverse_index[sid] = sorted(list({kanji, yomi, romaji}))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(reverse_index, f, ensure_ascii=False, indent=2)

    print(f"✓ public_reverse_index_v3.json を生成しました（{len(reverse_index)} 件）")


if __name__ == "__main__":
    build_public_reverse_index()
