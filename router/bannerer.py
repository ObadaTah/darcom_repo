from database import db_conn
from fastapi import APIRouter, Depends, HTTPException, status
from models.all import Banner
from schemas.banner_schemas import CreateBannerSchema
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

get_db = db_conn.get_db

router = APIRouter(tags=["Banner"])


@router.post("/create_banner/")
def create_banner(request:CreateBannerSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    city = db.query(City).filter(City.id == request.city_id).all()
    if not any(city):
        return HTTPException(status.HTTP_404_NOT_FOUND, detail='City Not Found')
    facility = db.query(Facilit).filter(Facilit.id == request.facility_id).all()
    if not any(facility):
        return HTTPException(status.HTTP_404_NOT_FOUND, detail='Facility Not Found')

    new_banner = Banner(
        facility_id=request.facility_id,
        city_id=request.city_id,
        banner_type = request.banner_type,
        # start_at = request.start_at,
        # end_at= request.end_at,
        url= request.url,
        status= request.status,   
    )
    db.add(new_banner)

    db.commit()

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

    city = db.query(City).filter(City.id == request.city_id).all()
    if not any(city):
        return HTTPException(status.HTTP_404_NOT_FOUND, detail='City Not Found')

    facility = db.query(Facilit).filter(Facilit.id == request.facility_id).all()
    if not any(facility):
        return HTTPException(status.HTTP_404_NOT_FOUND, detail='Facility Not Found')
        
    if request.facility_id is not None: banner.facility_id = request.facility_id
    if request.city_id is not None: banner.city_id = request.city_id
    if request.banner_type is not None: banner.banner_type = request.banner_type
    # if request.start_at is not None: banner.start_at = request.start_at # must be datetime object
    # if request.end_at is not None: banner.end_at = request.end_at # must be datetime object
    if request.url is not None: banner.url = request.url
    if request.status is not None: banner.status = request.status

    db.add(banner)

    db.commit()

    db.refresh(banner)

    return banner

@router.delete("/delete_banner/{id}")
def delete_banner(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    banner = db.query(Banner).filter(Banner.id == id)

    if not banner.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    banner.delete()
    db.commit()

    return "Deleted Succ"

