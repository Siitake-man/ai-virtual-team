from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.schemas import Project, ProjectCreate, OwnerContext
from app.repositories.json_repository import JsonRepository

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])

def get_repo():
    return JsonRepository()

@router.get("", response_model=List[Project])
def list_projects(repo: JsonRepository = Depends(get_repo)):
    """保存されているすべてのプロジェクトを一覧取得します"""
    return repo.list_projects()

@router.post("", response_model=Project)
def create_project(project_data: ProjectCreate, repo: JsonRepository = Depends(get_repo)):
    """新規にプロジェクトを作成します。IDが重複している場合は400エラーを返します"""
    existing = repo.get_project(project_data.id)
    if existing:
        raise HTTPException(status_code=400, detail=f"Project with ID '{project_data.id}' already exists")
    
    project = Project(
        id=project_data.id,
        name=project_data.name,
        owner_context=project_data.owner_context or OwnerContext(),
        github_repo=project_data.github_repo or "",
        employees=[]
    )
    return repo.save_project(project)

@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str, repo: JsonRepository = Depends(get_repo)):
    """指定されたIDのプロジェクト詳細を取得します。見つからない場合は404を返します"""
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
    return project

@router.delete("/{project_id}")
def delete_project(project_id: str, repo: JsonRepository = Depends(get_repo)):
    """指定されたIDのプロジェクトを削除します。"""
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
    success = repo.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete project")
    return {"status": "success", "message": f"Project '{project_id}' deleted"}

@router.put("/{project_id}/owner", response_model=Project)
def update_owner_context(project_id: str, owner_context: OwnerContext, repo: JsonRepository = Depends(get_repo)):
    """プロジェクトのオーナー設定（動機、ビジョン、価値観、NG事項など）を更新します"""
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
    project.owner_context = owner_context
    return repo.save_project(project)
