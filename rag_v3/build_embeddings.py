import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np

# ---------------------------------------------------------
#  内部辞書（full）を参照するための固定パス
#  ※ 公開用辞書（release_v3/dictionaries_v3）は使わない
# ---------------------------------------------------------
DICT_PATH = r"C:\KAMON\GitHub\KAMON-dictionary-archive\v3\surname_full_v3.json"

# rag_v3 内のパス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DIR = os.path.join(BASE_DIR, "vector_store")
META_DIR = os.path.join(BASE_DIR, "embeddings")

os.makedirs(VECTOR_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

# 軽量で高速な埋め込みモデル
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def build_text(item):
    """
    A3（簡潔スタイル）向けの文章化。
    canonical + yomi + variants を短くまとめる。
    """
    kanji = item.get("canonical_kanji", "")
    yomi = item.get("canonical_yomi", "")
    variants = item.get("kanji_variants", [])

    # variants は最大5件だけ使う（簡潔にするため）
    variants_text = "、".join(variants[:5]) if variants else "なし"

    text = f"{kanji}。読み：{yomi}。異体字：{variants_text}。"
    return text

def main():
    print("Loading dictionary...")
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = []
    ids = []

    print("Building text entries...")
    for item in data:
        stable_id = item.get("stable_id")
        if not stable_id:
            continue

        text = build_text(item)
        texts.append(text)
        ids.append(stable_id)

    print(f"Encoding {len(texts)} entries...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # ベクトル保存
    vec_path = os.path.join(VECTOR_DIR, "surname_vectors.npy")
    np.save(vec_path, embeddings)

    # ID 保存
    id_path = os.path.join(META_DIR, "surname_ids.json")
    with open(id_path, "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False, indent=2)

    print("Done.")
    print(f"Saved vectors to: {vec_path}")
    print(f"Saved IDs to: {id_path}")

if __name__ == "__main__":
    main()
