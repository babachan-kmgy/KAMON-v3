from app.loaders.surname_loader import load_variants

variants = load_variants()

def expand_variants(kanji: str):
    """
    異体字展開（variants.json が str / list / dict でも壊れない安全版）
    """
    if kanji not in variants:
        return [kanji]

    v = variants[kanji]

    # ① すでにリストならそのまま
    if isinstance(v, list):
        return [kanji] + v

    # ② 文字列なら単一要素リストに変換
    if isinstance(v, str):
        return [kanji, v]

    # ③ dict の場合（例: {"variant": "佐嶋"}）
    if isinstance(v, dict):
        # 値を全部取り出してリスト化
        extracted = []
        for val in v.values():
            if isinstance(val, list):
                extracted.extend(val)
            else:
                extracted.append(val)
        return [kanji] + extracted

    # ④ その他の型は無視
    return [kanji]
