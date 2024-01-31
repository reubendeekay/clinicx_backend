from http import HTTPStatus

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, database, models, config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# SECRET KEY
SECRET_KEY = config.settings.secret_key

# ALGORITHM
ALGORITHM = config.settings.algorithm

# EXPIRATION TIME
EXPIRATION_TIME_MINUTES = config.settings.access_token_expire_minutes


def create_access_token(data: dict):
    print("STARTING")
    print(config.settings.secret_key)
    print(ALGORITHM)
    print(EXPIRATION_TIME_MINUTES)

    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + \
        timedelta(minutes=EXPIRATION_TIME_MINUTES)

    to_encode['exp'] = expires
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


# sourcery skip: avoid-builtin-shadow
def verify_access_token(token: str):  # sourcery skip: avoid-builtin-shadow
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')

        return schemas.TokenData(id=id)
    except JWTError as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token", headers={
                            "WWW-Authenticate": "Bearer"}) from e


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = verify_access_token(token)

    return db.query(models.User).filter(models.User.id == token_data.id).first()
