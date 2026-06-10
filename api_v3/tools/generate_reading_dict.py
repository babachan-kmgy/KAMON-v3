import json
import os

BASE_DIR = r"C:\KAMON\development\api_v3"
SRC = os.path.join(BASE_DIR, "normalize_dv3", "surname_full_v3.json")
DST = os.path.join(BASE_DIR, "data", "surname_reading_v3.json")

def convert_v3_to_reading_dict(src_path, dst_path):
    with open(src_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("surname_full_v3.json は list 形式である必要があります。")

    result = {}

    for row in data:
        kanji = row.get("canonical_kanji")
        yomi = row.get("canonical_yomi")
        romaji = row.get("canonical_romaji")

        if not kanji:
            continue

        result[kanji] = {
            "yomi": yomi,
            "romaji": romaji
        }

    with open(dst_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✔ 読み専用辞書を生成しました: {dst_path}")


if __name__ == "__main__":
    convert_v3_to_reading_dict(SRC, DST)
