from fastapi import APIRouter
from app.services.search_engine import search_by_query

router = APIRouter(prefix="/search")

@router.get("")
def search(q: str):
    """
    名字検索 API（V3 完全版）
    - 正規化（漢字・読み・ローマ字）
    - variant_map_v3 による揺れ吸収
    - stable_id ベースで public_surname_v3.json を返す
    """
    return search_by_query(q)
