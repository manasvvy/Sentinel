#!/usr/bin/env python3
"""
Run the Sentinel backend server (local development).

Usage:
    python run.py

For production, use:
    uvicorn app.main:app --host 0.0.0.0 --port $PORT

Requires:
    - requirements.txt installed
    - .env file with OPENAI_API_KEY set (local dev)
      OR the OPENAI_API_KEY env var set directly (production)
"""

import os
import uvicorn
from dotenv import load_dotenv

# Load .env file for local dev (no-op if not present)
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY is not set.")
    print("Copy .env.example to .env and add your OpenAI API key for local dev.")
    print("In production, set OPENAI_API_KEY in your Render environment variables.")

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    print(f"🚀 Starting Sentinel backend on {host}:{port}")
    print(f"📊 Audit logs: {os.getenv('LOG_FILE', 'stdout')}")
    print(f"\n📖 API Documentation: http://localhost:{port}/docs")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
