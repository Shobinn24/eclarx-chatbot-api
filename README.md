# eclarx-chatbot-api

FastAPI backend for E-Clarx LLC's AI Chatbot Service.  
Powers the embeddable chat widget for law firms and small businesses.

## Stack
- **FastAPI** — REST API framework
- **Anthropic API (Claude)** — LLM brain
- **PostgreSQL** — conversation history
- **SQLAlchemy** — ORM
- **Railway** — deployment

---

## Local Development

### 1. Clone and install
```bash
git clone https://github.com/Shobinn24/eclarx-chatbot-api
cd eclarx-chatbot-api
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Open .env and add your ANTHROPIC_API_KEY
# Leave DATABASE_URL blank to use SQLite locally
```

### 3. Run the server
```bash
uvicorn app.main:app --reload
```

API docs available at: http://localhost:8000/docs

---

## Project Structure
```
eclarx-chatbot-api/
├── app/
│   ├── main.py          # FastAPI app, CORS, router registration
│   ├── database.py      # SQLAlchemy engine + session + get_db dependency
│   ├── prompts.py       # System prompts per client (firm_id)
│   ├── models/
│   │   └── conversation.py   # ConversationHistory DB model
│   ├── schemas/
│   │   └── chat.py           # Pydantic request/response schemas
│   └── routers/
│       └── chat.py           # /chat POST endpoint + /chat/history GET
├── requirements.txt
├── Procfile             # Railway start command
└── .env.example
```

---

## API Endpoints

### `POST /chat`
Send a message and get a reply.

**Request body:**
```json
{
  "session_id": "uuid-from-frontend",
  "message": "What are your office hours?",
  "firm_id": "demo"
}
```

**Response:**
```json
{
  "reply": "Our office is open Monday through Friday, 9am to 5pm EST.",
  "session_id": "uuid-from-frontend"
}
```

### `GET /chat/history/{session_id}`
Fetch all messages for a session (for debugging/admin).

---

## Deploy to Railway

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add a **PostgreSQL** plugin to the project
4. Set environment variables in Railway dashboard:
   - `ANTHROPIC_API_KEY` — your key from console.anthropic.com
   - `DATABASE_URL` — Railway auto-sets this when you add PostgreSQL
5. Railway will auto-deploy on every push to main

---

## Adding a New Client

1. Open `app/prompts.py`
2. Add a new key to `SYSTEM_PROMPTS` with the client's `firm_id`
3. Fill in their firm info, practice areas, hours, booking link
4. On the React widget embed code, set `data-firm="your-firm-id"`

---

*E-Clarx LLC | info@eclarx.com | eclarx.com*
