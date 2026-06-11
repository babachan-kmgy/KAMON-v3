import json
import os

# ---------------------------------------------------------
# 正しい辞書パス（api_v3/data/）
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "surname")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_public_surname():
    return load_json("public_surname_v3.json")


def load_public_reverse():
    return load_json("public_reverse_index_v3.json")


def load_variant_map():
    return load_json("variant_map_v3.json")
