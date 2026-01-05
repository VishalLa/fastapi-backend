from fastapi import Depends

from datetime import datetime, timedelta
from datetime import date as Date
from sqlalchemy.future import select
from sqlalchemy import  and_

from ...database.model import (
    Appointment,
    DoctorAvailability,
    Doctor
)

from datetime import datetime, timedelta
from datetime import date as Date
from sqlalchemy.future import select
from sqlalchemy import and_, delete

from app.database.session import AsyncSessionLocal


class Task:

    @staticmethod
    async def update_appointment_status():
        print(f"[{datetime.now()}] Running update_appointment_status")

        async with AsyncSessionLocal() as db:
            today_date = Date.today()

            query = select(Appointment).where(
                and_(
                    Appointment.status == "Booked",
                    Appointment.date < today_date
                )
            )
            
            result = await db.execute(query)
            appointments = result.scalars().all()

            if not appointments:
                print("No past appointments found.")
                return

            for appointment in appointments:
                appointment.status = "Missed"

            try:
                await db.commit()
                print(f"Updated {len(appointments)} appointments to Missed")
            except Exception as e:
                await db.rollback()
                print(f"Error: {e}")


    @staticmethod
    async def update_availability_dates():
        print(f"[{datetime.now()}] Running update_availability_dates")

        async with AsyncSessionLocal() as db:
            today = Date.today()
            start_of_week = today - timedelta(days=today.weekday())

            # delete past availability
            await db.execute(
                delete(DoctorAvailability).where(
                    DoctorAvailability.date < start_of_week
                )
            )

            doctors = (
                await db.execute(
                    select(Doctor).where(Doctor.status == True)
                )
            ).scalars().all()

            new_availability = [
                DoctorAvailability(
                    doctor_id=doctor.doctor_id,
                    date=start_of_week + timedelta(days=i),
                    morning_available=False,
                    evening_available=False
                )
                for doctor in doctors
                for i in range(7)
            ]

            db.add_all(new_availability)

            try:
                await db.commit()
                print(f"Added {len(new_availability)} availability records")
            except Exception as e:
                await db.rollback()
                print(f"Error: {e}")
