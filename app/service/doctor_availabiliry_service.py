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
    Doctor,
    DoctorAvailability
)

from ..database.api_models.doctor_availability_model import (
    DoctorAvailabilityUpdate,
    DoctorAvailabilityResponse
)

# from .helper import generate_new_doctor_availability

from datetime import date, timedelta, datetime


class DoctorAvailabilityService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db 


    async def get_availabilites(self, doctor_id: str):
        query = (
            select(DoctorAvailability)
            .where(
                DoctorAvailability.doctor_id == doctor_id
            )
        )

        result = await self.db.execute(query)
        availabilites = result.scalars().all()

        if not availabilites:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No availabilites found for doctor id: {doctor_id}"
            )

        summary_availabilites = [
            {
                "date": availability.date,
                "morning_available": availability.morning_available,
                "evening_available": availability.evening_available
            } for availability in availabilites
        ]

        return {doctor_id: summary_availabilites}


    async def create_availability_for_week(self, doctor_id: str):

        today_date = date.today()
        start_of_week = today_date - timedelta(days=today_date.weekday())
        # end_of_week = start_of_week + timedelta(days=6)

        avalibility_list: list[DoctorAvailability] = []
        
        for i in range(7):
            # availability_id  = generate_new_doctor_availability(doctor_id=doctor_id, iter=i)
            current_date = start_of_week + timedelta(days=i)

            query = (
                select(DoctorAvailability).
                where(
                    and_(
                        DoctorAvailability.doctor_id == doctor_id,
                        DoctorAvailability.date == current_date
                    )
                )
            )

            result = await self.db.execute(query)
            existing_date = result.scalars().first()

            if existing_date:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Avalibility already exists"
                )
            
            new_avalibility = DoctorAvailability(
                doctor_id = doctor_id,
                date = current_date,
                morning_available = False,
                evening_available = False
            )

            avalibility_list.append(new_avalibility)

        self.db.add_all(avalibility_list)
        try: 
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return {"message": f"Availability added for doctor id: {doctor_id}"}
            
    
    async def update_availability(self,doctor_id: str, date: datetime,payload: DoctorAvailabilityUpdate):
        query = (
            select(DoctorAvailability)
            .where(
                and_(
                    DoctorAvailability.doctor_id == doctor_id,
                    DoctorAvailability.date == date
                )
            )
        )

        result = await self.db.execute(query)
        availability = result.scalars().first()

        if not availability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No availability found for doctor id: {doctor_id} for date: {date}"
            )
        
        availability.morning_available = payload.morning_available 
        availability.evening_available = payload.evening_available 

        try:
            await self.db.commit()
            await self.db.refresh(availability)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return {"message": f"availability update for doctor id: {doctor_id} for date: {date}"}
    

    async def delete_availabilites(self, doctor_id: str):
        query = (
            select(DoctorAvailability)
            .where(
                DoctorAvailability.doctor_id == doctor_id
            )
        )

        result = await self.db.execute(query)
        availabilites = result.scalars().all()

        if not availabilites:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No availabilites found for doctor id: {doctor_id}"
            )
        
        for availability in availabilites:
            await self.db.delete(availability)

        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        return {"message": f"availability deleted for doctor id: {doctor_id}"}
