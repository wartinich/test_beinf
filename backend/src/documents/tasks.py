from celery import Celery
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from documents.models import Record
from database import DATABASE_URL

celery = Celery(__name__, broker="redis://redis:6379/0", include=['documents.tasks'])

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


@celery.task(name="documents.tasks.process_task")
def process_task(record_id: int):
    db = SessionLocal()
    try:
        record = db.query(Record).filter(Record.id == record_id).first()
        if not record:
            print(f"Record with ID {record_id} not found.")
            return

        print(f"Updating record {record_id} to status 'done'.")
        record.status = "done"
        db.commit()
    except Exception as e:
        print(f"Error processing record {record_id}: {e}")
        db.rollback()
    finally:
        db.close()
