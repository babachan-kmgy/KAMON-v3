import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------
#  内部辞書（full）を参照するための固定パス
# ---------------------------------------------------------
DICT_PATH = r"C:\KAMON\GitHub\KAMON-dictionary-archive\v3\surname_full_v3.json"

# rag_v3 内のパス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_PATH = os.path.join(BASE_DIR, "vector_store", "surname_vectors.npy")
ID_PATH = os.path.join(BASE_DIR, "embeddings", "surname_ids.json")

# モデル（MiniLM-L6）
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ---------------------------------------------------------
#  データ読み込み
# ---------------------------------------------------------
print("Loading vectors and IDs...")
vectors = np.load(VECTOR_PATH)

with open(ID_PATH, "r", encoding="utf-8") as f:
    stable_ids = json.load(f)

with open(DICT_PATH, "r", encoding="utf-8") as f:
    full_dict = json.load(f)

# stable_id → 辞書データ の高速参照
dict_by_id = {item["stable_id"]: item for item in full_dict}


# ---------------------------------------------------------
#  類似姓検索（semantic search）
# ---------------------------------------------------------
def search_similar_surnames(query, top_k=5):
    """
    入力された姓に対して、semantic search で類似姓を返す。
    自分自身（完全一致 stable_id）は除外する。
    """

    # クエリを埋め込みに変換
    query_vec = model.encode([query])

    # 類似度計算（cosine similarity）
    sims = cosine_similarity(query_vec, vectors)[0]

    # まず最も似ている stable_id を取得（＝自分自身の可能性が高い）
    # 完全一致の stable_id を取得するために、辞書を検索
    query_stable_id = None
    for sid, item in dict_by_id.items():
        if item.get("canonical_kanji") == query:
            query_stable_id = sid
            break

    # 自分自身を除外したリストを作成
    filtered = []
    for idx, sid in enumerate(stable_ids):
        if sid == query_stable_id:
            continue  # 自分自身を除外
        filtered.append((idx, sims[idx]))

    # 類似度順にソート
    filtered = sorted(filtered, key=lambda x: x[1], reverse=True)

    # 上位 top_k を取得
    top_idx = [idx for idx, _ in filtered[:top_k]]

    results = []
    for idx in top_idx:
        sid = stable_ids[idx]
        item = dict_by_id.get(sid)

        if not item:
            continue

        results.append({
            "stable_id": sid,
            "kanji": item.get("canonical_kanji", ""),
            "yomi": item.get("canonical_yomi", ""),
            "romaji": item.get("canonical_romaji", ""),
            "variants": item.get("kanji_variants", []),
            "similarity": float(sims[idx])
        })

    return results


# ---------------------------------------------------------
#  テスト実行（直接実行時のみ）
# ---------------------------------------------------------
if __name__ == "__main__":
    q = input("姓を入力してください：")
    res = search_similar_surnames(q)

    print("\n--- 類似姓（自分自身除外済） ---")
    for r in res:
        print(f"{r['kanji']}（{r['yomi']}）  score={r['similarity']:.3f}")
