import json
import os

from app.loaders.cache import get, set

# ---------------------------------------------------------
# KAMON v3 surname loader（TB 環境用 完全版）
# ---------------------------------------------------------

# v3 辞書ディレクトリ（TB の環境に合わせた絶対パス）
DATA_DIR = r"C:\KAMON\GitHub\release_v3\dictionaries_v3"

def _load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    print(f"[DEBUG] Trying to load: {path}")
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# canonical.json（正規化用）
def load_canonical():
    print("[DEBUG] load_canonical called")
    key = "surname_canonical_v3"
    cached = get(key)
    if cached:
        print("[DEBUG] canonical loaded from cache")
        return cached

    data = _load_json("canonical.json")
    set(key, data)
    return data

# variant_map_v3.json（異体字マップ）
def load_variants():
    print("[DEBUG] load_variants called")
    key = "surname_variants_v3"
    cached = get(key)
    if cached:
        print("[DEBUG] variants loaded from cache")
        return cached

    data = _load_json("variant_map_v3.json")
    set(key, data)
    return data

# reverse_index_v3.json（逆引き辞書）
def load_reverse_index():
    print("[DEBUG] load_reverse_index called")
    key = "surname_reverse_index_v3"
    cached = get(key)
    if cached:
        print("[DEBUG] reverse_index loaded from cache")
        return cached

    data = _load_json("reverse_index_v3.json")
    set(key, data)
    return data

# surname_full_v3.json（フル姓辞書）
def load_full():
    print("[DEBUG] load_full called")
    key = "surname_full_v3"
    cached = get(key)
    if cached:
        print("[DEBUG] full loaded from cache")
        return cached

    data = _load_json("surname_full_v3.json")
    set(key, data)
    return data
