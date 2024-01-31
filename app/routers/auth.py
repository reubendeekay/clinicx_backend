from http import HTTPStatus
from fastapi import Depends, APIRouter, HTTPException
from .. import schemas, models, utils, database, oauth2
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/login",
    tags=["login"]
)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: database.SessionLocal = Depends(database.get_db)):

    credentials = db.query(models.User).filter(
        models.User.email == user.username).first()

    if credentials is None:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail="Incorrect username or password")

    if utils.verify(user.password, credentials.password):
        return oauth2.create_access_token(data={"user_id": credentials.id})

    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail="Incorrect username or password")
