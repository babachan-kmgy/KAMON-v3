import json
import os


def test_variant_map_data():
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "api_v3",
        "data",
        "surname",
        "variant_map_v3.json",
    )
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)
    assert "佐藤" in data
    assert "髙橋" in data
    assert data["佐藤"] == "1"
