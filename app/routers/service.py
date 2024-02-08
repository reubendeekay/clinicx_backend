from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/services",
    tags=["services"],
)


@router.get("/", response_model=List[schemas.ServiceOut])
def get_services(
    db: SessionLocal = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    if search != "":
        query = f"SELECT * FROM services WHERE name ILIKE '%{search}%' OR price ILIKE '%{search}%'"
        return db.execute(query).fetchall()

    return (
        db.query(models.Service)
        .filter(models.Service.name.ilike(f"%{search}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{service_id}", response_model=schemas.ServiceOut)
def get_service(
    service_id: int,
    db: SessionLocal = Depends(get_db),
):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.ServiceOut)
def create_service(
    service: schemas.ServiceBase,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    service_query = db.query(models.Service).filter(models.Service.name == service.name)
    if service_query.first() is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Service already exists"
        )

    new_service = models.Service(**service.dict())

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@router.delete("/{service_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_service(
    service_id: int,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    service_query = db.query(models.Service).filter(models.Service.id == service_id)
    service = service_query.first()
    if service is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Service not found"
        )

    service_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Service deleted"}


@router.put(
    "/{service_id}",
    status_code=HTTPStatus.OK,
)
def update_service(
    service_id: int,
    updated_service: schemas.ServiceBase,
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    service = (
        db.query(models.Service)
        .filter(models.Service.id == service_id)
        .update(updated_service.dict(), synchronize_session=False)
    )
    db.commit()

    if service is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Service not found"
        )

    return updated_service


@router.get("/count", response_model=int)
def get_service_count(
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return db.query(func.count(models.Service.id)).scalar()


@router.get("/search", response_model=List[schemas.ServiceOut])
def search_service(
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
    search: Optional[str] = "",
):
    return (
        db.query(models.Service).filter(models.Service.name.ilike(f"%{search}%")).all()
    )


@router.get("/search/count", response_model=int)
def search_service_count(
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
    search: Optional[str] = "",
):
    return (
        db.query(func.count(models.Service.id))
        .filter(models.Service.name.ilike(f"%{search}%"))
        .scalar()
    )


@router.get("/search/limit", response_model=List[schemas.ServiceOut])
def search_service_limit(
    db: SessionLocal = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    return (
        db.query(models.Service)
        .filter(models.Service.name.ilike(f"%{search}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )
