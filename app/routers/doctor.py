from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2
from ..enums import Role


router = APIRouter(prefix="/doctors", tags=["doctors"])


# DOCTORS
@router.get("/", response_model=List[schemas.DoctorOut])
def get_doctors(
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    return db.query(models.Doctor).offset(skip).limit(limit).all()


@router.get("/{doctor_id}", response_model=schemas.DoctorOut)
def get_doctor(
    doctor_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.DoctorOut)
def create_doctor(
    doctor: schemas.DoctorBase,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    doctor_query = db.query(models.Doctor).filter(
        models.Doctor.user_id == doctor.user_id
    )
    if doctor_query.first() is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Doctor already exists"
        )

    new_doctor = models.Doctor(**doctor.dict())
    # Update user role to doctor
    db.query(models.User).filter(models.User.id == doctor.user_id).update(
        {"role": Role.DOCTOR}
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


@router.delete("/{doctor_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_doctor(
    doctor_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    doctor_query = db.query(models.Doctor).filter(models.Doctor.id == doctor_id)
    doctor = doctor_query.first()
    if doctor is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Doctor not found")

    doctor_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Doctor deleted"}


@router.put("/{doctor_id}", status_code=HTTPStatus.OK, response_model=schemas.DoctorOut)
def update_doctor(
    doctor_id: int,
    updated_doctor: schemas.DoctorBase,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    doctor = (
        db.query(models.Doctor)
        .filter(models.Doctor.id == doctor_id)
        .update(updated_doctor.dict(), synchronize_session=False)
    )
    db.commit()

    if doctor is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Doctor not found")
    return updated_doctor
