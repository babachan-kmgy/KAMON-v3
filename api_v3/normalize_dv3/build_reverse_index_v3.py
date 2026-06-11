import json
import os

INPUT_PATH = os.path.join(os.path.dirname(__file__), "variant_map_v3.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "reverse_index_v3.json")


def load_variant_map():
    with open(INPUT_PATH, encoding="utf-8") as f:
        return json.load(f)


def build_reverse_index():
    variant_map = load_variant_map()
    reverse_index = {}

    for key, stable_id in variant_map.items():
        if stable_id not in reverse_index:
            reverse_index[stable_id] = []

        reverse_index[stable_id].append(key)

    # 各 stable_id のキーをソートして重複排除
    for sid in reverse_index:
        reverse_index[sid] = sorted(list(set(reverse_index[sid])))

    # 保存
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(reverse_index, f, ensure_ascii=False, indent=2)

    print(f"✓ reverse_index_v3.json を生成しました（{len(reverse_index)} 件）")


if __name__ == "__main__":
    build_reverse_index()
