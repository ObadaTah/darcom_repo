from database import db_conn
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from models.all import Facility, Media, Product, Story
from schemas.story_schemas import CreateStorySchema
from schemas.user_schemas import UserSchema
from security.JWToken import get_current_user
from sqlalchemy.orm import Session

from .mediaer import data_parser_and_saver

get_db = db_conn.get_db

router = APIRouter(tags=["Story"])


def add_story_photo(file, tag, db, story_id):

    data = data_parser_and_saver(file, tag)
    if type(data) is not dict:
        return data
    media = Media(
        mediable_type="story",
        mediable_id=story_id,
        tag=tag,
        disk="local",
        directory=data["directory"],
        media_tag=tag,
        file_name=data["filename"],
        original_name=file.filename,
        extension=data["extension"],
        mime_type=data["extension"],
        size=data["size"],
    )
    db.add(media)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})
    return True


@router.post("/create_story/{facility_id}")
def create_story(
    facility_id: int,
    request: CreateStorySchema = Depends(),
    file: UploadFile = File(default=None),
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):

    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="FACILITY NOT FOUND"
        )

    new_story = Story(
        title=request.title,
        description=request.description,
        target_group=request.target_group,
        age_from=request.age_from,
        age_to=request.age_to,
        status=request.status,
        # publish_at= request.publish_at,
        days=request.days,
        duration=request.duration,
        facility_id=facility_id,
    )

    db.add(new_story)
    try:
        db.commit()
    except Exception as x:
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error": x})
    if file is not None:
        photo = add_story_photo(file=file, tag=request.tag, db=db, story_id=new_story.id)
        if type(photo) is not bool:
            return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail={"error at photo commiting": photo})

    db.refresh(new_story)
    return new_story


@router.get("/get_story/{story_id}")
def get_story(
    story_id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return story


@router.get("/get_all_stories")
def get_all_stories(
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    stories = db.query(Story).filter().all()
    return stories


@router.get("/get_all_facility_stories/{facility_id}")
def get_all_facility_stories(
    facility_id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):

    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="FACILITY NOT FOUND"
        )

    stories = db.query(Story).filter(Story.facility_id == facility_id).all()
    return stories


@router.put("/update_story/{id}")
def update_story(
    id,
    request: CreateStorySchema,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    story = db.query(Story).filter(Story.id == id).first()
    if not story:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    if request.title:
        story.title = request.title
    if request.description:
        story.description = request.description
    if request.target_group:
        story.target_group = request.target_group
    if request.age_from:
        story.age_from = request.age_from
    if request.age_to:
        story.age_to = request.age_to
    if request.status:
        story.status = request.status
    if request.publish_at:
        story.publish_at = request.publish_at
    if request.days:
        story.days = request.days
    if request.duration:
        story.duration = request.duration

    db.add(story)
    db.commit()

    db.refresh(story)

    return story


@router.delete("/delete_story/{id}")
def delete_story(
    id,
    db: Session = Depends(get_db),
    get_current_user: UserSchema = Depends(get_current_user),
):
    story = db.query(Story).filter(Story.id == id)

    if not story.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")


    story.delete()
    db.commit()

    return "Deleted Succ"
