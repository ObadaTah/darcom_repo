from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.all import Category

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema
from schemas.category_schemas import CreateCategorySchema


get_db = db_conn.get_db

router = APIRouter(tags=["Category"])


@router.post("/create_category")
def create_category(request:CreateCategorySchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    if request.parent_id:
        parent_category = db.query(Category).filter(Category.id == request.parent_id).first()
        if not parent_category:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

        new_category = Category(
            title= request.title,
            parent_id=request.parent_id
        )
        db.add(new_category)
        try:
            db.commit()
        except Exception as x:
            return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

        if new_category.parent_id == parent_category.parent_id:
            return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="CATEGORY CAN'T BE PARENT AND CHILD TO THE SAME CATEGORY")
        db.refresh(new_category)
        return new_category
    
    new_category = Category(
        title= request.title,
        parent_id=request.parent_id
    )
    db.add(new_category)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})
    db.refresh(new_category)
    return new_category


@router.get("/get_category/{category_id}")
def get_category(category_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return category


@router.get("/get_all_categories")
def get_all_categories(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    categories = db.query(Category).filter().all()
    return categories

@router.put("/update_category/{id}")
def update_category(id, request: CreateCategorySchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CATEGORY NOT FOUND")
    if request.parent_id:
        parent_category = db.query(Category).filter(Category.id == request.parent_id).first()
        if not parent_category:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PARENT CATEGORY NOT FOUND")
        if request.title:category.title = request.title
        if request.parent_id:category.parent_id = request.parent_id
        db.add(category)
        try:
            db.commit()
        except Exception as x:
            return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

        if category.parent_id == parent_category.parent_id:
            return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="CATEGORY CAN'T BE PARENT AND CHILD TO THE SAME CATEGORY")
        db.refresh(category)
        return category


    if request.title:category.title = request.title
    if request.parent_id:category.parent_id = request.parent_id

    db.add(category)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(category)

    return category

@router.delete("/delete_category/{id}")
def delete_category(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == id)
    child_catagories = any(db.query(Category).filter(Category.parent_id == id).all())

    if child_catagories:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WE CAN'T DELETE THIS CATEGORY CUZ THERE IS A REFERENCE TO A CHILD CATEGORY")
    if not category.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    try:
        category.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"

