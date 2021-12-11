from database import db_conn
from fastapi import APIRouter, Depends, HTTPException, status
from models.all import Product, Purchase
from schemas.purchase_schemas import CreatePurchaseSchema
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

get_db = db_conn.get_db

router = APIRouter(tags=["Purchase"])


@router.post("/create_purchase/{product_id}")
def create_purchase(
    product_id: int,
    request: CreatePurchaseSchema,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PRODUCT NOT FOUND")
    new_purchase = Purchase(
        product_id=product_id,
        user_id=get_current_user.id,
        customer_name=request.customer_name,
        customer_mobile=request.customer_mobile,
        customer_address=request.customer_address,
        info=request.info,
        quantity=request.quantity,
        status=request.status,
    )
    db.add(new_purchase)
    
    db.commit()

    db.refresh(new_purchase)
    return new_purchase


@router.get("/get_purchase/{purchase_id}")
def get_purchase(
    purchase_id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return purchase


@router.get("/get_all_purchases")
def get_all_purchases(
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    purchases = db.query(Purchase).filter().all()
    return purchases


@router.put("/update_purchase/{id}")
def update_purchase(
    id,
    request: CreatePurchaseSchema,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    purchase = db.query(Purchase).filter(Purchase.id == id).first()
    if not purchase:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    if request.customer_name is not None:
        purchase.customer_name = request.customer_name
    if request.customer_mobile is not None:
        purchase.customer_mobile = request.customer_mobile
    if request.info is not None:
        purchase.info = request.info
    if request.quantity is not None:
        purchase.quantity = request.quantity
    if request.status is not None:
        purchase.status = request.status
    db.add(purchase)

    db.commit()

    db.refresh(purchase)

    return purchase


@router.delete("/delete_purchase/{id}")
def delete_purchase(
    id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    purchase = db.query(Purchase).filter(Purchase.id == id)

    if not purchase.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")


    purchase.delete()
    db.commit()

    return "Deleted Succ"
