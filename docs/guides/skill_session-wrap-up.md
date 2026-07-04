# ガイド：session-wrap-up スキルの使い方

**対象プロジェクト**: AI Virtual Team Builder  
**スキルファイル**: `.agents/skills/session-wrap-up/SKILL.md`

---

## このスキルは何をするのか？

開発セッションの終わりに「今日やったことを整理し、次回すぐに再開できる状態を作る」ための自動化スキルです。以下のすべてを**AIが一括で実行**します。

| やること | 自動化の内容 |
|:---|:---|
| ① ドキュメント更新 | `docs/task.md` と `docs/implementation_plan.md` のステータスを更新 |
| ② 学習メモ生成 | `docs/learning-memos/学習メモ_YYYYMMDD.md` を自動生成 |
| ③ Jules指示書生成 | `docs/handover/prompt_for_jules_YYYYMMDD.md` を自動生成 |
| ④ Gitコマンド出力 | コピペ可能なコミット・プッシュコマンドを提示 |
| ⑤ 次回プロンプト出力 | 次回セッションの「魔法のプロンプト」を提示 |

---

## 使い方（3ステップ）

### Step 1：セッション終了時にチャットで呼び出す

チャット欄に以下のいずれかを入力します：

```
session-wrap-up
```

または

```
今日の作業を締めてください
```

### Step 2：AIが自動実行する内容を確認する

AIが以下を順番に実行します：

1. `docs/task.md` の完了タスクを `✅` に更新
2. `docs/implementation_plan.md` に更新履歴を追記
3. `docs/learning-memos/` に今日の学習メモを新規作成
4. `docs/handover/` にJules向け引き継ぎ指示書を新規作成

### Step 3：出力された3点をコピーして実行する

AIが以下を最後に出力します：

1. **Gitコマンド** → ターミナルにコピペしてコミット・プッシュ
2. **Jules指示プロンプト** → Julesの起動画面に貼り付け
3. **次回の魔法のプロンプト** → メモ帳などに保存しておく

---

## 主要なファイルパス（このプロジェクト固有）

| 用途 | パス |
|:---|:---|
| タスク管理 | `docs/task.md` |
| 実装計画 | `docs/implementation_plan.md` |
| 仕様書 | `SPEC.md`, `GEMINI.md` |
| 学習メモ保存先 | `docs/learning-memos/` |
| Jules引き継ぎ先 | `docs/handover/` |
| アーカイブ先 | `docs/archive/` |

---

## 注意事項

- `.env` ファイルはGit管理外（`.gitignore` 対象）なので、コミットコマンドに含まれません
- `data/projects/` のJSONファイルはユーザーのプロジェクトデータのため、絶対に削除・移動されません
- アーカイブ候補のファイルは、移動前にAIがユーザーへ確認します
