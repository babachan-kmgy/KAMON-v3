import json
import os

from normalize_romaji_v3 import normalize_romaji, generate_romaji_variants
from normalize_yomi_v3 import normalize_yomi
from normalize_kanji_v3 import normalize_kanji

# A1_clean.json の場所（tools_dv3）
INPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "tools_dv3", "A1_clean.json")

# 出力ファイル
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "surname_full_v3.json")


def load_input():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_surname_entry(row):
    """
    A1_clean.json の1行を surname_full_v3 の1エントリに変換する
    """

    kanji = row.get("kanji", "")
    yomi = row.get("yomi", "")
    romaji = row.get("romaji", "")
    stable_id = row.get("stable_id", "")
    rank = row.get("rank", None)

    # --- canonical（正準形） ---
    canonical_kanji = normalize_kanji(kanji)
    canonical_yomi = normalize_yomi(yomi)
    canonical_romaji = normalize_romaji(romaji)

    # --- variants（揺れ） ---
    romaji_variants = generate_romaji_variants(romaji)

    # yomi_variants（辞書 v3 では最小限）
    yomi_variants = list({canonical_yomi})

    # kanji_variants（旧字体揺れ → 正準形）
    kanji_variants = list({kanji, canonical_kanji})

    return {
        "stable_id": stable_id,
        "rank": rank,
        "canonical_kanji": canonical_kanji,
        "canonical_yomi": canonical_yomi,
        "canonical_romaji": canonical_romaji,
        "romaji_variants": sorted(romaji_variants),
        "yomi_variants": sorted(yomi_variants),
        "kanji_variants": sorted(kanji_variants)
    }


def build_surname_full():
    rows = load_input()
    output = []

    for row in rows:
        entry = build_surname_entry(row)
        output.append(entry)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✓ surname_full_v3.json を生成しました（{len(output)} 件）")


if __name__ == "__main__":
    build_surname_full()
