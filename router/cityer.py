from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.all import City

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema
from schemas.city_schemas import CreateCitySchema


get_db = db_conn.get_db

router = APIRouter(tags=["City"])


@router.post("/create_city")
def create_city(request:CreateCitySchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_city = City(name= request.name)

    db.add(new_city)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(new_city)
    return new_city

@router.get("/get_city/{city_id}")
def get_city(city_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return city


@router.get("/get_all_cities")
def get_all_cities(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    cities = db.query(City).filter().all()
    return cities


@router.put("/update_city/{id}")
def update_city(id, request: CreateCitySchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    city = db.query(City).filter(City.id == id).first()

    if not city:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    city.name = request.name

    db.add(city)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(city)

    return city

@router.delete("/delete_city/{id}")
def delete_city(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    city = db.query(City).filter(City.id == id)

    if not city.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    try:
        city.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"

