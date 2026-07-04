import os
import requests
from typing import List, Dict, Any, Optional, Union

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
    def list_projects(cls) -> List[Dict[str, Union[str, list, dict, bool]]]:
        """
        全プロジェクトの一覧を取得します。

        Returns:
            List[Dict[str, Union[str, list, dict, bool]]]: プロジェクトの辞書のリスト
        """
        try:
            response = requests.get(cls._get_url("/api/v1/projects"))
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error listing projects: {e}")
            return []

    @classmethod
    def create_project(
        cls, project_id: str, name: str
    ) -> Optional[Dict[str, Union[str, list, dict, bool]]]:
        """
        プロジェクトを新規作成します。

        Args:
            project_id (str): プロジェクトのID
            name (str): プロジェクト名

        Returns:
            Optional[Dict[str, Union[str, list, dict, bool]]]: 作成されたプロジェクトの辞書、失敗時はNone
        """
        payload = {"id": project_id, "name": name}
        try:
            response = requests.post(cls._get_url("/api/v1/projects"), json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creating project {project_id}: {e}")
            return None

    @classmethod
    def get_project(
        cls, project_id: str
    ) -> Optional[Dict[str, Union[str, list, dict, bool]]]:
        """
        プロジェクトの詳細情報を取得します。

        Args:
            project_id (str): 取得するプロジェクトのID

        Returns:
            Optional[Dict[str, Union[str, list, dict, bool]]]: プロジェクト情報の辞書、失敗時はNone
        """
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
        """
        プロジェクトを削除します。

        Args:
            project_id (str): 削除するプロジェクトのID

        Returns:
            bool: 成功した場合はTrue、それ以外はFalse
        """
        try:
            response = requests.delete(cls._get_url(f"/api/v1/projects/{project_id}"))
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error deleting project {project_id}: {e}")
            return False

    @classmethod
    def update_owner_context(
        cls, project_id: str, owner_context: Dict[str, str]
    ) -> Optional[Dict[str, Union[str, list, dict, bool]]]:
        """
        オーナー設定（動機・ビジョンなど）を更新します。

        Args:
            project_id (str): 更新するプロジェクトのID
            owner_context (Dict[str, str]): 更新するオーナー設定の辞書

        Returns:
            Optional[Dict[str, Union[str, list, dict, bool]]]: 更新されたプロジェクト情報の辞書、失敗時はNone
        """
        try:
            response = requests.put(
                cls._get_url(f"/api/v1/projects/{project_id}/owner"), json=owner_context
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating owner context for {project_id}: {e}")
            return None

    @classmethod
    def add_employee(
        cls, project_id: str, employee_data: Dict[str, Union[str, bool, None]]
    ) -> Optional[Dict[str, Union[str, list, dict, bool]]]:
        """
        従業員をプロジェクトに追加します。

        Args:
            project_id (str): 従業員を追加するプロジェクトのID
            employee_data (Dict[str, Union[str, bool, None]]): 追加する従業員のデータ

        Returns:
            Optional[Dict[str, Union[str, list, dict, bool]]]: 追加された従業員情報の辞書、失敗時はNone
        """
        try:
            response = requests.post(
                cls._get_url(f"/api/v1/projects/{project_id}/employees"),
                json=employee_data,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error adding employee to project {project_id}: {e}")
            return None

    @classmethod
    def update_employee(
        cls,
        project_id: str,
        employee_id: str,
        employee_data: Dict[str, Union[str, bool, None]],
    ) -> Optional[Dict[str, Union[str, list, dict, bool]]]:
        """
        従業員の情報を更新します。

        Args:
            project_id (str): プロジェクトID
            employee_id (str): 更新する従業員のID
            employee_data (Dict[str, Union[str, bool, None]]): 更新する従業員のデータ

        Returns:
            Optional[Dict[str, Union[str, list, dict, bool]]]: 更新された従業員情報の辞書、失敗時はNone
        """
        try:
            response = requests.put(
                cls._get_url(f"/api/v1/projects/{project_id}/employees/{employee_id}"),
                json=employee_data,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating employee {employee_id} in project {project_id}: {e}")
            return None

    @classmethod
    def delete_employee(cls, project_id: str, employee_id: str) -> bool:
        """
        従業員をプロジェクトから削除します。

        Args:
            project_id (str): プロジェクトID
            employee_id (str): 削除する従業員のID

        Returns:
            bool: 成功した場合はTrue、それ以外はFalse
        """
        try:
            response = requests.delete(
                cls._get_url(f"/api/v1/projects/{project_id}/employees/{employee_id}")
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(
                f"Error deleting employee {employee_id} from project {project_id}: {e}"
            )
            return False

    @classmethod
    def send_chat_message(
        cls, project_id: str, employee_id: str, message: str
    ) -> Optional[Dict[str, str]]:
        """
        仮想従業員にメッセージを送信し、応答を取得します。

        Args:
            project_id (str): プロジェクトID
            employee_id (str): 従業員のID
            message (str): 送信するメッセージ

        Returns:
            Optional[Dict[str, str]]: 応答メッセージの辞書、失敗時はNone
        """
        payload = {"message": message}
        try:
            response = requests.post(
                cls._get_url(
                    f"/api/v1/projects/{project_id}/employees/{employee_id}/chat"
                ),
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(
                f"Error sending chat message to {employee_id} in project {project_id}: {e}"
            )
            return None

    @classmethod
    def get_chat_history(
        cls, project_id: str, employee_id: str
    ) -> List[Dict[str, str]]:
        """
        仮想従業員との会話履歴を取得します。

        Args:
            project_id (str): プロジェクトID
            employee_id (str): 従業員のID

        Returns:
            List[Dict[str, str]]: 会話履歴の辞書のリスト
        """
        try:
            response = requests.get(
                cls._get_url(
                    f"/api/v1/projects/{project_id}/employees/{employee_id}/chat/history"
                )
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(
                f"Error getting chat history for {employee_id} in project {project_id}: {e}"
            )
            return []

    @classmethod
    def clear_chat_history(cls, project_id: str, employee_id: str) -> bool:
        """
        会話履歴を消去します。

        Args:
            project_id (str): プロジェクトID
            employee_id (str): 従業員のID

        Returns:
            bool: 成功した場合はTrue、それ以外はFalse
        """
        try:
            response = requests.delete(
                cls._get_url(
                    f"/api/v1/projects/{project_id}/employees/{employee_id}/chat/history"
                )
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(
                f"Error clearing chat history for {employee_id} in project {project_id}: {e}"
            )
            return False
