from pydantic import BaseModel, Field
from typing import List, Optional

class OwnerContext(BaseModel):
    motivation: str = Field(default="", description="プロジェクトを始めた動機・背景")
    vision: str = Field(default="", description="5年後のビジョン")
    values: str = Field(default="", description="大切にしている価値観・判断基準")
    ng_items: str = Field(default="", description="絶対にやってはいけないこと")
    current_phase: str = Field(default="", description="現在の開発フェーズ")

class KnowledgeSource(BaseModel):
    type: str = Field(..., description="ソースのタイプ (markdown / text / url / github)")
    path: Optional[str] = Field(default=None, description="ローカルのファイルパス (type: markdown, github)")
    url: Optional[str] = Field(default=None, description="WebページのURL (type: url)")
    content: Optional[str] = Field(default=None, description="直接入力されたテキスト (type: text)")
    name: Optional[str] = Field(default=None, description="表示用のソース名")

class ChatMessage(BaseModel):
    role: str = Field(..., description="送信者の役割 (user / assistant / system)")
    content: str = Field(..., description="メッセージ内容")
    timestamp: str = Field(..., description="送信日時 (ISO 8601形式)")

class Employee(BaseModel):
    id: str = Field(..., description="従業員ID (例: emp-001)")
    name: str = Field(..., description="従業員名 (例: 鋭子)")
    attribute: str = Field(..., description="属性 (critical / dreamer / realist / expert / custom)")
    display_name: str = Field(..., description="表示用名 (例: 鋭子（クリティカル）)")
    specialty: str = Field(..., description="専門領域 (例: 批判的思考・リスク洗い出し)")
    personality_prompt: str = Field(default="", description="人格プロンプト (システムプロンプト)")
    knowledge_sources: List[KnowledgeSource] = Field(default_factory=list, description="知識ソースのリスト")
    llm_model: str = Field(default="gemini-2.0-flash", description="使用するLLMモデル名")
    is_active: bool = Field(default=True, description="アクティブ状態")
    chat_history: List[ChatMessage] = Field(default_factory=list, description="チャット履歴")

class Project(BaseModel):
    id: str = Field(..., description="プロジェクトID (例: npo-trust-platform)")
    name: str = Field(..., description="プロジェクト名")
    owner_context: OwnerContext = Field(default_factory=OwnerContext, description="オーナー設定情報")
    github_repo: Optional[str] = Field(default="", description="GitHubリポジトリ名 (例: username/repo)")
    employees: List[Employee] = Field(default_factory=list, description="所属する仮想従業員リスト")

# APIリクエスト用スキーマ
class ProjectCreate(BaseModel):
    id: str = Field(..., description="プロジェクトID (英数字とハイフン)")
    name: str = Field(..., description="プロジェクト名")
    owner_context: Optional[OwnerContext] = None
    github_repo: Optional[str] = ""

class EmployeeCreate(BaseModel):
    name: str = Field(..., description="従業員名")
    attribute: str = Field(..., description="属性 (例: クリティカル)")
    specialty: str = Field(..., description="専門領域")
    personality_prompt: Optional[str] = ""
    llm_model: Optional[str] = "gemini-2.0-flash"
    is_active: Optional[bool] = True

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    attribute: Optional[str] = None
    specialty: Optional[str] = None
    personality_prompt: Optional[str] = None
    llm_model: Optional[str] = None
    is_active: Optional[bool] = None
