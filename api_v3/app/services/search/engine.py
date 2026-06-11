import json
import os
import re
import unicodedata

# engine.py のあるディレクトリ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 正しい辞書フォルダ（api_v3/data/surname）
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "..", "data", "surname")

# --- Load V3 dictionaries ---
with open(os.path.join(DATA_DIR, "reverse_index_v3.json"), encoding="utf-8") as f:
    REVERSE_INDEX = json.load(f)

with open(os.path.join(DATA_DIR, "surname_full_v3.json"), encoding="utf-8") as f:
    FULL = json.load(f)

with open(os.path.join(DATA_DIR, "variant_map_v3.json"), encoding="utf-8") as f:
    VARIANT_MAP = json.load(f)

# O(1) 検索用のハッシュマップに変換
FULL_DICT = {item["stable_id"]: item for item in FULL}

# 高速化のため、VARIANT_MAP のキーをあらかじめ小文字化し、FULL_DICT に存在するIDのみに絞り込んで保持
VARIANT_MAP_LOWER = [(k.lower(), v) for k, v in VARIANT_MAP.items() if v in FULL_DICT]


def normalize_query(q: str) -> str:
    """異体字 → 正字（variant_map_v3 を使用）"""
    return VARIANT_MAP.get(q, q)


def search_surname(query: str):
    if not query:
        return []

    # クエリの標準化（前後のスペース除去、NFKC正規化、大文字小文字の統一）
    q_clean = unicodedata.normalize("NFKC", query).strip()
    q_clean = re.sub(r"[・･'’´` ]", "", q_clean)
    if not q_clean:
        return []
    q_lower = q_clean.lower()

    results = []

    # --- 1. 完全一致 (Exact Match) ---
    # variant_map_v3 のキーと完全一致するか（大文字小文字や半角全角を考慮）
    exact_sid = VARIANT_MAP.get(q_clean) or VARIANT_MAP.get(q_lower)
    if exact_sid and exact_sid in FULL_DICT:
        results.append((0, FULL_DICT[exact_sid]))

    # --- 2 & 3. 前方一致 & 部分一致 (Prefix & Partial Match) ---
    for v_lower, sid in VARIANT_MAP_LOWER:
        if q_lower in v_lower:
            if v_lower == q_lower:
                results.append((0, FULL_DICT[sid]))
            elif v_lower.startswith(q_lower):
                results.append((1, FULL_DICT[sid]))
            else:
                results.append((2, FULL_DICT[sid]))

    # --- 重複除去（stable_id ベースで、より良いスコアを優先） ---
    unique = {}
    for score, item in results:
        sid = item["stable_id"]
        if sid not in unique or score < unique[sid][0]:
            unique[sid] = (score, item)

    # --- ソート: スコア順 (完全 0 > 前方 1 > 部分 2) ➔ stable_id（人口順）順 ---
    final = sorted(
        unique.values(), key=lambda x: (x[0], int(x[1]["stable_id"].split(",")[0]))
    )

    # UI / API が期待するキー名（kanji, yomi, romaji, variants_public）にマッピングして返却
    formatted = []
    for _score, item in final:
        formatted.append(
            {
                "stable_id": item["stable_id"],
                "rank": item.get("rank"),
                "kanji": item.get("canonical_kanji", ""),
                "yomi": item.get("canonical_yomi", ""),
                "romaji": item.get("canonical_romaji", ""),
                "variants_public": item.get("kanji_variants", []),
            }
        )

    return formatted
