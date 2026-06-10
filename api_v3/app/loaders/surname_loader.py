import json
import os
from app.loaders.cache import get, set

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def _load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    print(f"[DEBUG] Trying to load: {path}")  # ★診断ログ
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")  # ★診断ログ
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_canonical():
    print("[DEBUG] load_canonical called")  # ★診断ログ
    return {}

def load_variants():
    print("[DEBUG] load_variants called")  # ★診断ログ
    key = "surname_variants_v3"
    cached = get(key)
    if cached:
        print("[DEBUG] variants loaded from cache")  # ★診断ログ
        return cached

    data = _load_json("variant_map_v3.json")
    set(key, data)
    return data

def load_reverse_index():
    print("[DEBUG] load_reverse_index called")  # ★診断ログ
    key = "surname_reverse_index_v3"
    cached = get(key)
    if cached:
        print("[DEBUG] reverse_index loaded from cache")  # ★診断ログ
        return cached

    data = _load_json("reverse_index_v3.json")
    set(key, data)
    return data

def load_full():
    print("[DEBUG] load_full called")  # ★診断ログ
    key = "surname_full_v3"
    cached = get(key)
    if cached:
        print("[DEBUG] full loaded from cache")  # ★診断ログ
        return cached

    data = _load_json("surname_full_v3.json")
    set(key, data)
    return data
