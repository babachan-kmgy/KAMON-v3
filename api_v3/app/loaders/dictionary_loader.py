import json
import os

# ---------------------------------------------------------
# KAMON v3 辞書ローダー（TB 環境用 完全版）
# ---------------------------------------------------------

# v3 辞書ディレクトリ（TB の環境に合わせた絶対パス）
DATA_DIR = r"C:\KAMON\GitHub\release_v3\dictionaries_v3"

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# 公開用姓辞書
def load_public_surname():
    return load_json("public_surname_v3.json")

# 公開用逆引き辞書
def load_public_reverse():
    return load_json("public_reverse_index_v3.json")

# 異体字マップ
def load_variant_map():
    return load_json("variant_map_v3.json")

# フル姓辞書（API 内部用）
def load_full_surname():
    return load_json("surname_full_v3.json")

# 読み辞書
def load_reading():
    return load_json("surname_reading_v3.json")

# canonical.json（正規化用）
def load_canonical():
    return load_json("canonical.json")
