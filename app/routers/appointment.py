from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
)


@router.get("/", response_model=List[schemas.AppointmentOut])
def get_appointments(db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    return db.query(models.Appointment).offset(skip).limit(limit).all()


@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(appointment_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.AppointmentOut)
def create_appointment(appointment: schemas.AppointmentBase, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_appointment = models.Appointment(**appointment.dict())
    
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.delete("/{appointment_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_appointment(appointment_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    appointment_query = db.query(models.Appointment).filter(models.Appointment.id ==
                                              appointment_id)
    appointment = appointment_query.first()
    if appointment is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Appointment not found")

    appointment_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Appointment deleted"}



@router.put("/{appointment_id}", status_code=HTTPStatus.OK, response_model=schemas.AppointmentOut)
def update_appointment(appointment_id: int, updated_appointment: schemas.AppointmentBase, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).update(
        updated_appointment.dict(), synchronize_session=False)
    db.commit()
    db.refresh(appointment)
    return appointment

@router.get("/count", response_model=int)
def get_appointment_count(db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(func.count(models.Appointment.id)).scalar()


@router.get("/count/{doctor_id}", response_model=int)
def get_appointment_count_by_doctor(doctor_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(func.count(models.Appointment.id)).filter(models.Appointment.doctor_id == doctor_id).scalar()


@router.get("/count/{patient_id}", response_model=int)
def get_appointment_count_by_patient(patient_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(func.count(models.Appointment.id)).filter(models.Appointment.patient_id == patient_id).scalar()


@router.get("/count/{branch_id}", response_model=int)
def get_appointment_count_by_branch(branch_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(func.count(models.Appointment.id)).filter(models.Appointment.branch_id == branch_id).scalar()


#All appointments of a doctor
@router.get("/doctor/{doctor_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_doctor(doctor_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id).all()


#All appointments of a patient
@router.get("/patient/{patient_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_patient(patient_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()


#All appointments of a branch
@router.get("/branch/{branch_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_branch(branch_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(models.Appointment).filter(models.Appointment.branch_id == branch_id).all()


#All appointments of a doctor on a particular date
@router.get("/doctor/{doctor_id}/{date}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_doctor_on_date(doctor_id: int, date: str, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id, models.Appointment.date == date).all()


#All appointments of a patient on a particular date
@router.get("/patient/{patient_id}/{date}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_patient_on_date(patient_id: int, date: str, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id, models.Appointment.date == date).all()


#All appointments of a branch on a particular date
@router.get("/branch/{branch_id}/{date}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_branch_on_date(branch_id: int, date: str, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(models.Appointment).filter(models.Appointment.branch_id == branch_id, models.Appointment.date == date).all()
