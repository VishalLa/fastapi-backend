from fastapi import (
    APIRouter,
    Depends,
    status
)

from ..database.api_models.appointment_treatment_model import (
    AppointmentCreate,
    AppointmentResponse
)

from ..service import AppointmentService


appointment_api_route = APIRouter(prefix="/appointment", tags=["Appointment"])


@appointment_api_route.get(
    "/get/all",
    status_code=status.HTTP_200_OK,
    response_model=list[AppointmentResponse]
)
async def get_appointments(
    service: AppointmentService = Depends(AppointmentService)
):
    return await service.get_all_appointment()


@appointment_api_route.get(
    "/get/{appointment_id}",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentResponse
)
async def get_appointment_by_appointment_id(
    appointment_id: str, 
    service: AppointmentService = Depends(AppointmentService)
):
    return await service.get_appointment_by_appointment_id_(appointment_id=appointment_id)


@appointment_api_route.get(
    "/get/{patient_id}/{doctor_id}",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentResponse
)
async def get_appointment_by_patient_and_doctor_id(
    doctor_id: str, 
    patient_id: str, 
    service: AppointmentService = Depends(AppointmentService)
):
    return await service.get_appointment_with_patient_and_doctor_(doctor_id=doctor_id, patient_id=patient_id)


@appointment_api_route.delete(
    "/delete/{appointment_id}",
    status_code=status.HTTP_200_OK
)
async def delete_appointment_by_appointment_id(
    appointment_id: str,
    service: AppointmentService = Depends(AppointmentService)
):
    return await service.delete_appointment_by_appointment_id_(appointment_id=appointment_id)


@appointment_api_route.delete(
    "/delete/{patient_id}/{doctor_id}",
    status_code=status.HTTP_200_OK
)
async def delete_appointment_by_patient_and_doctor_id(
    patient_id: str, 
    doctor_id: str, 
    service: AppointmentService = Depends(AppointmentService)
):
    return await service.delete_appointment_by_patient_and_doctor_id_(doctor_id=doctor_id, patient_id=patient_id)


@appointment_api_route.post(
    "/create",
    status_code=status.HTTP_201_CREATED
)
async def create_appointment(
    payload: AppointmentCreate,
    service: AppointmentService = Depends(AppointmentService)
):
    return await service.create_appointment_(payload=payload)


@appointment_api_route.put(
    "/complete/{patient_id}/{doctor_id}/{date}/{shift}",
    status_code=status.HTTP_200_OK
)
async def complete_appointment(
    patient_id: str,
    doctor_id: str,
    date: str,
    shift: str,
    service: AppointmentService = Depends(AppointmentService)
):
    return await service.update_status_(
        patient_id = patient_id,
        doctor_id = doctor_id,
        date = date,
        shift = shift,
        appointment_status = "complete"
    )


@appointment_api_route.put(
    "/cancel/{patient_id}/{doctor_id}/{date}/{shift}",
    status_code=status.HTTP_200_OK
)
async def cancel_appointment(
    patient_id: str,
    doctor_id: str,
    date: str,
    shift: str,
    service: AppointmentService = Depends(AppointmentService)
):
    return await service.update_status_(
        patient_id = patient_id,
        doctor_id = doctor_id,
        date = date,
        shift = shift,
        appointment_status = "cancel"
    )


@appointment_api_route.put(
    "/missed/{patient_id}/{doctor_id}/{date}/{shift}",
    status_code=status.HTTP_200_OK
)
async def missed_appointment(
    patient_id: str,
    doctor_id: str,
    date: str,
    shift: str,
    service: AppointmentService = Depends(AppointmentService)
):
    return await service.update_status_(
        patient_id = patient_id,
        doctor_id = doctor_id,
        date = date,
        shift = shift,
        appointment_status = "missed"
    )


