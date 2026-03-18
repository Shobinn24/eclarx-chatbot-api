import os
import uuid
import anthropic
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.conversation import ConversationHistory
from app.schemas.chat import ChatRequest, ChatResponse, ConversationMessage
from app.prompts import get_system_prompt
from typing import List

router = APIRouter(prefix="/chat", tags=["chat"])

# Anthropic client — reads ANTHROPIC_API_KEY from environment automatically
client = anthropic.Anthropic()

# Max messages to send to Claude as conversation context
# Keeps costs low; only the last N turns are included
MAX_HISTORY = 10


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint.
    1. Load recent conversation history for this session from DB
    2. Build the message list for the Anthropic API
    3. Call Claude with the appropriate system prompt
    4. Save both the user message and assistant reply to DB
    5. Return the reply to the React widget
    """

    # --- 1. Load recent history ---
    history = (
        db.query(ConversationHistory)
        .filter(ConversationHistory.session_id == request.session_id)
        .order_by(ConversationHistory.created_at.asc())
        .limit(MAX_HISTORY)
        .all()
    )

    # --- 2. Build messages list for Anthropic ---
    # Anthropic expects: [{"role": "user", "content": "..."}, {"role": "assistant", ...}]
    messages = [{"role": msg.role, "content": msg.content} for msg in history]
    messages.append({"role": "user", "content": request.message})

    # --- 3. Call Claude ---
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=get_system_prompt(request.firm_id),
            messages=messages,
        )
        reply = response.content[0].text

    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Anthropic API error: {str(e)}")

    # --- 4. Save user message + assistant reply to DB ---
    db.add(ConversationHistory(
        id=str(uuid.uuid4()),
        session_id=request.session_id,
        firm_id=request.firm_id,
        role="user",
        content=request.message,
    ))
    db.add(ConversationHistory(
        id=str(uuid.uuid4()),
        session_id=request.session_id,
        firm_id=request.firm_id,
        role="assistant",
        content=reply,
    ))
    db.commit()

    # --- 5. Return reply ---
    return ChatResponse(reply=reply, session_id=request.session_id)


@router.get("/history/{session_id}", response_model=List[ConversationMessage])
def get_history(session_id: str, db: Session = Depends(get_db)):
    """
    Optional endpoint — fetch full conversation history for a session.
    Useful for debugging or building a conversation log admin view.
    """
    messages = (
        db.query(ConversationHistory)
        .filter(ConversationHistory.session_id == session_id)
        .order_by(ConversationHistory.created_at.asc())
        .all()
    )
    return messages
