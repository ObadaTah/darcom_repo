from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.all import User, Role, Permission, RolePermission

from security.JWToken import get_current_user

from database import db_conn

from schemas.user_schemas import UserSchema
from schemas.permission_schemas import CreatePermissionSchema, UpdatePermissionRole









get_db = db_conn.get_db

router = APIRouter(tags=["permissions"])


@router.post("/create_permission")
def create_permission(request:CreatePermissionSchema, db:Session =Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    new_permission = Permission(name= request.name, description=request.description, key=request.key)

    db.add(new_permission)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(new_permission)
    return new_permission

    
@router.post("/update_permission_role/")
def update_permission_role(request: UpdatePermissionRole, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    new_permission_role = RolePermission(role_id=request.role_id, permission_id=request.permission_id)

    db.add(new_permission_role)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(new_permission_role)
    return new_permission_role

@router.get("/get_permission/{permission_id}")
def get_permission(permission_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    permissions = db.query(Permission).filter(Permission.id == permission_id).first()
    return permissions


@router.get("/get_permission_roles/{permission_id}")
def get_permission_roles(permission_id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    permission_roles = db.query(RolePermission).filter(Permission.id == permission_id).all()
    roles_names = {"names": []}
    for permission_role in permission_roles:
        roles_names["names"].append(db.query(Role).filter(Role.id == permission_role.role_id).first())
    
    return roles_names

@router.get("/get_all_permissions")
def get_all_permissions(db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    permissions = db.query(Permission).filter().all()
    return permissions


@router.put("/update_permission/{id}")
def update_permissions(id, request: CreatePermissionSchema, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    permission = db.query(Permission).filter(Permission.id == id).first()

    if not permission:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    permission.name = request.name
    permission.description = request.description
    permission.key = request.key

    db.add(permission)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(permission)

    return permission

@router.delete("/delete_permission/{id}")
def delete_permission(id, db:Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):
    permission = db.query(Permission).filter(Permission.id == id)

    if not permission.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    try:
        permission.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"




@router.delete("/delete_permission_role")
def delete_permission_role(request: UpdatePermissionRole, db: Session = Depends(get_db), get_current_user: UserSchema = Depends(get_current_user)):

    permission_role = db.query(RolePermission).filter_by(permission_id = request.permission_id, role_id = request.role_id)
    if not permission_role.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")


    permission_role.delete()
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={'error': x})

    return "Deleted Succ"

