from database.database import SessionLocal
from database.models import Request
from sqlalchemy.orm import Session

def save_request(session_id: str, query: str, response: str, user_name: str = None, user_email: str = None):
    db: Session = SessionLocal()
    try:
        r = Request(
            session_id=session_id,
            user_name=user_name,
            user_email=user_email,
            query=query,
            response=response
        )

        db.add(r)
        db.commit()
        db.refresh(r)
        return r
    finally:
        db.close()
