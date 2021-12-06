from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.all import Banner

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema
from schemas.banner_schemas import CreateBannerSchema


get_db = db_conn.get_db

router = APIRouter(tags=["Banner"])


@router.post("/create_banner/{facility_id}")
def create_banner(facility_id, request:CreateBannerSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_banner = Banner(
        facility_id=facility_id,
        city_id=city_id,
        banner_type = request.banner_type,
        start_at = request.start_at,
        end_at= request.end_at,
        url= request.url,
        status= request.status,   
    )
    db.add(new_banner)
    try:
        db.commit()
    except Exception as x:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(new_banner)
    return new_banner

@router.get("/get_banner/{banner_id}")
def get_banner(banner_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return banner


@router.get("/get_all_banners")
def get_all_banners(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    banners = db.query(Banner).filter().all()
    return banners


@router.put("/update_banner/{id}")
def update_banner(id, request: CreateBannerSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    banner = db.query(Banner).filter(Banner.id == id).first()

    if not banner:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    if request.facility_id is not None: banner.facility_id = request.facility_id
    if request.city_id is not None: banner.city_id = request.city_id
    if request.banner_type is not None: banner.banner_type = request.banner_type
    # if request.start_at is not None: banner.start_at = request.start_at # must be datetime object
    # if request.end_at is not None: banner.end_at = request.end_at # must be datetime object
    if request.url is not None: banner.url = request.url
    if request.status is not None: banner.status = request.status

    db.add(banner)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(banner)

    return banner

@router.delete("/delete_banner/{id}")
def delete_banner(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    banner = db.query(Banner).filter(Banner.id == id)

    if not banner.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    try:
        banner.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"

