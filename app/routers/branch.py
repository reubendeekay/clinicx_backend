from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/branches",
    tags=["branches"],



)


@router.get("/", response_model=List[schemas.BranchOut])
def get_branches(db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    return db.query(models.Branch).filter(models.Branch.name.ilike(f"%{search}%")).offset(skip).limit(limit).all()


@router.get("/{branch_id}", response_model=schemas.BranchOut)
def get_post(branch_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.BranchOut)
def create_branch(branch: schemas.BranchBase, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    branch_query = db.query(models.Branch).filter(models.Branch.name == branch.name)
    if branch_query.first() is not None:
        raise HTTPException(status_code=HTTPStatus.CONFLICT,
                            detail="Branch already exists")
    


    new_branch = models.Branch( **branch.dict())
    
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)

    return new_branch


@router.delete("/{branch_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_branch(branch_id: int, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
 

    branch_query = db.query(models.Branch).filter(models.Branch.id ==
                                              branch_id)
    branch = branch_query.first()
    if branch is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Branch not found")
    # if branch.owner_id != current_user.id:
    #     raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
    #                         detail="You do not have permission to delete this branch")
    branch_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Branch deleted"}


@router.put("/{branch_id}", status_code=HTTPStatus.OK)
def update_branch(branch_id: int, updated_branch: schemas.BranchBase, db: SessionLocal = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    branch_query = db.query(models.Branch).filter(
        models.Branch.id == branch_id)

    branch = branch_query.first()

    if branch is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Branch not found")
    # if branch.owner_id != current_user.id:
    #     raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
    #                         detail="You do not have permission to delete this branch")
    branch_query.update(updated_branch.dict(), synchronize_session=False)
    db.commit()

    return branch.first()
