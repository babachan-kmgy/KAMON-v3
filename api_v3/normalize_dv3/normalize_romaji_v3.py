import unicodedata
import re
import json
import os

# ---------------------------------------------------------
# 正規化ルールの読み込み
# ---------------------------------------------------------
def load_rules():
    rules_path = os.path.join(os.path.dirname(__file__), "normalization_rules.json")
    if not os.path.exists(rules_path):
        return {}
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)

RULES = load_rules()


# ---------------------------------------------------------
# Unicode 正規化（NFKC）
# ---------------------------------------------------------
def unicode_normalize(text: str) -> str:
    if not text:
        return ""
    return unicodedata.normalize("NFKC", text)


# ---------------------------------------------------------
# 記号除去
# ---------------------------------------------------------
def remove_symbols(text: str) -> str:
    return re.sub(r"[-‐‑‒–—―'’´` ]", "", text)


# ---------------------------------------------------------
# 長音処理
# ---------------------------------------------------------
def normalize_long_vowels(text: str) -> str:
    if not text:
        return ""

    long_rules = RULES.get("romaji_long_vowels", {})
    for k, v in long_rules.items():
        text = text.replace(k, v)

    text = text.replace("ô", "o").replace("ö", "o")
    text = text.replace("ō", "o").replace("Ō", "o")

    return text


# ---------------------------------------------------------
# canonical_romaji を生成（正規形）
# ---------------------------------------------------------
def canonical_romaji(text: str) -> str:
    if not text:
        return ""

    t = unicode_normalize(text)
    t = t.lower()
    t = remove_symbols(t)
    t = normalize_long_vowels(t)

    return t


# ---------------------------------------------------------
# romaji_variants（揺れ生成）
# ---------------------------------------------------------
def generate_romaji_variants(text: str) -> list:
    if not text:
        return []

    variants = set()

    base = unicode_normalize(text)
    base_l = base.lower()

    variants.add(base)
    variants.add(base_l)
    variants.add(remove_symbols(base_l))

    canonical = canonical_romaji(text)
    variants.add(canonical)

    # 長音揺れ（最初の o のみ）
    if "o" in canonical:
        idx = canonical.index("o")
        variants.add(canonical[:idx] + "oo" + canonical[idx+1:])
        variants.add(canonical[:idx] + "ou" + canonical[idx+1:])
        variants.add(canonical[:idx] + "oh" + canonical[idx+1:])

    # 元の文字に ō が含まれていた場合
    if "ō" in base_l:
        variants.add(base_l.replace("ō", "o"))
        variants.add(base_l.replace("ō", "oo"))
        variants.add(base_l.replace("ō", "ou"))
        variants.add(base_l.replace("ō", "oh"))

    # combining mark 揺れ
    variants.add(unicodedata.normalize("NFKC", base_l))

    # normalization_rules.json の揺れ
    long_rules = RULES.get("romaji_long_vowels", {})
    for k, v in long_rules.items():
        if k in base_l:
            variants.add(base_l.replace(k, v))

    variants = {v for v in variants if v}

    return sorted(variants)


# ---------------------------------------------------------
# ★ 完全版 normalize_romaji（canonical + variants を返す）
# ---------------------------------------------------------
def normalize_romaji(text: str) -> dict:
    canonical = canonical_romaji(text)
    variants = generate_romaji_variants(text)

    return {
        "canonical": canonical,
        "variants": variants
    }


# --- 動作確認 ---
if __name__ == "__main__":
    text = "Ōshima"
    print("Input:", text)
    print("canonical_romaji:", canonical_romaji(text))
    print("romaji_variants:", generate_romaji_variants(text))
    print("normalize_romaji:", normalize_romaji(text))
