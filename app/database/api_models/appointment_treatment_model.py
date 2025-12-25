from typing import Optional
from datetime import date 
from pydantic import Field
from .api_base_model import TunedModel


class TreatmentBase(TunedModel):
    test_done: Optional[str] = None
    diagonsis: Optional[str] = None
    prescription: Optional[str] = None
    follow_up_date: Optional[str] = None

class TreatmentCreate(TreatmentBase):
    treatment_id: str
    appointment_id: str

class TreatmentResponse(TreatmentBase):
    treatment_id: str


# Appointment Schema
class AppointmentBase(TunedModel):
    patient_id: str
    doctor_id: str
    visit_type: str = Field(..., max_length=15)
    date: date
    shift: str = Field(..., max_length=10)
    status: str = Field(..., max_length=12)
    reason: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    appointment_id: str = Field(..., max_length=32)

class AppointmentResponse(AppointmentBase):
    appointment_id: str
    treatment: Optional[TreatmentResponse] = None
