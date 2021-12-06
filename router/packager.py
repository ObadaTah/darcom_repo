from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.all import Package

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema
from schemas.package_schemas import CreatePackageSchema


get_db = db_conn.get_db

router = APIRouter(tags=["Package"])


@router.post("/create_package")
def create_package(request:CreatePackageSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_package = Package(
        title= request.title,
        description= request.description,
        package_type= request.package_type,
        visible= request.visible,   
        quantity= request.quantity,   
        price= request.price,   
    )

    db.add(new_package)
    try:
        db.commit()
    except Exception as x:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(new_package)
    return new_package

@router.get("/get_package/{package_id}")
def get_package(package_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    package = db.query(Package).filter(Package.id == package_id).first()
    if not package:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return package


@router.get("/get_all_packages")
def get_all_packages(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    packages = db.query(Package).filter().all()
    return packages


@router.put("/update_package/{id}")
def update_package(id, request: CreatePackageSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    package = db.query(Package).filter(Package.id == id).first()

    if not package:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    if request.title is not None: package.title = request.title
    if request.description is not None: package.description = request.description
    if request.package_type is not None: package.package_type = request.package_type
    if request.visible is not None: package.visible = request.visible
    if request.quantity is not None: package.quantity = request.quantity
    if request.price is not None: package.price = request.price

    db.add(package)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(package)

    return package

@router.delete("/delete_package/{id}")
def delete_package(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    package = db.query(Package).filter(Package.id == id)

    if not package.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    try:
        package.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"

