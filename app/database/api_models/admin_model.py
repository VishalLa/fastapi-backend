from typing import List
from pydantic import EmailStr, Field
from .api_base_model import TunedModel, BaseModel

from .department_model import DepartmentResponse
from .appointment_treatment_model import AppointmentResponse
from .doctor_model import DoctorSummary
from .patient_model import PatientSummary

# Admin Schemas
class AdminBase(TunedModel):
    email: EmailStr

class AdminCreate(AdminBase):
    admin_id: str = Field(..., max_length=8)
    password: str 

class Admin_Response(AdminBase):
    admin_id: str 


class DashboardSearchResponse(BaseModel):
    doctors: List[DoctorSummary]
    patients: List[PatientSummary]
    appointments: List[AppointmentResponse]
    departments: List[DepartmentResponse]
