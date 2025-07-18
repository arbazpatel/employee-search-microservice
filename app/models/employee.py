from pydantic import BaseModel, EmailStr

class Employee(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    department: str
    position: str
    location: str
    employee_ssn: str