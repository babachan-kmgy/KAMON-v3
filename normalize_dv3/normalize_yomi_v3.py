import unicodedata
import re

# ---------------------------------------------------------
# Unicode 正規化（NFKC）
# ---------------------------------------------------------
def unicode_normalize(text: str) -> str:
    if not text:
        return ""
    return unicodedata.normalize("NFKC", text)


# ---------------------------------------------------------
# カタカナ → ひらがな
# ---------------------------------------------------------
def katakana_to_hiragana(text: str) -> str:
    result = []
    for ch in text:
        code = ord(ch)
        if 0x30A1 <= code <= 0x30F6:  # カタカナ範囲
            result.append(chr(code - 0x60))
        else:
            result.append(ch)
    return "".join(result)


# ---------------------------------------------------------
# 記号除去
# ---------------------------------------------------------
def remove_symbols(text: str) -> str:
    return re.sub(r"[・･'’´` ]", "", text)


# ---------------------------------------------------------
# canonical（正規形）生成
# ---------------------------------------------------------
def canonical_yomi(text: str) -> str:
    if not text:
        return ""

    t = unicode_normalize(text)
    t = katakana_to_hiragana(t)
    t = remove_symbols(t)

    # 半角カナ → 全角 → ひらがな
    t = unicodedata.normalize("NFKC", t)
    t = katakana_to_hiragana(t)

    return t


# ---------------------------------------------------------
# variants（揺れ）生成
# ---------------------------------------------------------
def generate_yomi_variants(text: str) -> list:
    if not text:
        return []

    variants = set()

    # 元の入力
    base = unicode_normalize(text)
    variants.add(base)

    # カタカナ版
    kana = katakana_to_hiragana(base)
    variants.add(kana)

    # 記号除去版
    variants.add(remove_symbols(kana))

    # canonical（正規形）
    canonical = canonical_yomi(text)
    variants.add(canonical)

    # 半角カナ → 全角 → ひらがな
    full = unicodedata.normalize("NFKC", text)
    full = katakana_to_hiragana(full)
    variants.add(full)

    # ひらがな・カタカナ両方を揺れとして追加
    hira = canonical
    kata = "".join(chr(ord(ch) + 0x60) if "ぁ" <= ch <= "ゖ" else ch for ch in hira)
    variants.add(kata)

    return sorted({v for v in variants if v})


# ---------------------------------------------------------
# ★ 完全版 normalize_yomi（canonical + variants を返す）
# ---------------------------------------------------------
def normalize_yomi(text: str) -> dict:
    canonical = canonical_yomi(text)
    variants = generate_yomi_variants(text)

    return {
        "canonical": canonical,
        "variants": variants
    }


# --- 動作確認 ---
if __name__ == "__main__":
    tests = ["シマウチ", "ｼﾏｳﾁ", "しまうち", "シマ・ウチ", "ｼﾏ･ｳﾁ"]
    for t in tests:
        print(t, "→", normalize_yomi(t))
