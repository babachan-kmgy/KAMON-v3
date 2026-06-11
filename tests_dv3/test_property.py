import os
import re
import sys

from hypothesis import given
from hypothesis import strategies as st

# Add normalize_dv3 to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "api_v3", "normalize_dv3"))

from normalize_kanji_v3 import canonical_kanji, normalize_kanji
from normalize_romaji_v3 import canonical_romaji, normalize_romaji
from normalize_yomi_v3 import canonical_yomi, normalize_yomi


@given(st.text())
def test_kanji_properties(s):
    # Property 1: No crash for any arbitrary text
    result = normalize_kanji(s)
    assert isinstance(result, dict)
    assert "canonical" in result
    assert "variants" in result

    canonical = result["canonical"]
    variants = result["variants"]

    # Property 2: Idempotency (canonical of canonical is the same)
    assert canonical_kanji(canonical) == canonical

    # Property 3: Canonical form must always be present in the variants list (if canonical is not empty)
    if canonical:
        assert canonical in variants

    # Property 4: Canonical kanji must not contain symbols like middle dots or spaces
    assert not any(ch in canonical for ch in "・･'’´` ")


@given(st.text())
def test_yomi_properties(s):
    # Property 1: No crash
    result = normalize_yomi(s)
    assert isinstance(result, dict)

    canonical = result["canonical"]
    variants = result["variants"]

    # Property 2: Idempotency
    assert canonical_yomi(canonical) == canonical

    # Property 3: Canonical form is in variants
    if canonical:
        assert canonical in variants

    # Property 4: No symbols
    assert not any(ch in canonical for ch in "・･'’´` ")


@given(st.text())
def test_romaji_properties(s):
    # Property 1: No crash
    result = normalize_romaji(s)
    assert isinstance(result, dict)

    canonical = result["canonical"]
    variants = result["variants"]

    # Property 2: Idempotency
    assert canonical_romaji(canonical) == canonical

    # Property 3: Canonical form is in variants
    if canonical:
        assert canonical in variants

    # Property 4: No symbols (including hyphens and dashes for romaji)
    assert not any(ch in canonical for ch in "-‐‑‒–—―'’´` ")

    # Property 5: Romaji canonical must be completely lowercase
    # (Checking if it contains letters, and if so, it must be lowercase)
    if re.search(r"[a-zA-Z]", canonical):
        assert canonical.islower()
