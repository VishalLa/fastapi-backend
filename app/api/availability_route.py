from fastapi import (
    APIRouter,
    Depends,
    status
)

from ..service import DoctorAvailabilityService 
from ..database.api_models.doctor_availability_model import (
    DoctorAvailabilityUpdate,
    DoctorAvailabilityResponse
)

from datetime import date


availability_api = APIRouter(prefix="/doctor/availability", tags=["Doctor Availability"])


@availability_api.get(
    "/get/{doctor_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict[str,list[DoctorAvailabilityResponse]]
)
async def get_availability(
    doctor_id: str,
    service: DoctorAvailabilityService = Depends(DoctorAvailabilityService)
):
    return await service.get_availabilites(doctor_id=doctor_id)


@availability_api.post(
    "create/{doctor_id}",
    status_code=status.HTTP_201_CREATED,
)
async def create_availabilitys(
    doctor_id: str,
    service: DoctorAvailabilityService = Depends(DoctorAvailabilityService)
):
    return await service.create_availability_for_week(doctor_id=doctor_id)


@availability_api.put( 
    "/{doctor_id}/{date}",
    status_code=status.HTTP_200_OK
)
async def update_availability_for_day(
    doctor_id: str, 
    date: date, 
    payload: DoctorAvailabilityUpdate,
    service: DoctorAvailabilityService = Depends(DoctorAvailabilityService)
):
    return await service.update_availability(doctor_id=doctor_id, date=date, payload=payload)


@availability_api.delete(
    "/delete/{doctor_id}",
    status_code=status.HTTP_200_OK
)
async def delete_availability(
    doctor_id: str, 
    service: DoctorAvailabilityService = Depends(DoctorAvailabilityService)
):
    return await service.delete_availabilites(doctor_id=doctor_id)
