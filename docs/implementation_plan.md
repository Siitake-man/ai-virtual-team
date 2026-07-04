# AI Virtual Team Builder - Phase 1 実装計画 (基盤構築)

## 目的
AI Virtual Team Builderのコアとなるデータ永続化（JSON）、バックエンドAPI（FastAPI）、フロントエンドUI（Streamlit）、および個別チャット機能を構築し、アプリの土台を完成させる。

## 前提: 起動アーキテクチャ
- **FastAPI**: `http://localhost:8000` で起動（APIサーバー）
- **Streamlit**: `http://localhost:8501` で起動（UIサーバー）
- 2プロセスを同時起動する必要がある。環境変数 `API_BASE_URL=http://localhost:8000` でStreamlitからAPIの向き先を制御する。
- **Windows対応**: `.bat`（コマンドプロンプト用）と `.ps1`（PowerShell用）の両方を提供する。

---

## 実装ステップ

### Step 1: ディレクトリ構築 + 依存関係定義 + Windows用起動スクリプト
- **成果物（確認基準）**: `streamlit run app/main.py` で空のStreamlit画面が起動する
- **対象ファイル**: 
  - `requirements.txt` — 全依存ライブラリの定義
  - `.env.example` — APIキー・設定項目のテンプレート
  - `setup.ps1` / `setup.bat` — 仮想環境作成 + pip install
  - `run.ps1` / `run.bat` — FastAPI + Streamlitの並行起動
  - `app/main.py` — Streamlitエントリーポイント（空のスケルトン）
  - `app/api/main.py` — FastAPIエントリーポイント（空のスケルトン）
  - 各ディレクトリの `__init__.py`

### Step 2: Pydanticスキーマ + JSONリポジトリ層
- **成果物（確認基準）**: テスト用スクリプトでJSONのデータ読み書きが確認できる
- **対象ファイル**: 
  - `app/models/schemas.py` — Project・Employee・OwnerContext等のPydanticモデル定義
  - `app/repositories/json_repository.py` — `data/projects/{id}.json` に対するCRUD操作クラス（将来のSupabase移行を想定したインターフェース設計）

### Step 3: FastAPI サーバー + プロジェクトCRUD API
- **成果物（確認基準）**: `http://localhost:8000/docs` のSwagger UIでAPIが確認できる
- **対象ファイル**: 
  - `app/api/routers/projects.py` — `/api/v1/projects` の一覧取得・新規作成・詳細取得・削除
  - `app/api/routers/employees.py` — `/api/v1/projects/{id}/employees` の追加・更新・削除
  - `app/api/main.py` — ルーター登録・CORS設定

### Step 4: StreamlitサイドバーUI + 従業員管理タブ
- **成果物（確認基準）**: ブラウザでプロジェクト作成・従業員追加・削除が操作できる
- **対象ファイル**: 
  - `app/main.py` — サイドバー（プロジェクト選択・新規作成）+ 「従業員管理」タブ（一覧表示・追加ダイアログ・アクティブ切替）
  - `app/api_client.py` — StreamlitからFastAPI呼び出しを行うユーティリティ（`API_BASE_URL`環境変数を参照）

### Step 5: LLMサービス + 個別チャットタブ
- **成果物（確認基準）**: 実際に従業員と会話でき、会話履歴がJSONに永続化されるのが確認できる
- **対象ファイル**: 
  - `app/services/llm_service.py` — Gemini APIを呼び出し、人格プロンプトをシステムプロンプトとして適用。LLMモデルを環境変数で切り替え可能。
  - `app/api/routers/chat.py` — `/api/v1/projects/{id}/employees/{emp_id}/chat` のメッセージ送受信・履歴取得
  - `app/main.py` — 「個別チャット」タブに `st.chat_message` UIを実装
