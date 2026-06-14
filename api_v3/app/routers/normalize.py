from fastapi import APIRouter
from app.services.search_engine import normalize_query

router = APIRouter()

@router.get("/normalize")
def normalize(q: str):
    """
    入力文字列 q をローマ字・読み・漢字の3方向で正規化して返す
    - normalize_query は v3 の normalize_romaji / yomi / kanji を統合
    - canonical + variants をすべて返す
    """
    normalized = list(normalize_query(q))
    return {
        "input": q,
        "normalized": normalized
    }
