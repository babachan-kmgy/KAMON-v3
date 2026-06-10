import json
import os

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


def normalize_query(q: str) -> str:
    """異体字 → 正字（variant_map_v3 を使用）"""
    return VARIANT_MAP.get(q, q)


def search_surname(query: str):
    if not query:
        return []

    q = normalize_query(query)
    results = []

    # --- 1. 完全一致 ---
    if q in REVERSE_INDEX:
        sid = REVERSE_INDEX[q]
        if sid in FULL:
            results.append((0, FULL[sid]))

    # --- 2. 前方一致 ---
    for key, sid in REVERSE_INDEX.items():
        if key.startswith(q) and sid in FULL:
            results.append((1, FULL[sid]))

    # --- 3. 部分一致 ---
    for key, sid in REVERSE_INDEX.items():
        if q in key and sid in FULL:
            results.append((2, FULL[sid]))

    # --- 重複除去（stable_id ベース） ---
    unique = {}
    for score, item in results:
        sid = item["stable_id"]
        if sid not in unique or score < unique[sid][0]:
            unique[sid] = (score, item)

    # --- スコア順 → stable_id 順 ---
    final = sorted(
        unique.values(),
        key=lambda x: (x[0], int(x[1]["stable_id"].split(",")[0]))
    )

    return [item for score, item in final]
