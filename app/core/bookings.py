from database.database import SessionLocal
from database.models import Booking
from sqlalchemy.orm import Session
from typing import Any

def save_booking(name: str, email: str, date: str, time: str) -> Booking:
    db: Session = SessionLocal()
    try:
        b = Booking(name=name, email=email, date=date, time=time)
        db.add(b)
        db.commit()
        db.refresh(b)
        return b
    finally:
        db.close()
