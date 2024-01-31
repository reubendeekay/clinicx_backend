from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


@router.get("/", response_model=List[schemas.PaymentOut])
def get_payments(db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    return db.query(models.Payment).filter(models.Payment.description.ilike(f"%{search}%")).offset(skip).limit(limit).all()


@router.get("/{payment_id}", response_model=schemas.PaymentOut)
def get_payment(payment_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.PaymentOut)
def create_payment(payment: schemas.PaymentBase, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    payment_query = db.query(models.Payment).filter(models.Payment.description == payment.description)
    if payment_query.first() is not None:
        raise HTTPException(status_code=HTTPStatus.CONFLICT,
                            detail="Payment already exists")
    

    new_payment = models.Payment( **payment.dict())
    
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment


@router.delete("/{payment_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_payment(payment_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    payment_query = db.query(models.Payment).filter(models.Payment.id ==
                                              payment_id)
    payment = payment_query.first()
    if payment is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Payment not found")

    payment_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Payment deleted"}



@router.put("/{payment_id}", status_code=HTTPStatus.OK, response_model=schemas.PaymentOut)
def update_payment(payment_id: int, updated_payment: schemas.PaymentBase, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).update(
        updated_payment.dict(), synchronize_session=False)
    db.commit()

    if payment is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Payment not found")
    
    return updated_payment


@router.get("/count", response_model=int)
def get_payment_count(db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(func.count(models.Payment.id)).scalar()

#Payments for a specific patient
@router.get("/count/{patient_id}", response_model=int)
def get_payment_count_by_patient(patient_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(func.count(models.Payment.id)).filter(models.Payment.appointment.patient_id == patient_id).scalar()

#Payments for a specific doctor
@router.get("/count/{doctor_id}", response_model=int)
def get_payment_count_by_doctor(doctor_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(func.count(models.Payment.id)).filter(models.Payment.appointment.doctor_id == doctor_id).scalar()


#Payments for a specific branch
@router.get("/count/{branch_id}", response_model=int)
def get_payment_count_by_branch(branch_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return db.query(func.count(models.Payment.id)).filter(models.Payment.appointment.branch_id == branch_id).scalar()
