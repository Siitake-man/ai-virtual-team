# AI Virtual Team Builder — タスク管理

**更新日**: 2026年7月5日  
**ステータス**: Phase 1 実装完了・動作検証待ち

---

## 📊 現在の進捗

| Phase | ステップ | ステータス |
|:---|:---|:---:|
| **Phase 1** | Step 1: 環境構築・起動スクリプト | ✅ 完了 |
| **Phase 1** | Step 2: Pydanticスキーマ + JSONリポジトリ | ✅ 完了（テスト通過済み）|
| **Phase 1** | Step 3: FastAPI CRUD API | ✅ 完了（Swagger UI確認済み）|
| **Phase 1** | Step 4: Streamlit サイドバーUI + 従業員管理タブ | ✅ 完了（画面表示確認済み）|
| **Phase 1** | Step 5: LLMサービス + 個別チャットタブ | ⏳ 実装済み・動作検証待ち |
| **Phase 2** | 人格自動生成機能 | 📋 未着手 |
| **Phase 2** | 知識ストック管理 | 📋 未着手 |
| **Phase 2** | GitHub連携 | 📋 未着手 |
| **Phase 2** | 全員同時レビュー | 📋 未着手 |
| **Phase 3** | 統合サマリー生成 | 📋 未着手 |
| **Phase 3** | Markdownエクスポート | 📋 未着手 |
| **Phase 3** | NPO Trust Platform プリセット同梱 | 📋 未着手 |
| **Phase 3** | README.md（社内配布用） | 📋 未着手 |

---

## 🔥 次の5分タスク（最優先）

### ① Phase 1 の動作検証（必須）

**目的**: チャット機能が実際のGemini APIキーで正常動作することを確認する。

1. `.env` ファイルを開き、`GEMINI_API_KEY=` に自分のGemini APIキーを設定して保存する。
2. FastAPIサーバーが再起動されていなければ、`run.ps1` を再実行する。
3. Streamlit画面（`http://localhost:8501`）を開く。
4. 「**従業員管理タブ**」で従業員（例: `鋭子`、属性: `クリティカル`）を1名追加する。
5. 「**💬 個別チャット**」タブを開き、従業員を選択してメッセージを送信する。
6. `data/projects/npo-trust-platform.json` を開き、`chat_history` に履歴が保存されていることを確認する。

**確認基準**: 従業員からLLMの応答が返り、JSONに会話履歴が永続化されること。

---

## 📋 Phase 2 タスク詳細（次のセッションで計画書作成）

### タスク A: 人格自動生成機能
- **内容**: 従業員管理タブの「人格プロンプト」欄に「**自動生成**」ボタンを追加する。
- **仕組み**: オーナー設定（動機・ビジョン・価値観）+ 従業員の属性・専門領域 を `PERSONA_GENERATION_PROMPT` テンプレートに組み込み、Gemini APIに人格プロンプトを生成させる。
- **実装ファイル**: `app/services/persona_generator.py`、`app/api/routers/employees.py`（新規エンドポイント追加）、`app/main.py`（ボタン追加）

### タスク B: 知識ストック管理
- **内容**: 「📚 知識ストック」タブに、各従業員へのソース追加・削除UIを実装する。
- **対応ソース**: テキスト直接入力、WebページURL（スクレイピング）、Markdownファイルのアップロード
- **実装ファイル**: `app/api/routers/knowledge.py`（新規）、`app/services/scraper.py`（新規）、`app/main.py`

### タスク C: GitHub連携
- **内容**: 「📚 知識ストック」タブのGitHub連携UIで、リポジトリのファイルツリーを表示してチェックボックスで選択したファイルを知識ストックに追加する。
- **実装ファイル**: `app/services/github_service.py`、`app/api/routers/github.py`（新規）、`app/main.py`

### タスク D: 全員同時レビュー
- **内容**: 「🔍 全員同時レビュー」タブで、アクティブな全従業員が並列にLLMへリクエストを送り、結果を各従業員タブで表示する。「全員の意見をまとめる」ボタンで統合サマリーも生成する。
- **実装ファイル**: `app/api/routers/review.py`（新規）、`app/main.py`

---

## ⚙️ 既知の技術的負債（次回以降で対応）

| 項目 | 詳細 | 優先度 |
|:---|:---|:---:|
| `.env`の再読み込み | FastAPIサーバー起動後にAPIキーを変更した場合、サーバーを再起動しないと反映されない | 低 |
| エラーハンドリングのUI改善 | APIコール失敗時のエラーメッセージが英語のまま | 低 |
| `st.form` の入力UI検討 | サイドバーの幅制限で `st.form` を使えない（現在は `st.button`で代替） | 低 |
| モデル選択の正規化 | LLMモデルの識別子が `requirements.txt` と `selectbox` 内で表記揺れあり | 中 |

---

## 🗂️ ファイル構成（現在の実装状態）

```
ai-virtual-team/
├── .env.example            ✅ 作成済み
├── .env                    ⚠️ APIキー設定が必要
├── setup.ps1 / setup.bat   ✅ 作成済み（動作確認済み）
├── run.ps1 / run.bat       ✅ 作成済み（動作確認済み）
├── requirements.txt        ✅ 作成済み（Python 3.13対応）
├── app/
│   ├── main.py             ✅ Streamlit全画面実装済み
│   ├── api_client.py       ✅ 全メソッド実装済み
│   ├── api/
│   │   ├── main.py         ✅ 全ルーター登録済み
│   │   └── routers/
│   │       ├── projects.py  ✅ 完全実装済み
│   │       ├── employees.py ✅ 完全実装済み
│   │       └── chat.py      ✅ 完全実装済み（検証待ち）
│   ├── services/
│   │   └── llm_service.py   ✅ Gemini API実装済み（検証待ち）
│   ├── repositories/
│   │   └── json_repository.py ✅ 完全実装済み（テスト通過）
│   └── models/
│       └── schemas.py       ✅ 完全実装済み
├── data/
│   ├── projects/            ✅ ディレクトリ作成済み
│   └── presets/             📋 Phase 3で同梱予定
├── exports/                 ✅ ディレクトリ作成済み
└── .backups/initial_docs/   ✅ 設計書初期バックアップ済み
```
