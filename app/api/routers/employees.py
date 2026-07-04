from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import Employee, EmployeeCreate, EmployeeUpdate
from app.repositories.json_repository import JsonRepository

router = APIRouter(prefix="/api/v1/projects/{project_id}/employees", tags=["employees"])

def get_repo():
    return JsonRepository()

@router.post("", response_model=Employee)
def add_employee(project_id: str, employee_data: EmployeeCreate, repo: JsonRepository = Depends(get_repo)):
    """プロジェクトに仮想従業員を新規追加します。IDは自動で連番生成されます"""
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
    
    # 従業員IDの自動生成（連番）
    emp_num = len(project.employees) + 1
    emp_id = f"emp-{emp_num:03d}"
    
    existing_ids = {e.id for e in project.employees}
    while emp_id in existing_ids:
        emp_num += 1
        emp_id = f"emp-{emp_num:03d}"

    # 表示名 (display_name) の自動生成
    display_name = f"{employee_data.name}（{employee_data.attribute}）"
    
    employee = Employee(
        id=emp_id,
        name=employee_data.name,
        attribute=employee_data.attribute,
        display_name=display_name,
        specialty=employee_data.specialty,
        personality_prompt=employee_data.personality_prompt or "",
        llm_model=employee_data.llm_model or "gemini-2.0-flash",
        is_active=employee_data.is_active if employee_data.is_active is not None else True,
        knowledge_sources=[],
        chat_history=[]
    )
    
    project.employees.append(employee)
    repo.save_project(project)
    return employee

@router.put("/{employee_id}", response_model=Employee)
def update_employee(project_id: str, employee_id: str, employee_data: EmployeeUpdate, repo: JsonRepository = Depends(get_repo)):
    """指定された従業員IDの情報を更新します。表示名も自動で再生成されます"""
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
    
    emp_index = -1
    for i, e in enumerate(project.employees):
        if e.id == employee_id:
            emp_index = i
            break
            
    if emp_index == -1:
        raise HTTPException(status_code=404, detail=f"Employee '{employee_id}' not found")
        
    employee = project.employees[emp_index]
    
    # 送信された項目のみを更新
    if employee_data.name is not None:
        employee.name = employee_data.name
    if employee_data.attribute is not None:
        employee.attribute = employee_data.attribute
    if employee_data.specialty is not None:
        employee.specialty = employee_data.specialty
    if employee_data.personality_prompt is not None:
        employee.personality_prompt = employee_data.personality_prompt
    if employee_data.llm_model is not None:
        employee.llm_model = employee_data.llm_model
    if employee_data.is_active is not None:
        employee.is_active = employee_data.is_active
        
    # 表示名の更新
    employee.display_name = f"{employee.name}（{employee.attribute}）"
    
    project.employees[emp_index] = employee
    repo.save_project(project)
    return employee

@router.delete("/{employee_id}")
def delete_employee(project_id: str, employee_id: str, repo: JsonRepository = Depends(get_repo)):
    """指定された従業員IDをプロジェクトから削除します"""
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
        
    emp_index = -1
    for i, e in enumerate(project.employees):
        if e.id == employee_id:
            emp_index = i
            break
            
    if emp_index == -1:
        raise HTTPException(status_code=404, detail=f"Employee '{employee_id}' not found")
        
    project.employees.pop(emp_index)
    repo.save_project(project)
    return {"status": "success", "message": f"Employee '{employee_id}' deleted from project '{project_id}'"}
