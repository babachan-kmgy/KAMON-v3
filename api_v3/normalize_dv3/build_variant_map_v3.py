import json
import os

from normalize_romaji_v3 import normalize_romaji
from normalize_yomi_v3 import normalize_yomi
from normalize_kanji_v3 import normalize_kanji


INPUT_PATH = os.path.join(os.path.dirname(__file__), "surname_full_v3.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "variant_map_v3.json")


def load_input():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def add_entry(variant_map, key, stable_id):
    if key and key not in variant_map:
        variant_map[key] = stable_id


def build_variant_map():
    rows = load_input()
    variant_map = {}

    for row in rows:
        stable_id = row["stable_id"]

        # --- canonical ---
        ck = row["canonical_kanji"]
        cy = row["canonical_yomi"]
        cr = row["canonical_romaji"]

        # --- variants ---
        kanji_vars = row["kanji_variants"]
        yomi_vars = row["yomi_variants"]
        romaji_vars = row["romaji_variants"]

        # --- 1) canonical を登録 ---
        nk = normalize_kanji(ck)
        ny = normalize_yomi(cy)
        nr = normalize_romaji(cr)

        add_entry(variant_map, nk["canonical"], stable_id)
        add_entry(variant_map, ny["canonical"], stable_id)
        add_entry(variant_map, nr["canonical"], stable_id)

        # --- 2) variants を登録 ---
        for kv in kanji_vars:
            nkv = normalize_kanji(kv)
            for v in nkv["variants"]:
                add_entry(variant_map, v, stable_id)

        for yv in yomi_vars:
            nyv = normalize_yomi(yv)
            for v in nyv["variants"]:
                add_entry(variant_map, v, stable_id)

        for rv in romaji_vars:
            nrv = normalize_romaji(rv)
            for v in nrv["variants"]:
                add_entry(variant_map, v, stable_id)

    # --- 保存 ---
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(variant_map, f, ensure_ascii=False, indent=2)

    print(f"✓ variant_map_v3.json を生成しました（{len(variant_map)} 件）")


if __name__ == "__main__":
    build_variant_map()
