from fastapi import (
    Depends, 
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from ..database.session import get_db
from ..database.model import (
    Doctor
)

from ..database.api_models.doctor_model import (
    DoctorCreate, 
    DoctorSummary,
    DoctorUpdate
)

from .helper import (
    generate_new_doctor_id,
    generate_new_doctor_email,
    generate_new_doctor_password
)

class DoctorService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db


    async def create_new_doctor_(self, payload: DoctorCreate):
        doctor_id: str = generate_new_doctor_id()
        doctor_email: str = generate_new_doctor_email(doctor_id=doctor_id)
        doctor_password: str = generate_new_doctor_password(doctor_id=doctor_id)

        query = select(Doctor).where(Doctor.doctor_id == doctor_id)

        result = await self.db.execute(query)
        existing_doctor = result.scalars().first()

        if existing_doctor:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Doctor with doctor id: {doctor_id} already exists!"
            )
        
        new_doctor = Doctor(
            doctor_id = doctor_id,
            doctor_name = payload.doctor_name,
            email = doctor_email,
            gender = payload.gender, 
            qualification = payload.qualification,
            experience = payload.experience,
            special_experience = payload.special_experience,
            speciality = payload.speciality,
            phone_no = payload.phone_no,
            department_id = payload.department_id,
            status = payload.status
        )

        new_doctor.set_password(doctor_password)

        self.db.add(new_doctor)
        try:
            await self.db.commit()
            await self.db.refresh(new_doctor)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        return {
            "message": "Doctor created", 
            "doctor_id": new_doctor.doctor_id
        }
    
    
    async def update_doctor_(self, doctor_id: str, payload: DoctorUpdate):
        query = (
            select(Doctor).
            where(Doctor.doctor_id == doctor_id)
        )
        
        result = await self.db.execute(query)
        doctor = result.scalars().first()

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No doctor with doctor id: {doctor_id} found !"
            )
        
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(doctor, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(doctor)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        return {"message": f"Doctor with doctor id: {doctor_id} Updated !"}
    

    async def update_doctor_status_(self, doctor_id: str, doctor_status: bool):
        query = select(Doctor).where(Doctor.doctor_id == doctor_id)

        result = await self.db.execute(query)
        doctor = result.scalars().first()

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No doctor with doctor id: {doctor_id} found !"
            )
        
        doctor.status = doctor_status

        try:
            await self.db.commit()
            await self.db.refresh(doctor)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return {"message": f"Doctor with doctor id: {doctor_id} status changed to: {doctor_status}"}
    

    async def get_doctor_(self, doctor_id: str) -> DoctorSummary:
        query = (
            select(Doctor)
            .options(selectinload(Doctor.department))
            .where(Doctor.doctor_id == doctor_id)
        )

        result = await self.db.execute(query)
        doctor = result.scalars().first()

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Doctor with doctor id: {doctor_id} found !"
            )
        
        response = {
            "doctor_id": doctor_id,
            "doctor_name": doctor.doctor_name,
            "department_name": doctor.department.department_name,
            "phone_no": str(doctor.phone_no),
        }
        
        return response
        
    
    async def get_all_doctors_(self) -> list[dict]:
        query = (
            select(Doctor).
            options(selectinload(Doctor.department))
        )

        result = await self.db.execute(query)
        doctors = result.scalars().all()

        summary_list = [
            {
                "doctor_id": doc.doctor_id,
                "doctor_name": doc.doctor_name,
                "phone_no": str(doc.phone_no),
                "department_name": doc.department.department_name if doc.department else "Null"
            } for doc in doctors
        ]

        return summary_list


    async def delete_doctor_(self, doctor_id: str):
        query = (
            select(Doctor)
            .where(Doctor.doctor_id == doctor_id)
            ) 
        result = await self.db.execute(query)
        doctor = result.scalars().first()

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No doctor with doctor id: {doctor_id} found !"
            )
        
        try:
            await self.db.delete(doctor)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        return {"message": f"doctor with doctor id: {doctor_id} deleted !"}
    
