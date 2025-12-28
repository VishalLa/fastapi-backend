import asyncio

from fastapi import (
    Depends, 
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from sqlalchemy.orm import selectinload
from sqlalchemy import or_

from ..database.session import get_db
from ..database.model import (
    Doctor,
    Department,
    Patient,
    Appointment
)

class AdminService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db 

    
    async def query_(self, query_string: str):
        search_item = f"%{query_string}%"

        doctor_query = (
            select(Doctor)
            .options(selectinload(Doctor.department))
            .where(
                or_(
                    Doctor.doctor_id.like(search_item),
                    Doctor.doctor_name.like(search_item),
                    Doctor.email.like(search_item),
                    Doctor.phone_no.like(search_item)
                )
            )
        )

        patient_query = (
            select(Patient)
            .where(
                or_(
                    Patient.patient_id.like(search_item),
                    Patient.patient_name.like(search_item),
                    Patient.phone_no.like(search_item),
                    Patient.emergency_contact.like(search_item)
                )
            )
        )

        appointment_query = (
            select(Appointment)
            .where(
                or_(
                    Appointment.appointment_id.like(search_item),
                    Appointment.doctor_id.like(search_item),
                    Appointment.patient_id.like(search_item),
                    Appointment.visit_type.like(search_item),
                    Appointment.status.like(search_item),
                )
            )
        )

        department_query = (
            select(Department)
            .where(
                or_(
                    Department.department_id.like(search_item),
                    Department.department_name.like(search_item),
                    Department.head_of_department.like(search_item),
                    Department.location.like(search_item),
                    Department.description.like(search_item)
                )
            )
        )

        doctor_result = await self.db.execute(doctor_query)
        patient_result = await self.db.execute(patient_query)
        appointment_result = await self.db.execute(appointment_query)
        deaprtment_result = await self.db.execute(department_query)
        

        doctors = doctor_result.scalars().all()
        patients = patient_result.scalars().all()
        appointments = appointment_result.scalars().all() 
        departments = deaprtment_result.scalars().all()

        return {
            "doctors": [
                {
                    "doctor_id": d.doctor_id,
                    "doctor_name": d.doctor_name,
                    "phone_no": str(d.phone_no),
                    "department_name": d.department.department_name if d.department else "Null"
                } for d in doctors
            ],
            "patients": [
                {
                    "patient_id": p.patient_id,
                    "patient_name": p.patient_name,
                    "email": p.email,
                    "phone_no": str(p.phone_no),
                    "emergency_contact": str(p.emergency_contact)
                } for p in patients
            ],
            "appointments": [
                {
                    "appointment_id": a.appointment_id,
                    "doctor_id": a.doctor_id,
                    "patient_id": a.patient_id,
                    "visit_type": a.visit_type,
                    "date": str(a.date),
                    "status": str(a.status)
                } for a in appointments
            ],
            "departments": [
                {
                    "department_id": dp.department_id,
                    "department_name": dp.department_name,
                    "head": dp.head_of_department,
                    "location": dp.location
                } for dp in departments
            ]
        }
    