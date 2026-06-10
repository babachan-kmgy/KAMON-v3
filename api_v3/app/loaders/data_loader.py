import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SURNAME_DIR = os.path.join(BASE_DIR, "data", "surname")

def load_public_surname():
    path = os.path.join(SURNAME_DIR, "canonical.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_variant_map():
    path = os.path.join(SURNAME_DIR, "variants.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_reading_dict():
    path = os.path.join(SURNAME_DIR, "reading.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
