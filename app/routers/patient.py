from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)

@router.get("/", response_model=List[schemas.PatientOut])
def get_patients(db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    return db.query(models.Patient).offset(skip).limit(limit).all()


@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.PatientOut)

def create_patient(patient: schemas.PatientBase, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):


    patient_query = db.query(models.Patient).filter(models.Patient.id == patient.user_id)
    if patient_query.first() is not None:
        raise HTTPException(status_code=HTTPStatus.CONFLICT,
                            detail="Patient already exists")
    

    new_patient = models.Patient(**patient.dict())
    
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.delete("/{patient_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_patient(patient_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    patient_query = db.query(models.Patient).filter(models.Patient.id ==
                                              patient_id)
    patient = patient_query.first()
    if patient is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Patient not found")

    patient_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Patient deleted"}


@router.put("/{patient_id}", status_code=HTTPStatus.OK, response_model=schemas.PatientOut)
def update_patient(patient_id: int, updated_patient: schemas.PatientBase, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).update(
        updated_patient.dict(), synchronize_session=False)
    db.commit()

    if patient is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Patient not found")
    return updated_patient