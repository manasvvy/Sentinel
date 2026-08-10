#!/bin/bash
set -e

echo "🚀 Starting Sentinel Backend & Frontend Setup..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend Setup
echo -e "${BLUE}=== Backend Setup ===${NC}"

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env and add your OPENAI_API_KEY${NC}"
fi

echo -e "${GREEN}✅ Backend ready!${NC}"
echo ""

# Frontend Setup
echo -e "${BLUE}=== Frontend Setup ===${NC}"

cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install -q
fi

if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.example .env.local
fi

echo -e "${GREEN}✅ Frontend ready!${NC}"
echo ""

cd ..

# Summary
echo -e "${GREEN}=== Setup Complete ===${NC}"
echo ""
echo "To start the system:"
echo ""
echo -e "${BLUE}Terminal 1 (Backend):${NC}"
echo "  python run.py"
echo ""
echo -e "${BLUE}Terminal 2 (Frontend):${NC}"
echo "  cd frontend && npm run dev"
echo ""
echo -e "${GREEN}Then open: http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}API Docs: http://localhost:8000/docs${NC}"
