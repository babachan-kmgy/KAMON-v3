import os
import sys

# ---------------------------------------------------------
# 正しいパス設定（services → app → api_v3 → normalize_dv3）
# ---------------------------------------------------------
sys.path.append(
    os.path.join(
        os.path.dirname(__file__),  # .../api_v3/app/services
        "..",  # .../api_v3/app
        "..",  # .../api_v3
        "normalize_dv3",  # .../api_v3/normalize_dv3
    )
)

from normalize_kanji_v3 import normalize_kanji
from normalize_romaji_v3 import normalize_romaji
from normalize_yomi_v3 import normalize_yomi

# ---------------------------------------------------------
# v3 辞書ローダー（TB 環境用）
# ---------------------------------------------------------
from app.loaders.surname_loader import (
    load_variants,
    load_full,
    load_reverse_index,
    load_canonical,
)
from app.loaders.dictionary_loader import (
    load_public_surname,
    load_public_reverse,
)


# ---------------------------------------------------------
# 正規化（ローマ字・読み・漢字）完全版
# 3方向の canonical + variants をすべて統合して返す
# ---------------------------------------------------------
def normalize_query(q: str):
    romaji = normalize_romaji(q)  # {"canonical": "...", "variants": [...]}
    yomi = normalize_yomi(q)
    kanji = normalize_kanji(q)

    results = set()

    # ローマ字
    results.add(romaji["canonical"])
    for v in romaji["variants"]:
        results.add(v)

    # 読み
    results.add(yomi["canonical"])
    for v in yomi["variants"]:
        results.add(v)

    # 漢字
    results.add(kanji["canonical"])
    for v in kanji["variants"]:
        results.add(v)

    return results


# ---------------------------------------------------------
# 検索（query → stable_id → public_surname）
# normalize_query() の揺れをすべて variant_map に照合
# ---------------------------------------------------------
def search_by_query(q):
    normalized_keys = normalize_query(q)

    variant_map = load_variants()
    public_surname = load_public_surname()

    stable_ids = set()
    for key in normalized_keys:
        if key in variant_map:
            stable_ids.add(variant_map[key])

    results = []
    for sid in stable_ids:
        for row in public_surname:
            if row["stable_id"] == sid:
                results.append(row)

    return results


# ---------------------------------------------------------
# ID から surname を取得
# ---------------------------------------------------------
def lookup_by_id(sid):
    public_surname = load_public_surname()
    for row in public_surname:
        if row["stable_id"] == sid:
            return row
    return None


# ---------------------------------------------------------
# ID から public_reverse を取得
# ---------------------------------------------------------
def variants_public_by_id(sid):
    public_reverse = load_public_reverse()
    return public_reverse.get(sid)
