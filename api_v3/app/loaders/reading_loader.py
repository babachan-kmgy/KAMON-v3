import json
import os

from app.loaders.cache import get, set

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SURNAME_DIR = os.path.join(BASE_DIR, "data", "surname")


def load_reading():
    key = "surname_reading"
    cached = get(key)
    if cached:
        return cached

    path = os.path.join(SURNAME_DIR, "reading.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    set(key, data)
    return data
