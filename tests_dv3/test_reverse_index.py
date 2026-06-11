import json
import os


def test_reverse_index_data():
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "api_v3",
        "data",
        "surname",
        "reverse_index_v3.json",
    )
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)
    assert "1" in data
    assert "佐藤" in data["1"]
