from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.all import User, Role, UserRole

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema
from schemas.role_schemas import CreateRoleSchema, UpdateUsersRole




get_db = db_conn.get_db

router = APIRouter(tags=["roles"])


@router.post("/create_role")
def create_role(request:CreateRoleSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_role = Role(name= request.name, description=request.description)

    db.add(new_role)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(new_role)
    return new_role

    
@router.post("/update_users_role/")
def update_user_role(request: UpdateUsersRole, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    role = db.query(Role).filter(Role.id == request.role_id)

    user = db.query(User).filter(User.id == request.user_id)

    new_user_role = UserRole(role_id=request.role_id, user_id=request.user_id)

    db.add(new_user_role)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    return new_user_role

@router.get("/get_role/{id}")
def get_role(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    role = db.query(Role).filter(Role.id == id).first()
    if not role:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return role

@router.get("/get_users_roles/{user_id}")
def get_users_roles(user_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    user_roles = db.query(UserRole).filter(User.id == user_id).all()
    roles_names = {"names": []}
    for user_role in user_roles:
        roles_names["names"].append(db.query(Role).filter(Role.id == user_role.role_id).first())
    
    return roles_names

@router.get("/get_all_roles")
def get_all_roles(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    role = db.query(Role).filter().all()
    return role


@router.put("/update_role/{id}")
def update_role(id, request: CreateRoleSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    role = db.query(Role).filter(Role.id == id)

    if not role.first():

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    role.name = request.name
    role.description = request.description
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})


    return request

@router.delete("/delete_role/{id}")
def delete_role(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    role = db.query(Role).filter(Role.id == id)
    if not role.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    role.delete()
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"




@router.delete("/delete_users_role")
def delete_user_role(request: UpdateUsersRole, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    user_role = db.query(UserRole).filter_by(user_id = request.user_id, role_id = request.role_id)


    user_role.delete()
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"

