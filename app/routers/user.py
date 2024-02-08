from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..database import SessionLocal, get_db
from .. import models, schemas, utils, communication, oauth2


router = APIRouter(prefix="/users", tags=["users"])
# USERS


@router.get("/", response_model=List[schemas.User])
def get_users(
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return db.query(models.User).all()


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Check if user exists
    user_query = db.query(models.User).filter(models.User.email == user.email)
    if user_query.first() is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="User already exists"
        )

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await communication.send_email(
        email=user.email,
        subject="Welcome to the clinic",
        body=f"Hi {user.first_name}, welcome to the clinic. Your account has been created successfully",
    )
    return new_user


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    user_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    cur = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .delete(synchronize_session=False)
    )

    db.commit()
    if cur is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")


@router.put("/{user_id}", status_code=HTTPStatus.OK)
def update_user(
    user_id: int,
    updated_user: schemas.UserBase,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .update(updated_user.dict(), synchronize_session=False)
    )

    db.commit()
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user
