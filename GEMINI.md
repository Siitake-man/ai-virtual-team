# GEMINI.md — AI Virtual Team Builder
# Google Antigravity エージェント設定ファイル
# このファイルをプロジェクトルートに配置してください

---

## 基本ルール

- 常に日本語で回答してください。
- 結論ファーストで前置きを省いてください。
- コードを書く前に必ず`implementation_plan.md`を生成し、ユーザーの承認を得てから実装を開始してください（Planning Modeを使用）。
- `SPEC.md`に記載された仕様を厳守してください。仕様にない機能を勝手に追加しないこと。

---

## プロダクトビジョン

どんなプロジェクトにも使える**汎用AI従業員チームビルダー**を構築する。

「知識を入れるだけのAI」ではなく、役割・人格・思考スタイル・プロジェクトの魂を持つ仮想従業員チームを誰でも5分で作れるツール。

---

## 技術スタック（確定・変更禁止）

```yaml
frontend: Streamlit（ローカル優先）
backend: FastAPI（Python）
data: JSONファイル（./data/projects/配下）
llm:
  - Gemini 2.0 Flash（デフォルト）
  - Claude Sonnet 4.5
  - GPT-4o
github_lib: PyGithub
env_management: python-dotenv
```

---

## ディレクトリ構成

```
ai-virtual-team/
├── GEMINI.md               ← このファイル
├── SPEC.md                 ← 仕様書（必ず読むこと）
├── .env.example            ← 配布用テンプレート
├── .env                    ← 実際のAPIキー（gitignore対象）
├── setup.ps1               ← 依存関係インストール（PowerShell用）
├── setup.bat               ← 依存関係インストール（コマンドプロンプト用）
├── run.ps1                 ← FastAPI + Streamlit 並行起動（PowerShell用）
├── run.bat                 ← FastAPI + Streamlit 並行起動（コマンドプロンプト用）
├── README.md               ← セットアップ手順
├── requirements.txt        ← Python依存ライブラリ定義
├── app/
│   ├── main.py             ← Streamlitエントリーポイント
│   ├── api_client.py       ← StreamlitからFastAPIを呼ぶユーティリティ（API_BASE_URL参照）
│   ├── api/
│   │   ├── main.py         ← FastAPIエントリーポイント（ポート8000）
│   │   └── routers/
│   │       ├── projects.py
│   │       ├── employees.py
│   │       ├── chat.py
│   │       └── github.py
│   ├── services/
│   │   ├── llm_service.py      ← LLM API呼び出しの抽象化
│   │   ├── github_service.py   ← GitHub連携
│   │   └── persona_generator.py ← 人格自動生成ロジック
│   ├── repositories/
│   │   └── json_repository.py  ← データ永続化（将来Supabase移行可能な設計）
│   └── models/
│       └── schemas.py          ← Pydanticモデル定義
├── data/
│   ├── projects/           ← プロジェクトJSONファイル
│   └── presets/
│       └── npo-trust-platform.json  ← 初期プリセット
└── exports/                ← Markdownエクスポート出力先
```

---

## 実装フェーズ（この順序で実装すること）

### Phase 1: 基盤構築（最初に実装）
1. ディレクトリ構築 + `requirements.txt` + Windows用起動スクリプト（`.ps1`/`.bat`）
2. Pydanticスキーマ + JSONリポジトリ層
3. FastAPIサーバー + プロジェクト・従業員 CRUD API
4. StreamlitサイドバーUI + 従業員管理タブ（`api_client.py`経由でAPIと連携）
5. LLMサービス + 個別チャットタブ（会話履歴のJSON永続化）

### Phase 2: コア機能（Phase 1完了後）
5. 人格自動生成機能（オーナー設定 + 属性 → 人格プロンプト自動生成）
6. 知識ストック管理（Markdown・テキスト・URL・GitHubファイル）
7. GitHub連携（ファイルツリー表示 + チェックボックス選択）
8. 全員同時レビュー（並列LLM呼び出し + タブ表示）

### Phase 3: 仕上げ
9. 統合サマリー生成（全員のレビュー結果をまとめる）
10. Markdownエクスポート
11. NPO Trust Platformプリセットの同梱
12. README.md（社内配布用セットアップ手順）

---

## 重要な設計制約（変更禁止）

- データ層は`repositories/`に抽象化し、JSONとSupabaseを切り替え可能にすること
- LLM呼び出しは`llm_service.py`に集約し、モデルを環境変数で切り替え可能にすること
- FastAPIのエンドポイントは`/api/v1/`プレフィックスで統一すること
- 会話履歴はプロジェクトJSONに保存し、セッションをまたいで継続できること
- `.env`ファイルにAPIキーを記載し、`.env.example`には値を入れずキー名のみ記載すること

---

## .env.example の内容

```
# LLM API Keys（使用するモデルのキーのみ設定）
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# GitHub
GITHUB_TOKEN=your_github_personal_access_token_here

# Default Settings
DEFAULT_LLM_MODEL=gemini-2.0-flash
OWNER_NAME=your_name_here

# API Server（StreamlitからFastAPIへのリクエスト先）
API_BASE_URL=http://localhost:8000
```

---

## 人格自動生成のプロンプトテンプレート

```python
PERSONA_GENERATION_PROMPT = """
以下の情報をもとに、この従業員の「人格プロンプト（カスタム指示）」を日本語で生成してください。

## オーナー情報
- 名前: {owner_name}
- プロジェクトへの動機・背景: {motivation}
- ビジョン（5年後の目標）: {vision}
- 大切にしている価値観・判断基準: {values}
- 絶対にやってはいけないこと: {ng_items}

## この従業員の設定
- 名前: {employee_name}
- 属性: {attribute}
- 専門領域: {specialty}

## 生成する人格プロンプトに含めるべき要素
1. あなたの役割（この従業員が何者か）
2. あなたが仕える相手（オーナー）の思考・価値観・目標
3. 口調・態度（プロフェッショナルかつ誠実。専門用語は必ず一言で補足）
4. 思考スタイル（属性に応じた思考パターン）
5. 行動指針（受け身ではなく先回り、結論ファースト、次の一手を必ず示す）
6. 情報不足時の対応（逆質問で確認する）

## 属性別の思考スタイル指示
- クリティカル: 最悪ケース・リスク・設計の穴を先に提示する。「なぜ失敗するか」を教える。希望的観測を排除する。
- ドリーマー: 制約を無視して可能性を最大化する。熱量を増幅させる。「もっとこうできる」を教える。現実的かどうかは問わない。
- リアリスト: 工数・優先順位・実行可能性を判断する。クリティカルとドリーマーの橋渡しをする。「では具体的にどうするか」を教える。
- 専門家: 自分の専門領域のファクトに基づいて回答する。推論と事実を明確に区別する。

人格プロンプトのみを出力してください。説明文は不要です。
"""
```

---

## 禁止事項

- `SPEC.md`に記載されていない機能の勝手な追加
- APIキーのコードへのハードコーディング
- 会話履歴のセッション限りの保存（必ずJSONに永続化すること）
- データ層のロジックをStreamlitのUIコードに混在させること
