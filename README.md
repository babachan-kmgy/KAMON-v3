[日本語版 README](README_ja.md)

KAMON‑v3 — Japanese Surname Normalization & Dictionary API
KAMON‑v3 is a comprehensive system for processing Japanese surnames, providing:

Variant normalization (unifying different kanji forms)

Reading estimation (kana & romaji)

Reverse index search

FastAPI-based API

Reproducible dictionary build pipeline

Lightweight public dictionary set

This repository contains the public release of the KAMON‑v3 system.

🚀 Features
1. Variant Normalization
Unifies variant kanji forms such as:

髙橋 → 高橋

渡邉 → 渡辺

齋藤 → 斎藤

2. Reading Estimation
Generates:

Hiragana

Katakana

Romaji (Hepburn)

3. Reverse Index Search
Supports:

Reading → Surname

Romaji → Surname

Variant → Canonical form

4. Fully Synchronized API & Dictionaries
The API always reflects the latest dictionary build.

5. v3 Improvements
Fully redesigned normalization rules

Stable ID structure

Public & full dictionary separation

Rebuildable pipeline via normalize/

Utility tools for validation & generation

📁 Repository Structure
コード
KAMON-v3/
    api/                # FastAPI application
    dictionaries/       # v3 dictionary data
    normalize/          # Normalization rules & build scripts
    tools/              # Utility tools
    ui/                 # Simple search UI
    tests/              # Test suite
    README.md
    README_ja.md
    requirements.txt
🧩 API Overview
Run the API
コード
uvicorn api.app.main:app --reload
Main Endpoints
Method	Path	Description
GET	/normalize	Normalize variant kanji
GET	/search	Search surnames
GET	/variants	List variant forms
GET	/reverse	Reverse index search


📚 Dictionaries
public_surname_v3.json
Lightweight public dictionary.

surname_full_v3.json
Full internal dictionary.

variant_map_v3.json
Variant → canonical mapping.

reverse_index_v3.json
Reading → surname mapping.

🔧 Tools
Located in tools/:

convert_canonical.py

generate_reading_dict.py

validate_v3.py

🧪 Tests
Run:

コード
pytest tests/
🛠 Development
Example requirements.txt
コード
fastapi
uvicorn
pydantic
python-Levenshtein
📄 License
To be added.

🙌 Acknowledgements
KAMON‑v3 aims to provide a reproducible, transparent, and accurate foundation for Japanese surname processing.