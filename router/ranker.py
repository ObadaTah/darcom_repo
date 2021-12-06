from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.all import Rank

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema
from schemas.rank_schemas import CreateRankSchema


get_db = db_conn.get_db

router = APIRouter(tags=["Rank"])


@router.post("/create_rank")
def create_rank(request:CreateRankSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_rank = Rank(
        title= request.title,
        points_from= request.points_from,
        points_to= request.points_to
    )

    db.add(new_rank)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(new_rank)
    return new_rank

@router.get("/get_rank/{rank_id}")
def get_rank(rank_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    rank = db.query(Rank).filter(Rank.id == rank_id).first()
    if not rank:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return rank


@router.get("/get_all_ranks")
def get_all_ranks(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    ranks = db.query(Rank).filter().all()
    return ranks


@router.put("/update_rank/{id}")
def update_rank(id, request: CreateRankSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    rank = db.query(Rank).filter(Rank.id == id).first()

    if not rank:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    if request.title is not None: rank.title = request.title
    if request.points_from is not None: rank.points_from = request.points_from
    if request.points_to is not None: rank.points_to = request.points_to

    db.add(rank)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(rank)

    return rank

@router.delete("/delete_rank/{id}")
def delete_rank(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    rank = db.query(Rank).filter(Rank.id == id)

    if not rank.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    try:
        rank.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"

