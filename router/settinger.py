from database import db_conn
from fastapi import APIRouter, Depends, HTTPException, status
from models.all import Setting
from schemas.setting_schemas import CreateSettingSchema
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

get_db = db_conn.get_db

router = APIRouter(tags=["Setting"])


@router.post("/create_setting")
def create_setting(request:CreateSettingSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_setting = Setting(
        key= request.key,
        value= request.value,
    )

    db.add(new_setting)
    db.commit()
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
    db.commit()
    db.refresh(setting)

    return setting

@router.delete("/delete_setting/{id}")
def delete_setting(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    setting = db.query(Setting).filter(Setting.id == id)

    if not setting.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")


    setting.delete()

    return "Deleted Succ"

