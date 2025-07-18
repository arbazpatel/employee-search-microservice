from fastapi import APIRouter, Depends, Query
from typing import List, Optional, Dict, Any

from app.core.config import OrgConfig
from app.core.security import get_current_org
from app.db.in_memory_db import get_employees_by_org

router = APIRouter()

@router.get(
    "/search/",
    response_model=List[Dict[str, Any]],
    summary="Search for employees within an organization"
)
def search_employees(
    q: Optional[str] = Query(None, description="Search term for employee name, email, or position"),
    org_config: OrgConfig = Depends(get_current_org),
):
    """
    Search for employees, with results tailored to the calling organization.
    - Requires `X-API-Key` header for authentication and configuration.
    - Search is performed on the organization's own employee data.
    - The columns returned in the response are dynamically determined by the
      organization's configuration.
    """
    employees = get_employees_by_org(org_config.name)
    results = employees

    if q:
        search_term = q.lower()
        results = [
            emp for emp in employees
            if search_term in emp.first_name.lower()
            or search_term in emp.last_name.lower()
            or search_term in emp.email.lower()
            or search_term in emp.position.lower()
        ]

    final_response = []
    for emp in results:
        employee_data = {col: getattr(emp, col) for col in org_config.display_columns}
        final_response.append(employee_data)

    return final_response