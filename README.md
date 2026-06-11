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
```
KAMON-v3/
    api_v3/             # FastAPI application (includes normalize_dv3/)
    dictionaries_v3/    # Legacy dictionary data (v3 optimized files are placed in api_v3/data/)
    tools_dv3/          # Utility tools for dictionary generation & benchmarking
    ui/                 # Simple search UI
    tests_dv3/          # Test suite
    README.md
    README_ja.md
    requirements.txt
```
🧩 API Overview
Run the API
```bash
uvicorn api_v3.app.main:app --reload
```
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
Located in tools_dv3/:
* `convert_canonical.py`
* `generate_reading_dict.py`
* `validate_v3.py`
* `benchmark.py` (Search performance benchmarking)

🧪 Tests

#### 1. Unit Tests (pytest)
To run API functionality and normalization logic tests:
```bash
# Activate virtual environment, then run:
pytest tests_dv3/

# Run with stdout logging enabled:
pytest -s tests_dv3/
```

#### 2. Load Tests (Locust)
To run load tests against the API:
```bash
# With the API running (at http://localhost:8000), execute:
locust -f locustfile.py -H http://localhost:8000

# Open http://localhost:8089 in your browser to configure and launch the load test.
```
🛠 Development
Example requirements.txt
```
fastapi
uvicorn
pydantic
python-Levenshtein
locust
pytest
```
📄 License
To be added.

🙌 Acknowledgements
KAMON‑v3 aims to provide a reproducible, transparent, and accurate foundation for Japanese surname processing.