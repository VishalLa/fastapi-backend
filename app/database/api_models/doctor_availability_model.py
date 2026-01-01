from datetime import date as Date
from .api_base_model import TunedModel

class DoctorAvailabilityBase(TunedModel):
    doctor_id: str
    date: Date
    morning_available: bool
    evening_available: bool

class DoctorAvailabilityUpdate(TunedModel):
    morning_available: bool
    evening_available: bool

class DoctorAvailabilityResponse(TunedModel):
    date: Date
    morning_available: bool
    evening_available: bool


