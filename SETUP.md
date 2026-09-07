# Sentinel Backend Setup

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run the Server
```bash
python run.py
```

Server will start at `http://localhost:8000`

---

## API Endpoints

### Chat Endpoint
```bash
POST /chat
```

Request:
```json
{
  "user_input": "What is machine learning?",
  "session_id": "user-123-session-1"
}
```

Response:
```json
{
  "response_text": "Machine learning is...",
  "confidence_state": "confident",
  "confidence_score": 0.85,
  "reasoning": [
    "Multiple reasoning paths present",
    "Response includes citations/evidence"
  ]
}
```

### Record Correction Endpoint
```bash
POST /correct
```

Request:
```json
{
  "session_id": "user-123-session-1",
  "correct_info": "Actually, machine learning also includes...",
  "note": "Missing important concept"
}
```

Response:
```json
{
  "status": "correction recorded",
  "total_corrections": 1
}
```

### Session Summary Endpoint
```bash
GET /session/{session_id}/summary
```

Response:
```json
{
  "session_id": "user-123-session-1",
  "created_at": "2024-01-15T10:30:00",
  "total_messages": 5,
  "total_corrections": 2,
  "correction_rate": 0.4,
  "avg_confidence": 0.72,
  "confidence_trend": [0.85, 0.65, 0.72, 0.80]
}
```

### Health Check
```bash
GET /health
```

Response:
```json
{"status": "ok"}
```

---

## Core Components

### Confidence Engine (`app/core/confidence.py`)
Evaluates response quality based on:
- Explicit uncertainty markers ("maybe", "possibly", etc.)
- Evidence/citations in the response
- Multiple reasoning paths
- Response complexity vs. question complexity

Returns confidence level: **confident** (0.7+), **cautious** (0.4-0.7), **guessing** (<0.4)

### Session Manager (`app/core/session.py`)
Tracks:
- Message history per session
- User corrections (primary learning signal)
- Confidence history
- Correction rate (metric of improvement)

### Audit Logger (`app/core/logging.py`)
Logs all interactions for governance:
- LLM interactions with full context
- User corrections
- Safety events
- Errors and exceptions

All entries are timestamped and immutable for audit trails.

### LLM Client (`app/models/llm_client.py`)
Handles OpenAI API calls with:
- Error handling
- Configurable model selection
- Temperature and token limits

---

## Key Design Principles

1. **Confidence is transparent** - Every response includes confidence level and reasoning
2. **Corrections drive learning** - User corrections are the primary signal, not confidence scores
3. **All decisions are logged** - Governance requires full audit trails
4. **Simple systems survive** - Architecture prioritizes clarity over complexity
5. **Backend-first safety** - All trust decisions live in the backend, not the UI

---

## Testing the System

### Manual Test
```bash
# Terminal 1: Run server
python run.py

# Terminal 2: Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "What is quantum computing?",
    "session_id": "test-session-1"
  }'

# Check the audit log
cat audit.log
```

### Interactive Testing
Visit `http://localhost:8000/docs` for interactive Swagger UI

---

## Next Steps

1. **Frontend Integration** - Build UI that respects confidence states
2. **Memory System** - Add opt-in user memory with consent management
3. **Topic Learning** - Adjust confidence by topic based on correction patterns
4. **Monitoring Dashboard** - Visualize metrics (correction rate, confidence trends)
5. **Safety Rules** - Add explicit safety checks and rate limiting

---

## Troubleshooting

### OpenAI API errors
- Check OPENAI_API_KEY is set correctly in .env
- Verify API key has access to chosen model
- Check account has credits

### Server won't start
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check port 8000 is not in use: `lsof -i :8000`
- Run in different port: `PORT=8001 python run.py`

### Audit logs not writing
- Check write permissions to current directory
- Verify LOG_FILE path is correct in .env

---

## Architecture

```
User
  ↓
FastAPI Server (app/main.py)
  ├→ /chat endpoint (app/api/chat.py)
  │   ├→ LLM Client (calls OpenAI)
  │   ├→ Confidence Engine (evaluates quality)
  │   ├→ Session Manager (tracks history)
  │   └→ Audit Logger (logs all interactions)
  ├→ /correct endpoint (records learning signals)
  └→ /health endpoint (status check)
```

---

For questions or issues, check the README.md in the repo root.
