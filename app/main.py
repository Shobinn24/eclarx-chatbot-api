from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from app.database import engine, Base

# Create all DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Clarx Chatbot API",
    description="AI-powered chatbot backend for businesses — FirmChat by E-Clarx",
    version="1.0.0",
)

# CORS — allows the React widget to call this API from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this in production to your widget domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)


@app.get("/")
def root():
    return {"status": "E-Clarx Chatbot API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
