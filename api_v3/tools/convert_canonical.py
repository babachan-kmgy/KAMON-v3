import json
import os

BASE = os.path.join("data", "surname")
SRC = os.path.join(BASE, "canonical.json")

with open(SRC, "r", encoding="utf-8") as f:
    arr = json.load(f)

# arr は list のはず
new_dict = {}

for item in arr:
    kanji = item["kanji"]
    new_dict[kanji] = item

with open(SRC, "w", encoding="utf-8") as f:
    json.dump(new_dict, f, ensure_ascii=False, indent=2)

print("canonical.json converted to dict format.")
