from database import db_conn
from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile, status)
from models.all import (Facility, FacilityPhoto, FacilityPhotoLike, Media,
                        SubscribeFacility)
from schemas.facility_schemas import CreateFacilitySchema
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

from .mediaer import data_parser_and_saver

get_db = db_conn.get_db

router = APIRouter(tags=["Facility"])


def add_facility_photo(
    facility_id: int,
    tag: str,
    file: UploadFile = File(default=None),
    db: Session = Depends(get_db),
):
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    data = data_parser_and_saver(file, "asdasdas")
    if type(data) is not dict:
        return data

    media = Media(
        mediable_type="facility",
        mediable_id=facility.id,
        tag=tag,
        disk="local",
        directory=data["directory"],
        media_tag=tag,
        file_name=data["filename"],
        original_name=file.filename,
        extension=data["extension"],
        mime_type=data["extension"],
        size=data["size"],
    )

    db.add(media)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    photo = FacilityPhoto(facility_id=facility_id, media_id=media.id)
    db.add(photo)

    db.commit()

    db.refresh(photo)
    return True


@router.post("/create_facility")
def create_facility(
    request: CreateFacilitySchema = Depends(),
    file: UploadFile = File(default=None),
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    city = db.query(City).filter(City.id == request.city_id).first()
    if not city:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="city not found")

    new_facility = Facility(
        name=request.name,
        user_id=get_current_user.id,
        owner_name=request.owner_name,
        owner_number=request.owner_number,
        mobile_number=request.mobile_number,
        building=request.building,
        email=request.email,
        floor=request.floor,
        street=request.street,
        balance=request.balance,
        city_id=request.city_id,
        description=request.description,
        notes=request.notes,
        latitude=request.latitude,
        longitude=request.longitude,
        instagram_url=request.instagram_url,
        facebook_url=request.facebook_url,
        name_subscription=request.name_subscription,
        disabled=False,
        visible=True,
        #   end_subscription_date=request.end_subscription_date,
    )

    db.add(new_facility)
    db.commit()

    if file is not None:
        photo = add_facility_photo(
            file=file, tag=request.tag, db=db, facility_id=new_facility.id
        )
        if type(photo) is not bool:
            return HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                detail={"error at photo commiting": photo},
            )

    db.refresh(new_facility)
    return new_facility


@router.get("/get_facility/{facility_id}")
def get_facility(
    facility_id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return facility


@router.get("/get_all_facilities")
def get_all_facilities(
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    facilities = db.query(Facility).filter().all()
    return facilities


@router.get("/subscribe_user_to_facility/{facility_id}")
def get_facility(
    facility_id: int,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail='facility not found')
    
    is_subscribed = (
        db.query(SubscribeFacility)
        .filter_by(
            subscribable_type="user", subscribable_id=get_current_user.id, facility_id=facility_id
        )
        .first()
    )
    if is_subscribed is not None:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="already subscribed"
        )

    subscribe = SubscribeFacility(
        subscribable_type="user", subscribable_id=get_current_user.id, facility_id=facility_id
    )

    db.add(subscribe)
    db.commit()
    db.refresh(subscribe)

    return subscribe


@router.put("/update_facility/{id}")
def update_facility(
    id,
    request: CreateFacilitySchema = Depends(),
    file: UploadFile = File(default=None),
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    facility = db.query(Facility).filter(Facility.id == id).first()

    if not facility:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FACILITY NOT FOUND")

    if request.name:
        facility.name = request.name
    if request.owner_name:
        facility.owner_name = request.owner_name
    if request.owner_number:
        facility.owner_number = request.owner_number
    if request.mobile_number:
        facility.mobile_number = request.mobile_number
    if request.building:
        facility.building = request.building
    if request.email:
        facility.email = request.email
    if request.floor:
        facility.floor = request.floor
    if request.street:
        facility.street = request.street
    if request.balance:
        facility.balance = request.balance
    if request.city_id:
        facility.city_id = request.balance
    if request.description:
        facility.description = request.description
    if request.notes:
        facility.notes = request.notes
    if request.latitude:
        facility.latitude = request.latitude
    if request.longitude:
        facility.longitude = request.longitude
    if request.instagram_url:
        facility.instagram_url = request.instagram_url
    if request.facebook_url:
        facility.facebook_url = request.facebook_url
    if request.disabled:
        facility.disabled = False
    if request.visible:
        facility.visible = True
    # if (request.end_subscription_date):
    #     facility.end_subscription_date=request.end_subscription_date
    
    if file is not None:
        photo = add_facility_photo(
            file=file, tag=request.tag, db=db, facility_id=new_facility.id
        )
        if type(photo) is not bool:
            return HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                detail={"error at photo commiting": photo},
            )
        # Delete The Previous Photo With The Same Tag

    db.add(facility)

    db.commit()

    db.refresh(facility)

    return facility


@router.delete("/delete_facility/{id}")
def delete_facility(
    id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    facility = db.query(Facility).filter(Facility.id == id)

    if not facility.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    facility.delete()
    db.commit()

    return "Deleted Succ"


@router.post("/add_facility_like/{facility_photo_id}")
def add_facility_like(
    facility_photo_id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    facility_photo = (
        db.query(FacilityPhoto).filter(FacilityPhoto.id == facility_photo_id).first()
    )
    if not facility_photo:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="facility_photo NOT FOUND "
        )
    facility_photo_like = FacilityPhotoLike(
        facility_photo_id=facility_photo.id, user_id=get_current_user.id
    )

    db.add(facility_photo_like)

    db.commit()

    db.refresh(facility_photo_like)

    return facility_photo_like
