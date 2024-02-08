from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2
from ..communication import send_user_email
import random


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.get("/", response_model=List[schemas.PatientOut])
def get_patients(
    db: SessionLocal = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    if search != "":
        query = f"SELECT * FROM patients WHERE first_name ILIKE '%{search}%' OR last_name ILIKE '%{search}%' OR email ILIKE '%{search}%' OR phone_number ILIKE '%{search}%'"
        return db.execute(query).fetchall()

    return db.query(models.Patient).offset(skip).limit(limit).all()


@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(
    patient_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.PatientOut)
async def create_patient(
    patient: schemas.PatientBase,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    patient_query = db.query(models.Patient).filter(
        models.Patient.phone_number == patient.phone_number
    )
    if patient_query.first() is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Patient already exists"
        )

    new_patient = models.Patient(**patient.dict())

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    await send_user_email(
        email=new_patient.email,
        user=new_patient.first_name,
        # body=f"Hi {new_patient.first_name}, welcome to the clinic. Your account has been created successfully. Your patient id is {new_patient.id} and use your phone number to always access our services.",
    )
    return new_patient


@router.delete("/{patient_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_patient(
    patient_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    patient_query = db.query(models.Patient).filter(models.Patient.id == patient_id)
    patient = patient_query.first()
    if patient is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Patient not found"
        )

    patient_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Patient deleted"}


@router.patch("/{patient_id}", status_code=HTTPStatus.OK)
def update_patient(
    patient_id: int,
    updated_patient: schemas.PatientBase,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    patient = (
        db.query(models.Patient)
        .filter(models.Patient.id == patient_id)
        .update(updated_patient.dict(), synchronize_session=False)
    )
    db.commit()

    if patient is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Patient not found"
        )
    return updated_patient


# Implement patient login
@router.post("/login", response_model=schemas.User)
async def login_patient(
    user: schemas.PatientLogin,
    db: SessionLocal = Depends(get_db),
):
    if user.email is None or user.phone_number is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email or phone number is required",
        )

    patient = (
        db.query(models.Patient)
        .filter(
            models.Patient.email == user.email
            or models.Patient.phone_number == user.phone_number
        )
        .first()
    )

    if patient is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Patient not found"
        )

    # Generate OTP randomly of 4 digits
    otp = random.randint(1000, 9999)

    # Save the OTP in the database
    otp_data = models.OTP(user_id=patient.id, otp=otp)
    db.add(otp_data)
    db.commit()
    db.refresh(otp_data)

    # Send the OTP to the patient
    await send_user_email(
        email=patient.email,
        user=patient.first_name,
        body=f"Hi {patient.first_name}, welcome to the clinic. Your OTP is {otp}.",
    )
    print(otp)

    return {"message": "OTP sent"}
