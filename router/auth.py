from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Optional

from models.all import User
from schemas.user_schemas import UserSchema
from database import db_conn

from security.encryption import pwd_cxt
from security.validators import validate_password, validate_email

from sqlalchemy.orm import Session
from datetime import timedelta
from security.JWToken import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, Roler



get_db = db_conn.get_db
router = APIRouter(tags=["auth"])

@router.post("/login")
def login(ACCESS_TOKEN_EXPIRE_MINUTES:Optional[int] = 30, request:OAuth2PasswordRequestForm = Depends(), db:Session =Depends(get_db)):

    user = db.query(User).filter(
        User.username == request.username).first()    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Doesn't Exist")

    if not pwd_cxt.verify(request.password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Password Doesn't Match")

    access_token = create_access_token(data={"sub":user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": access_token, "token_type": "bearer", "user": user}


@router.post("/register")
def register(request: UserSchema, db:Session = Depends(get_db)):
    # if not Roler.role(1, db, 'login'):
    #     return HTTPException(status.HTTP_401_UNAUTHORIZED, detail={'error': "NO PERMISSION"})
    # validators to be uncommented when we release 
    
    # password = validate_password(request.password)
    # if not (type(password) == bool and password==True):
    #     return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=password)
    # email = validate_email(request.email)
    # if not email:
    #     return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="email is not valid")

    # hashed_password = pwd_cxt.hash(request.password)
    # new_user = User(username=request.username, password=hashed_password, email= request.email)

    db.add(new_user)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub":new_user.username})

    return {"User":new_user, "access_token": access_token, "token_type": "bearer"}