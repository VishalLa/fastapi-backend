from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    Boolean,
    Date,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from .base import Base 
from ..core.security import hash_password, verify_password


class Admin(Base):
    __tablename__ = "admin"
    admin_id = Column(String(8), primary_key=True, nullable=False)
    email = Column(String(25), nullable=False, unique=True)
    password_hash = Column(String(240), nullable=False) 

    def set_password(self, password: str):
        self.password_hash = hash_password(password=password)
    
    def check_password(self, password: str) -> bool:
        return verify_password(
            hashed_password=self.password_hash, 
            plain_password=password
        )


class Doctor(Base):
    __tablename__ = "doctor"
    doctor_id = Column(String(16), primary_key=True, nullable=False)
    doctor_name = Column(String(20), nullable=False)

    email = Column(String(25), nullable=False, unique=True)
    password_hash = Column(String(240), nullable=False)

    gender = Column(String(6), nullable=False)

    qualification = Column(Text, nullable=False)
    experience = Column(Integer, nullable=False)
    special_experience = Column(Integer, nullable=False)
    speciality = Column(Text, nullable=False)

    phone_no = Column(Integer, nullable=False)

    department_id = Column(
        String(20),
        ForeignKey('department.department_id', ondelete="CASCADE"), 
        nullable=False
    )

    status = Column(Boolean, nullable=False)

    appointments = relationship(
        "Appointment",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    department = relationship(
        "Department",
        back_populates="doctors",
        foreign_keys=[department_id]
    )

    def set_password(self, password: str):
        self.password_hash = hash_password(password=password)
    
    def check_password(self, password: str) -> bool:
        return verify_password(
            hashed_password=self.password_hash, 
            plain_password=password
        )
    

class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(String(16), primary_key=True, nullable=False)
    patient_name = Column(String(100), nullable=False)

    email = Column(String(25), nullable=False, unique=True)
    password_hash = Column(String(240), nullable=False)

    gender = Column(String(6), nullable=False)

    phone_no = Column(String(15), nullable=False)
    emergency_contact = Column(String(15))

    date_of_birth = Column(Date, nullable=False)
    address = Column(Text, nullable=False)

    status = Column(Boolean, nullable=False)
    medical_history = Column(Text)

    appointments = relationship(
        "Appointment",
        back_populates="patient",
        cascade="all, delete-orphan"
    )

    def set_password(self, password: str):
        self.password_hash = hash_password(password=password)
    
    def check_password(self, password: str) -> bool:
        return verify_password(
            hashed_password=self.password_hash, 
            plain_password=password
        )
    

class Department(Base):
    __tablename__ = "department"
    department_id = Column(String(20), primary_key=True, nullable=False)
    department_name = Column(String(100), nullable=False)
    head_of_department = Column(String(8), ForeignKey("doctor.doctor_id"))    
    location = Column(String(30), nullable=False)
    description = Column(Text)

    doctors = relationship(
        "Doctor",
        back_populates="department",
        foreign_keys="Doctor.department_id",
        cascade="all, delete-orphan"
    )

    head = relationship(
        "Doctor", 
        foreign_keys=[head_of_department]
    )


class Appointment(Base):
    __tablename__ = "appointment"
    appointment_id = Column(String(32), primary_key=True, nullable=False)
    
    patient_id = Column(String(16), ForeignKey("patient.patient_id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String(16), ForeignKey("doctor.doctor_id", ondelete="CASCADE"), nullable=False)

    visit_type = Column(String(15), nullable=False)
    date = Column(Date, nullable=False)

    shift = Column(String(10), nullable=False)
    status = Column(String(12), nullable=False)
    
    reason = Column(Text) 

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates='appointments')
    treatment = relationship(
        "Treatment", 
        back_populates="appointment", 
        uselist=False, 
        cascade="all, delete-orphan"
    )


class Treatment(Base):
    __tablename__ = "treatment"
    treatment_id = Column(String(8), primary_key=True, nullable=False)
    appointment_id = Column(String(32), ForeignKey("appointment.appointment_id", ondelete="CASCADE"), nullable=False)

    test_done = Column(Text)
    diagonsis = Column(Text)
    prescription = Column(Text)
    follow_up_date = Column(Text)

    appointment = relationship(
        "Appointment",
        back_populates="treatment"
    )


class DoctorAvailability(Base):
    __tablename__ = "doctor_availability"
    availability_id  = Column(String(45), primary_key=True)
    doctor_id = Column(String(16), ForeignKey("doctor.doctor_id"), nullable=False)
    date = Column(Date, nullable=False)
    morning_available = Column(Boolean, default=False)
    evening_available = Column(Boolean, default=True)
