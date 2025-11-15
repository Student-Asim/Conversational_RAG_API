from sqlalchemy import Column, Integer, String, DateTime, Text
from database.database import Base
import datetime

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    date = Column(String(50), nullable=False)
    time = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
 
class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(200), nullable=False)     # ← ADD THIS
    user_name = Column(String(100), nullable=True)
    user_email = Column(String(100), nullable=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
