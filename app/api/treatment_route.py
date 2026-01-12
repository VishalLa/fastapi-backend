from fastapi import (
    APIRouter,
    Depends,
    status
)

from ..database.api_models.appointment_treatment_model import (
    PatientHistoryData,
    TreatmentCreate
)

from ..service import TreatmentService

treatment_api_route = APIRouter(prefix="/treatment", tags=["Treatment"])

@treatment_api_route.get(
    "/history/{patient_id}",
    status_code=status.HTTP_200_OK,
    response_model=PatientHistoryData
)
async def get_patient_history(
    patient_id: str,
    service: TreatmentService = Depends(TreatmentService)
):
    return await service.get_patient_history_(patient_id=patient_id)


@treatment_api_route.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
)
async def create_treatment(
    payload: TreatmentCreate,
    service: TreatmentService = Depends(TreatmentService)
):
    return service.create_new_treatment_(payload=payload)
