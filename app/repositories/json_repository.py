import os
import json
from typing import List, Optional
from app.models.schemas import Project

class JsonRepository:
    """
    JSONファイルを用いてプロジェクトデータを保存・取得するリポジトリ。
    各プロジェクトは {project_id}.json というファイル名で data_dir 配下に保存される。
    """
    def __init__(self, data_dir: str = "./data/projects"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def _get_filepath(self, project_id: str) -> str:
        # ディレクトリトラバーサル防止のため、ファイル名を安全な文字のみにする
        safe_id = "".join(c for c in project_id if c.isalnum() or c in ("-", "_"))
        return os.path.join(self.data_dir, f"{safe_id}.json")

    def list_projects(self) -> List[Project]:
        """保存されているすべてのプロジェクトを一覧取得する"""
        projects = []
        if not os.path.exists(self.data_dir):
            return projects
            
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        projects.append(Project(**data))
                except Exception as e:
                    print(f"Error loading project file {filepath}: {e}")
        return projects

    def get_project(self, project_id: str) -> Optional[Project]:
        """指定したIDのプロジェクトを取得する。存在しない場合は None を返す"""
        filepath = self._get_filepath(project_id)
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Project(**data)
        except Exception as e:
            print(f"Error reading project {project_id} from {filepath}: {e}")
            return None

    def save_project(self, project: Project) -> Project:
        """プロジェクトデータをJSONファイルに新規保存または上書き保存する"""
        filepath = self._get_filepath(project.id)
        # Pydantic v2 の model_dump を使用
        data = project.model_dump()
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return project
        except Exception as e:
            print(f"Error saving project {project.id} to {filepath}: {e}")
            raise e

    def delete_project(self, project_id: str) -> bool:
        """指定したIDのプロジェクトファイルを削除する。成功した場合は True を返す"""
        filepath = self._get_filepath(project_id)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except Exception as e:
                print(f"Error deleting project file {filepath}: {e}")
                return False
        return False
