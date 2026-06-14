[日本語版 READMEはこちら](README_ja.md)

# KAMON‑v3 — Japanese Surname Dictionary & RAG API

KAMON‑v3 is an open‑source project that provides a fast Japanese surname dictionary API,  
combined with a Retrieval‑Augmented Generation (RAG) system for generating concise explanations.

This version is a complete redesign of previous releases (v1 / v2),  
featuring a new dictionary structure, improved search engine, and a lightweight web UI.

---

## ✨ Features

### 🔍 1. High‑performance surname search API
- Endpoint: `/api_v3/search?query=sato`
- Uses the public dictionary `public_surname_v3.json`
- Supports partial matching

### 🧠 2. RAG‑based explanation generation
- Endpoint: `/api_v3/rag?query=sato`
- Vector‑based similar‑surname retrieval
- LLM‑generated brief explanations

### 🖥 3. Web UI (ui_v3)
- Simple browser‑based interface
- Displays search results, similar surnames, and explanations
- Fully local and lightweight

### 📚 4. Public dictionary (public_surname_v3.json)
Dictionary format:

{
"SN000001": { "kanji": "佐藤", "yomi": "さとう", "romaji": "sato" },
"SN000002": { "kanji": "鈴木", "yomi": "すずき", "romaji": "suzuki" }
}

コード

The API converts this key‑value structure into a list internally.

---

## 📦 Directory Structure

api_v3/            → FastAPI-based search API
rag_v3/            → Similar surname search + RAG explanation
ui_v3/             → Web UI (HTML / CSS / JS)
dictionaries_v3/   → Public dictionary files
docs/              → Technical documentation

コード

---

## 🚀 Getting Started

### 1. Start the RAG API (port 8010)
cd rag_v3
python rag_api.py

コード

### 2. Start the main API + UI (port 8011)
cd api_v3/app
python main.py

コード

### 3. Open the UI
http://127.0.0.1:8011/

コード

---

## 📄 License
MIT License

---

## 🏛 Project Goals

- Provide a structured, open Japanese surname dictionary  
- Preserve historical and cultural information  
- Support researchers, developers, and genealogical projects  
- Future integration with Japanese family crest (家紋) datasets

---

## 🙏 Acknowledgements
This project is supported by contributors interested in Japanese linguistics,  
historical preservation, and open cultural datasets.
