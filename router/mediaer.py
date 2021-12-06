
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from PIL import Image 

from models.all import Facility, Media, FacilityPhoto

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema

from datetime import datetime


get_db = db_conn.get_db

router = APIRouter(tags=["Media"])
VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
]
import os.path
from os import path

import random  
import string 
def data_parser_and_saver(file, tag='untaged'):
    extension = ''
    for e in VALID_IMAGE_EXTENSIONS:
        if file.filename.endswith(e):
            extension = e
    if extension == '':
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"text":"File Type Is Not Supported"})

    if not path.exists(f'media/{tag}'):
        os.mkdir(f"media/{tag}")
    try:
        image = Image.open(file.file)
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"text":"Error Occured While Opining The file", "Error":x})

    result = ''.join((random.choice(string.ascii_letters) for _ in range(40)))
    directory = f'media/{tag}/{result}{extension}'
    try:
        image.save(directory)
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"text":"Error Occured While Saving The file", "Error":x})
    return {'directory':directory, 'filename':result, 'extension':extension, "size":os.path.getsize(directory)}



@router.get("/get_facility_media/{facility_id}")
def get_facility_media(facility_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    facility_media = db.query(Media).filter((Media.mediable_type == 'facility' or Media.mediable_id == facility_id)).all()
    if not facility_media:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return facility_media

@router.get("/get_product_media/{product_id}")
def get_product_media(product_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    product_media = db.query(Media).filter(Media.mediable_type == 'product' or Media.mediable_id == product_id).all()
    if not product_media:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    print(product_media)
    return product_media


@router.get("/get_all_media")
def get_all_media(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    media = db.query(Media).filter().all()
    return media

@router.delete("/delete_media/{id}")
def delete_media(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    media = db.query(Media).filter(Media.id == id)
    if not media.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    try:
        media.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"


