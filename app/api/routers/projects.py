from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.schemas import Project, ProjectCreate, OwnerContext
from app.repositories.json_repository import JsonRepository

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


def get_repo() -> JsonRepository:
    """
    JsonRepositoryのインスタンスを取得します。
    FastAPIのDependency Injectionで使用されます。

    Returns:
        JsonRepository: JSONファイルベースのリポジトリインスタンス
    """
    return JsonRepository()


@router.get("", response_model=List[Project])
def list_projects(repo: JsonRepository = Depends(get_repo)) -> List[Project]:
    """
    保存されているすべてのプロジェクトを一覧取得します

    Args:
        repo (JsonRepository): データリポジトリ

    Returns:
        List[Project]: プロジェクトのリスト
    """
    return repo.list_projects()


@router.post("", response_model=Project)
def create_project(
    project_data: ProjectCreate, repo: JsonRepository = Depends(get_repo)
) -> Project:
    """
    新規にプロジェクトを作成します。IDが重複している場合は400エラーを返します

    Args:
        project_data (ProjectCreate): 作成するプロジェクトのデータ
        repo (JsonRepository): データリポジトリ

    Returns:
        Project: 作成されたプロジェクト
    """
    existing = repo.get_project(project_data.id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Project with ID '{project_data.id}' already exists",
        )

    project = Project(
        id=project_data.id,
        name=project_data.name,
        owner_context=project_data.owner_context or OwnerContext(),
        github_repo=project_data.github_repo or "",
        employees=[],
    )
    return repo.save_project(project)


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str, repo: JsonRepository = Depends(get_repo)) -> Project:
    """
    指定されたIDのプロジェクト詳細を取得します。見つからない場合は404を返します

    Args:
        project_id (str): 取得するプロジェクトのID
        repo (JsonRepository): データリポジトリ

    Returns:
        Project: プロジェクト詳細
    """
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: str, repo: JsonRepository = Depends(get_repo)
) -> dict[str, str]:
    """
    指定されたIDのプロジェクトを削除します。

    Args:
        project_id (str): 削除するプロジェクトのID
        repo (JsonRepository): データリポジトリ

    Returns:
        dict[str, str]: 成功メッセージ
    """
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
    success = repo.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete project")
    return {"status": "success", "message": f"Project '{project_id}' deleted"}


@router.put("/{project_id}/owner", response_model=Project)
def update_owner_context(
    project_id: str,
    owner_context: OwnerContext,
    repo: JsonRepository = Depends(get_repo),
) -> Project:
    """
    プロジェクトのオーナー設定（動機、ビジョン、価値観、NG事項など）を更新します

    Args:
        project_id (str): 更新するプロジェクトのID
        owner_context (OwnerContext): 新しいオーナー設定
        repo (JsonRepository): データリポジトリ

    Returns:
        Project: 更新されたプロジェクト
    """
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
    project.owner_context = owner_context
    return repo.save_project(project)
