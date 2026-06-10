from fastapi import APIRouter
from app.services.search.engine import search_surname

# ルーターに prefix を付けることで、URL が二重にならない
router = APIRouter(prefix="/search")

@router.get("")
def search(q: str):
    """
    名字検索 API（V3 最適構造版）
    - 正規化は engine 側で実施
    - variant 展開 → scorer → 読み統合 → 結果整形
    """
    return search_surname(q)
