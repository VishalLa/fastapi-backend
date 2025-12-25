from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field, StringConstraints
from .api_base_model import TunedModel


class DoctorSummary(BaseModel):
    doctor_id: str
    doctor_name: str
    department_name: str 
    phone_no: str


class DoctorBase(TunedModel):
    doctor_name: str = Field(..., max_length=100)
    email: EmailStr
    gender: str = Field(..., max_length=6)
    qualification: str

    experience: Annotated[int, Field(ge=0)]
    special_experience: Annotated[int, Field(ge=0)]
    speciality: str 

    phone_no: Annotated[str, StringConstraints(pattern=r'^\+?\d+$', min_length=10, max_length=15)]

    department_id: str 
    status: bool 


class DoctorUpdate(TunedModel):
    # All fields optional for updates
    doctor_name: Optional[str] = None 
    email: Optional[str] = None 
    phone_no: Optional[str] = None 
    department_id: Optional[str] = None


class DoctorCreate(TunedModel):
    doctor_name: str = Field(..., max_length=100)
    gender: str = Field(..., max_length=6)
    qualification: str

    experience: Annotated[int, Field(ge=0)]
    special_experience: Annotated[int, Field(ge=0)]
    speciality: str 

    phone_no: Annotated[str, StringConstraints(pattern=r'^\+?\d+$', min_length=10, max_length=15)]

    department_id: str 
    status: bool 
    