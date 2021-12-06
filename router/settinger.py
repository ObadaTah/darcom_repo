from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.all import Setting

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema
from schemas.setting_schemas import CreateSettingSchema


get_db = db_conn.get_db

router = APIRouter(tags=["Setting"])


@router.post("/create_setting")
def create_setting(request:CreateSettingSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_setting = Setting(
        key= request.key,
        value= request.value,
    )

    db.add(new_setting)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(new_setting)
    return new_setting

@router.get("/get_setting/{setting_id}")
def get_setting(setting_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if not setting:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return setting


@router.get("/get_all_settings")
def get_all_settings(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    settings = db.query(Setting).filter().all()
    return settings


@router.put("/update_setting/{id}")
def update_setting(id, request: CreateSettingSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    setting = db.query(Setting).filter(Setting.id == id).first()

    if not setting:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    if request.key is not None: setting.key = request.key
    if request.value is not None: setting.value = request.value

    db.add(setting)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(setting)

    return setting

@router.delete("/delete_setting/{id}")
def delete_setting(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    setting = db.query(Setting).filter(Setting.id == id)

    if not setting.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    try:
        setting.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"

