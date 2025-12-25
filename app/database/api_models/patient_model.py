from typing import Optional
from datetime import datetime
from pydantic import EmailStr, Field
from .api_base_model import TunedModel


class PatientSummary(TunedModel):
    patient_id: str
    patient_name: str 
    email: EmailStr
    phone_no: str = Field(..., max_length=15)
    emergency_contact: str = Field(None, max_length=15)


class PatientBase(TunedModel):
    patient_name: str = Field(..., max_length=100)
    email: EmailStr
    gender: str = Field(..., max_length=6)
    phone_no: str = Field(..., max_length=15)
    emergency_contact: str = Field(None, max_length=15)
    date_of_birth: datetime 
    address: str 
    status: bool
    medical_history: Optional[str] = None 

class PateintUpdate(TunedModel):
    phone_no: Optional[str] = None 
    emergency_contact: Optional[str] = None 
    address: Optional[str] = None 
    medical_history: Optional[str] = None 
    date_of_birth: Optional[str] = None

class PateintCreate(TunedModel):
    patient_name: str = Field(..., max_length=100)
    email: EmailStr
    password: str       # Plain password

    gender: str = Field(..., max_length=6)
    phone_no: str = Field(..., max_length=15)
    emergency_contact: str = Field(None, max_length=15)
    date_of_birth: datetime
    address: str 
    status: bool
    medical_history: Optional[str] = None 
