import json
import os


def test_surname_full_data():
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "api_v3",
        "data",
        "surname",
        "surname_full_v3.json",
    )
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["stable_id"] == "1"
    assert data[0]["canonical_kanji"] == "佐藤"
