import os
import sys

# Add api_v3 and api_v3/app to path
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "api_v3")
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "app"))

from app.services.search.engine import search_surname


def test_search_exact_match():
    # Test exact match of a common surname
    results = search_surname("佐藤")
    assert len(results) > 0
    assert results[0]["kanji"] == "佐藤"
    assert results[0]["stable_id"] == "1"


def test_search_variant_match():
    # Test variant match (髙橋 should map to stable_id 3 and return 高橋)
    results = search_surname("髙橋")
    assert len(results) > 0
    # The canonical form is 高橋
    assert results[0]["kanji"] == "高橋"
    assert results[0]["stable_id"] == "3"


def test_search_partial_match():
    # Test partial match
    results = search_surname("田")
    assert len(results) > 0
    # Let's ensure some items are returned and they contain "田" in their kanji
    assert any("田" in r["kanji"] for r in results)


def test_search_romaji_match():
    # Test searching by romaji
    results = search_surname("sato")
    assert len(results) > 0
    assert results[0]["kanji"] == "佐藤"


def test_search_empty():
    assert search_surname("") == []
    assert search_surname("   ") == []


def test_search_no_match():
    # Test queries that shouldn't match any surname
    assert search_surname("xyz") == []
    assert search_surname("無効な名字") == []


def test_search_case_insensitivity():
    # Test romaji search with different casings
    results_upper = search_surname("SATO")
    results_title = search_surname("Sato")
    results_lower = search_surname("sato")
    assert results_upper == results_lower
    assert results_title == results_lower


def test_search_symbols_and_spaces():
    # Test that symbols (dots, spaces) are stripped correctly in search query
    results_spaced = search_surname("佐 藤")
    results_exact = search_surname("佐藤")
    assert results_spaced == results_exact

    # Test middle dots and quotes
    # (Assuming "シマ・ウチ" or similar exists, let's test general symbol stripping)
    results_dots = search_surname("佐・藤")
    assert results_dots == results_exact


def test_search_sorting_order():
    # Test search sorting: exact match should have higher priority (score 0)
    # than prefix (score 1) and partial (score 2).
    # Also, within the same score level, it should sort by stable_id (population rank).
    results = search_surname("藤")
    # "藤" is a prefix match for "藤田", "藤井", etc.
    # It is a partial match for "佐藤", "伊藤", etc.
    # So prefix matches ("藤田") must be ranked before partial matches ("佐藤").
    # Let's verify that prefix matches come first.
    assert len(results) > 0

    # We find indices of prefix vs partial matches
    prefix_indices = []
    partial_indices = []
    for idx, r in enumerate(results):
        if r["kanji"].startswith("藤"):
            prefix_indices.append(idx)
        elif "藤" in r["kanji"]:
            partial_indices.append(idx)

    if prefix_indices and partial_indices:
        assert min(prefix_indices) < min(partial_indices)
