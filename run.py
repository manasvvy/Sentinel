#!/usr/bin/env python3
"""
Run the Sentinel backend server.

Usage:
    python run.py

Requires:
    - requirements.txt installed
    - .env file with OPENAI_API_KEY set
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Validate required environment variables
if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY not set in .env file")
    print("Copy .env.example to .env and add your OpenAI API key")
    sys.exit(1)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Sentinel backend on {host}:{port}")
    print(f"📊 Audit logs: {os.getenv('LOG_FILE', 'audit.log')}")
    print(f"\nAPI Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
