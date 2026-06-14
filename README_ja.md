# KAMON-v3 — Japanese Surname Dictionary + RAG API

KAMON-v3 は、日本の姓データを扱うための **高速辞書 API** と  
**RAG（Retrieval-Augmented Generation）による説明生成** を備えた  
オープンソースの日本語姓辞書プロジェクトです。

本リポジトリは、過去バージョン（v1 / v2）から構造を全面刷新し、  
より正確で拡張性の高い “新しい公開ライン” として設計されています。

---

## ✨ Features

### 🔍 1. 高速姓検索 API
- `/api_v3/search?query=佐藤`
- 公開辞書 `public_surname_v3.json` を使用
- 部分一致検索に対応

### 🧠 2. RAG による説明生成
- `/api_v3/rag?query=佐藤`
- 類似姓検索（ベクトル検索）
- LLM による簡潔な説明文生成

### 🖥 3. Web UI（ui_v3）
- ブラウザで姓検索が可能
- 類似姓と説明文を表示
- ローカルで動作する軽量 UI

### 📚 4. 公開辞書（public_surname_v3.json）
- Key-Value 形式  
{
"SN000001": { "kanji": "佐藤", "yomi": "さとう", "romaji": "sato" },
...
}

コード
- API 内で list 形式に変換して利用

---

## 📦 Directory Structure

api_v3/        → FastAPI ベースの検索 API
rag_v3/        → 類似姓検索 + 説明生成（RAG）
ui_v3/         → Web UI（HTML / CSS / JS）
dictionaries_v3/ → 公開辞書
docs/          → 技術資料

コード

---

## 🚀 Getting Started

### 1. RAG API を起動（ポート 8010）
cd rag_v3
python rag_api.py

コード

### 2. メイン API + UI を起動（ポート 8011）
cd api_v3/app
python main.py

コード

### 3. ブラウザでアクセス
http://127.0.0.1:8011/

コード

---

## 📄 License
MIT License

---

## 🏛 Project Goals

- 日本の姓データの体系化  
- 歴史的・文化的情報の保存  
- 研究者・開発者が利用できるオープンな基盤の提供  
- 将来的には家紋データとの統合も視野に入れる

---

## 🙏 Acknowledgements
本プロジェクトは、日本語辞書・家紋研究・歴史資料の保存に関心を持つ  
すべての人々の協力によって支えられています。
