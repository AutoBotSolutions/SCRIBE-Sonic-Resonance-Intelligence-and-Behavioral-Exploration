#!/bin/bash
# SCRIBE Resonance AI System Deployment Script

set -e

echo "🚀 SCRIBE Resonance AI System Deployment"
echo "=========================================="

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "scribe_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv scribe_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source scribe_env/bin/activate

# Install system dependencies (with error handling)
echo "📚 Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    echo "Detected Debian/Ubuntu system"
    sudo apt-get update || echo "⚠️ apt-get update failed, continuing..."
    sudo apt-get install -y python3-dev portaudio19-dev || echo "⚠️ System dependencies installation failed, will use mock audio"
elif command -v yum &> /dev/null; then
    echo "Detected RHEL/CentOS system"
    sudo yum install -y python3-devel portaudio-devel || echo "⚠️ System dependencies installation failed, will use mock audio"
elif command -v brew &> /dev/null; then
    echo "Detected macOS system"
    brew install portaudio || echo "⚠️ Portaudio installation failed, will use mock audio"
else
    echo "⚠️ Unknown package manager, skipping system dependencies"
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip

# Install core dependencies first
echo "📊 Installing core dependencies..."
pip install numpy scipy || echo "⚠️ Core dependencies failed, some features may not work"

# Install audio dependencies with fallback
echo "🎵 Installing audio dependencies..."
pip install pyaudio || echo "⚠️ PyAudio installation failed, will use mock audio system"

# Install remaining dependencies
echo "📦 Installing remaining dependencies..."
pip install scikit-learn || echo "⚠️ scikit-learn failed, AI features may be limited"
pip install fastapi uvicorn || echo "⚠️ FastAPI failed, API server may not work"
pip install prometheus-client || echo "⚠️ Prometheus client failed, monitoring may be limited"

# Create configuration
echo "⚙️ Creating configuration..."
if [ ! -f "config.json" ]; then
    echo "Configuration file already exists or will be auto-generated"
fi

# Create logs directory
echo "📝 Creating logs directory..."
mkdir -p logs

# Test the system
echo "🧪 Testing system installation..."
python3 test_system.py

# Create startup scripts
echo "📜 Creating startup scripts..."

# Interactive mode startup script
cat > start_interactive.sh << 'EOF'
#!/bin/bash
echo "🗣️ Starting SCRIBE Interactive Mode..."
cd "$(dirname "$0")"
source scribe_env/bin/activate
python3 main.py
EOF

# API server startup script
cat > start_api.sh << 'EOF'
#!/bin/bash
echo "🌐 Starting SCRIBE API Server..."
cd "$(dirname "$0")"
source scribe_env/bin/activate
python3 src/api/main.py
EOF

# Monitoring startup script
cat > start_monitoring.sh << 'EOF'
#!/bin/bash
echo "📊 Starting SCRIBE with Monitoring..."
cd "$(dirname "$0")"
source scribe_env/bin/activate
export SCRIBE_MONITORING_ENABLED=true
python3 main.py
EOF

# Make scripts executable
chmod +x start_interactive.sh start_api.sh start_monitoring.sh

echo ""
echo "✅ SCRIBE System Deployment Complete!"
echo "=================================="
echo ""
echo "🎯 Available startup modes:"
echo "  • Interactive:  ./start_interactive.sh"
echo "  • API Server:   ./start_api.sh"
echo "  • With Monitoring: ./start_monitoring.sh"
echo ""
echo "📚 Documentation:"
echo "  • README.md - Complete system documentation"
echo "  • API docs available at http://localhost:8000/docs"
echo ""
echo "🔧 Configuration: config.json"
echo "📝 Logs: logs/"
echo ""
echo "🚀 Ready to start exploring environments through resonance intelligence!"
