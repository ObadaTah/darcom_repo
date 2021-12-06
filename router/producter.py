from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from models.all import Product, Media

from security.JWToken import get_current_user

from database import db_conn

from .mediaer import data_parser_and_saver

from schemas.user_schemas import UserSchema
from schemas.product_schemas import CreateProductSchema


get_db = db_conn.get_db

router = APIRouter(tags=["Product"])

def add_product_photo(file, tag, db, product_id):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    data = data_parser_and_saver(file, "asdasdas")
    if type(data) is not dict:
        return data

    media = Media(mediable_type='product', mediable_id=product.id,
    tag=tag,
    disk='local',
    directory= data['directory'],
    media_tag=tag,
    file_name=data['filename'],
    original_name=file.filename,
    extension=data['extension'],
    mime_type=data['extension'],
    size=data['size']
    )
    db.add(media)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})
    return True


@router.post("/create_product/{facility_id}")
def create_product(
    facility_id,
    request: CreateProductSchema = Depends(),
    file:UploadFile = File(default=None),
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    new_product = Product(
        facility_id=facility_id,
        title=request.title,
        description=request.description,
        price=request.price,
        status=request.status,
    )

    db.add(new_product)
    try:
        db.commit()
    except Exception as x:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})
    if file is not None:
        photo = add_product_photo(file=file, tag=request.tag, db=db, product_id=new_product.id)
        if type(photo) is not bool:
            return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error at photo commiting": photo})
    db.refresh(new_product)
    return new_product


@router.get("/get_product/{product_id}")
def get_product(
    product_id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return product


@router.get("/get_all_products")
def get_all_products(
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    products = db.query(Product).filter().all()
    return products


@router.put("/update_product/{id}")
def update_product(
    id,
    request: CreateProductSchema,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    if request.title is not None:
        product.title = request.title
    if request.description is not None:
        product.description = request.description
    if request.price is not None:
        product.price = request.price
    if request.status is not None:
        product.status = request.status

    db.add(product)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    db.refresh(product)

    return product


@router.delete("/delete_product/{id}")
def delete_product(
    id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == id)

    if not product.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    try:
        product.delete()
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})

    return "Deleted Succ"
