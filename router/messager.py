from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.all import Message

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema
from schemas.message_schemas import CreateMessageSchema


get_db = db_conn.get_db

router = APIRouter(tags=["Message"])


@router.post("/create_message")
def create_message(request:CreateMessageSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_message = Message(
        messageable_id= request.messageable_id,
        messageable_type= request.messageable_type,
        message_title= request.message_title,
        message_description= request.message_description,
        message_audience= request.message_audience,
        message_reaction= request.message_reaction,
        message_status= request.message_status,
        user_id= get_current_user.id
    )

    db.add(new_message)
    # try:
    db.commit()
    # except Exception as x:
    #     return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(new_message)
    return new_message

@router.get("/get_message/{message_id}")
def get_message(message_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return message


@router.get("/get_all_messages")
def get_all_messages(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    messages = db.query(Message).filter().all()
    return messages


@router.put("/update_message/{id}")
def update_message(id, request: CreateMessageSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    message = db.query(Message).filter(Message.id == id).first()

    if not message:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    if request.messageable_type is not None: message.messageable_type = request.messageable_type
    if request.messageable_id is not None: message.messageable_id = request.messageable_id
    if request.message_title is not None: message.message_title = request.message_title
    if request.message_description is not None: message.message_description = request.message_description
    if request.message_audience is not None: message.message_audience = request.message_audience
    if request.message_reaction is not None: message.message_reaction = request.message_reaction
    if request.message_status is not None: message.message_status = request.message_status

    db.add(message)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(message)

    return message

@router.delete("/delete_message/{id}")
def delete_message(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    message = db.query(Message).filter(Message.id == id)

    if not message.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    try:
        message.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"

