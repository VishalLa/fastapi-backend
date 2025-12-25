from .api_base_model import TunedModel

class DoctorAvailabilityBase(TunedModel):
    doctor_id: str
    morning_available: bool
    evening_available: bool

class DoctorAvailabilityCreate(DoctorAvailabilityBase):
    pass

class DoctorAvailabilityResponse(DoctorAvailabilityBase):
    id: int
