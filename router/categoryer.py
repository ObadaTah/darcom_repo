from database import db_conn
from fastapi import APIRouter, Depends, HTTPException, status
from models.all import Category, SubscribeCategory
from schemas.category_schemas import CreateCategorySchema
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

get_db = db_conn.get_db

router = APIRouter(tags=["Category"])


@router.post("/create_category")
def create_category(request:CreateCategorySchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    if request.parent_id is not None:
        parent_category = db.query(Category).filter(Category.id == request.parent_id).first()
        if not parent_category:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PARENT CATEGORY IS NOT FOUND")

        new_category = Category(
            title= request.title,
            parent_id=request.parent_id
        )

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category
    
    new_category = Category(
        title= request.title
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/get_category/{category_id}")
def get_category(category_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return category


@router.get("/subscribe_user_to_category/{category_id}")
def get_category(category_id: int, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    is_subscribed = db.query(SubscribeCategory).filter_by(subscribable_type='user', subscribable_id=get_current_user.id, category_id=category_id).first()
    if is_subscribed is not None:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="already subscribed")

    subscribe = SubscribeCategory(subscribable_type='user', subscribable_id=get_current_user.id, category_id=category_id)

    db.add(subscribe)
    db.commit()
    db.refresh(subscribe)

    return subscribe

@router.get("/unsubscribe_user_to_category/{category_id}")
def unsubscribe_user_to_category(category_id:int, user_id:int, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    subscribe = db.query(SubscribeCategory).filter_by(subscribable_type='user', subscribable_id=get_current_user.id, category_id=category_id)
    if not subscribe.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")


    subscribe.delete()
    db.commit()
    return 'unsubscribed'





@router.get("/subscribe_facility_to_category/{category_id}")
def subscribe_facility_to_category(category_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    facility = db.query(Facility).filter(Facility.user_id == get_current_user.id).first()
    if not facility:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail='this user have no facility')

    is_subscribed = db.query(SubscribeCategory).filter_by(subscribable_type='facility', subscribable_id=facility.id, category_id=category_id).first()
    if is_subscribed is not None:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="already subscribed")


    subscribe = SubscribeCategory(subscribable_type='facility', subscribable_id=facility.id, category_id=category_id)
    db.add(subscribe)

    db.commit()

    db.refresh(subscribe)
    return subscribe

@router.get("/unsubscribe_facility_to_category/{category_id}")
def unsubscribe_user_to_category(category_id:int, user_id:int, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    facility = db.query(Facility).filter(Facility.user_id == get_current_user.id).first()
    if not facility:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail='this user have no facility')
    
    subscribe = db.query(SubscribeCategory).filter_by(subscribable_type='facility', subscribable_id=facility.id, category_id=category_id)
    if not subscribe.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")


    subscribe.delete()
    db.commit()
    return 'unsubscribe'


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

        if category.parent_id == parent_category.id:
            return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="CATEGORY CAN'T BE PARENT AND CHILD TO THE SAME CATEGORY")

        db.add(category)
        db.commit()
        db.refresh(category)
        return category


    if request.title:category.title = request.title

    db.add(category)
    db.commit()
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

    category.delete()
    db.commit()

    return "Deleted Succ"

