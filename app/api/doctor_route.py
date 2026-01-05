from fastapi import (
    APIRouter, 
    Depends,
    status
)
from ..database.api_models.doctor_model import (
    DoctorCreate,
    DoctorSummary,
    DoctorUpdate,
)
from ..service.doctor_availabiliry_service import DoctorAvailabilityService
from ..service.doctor_service import DoctorService

admin_doctor_api_route = APIRouter(prefix="/admin/doctor", tags=["Doctor"])


@admin_doctor_api_route.get(
    "/get/all",
    status_code=status.HTTP_200_OK,
    response_model=list[DoctorSummary]
)
async def get_doctors(
    service: DoctorService = Depends(DoctorService)
):
    return await service.get_all_doctors_()


@admin_doctor_api_route.get(
    "/get/{doctor_id}", 
    status_code=status.HTTP_200_OK,
    response_model=DoctorSummary
)
async def get_doctor(
    doctor_id: str,
    service: DoctorService = Depends(DoctorService)
):
    return await service.get_doctor_(doctor_id=doctor_id)


@admin_doctor_api_route.post(
    "/add", 
    status_code=status.HTTP_201_CREATED
)
async def create_new_doctor(
    payload: DoctorCreate,
    doctor_service: DoctorService = Depends(DoctorService),
    availability_service: DoctorAvailabilityService = Depends(DoctorAvailabilityService)
):
    doctor_response =  await doctor_service.create_new_doctor_(payload=payload)
    doctor_id = doctor_response["doctor_id"]
    _ = await availability_service.create_availability_for_week(doctor_id=doctor_id)
    return doctor_response



@admin_doctor_api_route.put(
    "/update/{doctor_id}",
    status_code=status.HTTP_200_OK
)
async def update_doctor(
    doctor_id: str,
    payload: DoctorUpdate,
    service: DoctorService = Depends(DoctorService)
):
    return await service.update_doctor_(doctor_id=doctor_id, payload=payload)


@admin_doctor_api_route.delete(
    "/delete/{doctor_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_doctor(
    doctor_id: str, 
    service: DoctorService = Depends(DoctorService)
):
    return await service.delete_doctor_(doctor_id=doctor_id)


@admin_doctor_api_route.put(
    "/blacklist/{doctor_id}",
    status_code=status.HTTP_200_OK
)
async def blacklist_doctor(
    doctor_id: str,
    service: DoctorService = Depends(DoctorService)
):
    return await service.update_doctor_status_(doctor_id=doctor_id, doctor_status=False)


@admin_doctor_api_route.put(
    "/unblacklist/{doctor_id}",
    status_code=status.HTTP_200_OK
)
async def unblacklist_doctor(
    doctor_id: str,
    service: DoctorService = Depends(DoctorService)
):
    return await service.update_doctor_status_(doctor_id=doctor_id, doctor_status=True)
