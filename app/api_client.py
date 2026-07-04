import os
import requests
from typing import List, Dict, Any, Optional

# API Server URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

class APIClient:
    """
    FastAPI バックエンドへのHTTPリクエストをカプセル化するクライアントクラス。
    """
    @staticmethod
    def _get_url(path: str) -> str:
        return f"{API_BASE_URL.rstrip('/')}{path}"

    @classmethod
    def list_projects(cls) -> List[Dict[str, Any]]:
        """全プロジェクトの一覧を取得します"""
        try:
            response = requests.get(cls._get_url("/api/v1/projects"))
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error listing projects: {e}")
            return []

    @classmethod
    def create_project(cls, project_id: str, name: str) -> Optional[Dict[str, Any]]:
        """プロジェクトを新規作成します"""
        payload = {"id": project_id, "name": name}
        try:
            response = requests.post(cls._get_url("/api/v1/projects"), json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creating project {project_id}: {e}")
            return None

    @classmethod
    def get_project(cls, project_id: str) -> Optional[Dict[str, Any]]:
        """プロジェクトの詳細情報を取得します"""
        try:
            response = requests.get(cls._get_url(f"/api/v1/projects/{project_id}"))
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting project {project_id}: {e}")
            return None

    @classmethod
    def delete_project(cls, project_id: str) -> bool:
        """プロジェクトを削除します"""
        try:
            response = requests.delete(cls._get_url(f"/api/v1/projects/{project_id}"))
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error deleting project {project_id}: {e}")
            return False

    @classmethod
    def update_owner_context(cls, project_id: str, owner_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """オーナー設定（動機・ビジョンなど）を更新します"""
        try:
            response = requests.put(
                cls._get_url(f"/api/v1/projects/{project_id}/owner"),
                json=owner_context
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating owner context for {project_id}: {e}")
            return None

    @classmethod
    def add_employee(cls, project_id: str, employee_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """従業員をプロジェクトに追加します"""
        try:
            response = requests.post(
                cls._get_url(f"/api/v1/projects/{project_id}/employees"),
                json=employee_data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error adding employee to project {project_id}: {e}")
            return None

    @classmethod
    def update_employee(cls, project_id: str, employee_id: str, employee_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """従業員の情報を更新します"""
        try:
            response = requests.put(
                cls._get_url(f"/api/v1/projects/{project_id}/employees/{employee_id}"),
                json=employee_data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating employee {employee_id} in project {project_id}: {e}")
            return None

    @classmethod
    def delete_employee(cls, project_id: str, employee_id: str) -> bool:
        """従業員をプロジェクトから削除します"""
        try:
            response = requests.delete(
                cls._get_url(f"/api/v1/projects/{project_id}/employees/{employee_id}")
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error deleting employee {employee_id} from project {project_id}: {e}")
            return False

    @classmethod
    def send_chat_message(cls, project_id: str, employee_id: str, message: str) -> Optional[Dict[str, Any]]:
        """仮想従業員にメッセージを送信し、応答を取得します"""
        payload = {"message": message}
        try:
            response = requests.post(
                cls._get_url(f"/api/v1/projects/{project_id}/employees/{employee_id}/chat"),
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error sending chat message to {employee_id} in project {project_id}: {e}")
            return None

    @classmethod
    def get_chat_history(cls, project_id: str, employee_id: str) -> List[Dict[str, Any]]:
        """仮想従業員との会話履歴を取得します"""
        try:
            response = requests.get(
                cls._get_url(f"/api/v1/projects/{project_id}/employees/{employee_id}/chat/history")
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting chat history for {employee_id} in project {project_id}: {e}")
            return []

    @classmethod
    def clear_chat_history(cls, project_id: str, employee_id: str) -> bool:
        """会話履歴を消去します"""
        try:
            response = requests.delete(
                cls._get_url(f"/api/v1/projects/{project_id}/employees/{employee_id}/chat/history")
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error clearing chat history for {employee_id} in project {project_id}: {e}")
            return False
