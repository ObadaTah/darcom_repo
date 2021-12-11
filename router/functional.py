import datetime
from datetime import timedelta

from database import db_conn
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from models.all import (Category, Story, SubscribeCategory, SubscribeFacility,
                        User)
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

get_db = db_conn.get_db
router = APIRouter(tags=["Home"])


@router.get("/")
def home(
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == get_current_user.id).first()
    categories_sub = (
        db.query(SubscribeCategory)
        .filter_by(subscribable_type="user", subscribable_id=get_current_user.id)
        .all()
    )
    categories = {"categories": [], 'sub_categories':[]}
    for category in categories_sub:
        category =  db.query(Category).filter(Category.id == category.id).first()
        if category.parent_id is None: 
            categories["categories"].append(
                category
            )
        else:
            categories['sub_categories'].append(category)

    facilities = (
        db.query(SubscribeFacility)
        .filter_by(subscribable_id=get_current_user.id, subscribable_type="user")
        .all()
    )

    stories = {"story": []}
    for facility in facilities:
        stories["story"].append(
            db.query(Story).filter_by(facility_id=facility.id).all()
        )

    did_login = (timedelta(days=1)>(datetime.datetime.now() - user.last_login))

    user.last_login = datetime.datetime.now()
    if did_login == False:
        user.current_day += 1
    db.add(user)
    # db.commit()
    db.refresh(user)
    # print(stories['story'][0][1].id)
    return stories, user, categories, {'did_login':did_login}
