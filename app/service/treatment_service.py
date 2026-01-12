from fastapi import (
    Depends,
    HTTPException,
    status 
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_

from ..database.session import get_db
from ..database.model import (
    Appointment,
    Treatment
)

from ..database.api_models.appointment_treatment_model import (
    TreatmentCreate
)

class TreatmentService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db 

    
    async def create_new_treatment_(self, payload: TreatmentCreate):
        appointment_id = payload.appointment_id
        treatment_id = f"T{appointment_id}"

        appointment_query = (
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
                    Appointment.doctor_id == payload.doctor_id,
                    Appointment.patient_id == payload.patient_id,
                    Appointment.status == "Booked",
                    Appointment.patient.status == True,
                    Appointment.doctor.status == True
                )
            )
        )

        appointment_result = await self.db.execute(appointment_query)
        appointment_data = appointment_result.scalars().first()

        if not appointment_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No booked appointment found for this patient and doctor"
            )

        new_treatment = Treatment( 
            treatment_id = treatment_id,
            appointment_id = appointment_id,
            test_done = payload.test_done,
            diagnosis = payload.diagonsis,
            prescription = payload.prescription,
            follow_up_date = payload.follow_up_date
        )

        self.db.add(new_treatment)
        try:
            await self.db.commit()
            await self.db.refresh(new_treatment)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        return {"message": f"Treatment for appointment : {appointment_id} created"}
    

    async def get_patient_history_(self, patient_id):
        query = (
            select(Appointment)
            .options(
                selectinload(Appointment.patient),
                selectinload(Appointment.doctor),
                selectinload(Appointment.treatment)
            )
            .where(
                Appointment.patient_id == patient_id,
                Appointment.status == "complete"
            )
        )

        result = await self.db.execute(query)
        appointments = result.scalars().all()

        if not appointments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No appointment history found for patient id: {patient_id}"
            )

        return {
            "patient_doctor_data": {
                "patient_name": Appointment.patient.patient_name,
                "doctor_name": Appointment.doctor.doctor_name,
            },

            "patient_history": [
                {
                    "visit_type": appointment.visit_type,
                    "test_done": appointment.treatment.test_done if appointment.treatment else None,
                    "diagnosis": appointment.treatment.diagnosis if appointment.treatment else None,
                    "prescription": appointment.treatment.prescription if appointment.treatment else None,
                } for appointment in appointments
            ]
        }
    