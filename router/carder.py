from database import db_conn
from fastapi import APIRouter, Depends, HTTPException, status
from models.all import Card
from schemas.card_schemas import CreateCardSchema
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

get_db = db_conn.get_db

router = APIRouter(tags=["Card"])


@router.post("/create_card/{facility_id}")
def create_card(facility_id:int, request:CreateCardSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FACILITY NOT FOUND")
        
    new_card = Card(
        number= request.number,
        price= request.price,
        facility_id= facility_id,

    )

    db.add(new_card)
    db.commit()

    db.refresh(new_card)
    return new_card

@router.get("/get_card/{card_id}")
def get_card(card_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return card


@router.get("/get_all_cards")
def get_all_cards(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    cards = db.query(Card).filter().all()
    return cards

@router.get("/get_all_facility_cards/{facility_id}")
def get_all_facility_cards(facility_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    cards = db.query(Card).filter(Card.facility_id == facility_id).all()
    return cards


@router.put("/update_card/{id}")
def update_card(id, request: CreateCardSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    card = db.query(Card).filter(Card.id == id).first()
    if not card:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    if request.number:card.number = request.number
    if request.price:card.price = request.price

    db.add(card)

    db.commit()

    db.refresh(card)

    return card

@router.delete("/delete_card/{id}")
def delete_card(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    card = db.query(Card).filter(Card.id == id)

    if not card.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    card.delete()
    db.commit()

    return "Deleted Succ"

