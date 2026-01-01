from fastapi import (
    Depends,
    HTTPException,
    status 
)

from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select 
from sqlalchemy.orm import selectinload
from sqlalchemy import or_ , and_

from ..database.session import get_db 
from ..database.model import (
    Appointment,
    DoctorAvailability
)

from .helper import (
    generate_new_appointment_id,
    validate_date_format
)

from ..database.api_models.appointment_treatment_model import (
    AppointmentResponse,
    AppointmentBase
)

import datetime


class AppointmentService: 
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db 


    async def query_appointment_by_appointment_id_(self, appointment_id: str) -> Appointment:
        query = (
            select(Appointment)
            .options(
                selectinload(
                    Appointment.doctor,
                    Appointment.patient
                )
            )
            .where(
                and_(
                    Appointment.appointment_id == appointment_id,
                    Appointment.patient.status == True,
                    Appointment.doctor.status == True
                )
            )
        )

        result = await self.db.execute(query)
        appointment = result.scalars().first()

        return appointment
    

    async def query_appointment_by_patient_and_doctor_id_(self, doctor_id: str, patient_id: str)-> Appointment:
        query = (
            select(Appointment)
            .options(
                selectinload(
                    Appointment.doctor,
                    Appointment.patient
                )
            )
            .where(
                and_(
                    Appointment.doctor_id == doctor_id,
                    Appointment.patient_id == patient_id,
                    Appointment.doctor.status == True,
                    Appointment.patient.status == True
                )
            )
        )

        result = await self.db.execute(query)
        appointment = result.scalars().first()

        return appointment
    

    async def get_all_appointment(self) -> list[dict]:
        query = select(Appointment)

        result = await self.db.execute(query)
        appointments = result.scalars().all()

        summary_list = [
            {
                "appointment_id": appointment.appointment_id,
                "patient_id": appointment.patient_id,
                "doctor_id": appointment.doctor_id,
                "status": appointment.status,
                "date": appointment.date,
                "shift": appointment.shift
            } for appointment in appointments
        ]

        return summary_list

    
    async def get_appointment_by_appointment_id_(self, appointment_id: str)-> AppointmentResponse:
        appointment = await self.query_appointment_by_appointment_id_(appointment_id=appointment_id)
        
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No appointment with appointment id: {appointment_id} found !"
            )
        
        return appointment

    
    async def get_appointment_with_patient_and_doctor_(self, doctor_id: str, patient_id: str)-> AppointmentResponse:
        appointment = await self.query_appointment_by_patient_and_doctor_id_(doctor_id=doctor_id, patient_id=patient_id)

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No appointment with patient id: {patient_id} and doctor id: {doctor_id} found !"
            )
        
        return appointment
    
    
    async def delete_appointment_by_appointment_id_(self, appointment_id: str):
        appointment = await self.query_appointment_by_appointment_id_(appointment_id=appointment_id)
        
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No appointment with appointment id: {appointment_id} found !"
            )
        
        try:
            await self.db.delete(appointment)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return {"message": f"appointment with appointment id: {appointment_id} deleter"}
    

    async def delete_appointment_by_patient_and_doctor_id_(self, doctor_id: str, patient_id: str):
        appointment = await self.query_appointment_by_patient_and_doctor_id_(doctor_id=doctor_id, patient_id=patient_id)

        if not appointment: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No appointment with patient id: {patient_id} and doctor id: {doctor_id} found !"
            )
        
        try:
            await self.db.delete(appointment)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return {"message": f"appointment with doctor id: {doctor_id} and patient id: {patient_id} deleter"}
    

    async def create_appointment_(self, payload: AppointmentBase):
        valid_date = validate_date_format(payload.date)

        query = (
            select(Appointment)
            .options(
                selectinload(
                    Appointment.doctor,
                    Appointment.patient
                )
            )
            .where(
                and_(
                    Appointment.patient_id == payload.patient_id,
                    Appointment.doctor_id == payload.doctor_id,
                    Appointment.date == valid_date,
                    Appointment.shift == payload.shift,
                    Appointment.visit_type == payload.visit_type
                )
            )
        )

        result = await self.db.execute(query)
        existing_appointment = result.scalars().first()

        if existing_appointment:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Appointment with patient id: {payload.patient_id} for doctor id: {payload.doctor_id} at date: {payload.date} already exists!"
            )
        

        query_doctor_availability = (
            select(DoctorAvailability)
            .where(
                DoctorAvailability.doctor_id == payload.doctor_id,
                DoctorAvailability.date == valid_date
            )
        )

        result_doctor_availability = await self.db.execute(query_doctor_availability)
        doctor_availability = result_doctor_availability.scalars().first()

        if not doctor_availability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Doctor is not avaliable on: {valid_date}"
            )
        

        is_available: str | None = None 
        if payload.shift == "Morning" and doctor_availability.morning_available:
            is_available = "Morning"
        elif payload.shift == "Evening" and doctor_availability.evening_available:
            is_available = "Evening"

        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"doctor is not available at asked shift !"
            )

        appointment_id: str = generate_new_appointment_id(
            patient_id=payload.patient_id, 
            doctor_id=payload.doctor_id,
            shift=payload.shift,
            date=valid_date
        )

        new_appointment = Appointment(
            appointment_id = appointment_id,
            patient_id = payload.patient_id,
            doctor_id = payload.doctor_id,
            visit_type = payload.visit_type,
            date = valid_date,
            shift = payload.shift,
            status = "Booked",
            reason = payload.reason
        )

        self.db.add(new_appointment)
        try:
            await self.db.commit()
            await self.db.refresh(new_appointment)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        return {
            "message": "Appointment created",
            "appointment_id": appointment_id,
        }
    

    async def update_status_(self, patient_id: str, doctor_id: str, date: datetime.datetime, shift: str, appointment_status: str):
        query = (
            select(Appointment)
            .options(
                selectinload(
                    Appointment.doctor,
                    Appointment.patient
                )
            )
            .where(
                and_(
                    Appointment.doctor_id == doctor_id,
                    Appointment.patient_id == patient_id,
                    Appointment.date == validate_date_format(date),
                    Appointment.shift == shift
                )
            )
        )

        result = await self.db.execute(query)
        appointment = result.scalars().first()

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No appointment found!"
            )

        if appointment_status not in {"complete", "cancel", "missed"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid appointment status"
            )
        
        appointment.status = appointment_status

        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return {
            "message": f"Appointment marked as {appointment_status}"
        }

