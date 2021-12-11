import datetime
from datetime import timedelta
from typing import Optional

from database import db_conn
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.all import LoginHistory, User, UserLoginHistory
from schemas.user_schemas import UserSchema
from security.encryption import pwd_cxt
from security.JWToken import (ACCESS_TOKEN_EXPIRE_MINUTES, Roler,
                              create_access_token)
from security.validators import validate_email, validate_password
from sqlalchemy.orm import Session

get_db = db_conn.get_db
router = APIRouter(tags=["auth"])


@router.post("/login")
def login(
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 900,
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Doesn't Exist")

    if not pwd_cxt.verify(request.password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Password Doesn't Match")

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    login_history = LoginHistory()

    db.add(login_history)
    db.commit()
    db.refresh(login_history)

    user_login_history = UserLoginHistory(history_id=login_history.id, user_id= user.id)
    db.add(user_login_history)
        
    db.commit()

    return {"access_token": access_token, "token_type": "bearer", "user": user}


@router.post("/register")
def register(request: UserSchema, db: Session = Depends(get_db)):
    # if not Roler.role(1, db, 'register'):
    #     return HTTPException(status.HTTP_401_UNAUTHORIZED, detail={'error': "NO PERMISSION"})
    # validators to be uncommented when we release

    # password = validate_password(request.password)
    # if not (type(password) == bool and password==True):
    #     return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=password)
    # email = validate_email(request.email)
    # if not email:
    #     return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="email is not valid")

    other_users = db.query(User).filter(User.username==request.username).all()
    if any(other_users):
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="username already exist")

    other_users = db.query(User).filter(User.email==request.email).all()
    if any(other_users):
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="email already exist")
        
    hashed_password = pwd_cxt.hash(request.password)
    new_user = User(
        username=request.username, password=hashed_password, email=request.email
    )

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.username})

    return {"User": new_user, "access_token": access_token, "token_type": "bearer"}

