from typing import Optional
from datetime import date as Date
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
    date: Date
    shift: str = Field(..., max_length=10)
    status: str = Field(..., max_length=12)
    reason: Optional[str] = None


class AppointmentCreate(TunedModel):
    patient_id: str
    doctor_id: str
    visit_type: str = Field(..., max_length=15)
    date: Date
    shift: str = Field(..., max_length=10)
    reason: Optional[str] = None


class AppointmentResponse(TunedModel):
    appointment_id: str
    doctor_id: str
    patient_id: str 
    visit_type: str
    date: Date
    status: str
    shift: str
