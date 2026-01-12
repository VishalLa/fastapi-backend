from fastapi import (
    APIRouter, 
    Depends,
    status
)
from ..database.api_models.patient_model import (
    PateintCreate,
    PateintUpdate,
    PatientSummary
)
from ..service import PatientService

patient_api_route = APIRouter(prefix="/patient", tags=["Patient"])


@patient_api_route.get(
    "/get/all",
    status_code=status.HTTP_200_OK,
    response_model=list[PatientSummary]
)
async def get_patients(
    service: PatientService = Depends(PatientService)
):
    return await service.get_all_patient_()


@patient_api_route.get(
    "/get/{patient_id}",
    status_code=status.HTTP_200_OK,
    response_model=PatientSummary
)
async def get_doctor(
    patient_id: str,
    service: PatientService = Depends(PatientService)
):
    return await service.get_patient_(patient_id=patient_id)


@patient_api_route.post(
    "/add",
    status_code=status.HTTP_201_CREATED
)
async def create_new_patient(
    payload: PateintCreate,
    service: PatientService = Depends(PatientService)
):
    return await service.create_new_patient_(payload=payload)


@patient_api_route.put(
    "/update/{patient_id}",
    status_code=status.HTTP_200_OK
)
async def update_patient(
    patient_id: str,
    payload: PateintUpdate,
    service: PatientService = Depends(PatientService)
):
    return await service.update_patient_(patient_id=patient_id, payload=payload)


@patient_api_route.delete(
    "/delete/{patient_id}",
    status_code=status.HTTP_200_OK
)
async def delete_patient(
    patient_id: str, 
    service: PatientService = Depends(PatientService)
):
    return await service.delete_patient_(patient_id=patient_id)


@patient_api_route.put(
    "/blacklist/{patient_id}",
    status_code=status.HTTP_200_OK
)
async def blacklist_doctor(
    patient_id: str, 
    service: PatientService = Depends(PatientService)
):
    return await service.update_patient_status_(patient_id=patient_id, patient_status=False)


@patient_api_route.put(
    "/unblacklist/{patient_id}",
    status_code=status.HTTP_200_OK
)
async def unblacklist_doctor(
    patient_id: str, 
    service: PatientService = Depends(PatientService)
):
    return await service.update_patient_status_(patient_id=patient_id, patient_status=True)
