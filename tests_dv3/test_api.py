import os
import sys

from fastapi.testclient import TestClient

# Add api_v3 and api_v3/app to path for import resolution
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "api_v3")
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "app"))

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "KAMON API v3 is running"}


def test_api_normalize():
    # Test normalization endpoint with a variant kanji
    response = client.get("/normalize", params={"q": "髙橋"})
    assert response.status_code == 200
    data = response.json()
    assert data["input"] == "髙橋"
    assert "高橋" in data["normalized"]
    assert "髙橋" in data["normalized"]

    # Test normalization endpoint with katakana
    response = client.get("/normalize", params={"q": "タカハシ"})
    assert response.status_code == 200
    data = response.json()
    assert "たかはし" in data["normalized"]


def test_api_search_exact():
    # Test search endpoint with an exact match
    response = client.get("/search", params={"q": "佐藤"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert results[0]["kanji"] == "佐藤"
    assert results[0]["stable_id"] == "1"


def test_api_search_empty_and_spaces():
    # Test search endpoint with empty query
    response1 = client.get("/search", params={"q": ""})
    assert response1.status_code == 200
    assert response1.json() == []

    response2 = client.get("/search", params={"q": "   "})
    assert response2.status_code == 200
    assert response2.json() == []
