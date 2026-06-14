import os
import json

# ---------------------------------------------------------
#  内部辞書（full）を参照するための固定パス
# ---------------------------------------------------------
DICT_PATH = r"C:\KAMON\GitHub\KAMON-dictionary-archive\v3\surname_full_v3.json"

# 辞書読み込み
with open(DICT_PATH, "r", encoding="utf-8") as f:
    full_dict = json.load(f)

# stable_id → 辞書データ の高速参照
dict_by_id = {item["stable_id"]: item for item in full_dict}


# ---------------------------------------------------------
#  簡潔説明文生成（A3スタイル）
# ---------------------------------------------------------
def generate_brief_description(main_item, similar_items):
    """
    A3（簡潔スタイル）向けの説明文を生成する。
    main_item: 主姓（辞書データ）
    similar_items: 類似姓（rag_search.py の結果）
    """

    kanji = main_item.get("canonical_kanji", "")
    yomi = main_item.get("canonical_yomi", "")
    romaji = main_item.get("canonical_romaji", "")
    variants = main_item.get("kanji_variants", [])
    stable_id = main_item.get("stable_id", "")

    # 類似姓（最大3件）
    similar_kanji = [item["kanji"] for item in similar_items[:3]]

    # --- 説明文（簡潔スタイル） ---
    description = f"{kanji}（{yomi}）は日本の姓である。"

    # 異体字
    if variants:
        description += f"異体字として「{ '、'.join(variants[:3]) }」がある。"

    # 類似姓
    if similar_kanji:
        description += f"類似する姓には「{ '、'.join(similar_kanji) }」などがある。"

    # --- 付加情報 ---
    result = {
        "kanji": kanji,
        "yomi": yomi,
        "romaji": romaji,
        "stable_id": stable_id,
        "description": description,
        "variants": variants,
        "similar_surnames": similar_kanji
    }

    return result


# ---------------------------------------------------------
#  テスト実行（直接実行時のみ）
# ---------------------------------------------------------
if __name__ == "__main__":
    # テスト用に rag_search を呼び出す
    from rag_search import search_similar_surnames

    q = input("姓を入力してください：")
    similar = search_similar_surnames(q)

    if not similar:
        print("該当する姓が見つかりませんでした。")
        exit()

    # 主姓（最も類似度が高いもの）
    main_id = similar[0]["stable_id"]
    main_item = dict_by_id.get(main_id)

    result = generate_brief_description(main_item, similar)

    print("\n--- 説明文 ---")
    print(result["description"])

    print("\n--- 類似姓 ---")
    for s in result["similar_surnames"]:
        print(s)

    print("\n--- 異体字 ---")
    print("、".join(result["variants"]))
