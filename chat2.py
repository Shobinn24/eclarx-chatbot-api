from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """
    What the React widget sends to /chat
    session_id  — uuid stored in localStorage on the frontend
    message     — the user's text
    firm_id     — which bot persona to load (defaults to demo)
    """
    session_id: str
    message: str
    firm_id: Optional[str] = "demo"


class ChatResponse(BaseModel):
    """
    What /chat sends back to the React widget
    """
    reply: str
    session_id: str


class ConversationMessage(BaseModel):
    """
    A single message record, used when fetching history
    """
    id: str
    session_id: str
    firm_id: str
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  # Lets Pydantic read SQLAlchemy model objects
