import os
import sys

# Add normalize_dv3 to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "api_v3", "normalize_dv3"))

from normalize_kanji_v3 import canonical_kanji, normalize_kanji
from normalize_romaji_v3 import canonical_romaji, normalize_romaji
from normalize_yomi_v3 import canonical_yomi, normalize_yomi


def test_kanji_normalization():
    # Test canonical kanji mapping (e.g. 髙橋 -> 高橋, 嶋田 -> 島田)
    assert canonical_kanji("髙橋") == "高橋"
    assert canonical_kanji("嶋田") == "島田"
    assert canonical_kanji("島 田") == "島田"  # space removal

    # Test full normalize output
    res = normalize_kanji("髙橋")
    assert res["canonical"] == "高橋"
    assert "髙橋" in res["variants"]
    assert "高橋" in res["variants"]


def test_yomi_normalization():
    # Test katakana to hiragana and symbol removal
    assert canonical_yomi("シマ・ウチ") == "しまうち"
    assert canonical_yomi("ｼﾏ･ｳﾁ") == "しまうち"  # half-width kana

    res = normalize_yomi("シマウチ")
    assert res["canonical"] == "しまうち"
    assert "しまうち" in res["variants"]
    assert "シマウチ" in res["variants"]


def test_romaji_normalization():
    # Test long vowel removal and lowercase/symbol removal
    assert canonical_romaji("Ōshima") == "oshima"
    assert canonical_romaji("O-shima") == "oshima"

    res = normalize_romaji("Ōshima")
    assert res["canonical"] == "oshima"
    # Long vowels should be expanded in variants
    assert "ooshima" in res["variants"]
    assert "oushima" in res["variants"]
