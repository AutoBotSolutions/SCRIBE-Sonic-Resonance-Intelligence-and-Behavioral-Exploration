# SCRIBE Quick Reference

## 🚀 Quick Commands

### System Commands
```bash
# Start interactive mode
./start_interactive.sh

# Start API server
./start_api.sh

# Full deployment
./deploy.sh

# System validation
python3 validate_system.py
```

### Chat Interface Commands
```
🔍 SCRIBE> help              # Show help
🔍 SCRIBE> /scan            # Perform scan
🔍 SCRIBE> /status          # Check status
🔍 SCRIBE> /history         # View history
🔍 SCRIBE> What did you detect?  # Natural language
```

### API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Perform scan
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"signal_type": "sine", "frequency": 440, "duration": 2}'

# Get status
curl http://localhost:8000/status
```

## 📁 Key Files

### Main Files
- `main.py` - Main entry point
- `validate_system.py` - System validation
- `deploy.sh` - Deployment script
- `start_interactive.sh` - Interactive mode
- `start_api.sh` - API server

### Configuration
- `config.json` - System configuration
- `requirements.txt` - Dependencies
- `scribe_env/` - Virtual environment

### Source Code
- `src/core/system_controller.py` - System orchestration
- `src/emitter/` - Audio signal generation
- `src/listener/` - Audio capture
- `src/processing/` - Signal analysis
- `src/ai/` - AI interpretation
- `src/chat/` - User interface
- `src/api/` - REST API

## 🔧 Common Tasks

### Start System
```bash
# Interactive mode (recommended)
./start_interactive.sh

# API server mode
./start_api.sh
```

### Perform Scan
```bash
# In chat interface
🔍 SCRIBE> /scan

# Via API
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"signal_type": "sine", "frequency": 440, "duration": 2}'
```

### Check System Status
```bash
# In chat interface
🔍 SCRIBE> /status

# Via API
curl http://localhost:8000/status

# System validation
python3 validate_system.py
```

### Troubleshoot
```bash
# Check logs
tail -f scribe.log

# Validate system
python3 validate_system.py

# Restart system
pkill -f "python3 main.py"
./start_interactive.sh
```

## 📊 System Information

### Default Configuration
- **Sample Rate**: 44100 Hz
- **Audio Channels**: 1 (mono)
- **Chunk Size**: 1024 samples
- **FFT Size**: 2048 samples
- **Frequency Range**: 20Hz - 20kHz

### Component Status
- **System Controller**: Operational
- **Emission Engine**: Mock/Real audio
- **Listening Module**: Mock/Real audio
- **Signal Processing**: FFT analysis
- **AI Interpreter**: Pattern recognition
- **Feedback Loop**: Learning system
- **Chat Interface**: Natural language

### API Information
- **Base URL**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Endpoint**: http://localhost:8000/health
- **Status Endpoint**: http://localhost:8000/status

## 🔍 Scan Parameters

### Signal Types
- `sine` - Pure tone
- `sweep` - Frequency sweep
- `pulse` - Short pulse
- `harmonic` - Multiple harmonics

### Parameter Ranges
- **Frequency**: 20Hz - 20,000Hz
- **Duration**: 0.1s - 10s
- **Amplitude**: 0.0 - 1.0

### Example Scans
```bash
# Low frequency analysis
🔍 SCRIBE> /scan --type=sine --frequency=100 --duration=3

# High frequency analysis
🔍 SCRIBE> /scan --type=sine --frequency=8000 --duration=1

# Frequency sweep
🔍 SCRIBE> /scan --type=sweep --duration=5

# Custom amplitude
🔍 SCRIBE> /scan --type=sine --frequency=440 --duration=2 --amplitude=0.8
```

## 📚 Documentation Links

### Main Documentation
- [Main Wiki Index](README.md)
- [System Architecture](architecture/README.md)
- [User Guide](user-guide/README.md)
- [API Documentation](api/README.md)

### Technical Documentation
- [Component Documentation](components/README.md)
- [Developer Documentation](developer/README.md)
- [Troubleshooting](troubleshooting/README.md)
- [Deployment Guide](deployment/README.md)

### External Resources
- [API Documentation (Live)](http://localhost:8000/docs)
- [Main Project README](../README.md)
- [System Documentation](../Scribe%20Resonance%20AI%20System.html)

## 🚨 Common Issues

### PyAudio Not Available
```bash
# System uses mock audio automatically
# No action required for development
```

### Import Errors
```bash
# Install dependencies
pip install -r requirements.txt

# Rebuild environment
./deploy.sh
```

### API Not Responding
```bash
# Check if running
ps aux | grep python3

# Restart API server
./start_api.sh
```

### Memory Issues
```bash
# Restart system
pkill -f "python3 main.py"
./start_interactive.sh

# Use shorter scans
🔍 SCRIBE> /scan --duration=1
```

## 🎯 Tips and Tricks

### Power User Commands
```bash
# Quick scan and analysis
🔍 SCRIBE> /scan && what did you detect?

# Environment comparison
🔍 SCRIBE> /scan && compare to previous

# Learning check
🔍 SCRIBE> /feedback rating 5 && what have you learned?
```

### Natural Language Examples
```
🔍 SCRIBE> What material is this?
🔍 SCRIBE> Is this environment stable?
🔍 SCRIBE> How confident are you?
🔍 SCRIBE> Compare to last scan
🔍 SCRIBE> What changed recently?
```

### Keyboard Shortcuts
- **Up Arrow**: Previous commands
- **Ctrl+C**: Exit system
- **Tab**: Command completion (if supported)

## 📞 Getting Help

### Self-Service
1. **Type `help`** in chat interface
2. **Check `/status`** for system health
3. **Run `validate_system.py`** for full validation
4. **Review troubleshooting guide** for common issues

### Documentation
- **Quick Reference**: This file
- **User Guide**: [user-guide/README.md](user-guide/README.md)
- **Troubleshooting**: [troubleshooting/README.md](troubleshooting/README.md)
- **API Documentation**: [api/README.md](api/README.md)

### System Information
- **Version**: 1.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-05-06

---

**Quick Reference Version**: 1.0.0  
**Purpose**: Fast access to common commands and information
