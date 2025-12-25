from typing import Optional
from pydantic import Field
from .api_base_model import TunedModel


# Department Schema 
class DepartmentBase(TunedModel):
    department_id: str = Field(..., max_length=20)
    department_name: str = Field(..., max_length=20)
    location: str = Field(..., max_length=30)
    description: Optional[str] = None 
    head_of_department: Optional[str] = None 

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    pass

class DepatemtntUpdate(TunedModel):
    department_name: Optional[str] = None 
    location: Optional[str] = None 
    description: Optional[str] = None 
    head_of_department: Optional[str] = None 
