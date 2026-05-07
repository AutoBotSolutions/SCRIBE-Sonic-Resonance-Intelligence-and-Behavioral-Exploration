#!/bin/bash
# SCRIBE Interactive Mode Startup Script

echo "🗣️ Starting SCRIBE Interactive Mode..."
echo "====================================="

# Check if virtual environment exists
if [ ! -d "scribe_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv scribe_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source scribe_env/bin/activate

# Install basic dependencies if needed
echo "📚 Checking dependencies..."
pip install numpy scipy 2>/dev/null || echo "⚠️ Using mock implementations for some features"

# Start the system
echo "🧠 Starting SCRIBE Resonance AI System..."
echo "Type 'help' for commands or ask questions naturally"
echo "Press Ctrl+C to exit"
echo ""

python3 main.py
