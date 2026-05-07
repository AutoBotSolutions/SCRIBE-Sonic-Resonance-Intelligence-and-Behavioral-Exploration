#!/bin/bash
# SCRIBE API Server Startup Script

echo "🌐 Starting SCRIBE API Server..."
echo "==============================="

# Check if virtual environment exists
if [ ! -d "scribe_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv scribe_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source scribe_env/bin/activate

# Install API dependencies
echo "📚 Installing API dependencies..."
pip install fastapi uvicorn 2>/dev/null || echo "⚠️ API dependencies not available, using mock mode"

# Start the API server
echo "🚀 Starting API server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

python3 src/api/main.py
