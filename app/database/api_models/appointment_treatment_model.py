from typing import Optional, List
from datetime import date as Date
from pydantic import Field
from .api_base_model import TunedModel


class TreatmentCreate(TunedModel):
    appointment_id: str 
    doctor_id: str 
    patient_id: str
    treatment_id: str
    test_done: Optional[str] = None
    diagonsis: Optional[str] = None
    prescription: Optional[str] = None
    follow_up_date: Optional[str] = None


class PatientHistoryResponse(TunedModel):
    visit_type: str
    test_done: Optional[str]
    diagnosis: Optional[str]
    prescription: Optional[str]


class PatientDoctorData(TunedModel):
    patient_name: str
    doctor_name: str


class PatientHistoryData(TunedModel):
    patient_doctor_data: PatientDoctorData
    patient_history: List[PatientHistoryResponse]


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
