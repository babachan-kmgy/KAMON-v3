from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ルーター
from app.routers import normalize, search

app = FastAPI(
    title="KAMON API v3",
    description="Surname normalization + search + reading API",
    version="3.0.0",
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録（これが最重要）
app.include_router(normalize.router)
app.include_router(search.router)


@app.get("/")
def root():
    return {"message": "KAMON API v3 is running"}
