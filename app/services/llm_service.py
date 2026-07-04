import os
from typing import List
from google import genai
from google.genai import types
from app.models.schemas import Project, Employee, ChatMessage


class LLMService:
    """
    Gemini APIへの接続とチャット応答の生成を行うサービス。
    """

    @staticmethod
    def get_client() -> genai.Client:
        """
        Gemini APIのクライアントを初期化して取得します。

        Returns:
            genai.Client: 初期化されたGemini APIクライアント

        Raises:
            ValueError: 環境変数に GEMINI_API_KEY が設定されていない場合
        """
        # python-dotenvによりロードされた環境変数からAPIキーを取得
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY が環境変数に設定されていません。.env ファイルを確認してください。"
            )
        return genai.Client(api_key=api_key)

    @classmethod
    def generate_chat_response(
        cls, project: Project, employee: Employee, messages: List[ChatMessage]
    ) -> str:
        """
        従業員の個性やプロジェクト情報を元に、Gemini APIを使用してチャット応答を生成します。

        Args:
            project (Project): 従業員が所属するプロジェクト情報
            employee (Employee): 回答する仮想従業員情報
            messages (List[ChatMessage]): 過去の会話履歴

        Returns:
            str: 生成された応答テキスト
        """
        # 1. システムプロンプト（インストラクション）の構築
        # 従業員の個別人格設定と、プロジェクトの共通オーナー設定を統合する
        owner_ctx = project.owner_context
        system_instruction = f"""あなたは仮想従業員として、以下の役割とプロジェクトの背景（オーナーコンテキスト）に基づいて回答してください。

# あなたの役割・人格
{employee.personality_prompt}

# 担当専門領域
{employee.specialty}

# 所属プロジェクトのコンテキスト (共通注入)
- 起業動機・背景: {owner_ctx.motivation}
- 5年後のビジョン: {owner_ctx.vision}
- 大切にする価値観・判断基準: {owner_ctx.values}
- 絶対にやってはいけないこと (NG事項): {owner_ctx.ng_items}
- 現在のフェーズ: {owner_ctx.current_phase}

# 行動指針
- 受け身で答えるのではなく、プロとして先回りして指摘・提案・次の一手を示すこと。
- 結論ファーストで、前置きを省くこと。
- 日本語で回答すること。
- 情報が不足していると感じたら、オーナーに逆質問で確認すること。
- 回答の最後に必ず「次に取るべき具体的な一手」を1つ示すこと。
"""

        # 2. 会話履歴の変換 (google-genai SDK 形式)
        contents: List[types.Content] = []
        for msg in messages:
            role = "user" if msg.role == "user" else "model"
            contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg.content)])
            )

        # 3. 使用モデルの決定
        model_name = employee.llm_model or os.getenv(
            "DEFAULT_LLM_MODEL", "gemini-2.0-flash"
        )

        # Phase 1時点ではGeminiモデルのみを完全サポートとするため、他モデル指定時はフォールバック
        if "gemini" not in model_name.lower():
            print(
                f"Warning: Model '{model_name}' is not fully supported in Phase 1. Falling back to gemini-2.0-flash."
            )
            model_name = "gemini-2.0-flash"

        # 4. API呼び出し実行
        client = cls.get_client()
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,  # type: ignore
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                ),
            )
            return response.text or ""
        except Exception as e:
            print(f"Gemini API Error: {e}")
            raise e
