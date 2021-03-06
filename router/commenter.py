from database import db_conn
from fastapi import APIRouter, Depends, HTTPException, status
from models.all import Comment
from schemas.comment_schemas import CreateCommentSchema, UpdateCommentSchema
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

get_db = db_conn.get_db

router = APIRouter(tags=["Comment"])


@router.post("/create_comment")
def create_comment(request:CreateCommentSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_comment = Comment(
        commentable_id= request.commentable_id,
        commentable_type= request.commentable_type,
        comment_text= request.comment_text,
        comment_rate= request.comment_rate,
        comment_status= request.comment_status,
        user_id= get_current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.get("/get_comment/{comment_id}")
def get_comment(comment_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return comment


@router.get("/get_all_comments")
def get_all_comments(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    comments = db.query(Comment).filter().all()
    return comments


@router.put("/update_comment/{id}")
def update_comment(id, request: UpdateCommentSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == id).first()
    if not comment:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")


    if request.comment_text is not None: comment.comment_text = request.comment_text
    if request.comment_rate is not None: comment.comment_rate = request.comment_rate
    if request.comment_status is not None: comment.comment_status = request.comment_status

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


@router.delete("/delete_comment/{id}")
def delete_comment(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == id)

    if not comment.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    comment.delete()
    db.commit()

    return "Deleted Succ"

