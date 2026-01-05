import logging

import uvicorn
from fastapi import FastAPI 

from contextlib import asynccontextmanager

from app.database.session import sync_engine, SessionLocal
from app.database.base import Base 
from app.database.model import Admin
from app.core.config import settings

from sqlalchemy.orm import Session

from app.scheduler.scheduler_manager import start_scheduler,  scheduler

from app.api.doctor_route import admin_doctor_api_route
from app.api.department_route import admin_department_api_route
from app.api.patient_route import patient_api_route
from app.api.admin_route import admin_dashboard_api
from app.api.appointment_route import appointment_api_route
from app.api.availability_route import availability_api


logging.basicConfig(
    filename=settings.LOG_FILE,
    format=settings.LOG_FORMAT,
    level=logging.DEBUG if settings.DEBUG else logging.INFO
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--------------------------------------------------------------------")
    print("[STARTUP] Server starting...")

    try:
        Base.metadata.create_all(bind=sync_engine)
        print("[STARTUP] Database tables checked/created")

        db: Session = SessionLocal()

        if not db.query(Admin).filter(Admin.admin_id == "A1").first():
            print("[STARTUP] creating default super admin...")

            super_admin = Admin(
                admin_id="A1",
                email="superadmin@hospital.com"
            )
            super_admin.set_password("admin123")
            db.add(super_admin)
            db.commit()
            
            print("[STARTUP] super admin created successfully.")

    except Exception as e:
        print(f"[STARTUP ERROR]: {e}")
    finally:
        db.close()

    start_scheduler()
    
    print("[STARTUP] Scheduler started")

    print("[STARTUP] Startup complete.")
    print("--------------------------------------")
    
    yield  

    print("[SHUTDOWN] Server shutting down...")
    scheduler.shutdown()
    print("[SHUTDOWN] Scheduler stopped")


app = FastAPI(
    debug=settings.DEBUG,
    title="Hospital Management API",
    lifespan=lifespan
)

app.include_router(admin_doctor_api_route)
app.include_router(admin_department_api_route)
app.include_router(patient_api_route)
app.include_router(admin_dashboard_api)
app.include_router(appointment_api_route)
app.include_router(availability_api)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
