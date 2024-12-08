from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import verify_token
from documents.models import Record
from documents.schemas import RecordCreate
from documents.utils import upload_file_to_s3
from documents.tasks import process_task

router = APIRouter(prefix="/documents", tags=['documents'])


@router.post("/generate/")
async def create_record(payload: RecordCreate, db: Session = Depends(get_db)):
    db_record = Record(text=payload.text, status="processing")
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    file_url = upload_file_to_s3(payload.text, f"{db_record.id}.txt")
    db_record.link = file_url
    db.commit()

    process_task.delay(db_record.id)

    return db_record

