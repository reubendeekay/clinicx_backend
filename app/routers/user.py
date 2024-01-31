from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..database import SessionLocal, get_db
from .. import models, schemas, utils


router = APIRouter(
    prefix="/users",
    tags=["users"]

)
# USERS


@router.get("/", response_model=List[schemas.User])
def get_users(db: SessionLocal = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, db: SessionLocal = Depends(get_db)):

    cur = db.query(models.User).filter(models.User.id ==
                                       user_id).delete(synchronize_session=False)

    db.commit()
    if cur is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")


@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=schemas.User)
def update_user(user_id: int, updated_user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).update(
        updated_user.dict(), synchronize_session=False)
    db.commit()

    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")
    return updated_user
