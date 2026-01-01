import random 
import datetime
import uuid


def validate_date_format(date_string: str) -> str: 
    """Custom type validator for YYYY-MM-DD format."""
    if date_string is None:
        return 

    return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()


def validate_age(dob: datetime.datetime) -> bool:
    today = datetime.date.today()

    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    return False if age < 18 else True


def generate_new_appointment_id(
    doctor_id: str, 
    patient_id: str, 
    shift: str, 
    date: datetime.date
) -> str:
    
    prefix: str | None = None 
    if shift == "Morning":
        prefix = "M"
    elif shift == "Evening":
        prefix = "E"

    indeces: list[int] = [1, 2, 3]
    index: int = random.choice(indeces)
    uid: str = str(uuid.uuid4()).strip("-")[index]

    patient_id_digit: str = patient_id[1:]
    doctor_id_digit: str = doctor_id[2:]

    day_of_week:str = date.strftime("%a")

    appointment_id: str = str(prefix) + str(uid) + str(day_of_week) + str(patient_id_digit) + str(doctor_id_digit)

    return appointment_id


def generate_new_doctor_id()-> str:
    uid: str = str(uuid.uuid4()).split("-") 
    doctor_id: str = "DR" + str(uid[0] + uid[1])
    return doctor_id


def generate_new_doctor_email(doctor_id: str, hospital_name: str = "XYZ") -> str:
    return f"{doctor_id}-{hospital_name}@gmail.com"


def generate_new_doctor_password(doctor_id: str)-> str: 
    return f"{doctor_id}123" 


def generate_new_patient_id() -> str:
    uid: str = str(uuid.uuid4()).split('-')
    patient_id: str = 'P' + str(uid[0] + uid[1])
    return patient_id


def generate_new_doctor_availability(doctor_id: str, iter: int):
    uid: str = str(uuid.uuid4())
    return f"{doctor_id}_{uid}_{iter}"
