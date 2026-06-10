from app.loaders.reading_loader import load_reading

# ---------------------------------------------------------
# 読み辞書をロード（起動時に一度だけ）
# ---------------------------------------------------------
reading_dict = load_reading()

# ---------------------------------------------------------
# 読み（ひらがな）を取得
# ---------------------------------------------------------
def lookup_yomi(kanji: str):
    """
    指定した漢字の名字に対応する「読み（ひらがな）」を返す。
    辞書に存在しない場合は None を返す。
    """
    entry = reading_dict.get(kanji)
    return entry.get("yomi") if entry else None

# ---------------------------------------------------------
# ローマ字を取得
# ---------------------------------------------------------
def lookup_romaji(kanji: str):
    """
    指定した漢字の名字に対応する「ローマ字」を返す。
    辞書に存在しない場合は None を返す。
    """
    entry = reading_dict.get(kanji)
    return entry.get("romaji") if entry else None
