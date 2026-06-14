from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import json
import sys

# ---------------------------------------------------------
#  v3 公開辞書（public_surname_v3.json）
#  ※ この辞書は「辞書形式」なので、リストに変換する
# ---------------------------------------------------------
DICT_PATH = r"C:\KAMON\GitHub\release_v3\dictionaries_v3\public_surname_v3.json"

with open(DICT_PATH, "r", encoding="utf-8") as f:
    surname_dict_raw = json.load(f)

# surname_dict_raw は {"SN000001": {...}, ...} 形式
# → リスト形式に変換する
surname_dict = []
for stable_id, item in surname_dict_raw.items():
    surname_dict.append({
        "stable_id": stable_id,
        "canonical_kanji": item.get("kanji", ""),
        "canonical_yomi": item.get("yomi", ""),
        "canonical_romaji": item.get("romaji", "")
    })

# ---------------------------------------------------------
#  rag_v3 を import 可能にする
# ---------------------------------------------------------
sys.path.append(r"C:\KAMON\GitHub\release_v3\rag_v3")

from rag_search import search_similar_surnames
from rag_answer import generate_brief_description, dict_by_id

# ---------------------------------------------------------
#  FastAPI アプリ本体
# ---------------------------------------------------------
app = FastAPI(
    title="KAMON v3 API",
    description="KAMON v3 surname dictionary + RAG",
    version="3.0.0"
)

# ---------------------------------------------------------
#  UI（ui_v3）を公開
# ---------------------------------------------------------
UI_DIR = r"C:\KAMON\GitHub\release_v3\ui_v3"

app.mount("/ui_v3", StaticFiles(directory=UI_DIR), name="ui_v3")

@app.get("/", response_class=HTMLResponse)
def root():
    index_path = os.path.join(UI_DIR, "index_v3.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------------------------------------
#  /api_v3/search?query=佐藤
# ---------------------------------------------------------
@app.get("/api_v3/search")
def search_endpoint(query: str = Query(...)):
    query = query.strip()
    if not query:
        return JSONResponse({"error": "query が空です"}, status_code=400)

    # canonical_kanji に部分一致
    results = [
        item for item in surname_dict
        if query in item["canonical_kanji"]
    ]

    return JSONResponse(results, status_code=200)

# ---------------------------------------------------------
#  /api_v3/rag?query=佐藤
# ---------------------------------------------------------
@app.get("/api_v3/rag")
def rag_endpoint(query: str = Query(...)):
    query = query.strip()
    if not query:
        return JSONResponse({"error": "query が空です"}, status_code=400)

    similar = search_similar_surnames(query)
    if not similar:
        return JSONResponse({"error": "該当する姓が見つかりませんでした"}, status_code=404)

    main_id = similar[0]["stable_id"]
    main_item = dict_by_id.get(main_id)

    if not main_item:
        return JSONResponse({"error": "辞書データが見つかりません"}, status_code=500)

    result = generate_brief_description(main_item, similar)
    return JSONResponse(result, status_code=200)

# ---------------------------------------------------------
#  ローカル実行（8011）
# ---------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8011)
