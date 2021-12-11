from database import db_conn
from fastapi import APIRouter, Depends, HTTPException, status
from models.all import Subscription
from schemas.subscription_schemas import CreateSubscriptionSchema
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

get_db = db_conn.get_db

router = APIRouter(tags=["Subscription"])


@router.post("/create_subscription")
def create_subscription(request:CreateSubscriptionSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_subscription = Subscription(
        title= request.title,
        number_of_months= request.number_of_months,
        number_of_ad_text= request.number_of_ad_text,
        visible= request.visible,   
        cost= request.cost,   
    )

    db.add(new_subscription)
    db.commit()

    db.refresh(new_subscription)
    return new_subscription

@router.get("/get_subscription/{subscription_id}")
def get_subscription(subscription_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return subscription


@router.get("/get_all_subscriptions")
def get_all_subscriptions(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    subscriptions = db.query(Subscription).filter().all()
    return subscriptions


@router.put("/update_subscription/{id}")
def update_subscription(id, request: CreateSubscriptionSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    subscription = db.query(Subscription).filter(Subscription.id == id).first()

    if not subscription:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    if request.title is not None: subscription.title = request.title
    if request.number_of_months is not None: subscription.number_of_months = request.number_of_months
    if request.number_of_ad_text is not None: subscription.number_of_ad_text = request.number_of_ad_text
    if request.visible is not None: subscription.visible = request.visible
    if request.cost is not None: subscription.cost = request.cost

    db.add(subscription)
    db.commit()

    db.refresh(subscription)

    return subscription

@router.delete("/delete_subscription/{id}")
def delete_subscription(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    subscription = db.query(Subscription).filter(Subscription.id == id)

    if not subscription.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")


    subscription.delete()
    db.commit()

    return "Deleted Succ"

