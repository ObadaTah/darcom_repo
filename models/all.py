import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    Integer,
    UniqueConstraint,
    Float,
)
from database.db_conn import Base
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "Role"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), index=True)
    description = Column(Text)


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(255), index=True, nullable=True)
    username = Column(String(255), index=True, nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    phone_number = Column(String(13), unique=True, index=True, nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    password = Column(String(255), nullable=True)
    gender = Column(String(1), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    age = Column(Integer, nullable=True)
    unread_notification = Column(Integer, nullable=True)
    pointes = Column(Integer, nullable=True)
    user_status = Column(String(10), nullable=True)
    notes = Column(String(500), nullable=True)
    last_login = Column(DateTime, nullable=True)
    current_day = Column(Integer, nullable=True)
    api_token = Column(String, nullable=True)
    fcm_token = Column(String, nullable=True)
    facebook_id = Column(String, nullable=True)
    apple_id = Column(String, nullable=True)
    google_id = Column(String, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    remember_token = Column(String, nullable=True)
    rank_id = Column(Integer, nullable=True)
    city_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(
        Integer,
        ForeignKey("User.id"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        Integer,
        ForeignKey("Role.id"),
        primary_key=True,
        nullable=False,
    )

    role = relationship("Role")
    user = relationship("User")

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="unique_user_role"),)


class Permission(Base):
    __tablename__ = "Permission"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    key = Column(String, nullable=True)


class RolePermission(Base):
    __tablename__ = "role_permission"
    permission_id = Column(
        Integer,
        ForeignKey("Permission.id"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        Integer,
        ForeignKey("Role.id"),
        primary_key=True,
        nullable=False,
    )

    role = relationship("Role")
    user = relationship("Permission")

    __table_args__ = (
        UniqueConstraint("permission_id", "role_id", name="unique_permission_role"),
    )


class City(Base):
    __tablename__ = "City"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    deleted_at = Column(DateTime, nullable=True)


class Facility(Base):
    __tablename__ = "Facility"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=True)
    owner_name = Column(String, nullable=True)
    owner_number = Column(Integer, nullable=True)
    mobile_number = Column(Integer, nullable=True)
    building = Column(String, nullable=True)
    email = Column(String, nullable=True)
    floor = Column(Integer, nullable=True)
    street = Column(String, nullable=True)
    balance = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    latitude = Column(Integer, nullable=True)
    longitude = Column(Integer, nullable=True)
    instagram_url = Column(String, nullable=True)
    facebook_url = Column(String, nullable=True)
    disabled = Column(Boolean, nullable=True)
    visible = Column(Boolean, nullable=True)
    end_subscription_date = Column(DateTime)
    name_subscription = Column(String, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    city_id = Column(
        Integer,
        ForeignKey("City.id"),
        nullable=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("User.id"),
        nullable=True,
    )


class Media(Base):
    __tablename__ = "Media"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mediable_type = Column(String, nullable=True)
    mediable_id = Column(Integer, nullable=True)
    tag = Column(String, nullable=True)
    disk = Column(String, nullable=True)
    directory = Column(String, nullable=True)
    media_tag = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    original_name = Column(String, nullable=True)
    extension = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)

    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


class FacilityPhoto(Base):
    __tablename__ = "FacilityPhoto"
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    facility_id = Column(
        Integer,
        ForeignKey("Facility.id"),
        nullable=True,
    )
    media_id = Column(
        Integer,
        ForeignKey("Media.id"),
        nullable=True,
    )
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


class FacilityPhotoLike(Base):
    __tablename__ = "FacilityPhotoLike"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    facility_photo_id = Column(
        Integer,
        ForeignKey("FacilityPhoto.id"),
        nullable=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("User.id"),
        nullable=True,
    )


class Product(Base):
    __tablename__ = "Product"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    status = Column(String, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    facility_id = Column(
        Integer,
        ForeignKey("Facility.id"),
        nullable=True,
    )


class Purchase(Base):
    __tablename__ = "Purchase"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    customer_name = Column(String, nullable=True)
    customer_mobile = Column(String, nullable=True)
    customer_address = Column(String, nullable=True)
    info = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    product_id = Column(
        Integer,
        ForeignKey("Product.id"),
        nullable=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("User.id"),
        nullable=True,
    )


class Subscription(Base):
    __tablename__="Subscription"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    title = Column(String, nullable=True)
    number_of_months = Column(Integer, nullable=True)
    cost = Column(Integer, nullable=True)
    number_of_stories = Column(Integer, nullable=True)
    number_of_ad_text = Column(Integer, nullable=True)
    visible = Column(Boolean, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
class Package(Base):
    __tablename__="Package"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    package_type = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    visible = Column(Boolean, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


class Banner(Base):
    __tablename__ = "Banner"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    banner_type = Column(String, nullable=True)
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)
    url = Column(String, nullable=True)
    status = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    deleted_at = Column(DateTime, nullable=True)
    facility_id = Column(
        Integer,
        ForeignKey("Facility.id"),
        nullable=True,
    )
    city_id = Column(
        Integer,
        ForeignKey("City.id"),
        nullable=True,
    )


class Card(Base):
    __tablename__ = "Card"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    deleted_at = Column(DateTime, nullable=True)
    facility_id = Column(
        Integer,
        ForeignKey("Facility.id"),
        nullable=True,
    )




class Rank(Base):
    __tablename__ = "Rank"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    points_from = Column(Integer, nullable=True)
    points_to = Column(Integer, nullable=True)
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    deleted_at = Column(DateTime, nullable=True)

class Story(Base):
    __tablename__ = "Story"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    target_group = Column(String, nullable=True)
    age_from = Column(Integer, nullable=True)
    age_to = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
    publish_at = Column(DateTime, nullable=True)
    days = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    deleted_at = Column(DateTime, nullable=True)
    facility_id = Column(
        Integer,
        ForeignKey("Facility.id"),
        nullable=True,
    )

class Category(Base):
    __tablename__ = "Category"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    deleted_at = Column(DateTime, nullable=True)

    parent_id = Column(
        Integer,
        ForeignKey("Category.id"),
        nullable=True,
    )
    parent = relationship('Category', remote_side=[id])

class Setting(Base):
    __tablename__ = "Setting"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String, nullable=True)
    value = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    deleted_at = Column(DateTime, nullable=True)




