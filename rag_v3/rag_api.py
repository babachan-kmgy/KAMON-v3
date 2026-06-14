from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn
import os
import json

# rag_search / rag_answer を読み込む
from rag_search import search_similar_surnames
from rag_answer import generate_brief_description, dict_by_id

app = FastAPI(
    title="KAMON v3 RAG API",
    description="辞書ベース RAG（簡潔スタイル）API",
    version="1.0.0"
)

# ---------------------------------------------------------
#  /api_v3/rag?query=佐藤
# ---------------------------------------------------------
@app.get("/api_v3/rag")
def rag_endpoint(query: str = Query(..., description="姓を入力")):
    """
    RAG による説明文生成 API。
    """
    query = query.strip()
    if not query:
        return JSONResponse({"error": "query が空です"}, status_code=400)

    # 類似姓検索
    similar = search_similar_surnames(query)
    if not similar:
        return JSONResponse({"error": "該当する姓が見つかりませんでした"}, status_code=404)

    # 主姓（最も類似度が高いもの）
    main_id = similar[0]["stable_id"]
    main_item = dict_by_id.get(main_id)

    if not main_item:
        return JSONResponse({"error": "辞書データが見つかりません"}, status_code=500)

    # 説明文生成
    result = generate_brief_description(main_item, similar)

    return JSONResponse(result, status_code=200)


# ---------------------------------------------------------
#  ローカル実行用
# ---------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8010)
