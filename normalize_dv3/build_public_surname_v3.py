import json
import os

INPUT_PATH = os.path.join(os.path.dirname(__file__), "surname_full_v3.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "public_surname_v3.json")


def load_input():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_public_entry(row):
    """
    surname_full_v3 の1エントリから公開用の軽量辞書を作る
    """
    return {
        "stable_id": row["stable_id"],
        "rank": row["rank"],
        "kanji": row["canonical_kanji"],
        "yomi": row["canonical_yomi"],
        "romaji": row["canonical_romaji"]
    }


def build_public_surname():
    rows = load_input()
    output = []

    for row in rows:
        entry = build_public_entry(row)
        output.append(entry)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✓ public_surname_v3.json を生成しました（{len(output)} 件）")


if __name__ == "__main__":
    build_public_surname()
