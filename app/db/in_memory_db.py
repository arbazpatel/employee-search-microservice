from typing import Dict, List
from app.models.employee import Employee

DB: Dict[str, List[Employee]] = {
    "Stark Industries": [
        Employee(id=1, first_name="Tony", last_name="Stark", email="tony.stark@stark.com", department="Research and Development", position="Chief Executive Officer", location="New York", employee_ssn="SSN-STARK-001"),
        Employee(id=2, first_name="Pepper", last_name="Potts", email="pepper.potts@stark.com", department="Executive", position="CEO", location="New York", employee_ssn="SSN-STARK-002"),
        Employee(id=3, first_name="Happy", last_name="Hogan", email="happy.hogan@stark.com", department="Security", position="Head of Security", location="New York", employee_ssn="SSN-STARK-003"),
    ],
    "Wayne Enterprises": [
        Employee(id=4, first_name="Bruce", last_name="Wayne", email="bruce.wayne@wayne.com", department="Executive", position="CEO", location="Gotham", employee_ssn="SSN-WAYNE-001"),
        Employee(id=5, first_name="Lucius", last_name="Fox", email="lucius.fox@wayne.com", department="Applied Sciences", position="Head of R&D", location="Gotham", employee_ssn="SSN-WAYNE-002"),
    ],
}

def get_employees_by_org(org_name: str) -> List[Employee]:
    return DB.get(org_name, [])