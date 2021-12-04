
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from models.all import Facility, Media, FacilityPhoto

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema



get_db = db_conn.get_db

router = APIRouter(tags=["Media"])


def data_parser_and_saver(file):
    # do the saving stuff
    pass

@router.post("/add_facility_photo/{facility_id}")
def get_facility(
    facility_id:int,
    file:UploadFile = File(default=None),
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    data = data_parser_saver(file)
    photo = Media(mediable_type='facility', mediable_id=facility.id,
    # tag=request.tag,
    # disk=request.disk,
    # directory=request.directory,
    # media_tag=request.media_tag,
    # file_name=request.file_name,
    # original_name=request.original_name,
    # extension=request.extension,
    # mime_type=request.mime_type,
    # size=request.size
    )
    db.add(photo)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    photo = FacilityPhoto(facility_id=facility_id, media_id=photo.id)
    db.add(photo)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(photo)


    return photo