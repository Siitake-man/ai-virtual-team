# Jules向け指示書 (2026-07-05)

## 🎯 目的
AI Virtual Team BuilderのPhase 1実装が完了しました（ユーザーの動作検証待ち）。
Julesには、実装されたPythonコードの静的解析（Linting/Type Checking）と、コードフォーマットの整理をお願いします。

## ⚙️ 環境と技術スタック
- **Python**: 3.13
- **主要ライブラリ**: FastAPI, Streamlit, google-genai (v2.x), Pydantic (v2)
- **環境構築**: `.venv/Scripts/activate` -> `pip install -r requirements.txt`

## 📋 依頼タスク（優先順位順）

1. **コードの静的解析とフォーマット修正**
   - 以下のディレクトリ内のPythonファイルを対象に、型の不一致や未使用インポートの削除、フォーマット（PEP 8準拠）を行ってください。
     - `app/api/routers/` (`projects.py`, `employees.py`, `chat.py`)
     - `app/services/` (`llm_service.py`)
     - `app/repositories/` (`json_repository.py`)
     - `app/models/schemas.py`
     - `app/api_client.py`

2. **Docstringの補完**
   - パブリックな関数やクラスに、日本語のDocstring（役割、引数、戻り値の説明）が欠けている場合は追加してください。

3. **`any` 型の排除（可能な場合）**
   - 型注釈に `any` や `Any` が使われている箇所があれば、より厳密な型（`Dict[str, str]` や Pydanticのモデル）に置き換えてください。

## ⚠️ 禁止事項
- `run.ps1` などの起動スクリプトの自動実行はしないでください（ハングアップの原因となります）。
- `data/projects/` 配下のユーザーデータファイルは絶対に削除・変更しないでください。
- APIキー等の認証情報の書き換えは行わないでください。

## 🔄 成果物の引き継ぎ
作業が完了したら、`docs/handover/jules_handover_20260705.md` を作成し、実行した内容（フォーマット修正箇所のサマリーや、発見した静的解析上の潜在的バグなど）をまとめてPull Requestを作成してください。
