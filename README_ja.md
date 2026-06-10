KAMON‑v3 — 日本の姓データ 正規化・辞書・検索 API
KAMON‑v3 は、日本の姓データを
正規化・異体字統合・読み推定・ローマ字変換・逆引き検索  
まで一貫して処理できる最新版の辞書・API システムです。

本リポジトリは、KAMON‑v3 の 公開版 を含みます。

🚀 特徴
1. 異体字の統合（Variant Normalization）
例：

髙橋 → 高橋

渡邉 → 渡辺

齋藤 → 斎藤

2. 読み（よみ）の推定
ひらがな

カタカナ

ローマ字（ヘボン式）

を自動生成。

3. 逆引き検索（Reverse Index）
読み → 姓

ローマ字 → 姓

異体字 → 正字

などの検索が可能。

4. API と辞書が完全同期
辞書の更新は API に即時反映される構造。

5. v3 の改善点
正規化ルールを全面刷新

安定した ID 体系

公開用と内部用の辞書を分離

normalize/ による再構築可能なパイプライン

tools/ による辞書生成ツール群

📁 リポジトリ構成
コード
KAMON-v3/
    api/                # FastAPI アプリケーション
    dictionaries/       # v3 辞書データ
    normalize/          # 正規化ルール & ビルドスクリプト
    tools/              # ユーティリティツール
    ui/                 # 簡易検索 UI
    tests/              # テストコード
    README.md
    README_ja.md
    requirements.txt
🧩 API 概要
起動方法
コード
uvicorn api.app.main:app --reload
主なエンドポイント
Method	Path	説明
GET	/normalize	異体字 → 正字の正規化
GET	/search	姓の検索
GET	/variants	異体字一覧
GET	/reverse	読み → 姓の逆引き


📚 辞書データ
public_surname_v3.json
公開用の軽量辞書。

surname_full_v3.json
内部用の完全版辞書。

variant_map_v3.json
異体字 → 正字のマッピング。

reverse_index_v3.json
読み → 姓の逆引き。

🔧 ツール
tools/ には辞書生成・検証ツールが含まれます。

例：

convert_canonical.py

generate_reading_dict.py

validate_v3.py

🧪 テスト
コード
pytest tests/
🛠 開発
requirements.txt（例）
コード
fastapi
uvicorn
pydantic
python-Levenshtein
📄 ライセンス
後日追加予定。

🙌 謝辞
KAMON‑v3 は、日本の姓データの正規化・統合・検索を
より正確かつ再現性のある形で提供することを目的としています。