from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.schemas import ChatMessage
from app.repositories.json_repository import JsonRepository
from app.services.llm_service import LLMService

router = APIRouter(
    prefix="/api/v1/projects/{project_id}/employees/{employee_id}/chat", tags=["chat"]
)


def get_repo() -> JsonRepository:
    """
    JsonRepositoryのインスタンスを取得します。
    FastAPIのDependency Injectionで使用されます。

    Returns:
        JsonRepository: JSONファイルベースのリポジトリインスタンス
    """
    return JsonRepository()


class ChatRequest(BaseModel):
    message: str = Field(..., description="送信するメッセージ内容")


@router.post("", response_model=ChatMessage)
def send_message(
    project_id: str,
    employee_id: str,
    payload: ChatRequest,
    repo: JsonRepository = Depends(get_repo),
) -> ChatMessage:
    """
    従業員にメッセージを送信し、Gemini APIの応答を履歴とともに取得・保存します

    Args:
        project_id (str): プロジェクトID
        employee_id (str): 従業員ID
        payload (ChatRequest): 送信するメッセージ
        repo (JsonRepository): データリポジトリ

    Returns:
        ChatMessage: アシスタントからの応答メッセージ
    """
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")

    emp_index = -1
    for i, e in enumerate(project.employees):
        if e.id == employee_id:
            emp_index = i
            break

    if emp_index == -1:
        raise HTTPException(
            status_code=404, detail=f"Employee '{employee_id}' not found"
        )

    employee = project.employees[emp_index]

    # 1. ユーザーのメッセージを追加
    user_msg = ChatMessage(
        role="user", content=payload.message, timestamp=datetime.utcnow().isoformat()
    )
    employee.chat_history.append(user_msg)

    # 2. LLMサービスを呼び出して返答を取得
    try:
        response_text = LLMService.generate_chat_response(
            project, employee, employee.chat_history
        )
    except Exception as e:
        # 送信エラー時は履歴をロールバックして500エラーを返す
        employee.chat_history.pop()
        raise HTTPException(status_code=500, detail=f"LLM API エラー: {str(e)}")

    # 3. アシスタントのメッセージを追加
    assistant_msg = ChatMessage(
        role="assistant", content=response_text, timestamp=datetime.utcnow().isoformat()
    )
    employee.chat_history.append(assistant_msg)

    # 4. プロジェクトデータを上書き保存
    project.employees[emp_index] = employee
    repo.save_project(project)

    return assistant_msg


@router.get("/history", response_model=list[ChatMessage])
def get_chat_history(
    project_id: str, employee_id: str, repo: JsonRepository = Depends(get_repo)
) -> list[ChatMessage]:
    """
    指定された従業員との過去のチャット履歴を取得します

    Args:
        project_id (str): プロジェクトID
        employee_id (str): 従業員ID
        repo (JsonRepository): データリポジトリ

    Returns:
        list[ChatMessage]: チャット履歴
    """
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")

    employee = next((e for e in project.employees if e.id == employee_id), None)
    if not employee:
        raise HTTPException(
            status_code=404, detail=f"Employee '{employee_id}' not found"
        )

    return employee.chat_history


@router.delete("/history")
def clear_chat_history(
    project_id: str, employee_id: str, repo: JsonRepository = Depends(get_repo)
) -> dict[str, str]:
    """
    チャット履歴をクリアします

    Args:
        project_id (str): プロジェクトID
        employee_id (str): 従業員ID
        repo (JsonRepository): データリポジトリ

    Returns:
        dict[str, str]: 成功メッセージ
    """
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")

    emp_index = -1
    for i, e in enumerate(project.employees):
        if e.id == employee_id:
            emp_index = i
            break

    if emp_index == -1:
        raise HTTPException(
            status_code=404, detail=f"Employee '{employee_id}' not found"
        )

    project.employees[emp_index].chat_history = []
    repo.save_project(project)
    return {
        "status": "success",
        "message": f"Chat history for employee '{employee_id}' has been cleared",
    }
