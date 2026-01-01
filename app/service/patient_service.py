from fastapi import (
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select 

from ..database.session import get_db
from ..database.model import (
    Patient
)

from ..database.api_models.patient_model import (
    PateintUpdate,
    PateintCreate
)

from .helper import (
    generate_new_patient_id,
    validate_date_format,
    validate_age
)

import datetime

class PatientService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db 

    
    async def create_new_patient_(self, payload: PateintCreate):
        patient_id = generate_new_patient_id()

        query = select(Patient).where(Patient.patient_id == patient_id or Patient.email == payload.email)

        result = await self.db.execute(query)
        existing_patient = result.scalars().first()

        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Patient with patient id: {patient_id} or Email: {payload.email} already exists!"
            )
        
        data_dict = payload.model_dump(exclude={"password", "date_of_birth"})

        # valid_dob: datetime.datetime = validate_date_format(payload.date_of_birth)
        valid_dob = payload.date_of_birth

        if not validate_age(valid_dob):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Minimum age required is 18."
            )
        
        new_patient = Patient(
            patient_id = patient_id, 
            date_of_birth = valid_dob,
            **data_dict
        )
        new_patient.set_password(payload.password)

        self.db.add(new_patient)
        try:
            await self.db.commit()
            await self.db.refresh(new_patient)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        return {
            "message": "Patient created",
            "patient_id": patient_id,
            "email": payload.email
        }
    
    async def get_all_patient_(self)-> list[dict]:
        query = select(Patient)

        result = await self.db.execute(query)
        patients = result.scalars().all()

        summary_list = [
            {"patient_id": patient.patient_id,
            "patient_name": patient.patient_name,
            "email": patient.email,
            "phone_no": patient.phone_no,
            "emergency_contact": patient.emergency_contact}
            for patient in patients
        ]

        return summary_list
    

    async def get_patient_(self, patient_id: str):
        query = (
            select(Patient)
            .where(Patient.patient_id == patient_id)
        )

        result = await self.db.execute(query)
        patient = result.scalars().first()

        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Patient with patient id: {patient_id} found !"
            )

        response = {
            "patient_id": patient.patient_id,
            "patient_name": patient.patient_name,
            "email": patient.email,
            "phone_no": patient.phone_no,
            "emergency_contact": patient.emergency_contact
        }

        return response
    

    async def update_patient_(self,patient_id: str, payload: PateintUpdate):
        query = (
            select(Patient)
            .where(Patient.patient_id == patient_id)
        )

        result = await self.db.execute(query)
        patient = result.scalars().first()

        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Patient with patient id: {patient_id} found !"
            )
        
        update_data = payload.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key == "date_of_birth":
                valid_dob = validate_date_format(value)

                if not validate_age(valid_dob):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Minimum age required is 18."
                    )

                setattr(patient, key, valid_dob)
            else:
                setattr(patient, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(patient)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return {"message": f"Patient with patient id: {patient_id} Updated !"}
    

    async def update_patient_status_(self, patient_id: str, patient_status: bool):
        query = (
            select(Patient)
            .where(Patient.patient_id == patient_id)
        )

        result = await self.db.execute(query)
        patient = result.scalars().first()

        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Patient with patient id: {patient_id} found !"
            )
        
        patient.status = patient_status

        try:
            await self.db.commit()
            await self.db.refresh(patient)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                details=str(e)
            )
    

    async def delete_patient_(self, patient_id: str):
        query = (
            select(Patient)
            .where(Patient.patient_id == patient_id)
        )

        result = await self.db.execute(query)
        patient = result.scalars().first()

        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Patient with patient id: {patient_id} found !"
            )
        
        try:
            self.db.delete(patient)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                details=str(e)
            )
        
        return {"message": f"patient with patient id: {patient_id} deleted !"}
    
