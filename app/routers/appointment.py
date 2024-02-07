from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2
from ..communication import send_appointment_email


router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
)


@router.get("/", response_model=List[schemas.AppointmentOut])
def get_appointments(
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    if search != "":
        query = f"SELECT * FROM appointments WHERE reason ILIKE '%{search}%' OR appointment_date ILIKE '%{search}%' OR appointment_time ILIKE '%{search}%'"
        return db.execute(query).fetchall()

    return db.query(models.Appointment).offset(skip).limit(limit).all()


@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(
    appointment_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.AppointmentOut)
async def create_appointment(
    appointment: schemas.AppointmentBase,
    db: SessionLocal = Depends(get_db),
):

    # Check if doctor exists
    doctor = (
        db.query(models.Doctor)
        .filter(models.Doctor.id == appointment.doctor_id)
        .first()
    )
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    user_doctor = db.query(models.User).filter(models.User.id == doctor.user_id).first()
    print(user_doctor.first_name)

    # Check if patient exists
    patient = (
        db.query(models.Patient)
        .filter(models.Patient.id == appointment.patient_id)
        .first()
    )
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    new_appointment = models.Appointment(**appointment.dict())

    # Check if service exists
    service = (
        db.query(models.Service)
        .filter(models.Service.id == appointment.service_id)
        .first()
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    formatted_date = new_appointment.appointment_date
    formatted_time = new_appointment.appointment_time
    print(formatted_date, formatted_time)
    print(user_doctor.email, patient.email)
    print(user_doctor.first_name, patient.first_name)

    await send_appointment_email(
        email=patient.email,
        user=patient.first_name,
        doctor=f"{user_doctor.first_name} {user_doctor.last_name}",
        branch="TBD",
        reason=appointment.reason,
        date=formatted_date,
        time=formatted_time,
    )

    return new_appointment


@router.delete("/{appointment_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_appointment(
    appointment_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    appointment_query = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    )
    appointment = appointment_query.first()
    if appointment is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Appointment not found"
        )

    appointment_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Appointment deleted"}


@router.put(
    "/{appointment_id}",
    status_code=HTTPStatus.OK,
    response_model=schemas.AppointmentOut,
)
def update_appointment(
    appointment_id: int,
    updated_appointment: schemas.AppointmentBase,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .update(updated_appointment.dict(), synchronize_session=False)
    )
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/count", response_model=int)
def get_appointment_count(
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return db.query(func.count(models.Appointment.id)).scalar()


@router.get("/count/{doctor_id}", response_model=int)
def get_appointment_count_by_doctor(
    doctor_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return (
        db.query(func.count(models.Appointment.id))
        .filter(models.Appointment.doctor_id == doctor_id)
        .scalar()
    )


@router.get("/count/{patient_id}", response_model=int)
def get_appointment_count_by_patient(
    patient_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return (
        db.query(func.count(models.Appointment.id))
        .filter(models.Appointment.patient_id == patient_id)
        .scalar()
    )


@router.get("/count/{branch_id}", response_model=int)
def get_appointment_count_by_branch(
    branch_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return (
        db.query(func.count(models.Appointment.id))
        .filter(models.Appointment.branch_id == branch_id)
        .scalar()
    )


# All appointments of a doctor
@router.get("/doctor/{doctor_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_doctor(
    doctor_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.doctor_id == doctor_id)
        .all()
    )


# All appointments of a patient
@router.get("/patient/{patient_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_patient(
    patient_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.patient_id == patient_id)
        .all()
    )


# All appointments of a branch
@router.get("/branch/{branch_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_branch(
    branch_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.branch_id == branch_id)
        .all()
    )


# All appointments of a doctor on a particular date
@router.get("/doctor/{doctor_id}/{date}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_doctor_on_date(
    doctor_id: int,
    date: str,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == doctor_id, models.Appointment.date == date
        )
        .all()
    )


# All appointments of a patient on a particular date
@router.get("/patient/{patient_id}/{date}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_patient_on_date(
    patient_id: int,
    date: str,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return (
        db.query(models.Appointment)
        .filter(
            models.Appointment.patient_id == patient_id, models.Appointment.date == date
        )
        .all()
    )


# All appointments of a branch on a particular date
@router.get("/branch/{branch_id}/{date}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_branch_on_date(
    branch_id: int,
    date: str,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return (
        db.query(models.Appointment)
        .filter(
            models.Appointment.branch_id == branch_id, models.Appointment.date == date
        )
        .all()
    )
