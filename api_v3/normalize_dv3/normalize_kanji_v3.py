import unicodedata
import json
import os
import re

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
    return re.sub(r"[・･'’´` ]", "", text)


# ---------------------------------------------------------
# canonical（正規形）生成
# ---------------------------------------------------------
def canonical_kanji(text: str) -> str:
    if not text:
        return ""

    t = unicode_normalize(text)
    t = remove_symbols(t)

    # normalization_rules.json の kanji_normalization を適用
    kanji_rules = RULES.get("kanji_normalization", {})
    for old, new in kanji_rules.items():
        t = t.replace(old, new)

    return t


# ---------------------------------------------------------
# variants（揺れ）生成
# ---------------------------------------------------------
def generate_kanji_variants(text: str) -> list:
    if not text:
        return []

    variants = set()

    base = unicode_normalize(text)
    base = remove_symbols(base)

    variants.add(base)

    canonical = canonical_kanji(text)
    variants.add(canonical)

    # normalization_rules.json の逆引き（旧字体 → 新字体 → 旧字体）
    kanji_rules = RULES.get("kanji_normalization", {})
    reverse_rules = {}

    for old, new in kanji_rules.items():
        reverse_rules.setdefault(new, []).append(old)

    # canonical に対応する旧字体を追加
    for new, olds in reverse_rules.items():
        if new in canonical:
            for old in olds:
                variants.add(canonical.replace(new, old))

    return sorted({v for v in variants if v})


# ---------------------------------------------------------
# ★ 完全版 normalize_kanji（canonical + variants を返す）
# ---------------------------------------------------------
def normalize_kanji(text: str) -> dict:
    canonical = canonical_kanji(text)
    variants = generate_kanji_variants(text)

    return {
        "canonical": canonical,
        "variants": variants
    }


# --- 動作確認 ---
if __name__ == "__main__":
    tests = ["嶋田", "﨑山", "髙橋", "邉見", "𠮷田", "島 田"]
    for t in tests:
        print(t, "→", normalize_kanji(t))
