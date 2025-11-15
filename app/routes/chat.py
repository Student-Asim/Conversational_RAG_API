from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from core.redis_client import append_message, get_memory
from core.rag import rag_answer
from core.bookings import save_booking
from core.request import save_request


router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str
    top_k: Optional[int] = 5

class ChatResponse(BaseModel):
    reply: str

class BookingRequest(BaseModel):
    session_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    date: Optional[str] = None  # ISO date expected
    time: Optional[str] = None  # e.g., "15:00"

class BookingResponse(BaseModel):
    status: str
    booking_id: int


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # Save in Redis
    append_message(req.session_id, "user", req.message)

    # Build memory for RAG
    mem = get_memory(req.session_id)
    memory_text = "\n".join(f"{m['role']}: {m['content']}" for m in mem[-10:])

    # Get response
    answer = rag_answer(req.message, memory_text, top_k=req.top_k)
    append_message(req.session_id, "assistant", answer)

    # Save in MySQL requests table
    save_request(
        session_id=req.session_id,
        query=req.message,
        response=answer,
        user_name=None,      # Optional: you can fill if available
        user_email=None      # Optional: you can fill if available
    )

    return {"reply": answer}


@router.post("/book", response_model=BookingResponse)
async def book(req: BookingRequest):
    # If direct booking fields are provided, save
    if req.name and req.email and req.date and req.time:
        b = save_booking(req.name, req.email, req.date, req.time)
        return {"status": "booked", "booking_id": b.id}
    # Otherwise, ask client to provide structured fields (or you can implement LLM extraction)
    raise HTTPException(status_code=400, detail="Provide name, email, date, and time.")
