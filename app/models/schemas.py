from pydantic import BaseModel, Field
from typing import List, Optional


class OwnerContext(BaseModel):
    """
    プロジェクトのオーナーが設定するコンテキスト（動機、ビジョンなど）を表すモデル。
    仮想従業員に共通して注入される情報となります。
    """

    motivation: str = Field(default="", description="プロジェクトを始めた動機・背景")
    vision: str = Field(default="", description="5年後のビジョン")
    values: str = Field(default="", description="大切にしている価値観・判断基準")
    ng_items: str = Field(default="", description="絶対にやってはいけないこと")
    current_phase: str = Field(default="", description="現在の開発フェーズ")


class KnowledgeSource(BaseModel):
    """
    仮想従業員が参照する知識ソースを表すモデル。
    マークダウンファイル、URL、テキストなどが指定可能です。
    """

    type: str = Field(
        ..., description="ソースのタイプ (markdown / text / url / github)"
    )
    path: Optional[str] = Field(
        default=None, description="ローカルのファイルパス (type: markdown, github)"
    )
    url: Optional[str] = Field(default=None, description="WebページのURL (type: url)")
    content: Optional[str] = Field(
        default=None, description="直接入力されたテキスト (type: text)"
    )
    name: Optional[str] = Field(default=None, description="表示用のソース名")


class ChatMessage(BaseModel):
    """
    チャットのメッセージ履歴を表すモデル。
    """

    role: str = Field(..., description="送信者の役割 (user / assistant / system)")
    content: str = Field(..., description="メッセージ内容")
    timestamp: str = Field(..., description="送信日時 (ISO 8601形式)")


class Employee(BaseModel):
    """
    仮想従業員（AIエージェント）の情報を表すモデル。
    属性、プロンプト、チャット履歴などを保持します。
    """

    id: str = Field(..., description="従業員ID (例: emp-001)")
    name: str = Field(..., description="従業員名 (例: 鋭子)")
    attribute: str = Field(
        ..., description="属性 (critical / dreamer / realist / expert / custom)"
    )
    display_name: str = Field(..., description="表示用名 (例: 鋭子（クリティカル）)")
    specialty: str = Field(..., description="専門領域 (例: 批判的思考・リスク洗い出し)")
    personality_prompt: str = Field(
        default="", description="人格プロンプト (システムプロンプト)"
    )
    knowledge_sources: List[KnowledgeSource] = Field(
        default_factory=list, description="知識ソースのリスト"
    )
    llm_model: str = Field(
        default="gemini-2.0-flash", description="使用するLLMモデル名"
    )
    is_active: bool = Field(default=True, description="アクティブ状態")
    chat_history: List[ChatMessage] = Field(
        default_factory=list, description="チャット履歴"
    )


class Project(BaseModel):
    """
    システム内で管理されるプロジェクトの全体情報を表すモデル。
    オーナー設定や所属する仮想従業員を含みます。
    """

    id: str = Field(..., description="プロジェクトID (例: npo-trust-platform)")
    name: str = Field(..., description="プロジェクト名")
    owner_context: OwnerContext = Field(
        default_factory=OwnerContext, description="オーナー設定情報"
    )
    github_repo: Optional[str] = Field(
        default="", description="GitHubリポジトリ名 (例: username/repo)"
    )
    employees: List[Employee] = Field(
        default_factory=list, description="所属する仮想従業員リスト"
    )


# APIリクエスト用スキーマ
class ProjectCreate(BaseModel):
    """
    プロジェクト新規作成APIのリクエストボディを表すモデル。
    """

    id: str = Field(..., description="プロジェクトID (英数字とハイフン)")
    name: str = Field(..., description="プロジェクト名")
    owner_context: Optional[OwnerContext] = None
    github_repo: Optional[str] = ""


class EmployeeCreate(BaseModel):
    """
    従業員新規追加APIのリクエストボディを表すモデル。
    """

    name: str = Field(..., description="従業員名")
    attribute: str = Field(..., description="属性 (例: クリティカル)")
    specialty: str = Field(..., description="専門領域")
    personality_prompt: Optional[str] = ""
    llm_model: Optional[str] = "gemini-2.0-flash"
    is_active: Optional[bool] = True


class EmployeeUpdate(BaseModel):
    """
    従業員情報更新APIのリクエストボディを表すモデル。
    更新が必要なフィールドのみを指定可能です。
    """

    name: Optional[str] = None
    attribute: Optional[str] = None
    specialty: Optional[str] = None
    personality_prompt: Optional[str] = None
    llm_model: Optional[str] = None
    is_active: Optional[bool] = None
