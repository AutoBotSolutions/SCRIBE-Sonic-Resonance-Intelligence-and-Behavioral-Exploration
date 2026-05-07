# SCRIBE Troubleshooting Guide

## Troubleshooting Overview

This guide helps you diagnose and resolve common issues with the SCRIBE Resonance AI System. Problems are categorized by severity and component for easier resolution.

## Quick Diagnosis

### System Status Check
```bash
# Check system validation
python3 validate_system.py

# Check system status
./start_interactive.sh
# Then type: /status
```

### Common Error Patterns
- **Import errors**: Missing dependencies or path issues
- **Audio errors**: PyAudio or hardware problems
- **Permission errors**: File access or device permissions
- **Memory errors**: Insufficient resources
- **Network errors**: API or connectivity issues

## Common Issues and Solutions

### Installation & Setup Issues

#### Issue: "ModuleNotFoundError: No module named 'pyaudio'"
**Symptoms**: System fails to start, audio components not working
**Causes**: PyAudio not installed or system libraries missing
**Solutions**:
```bash
# Option 1: Install PyAudio (may fail on some systems)
pip install pyaudio

# Option 2: Use mock audio (recommended for development)
# System automatically falls back to mock audio

# Option 3: Install system dependencies (Ubuntu/Debian)
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

#### Issue: "No module named 'numpy', 'scipy', 'fastapi'"
**Symptoms**: Import errors during startup
**Causes**: Missing Python dependencies
**Solutions**:
```bash
# Install all dependencies
pip install numpy scipy fastapi uvicorn librosa soundfile

# Or use deployment script
./deploy.sh
```

#### Issue: Virtual environment not found
**Symptoms**: Command not found errors
**Causes**: Virtual environment not created or activated
**Solutions**:
```bash
# Create virtual environment
python3 -m venv scribe_env

# Activate it
source scribe_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Audio Component Issues

#### Issue: Audio capture fails
**Symptoms**: Scan errors, no audio data
**Causes**: Hardware issues, permissions, device conflicts
**Solutions**:
```bash
# Check audio devices
python3 -c "import pyaudio; p = pyaudio.PyAudio(); [print(i, p.get_device_info_by_index(i)['name']) for i in range(p.get_device_count())]"

# Use mock audio (automatic fallback)
# System will automatically use mock audio if real audio fails
```

#### Issue: "operands could not be broadcast together"
**Symptoms**: Signal processing errors
**Causes**: Array shape mismatches in FFT processing
**Solutions**:
```bash
# This is usually fixed in the current version
# If encountered, restart the system:
./start_interactive.sh
```

### Performance Issues

#### Issue: Slow scan processing
**Symptoms**: Scans taking >10 seconds
**Causes**: Insufficient CPU, large audio buffers, processing bottlenecks
**Solutions**:
```bash
# Check system resources
top
htop

# Reduce scan duration
SCRIBE> /scan --duration=1

# Use simpler signal types
SCRIBE> /scan --type=sine
```

#### Issue: High memory usage
**Symptoms**: System becoming slow, memory warnings
**Causes**: Large audio buffers, memory leaks
**Solutions**:
```bash
# Restart system to clear memory
pkill -f "python3 main.py"
./start_interactive.sh

# Use shorter scan durations
SCRIBE> /scan --duration=0.5
```

### API Issues

#### Issue: API server not starting
**Symptoms**: Connection refused, server not responding
**Causes**: Port conflicts, missing dependencies, configuration errors
**Solutions**:
```bash
# Check if port is in use
lsof -i :8000

# Kill existing process
pkill -f "uvicorn"

# Start API server
./start_api.sh
```

#### Issue: "No module named 'fastapi'"
**Symptoms**: API import errors
**Causes**: Missing web framework dependencies
**Solutions**:
```bash
# Install web dependencies
pip install fastapi uvicorn

# Or install all dependencies
./deploy.sh
```

### Database Issues

#### Issue: Database locked or corrupted
**Symptoms**: Feedback not saving, learning not working
**Causes**: File permissions, concurrent access, corruption
**Solutions**:
```bash
# Remove and recreate database
rm scribe_learning.db
./start_interactive.sh
```

### Monitoring Issues

#### Issue: "No module named 'prometheus_client'"
**Symptoms**: Monitoring not working, metrics errors
**Causes**: Missing monitoring dependencies
**Solutions**:
```bash
# Install monitoring dependencies
pip install prometheus_client
```

## Advanced Troubleshooting

### Debug Mode
Enable debug mode for detailed logging:
```bash
# Edit config.json
{
  "debug_mode": true
}

# Or set environment variable
export SCRIBE_DEBUG=true
./start_interactive.sh
```

### Log Analysis
Check log files for error patterns:
```bash
# View system logs
tail -f scribe.log

# View error logs
tail -f scribe_errors.log

# Search for specific errors
grep "ERROR" scribe.log
```

### Component Isolation
Test individual components:
```bash
# Test configuration
python3 -c "from utils.config import Config; print(Config().audio.sample_rate)"

# Test audio components
python3 -c "from emitter.mock_audio import MockResonanceEmissionEngine; print('Mock audio working')"

# Test signal processing
python3 -c "from processing.fft_analyzer import SignalProcessingLayer; print('Processing working')"
```

### Memory Profiling
Identify memory usage issues:
```bash
# Install profiling tools
pip install memory-profiler

# Profile memory usage
python3 -m memory_profiler main.py
```

### Performance Profiling
Identify performance bottlenecks:
```bash
# Install profiling tools
pip install line-profiler

# Profile performance
python3 -m line_profiler main.py
```

## Error Codes and Meanings

### System Error Codes
- **SCRIBE_001**: Configuration file not found
- **SCRIBE_002**: Audio initialization failed
- **SCRIBE_003**: Signal processing error
- **SCRIBE_004**: AI interpretation failed
- **SCRIBE_005**: Database error

### API Error Codes
- **API_400**: Bad request (invalid parameters)
- **API_401**: Unauthorized (authentication required)
- **API_404**: Not found (resource doesn't exist)
- **API_429**: Rate limit exceeded
- **API_500**: Internal server error

### Component Error Codes
- **AUDIO_001**: Device not found
- **AUDIO_002**: Permission denied
- **AUDIO_003**: Sample rate mismatch
- **PROCESSING_001**: FFT computation failed
- **PROCESSING_002**: Invalid audio data
- **AI_001**: Model not loaded
- **AI_002**: Invalid feature data

## Recovery Procedures

### System Recovery
```bash
# Complete system reset
pkill -f "python3 main.py"
rm -rf scribe_env/
./deploy.sh
```

### Database Recovery
```bash
# Backup and recreate database
cp scribe_learning.db scribe_learning.db.backup
rm scribe_learning.db
./start_interactive.sh
```

### Configuration Recovery
```bash
# Reset to default configuration
rm config.json
./start_interactive.sh
```

## Getting Help

### Self-Service Resources
1. **Check logs**: `tail -f scribe.log`
2. **Run validation**: `python3 validate_system.py`
3. **Check status**: Use `/status` command
4. **Review documentation**: Check relevant wiki sections

### Community Support
- Check GitHub issues for similar problems
- Review discussion forums
- Search existing troubleshooting cases

### Escalation
If issues persist after trying all solutions:
1. Document the exact error message
2. Provide system information (OS, Python version, dependencies)
3. Include steps to reproduce the issue
4. Share relevant log files

## 🧪 Testing Solutions

### Test Individual Components
```bash
# Test core imports
python3 -c "
from core.system_controller import ScribeSystemController
from utils.config import Config
print('Core imports working')
"

# Test audio components
python3 -c "
from emitter.mock_audio import MockResonanceEmissionEngine
from listener.mock_capture import MockMicroListeningModule
print('Audio components working')
"

# Test signal processing
python3 -c "
from processing.fft_analyzer import SignalProcessingLayer
print('Signal processing working')
"
```

### Test API Endpoints
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test scan endpoint
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"signal_type": "sine", "frequency": 440, "duration": 2}'
```

### Test Chat Interface
```bash
# Test basic commands
echo "/help" | ./start_interactive.sh

# Test scan functionality
echo "/scan" | ./start_interactive.sh
```

## Performance Optimization

### System Optimization
```bash
# Reduce audio buffer size
# Edit config.json:
{
  "audio": {
    "chunk_size": 512
  }
}

# Optimize processing parameters
{
  "processing": {
    "window_size": 1024,
    "hop_length": 256
  }
}
```

### Memory Optimization
```bash
# Reduce scan history
# Edit config.json:
{
  "system": {
    "max_history": 50
  }
}

# Enable garbage collection
import gc
gc.collect()
```

## 🔮 Future Issues and Prevention

### Known Limitations
- **PyAudio dependencies**: May fail on some systems (use mock audio)
- **Real-time processing**: Limited by CPU performance
- **Memory usage**: Large audio buffers consume memory
- **Database size**: Can grow large over time

### Preventive Measures
1. **Regular validation**: Run `validate_system.py` weekly
2. **Log monitoring**: Check error logs regularly
3. **Performance monitoring**: Track scan times and memory usage
4. **Backup configuration**: Save working config.json
5. **Update dependencies**: Keep packages current

### Monitoring Setup
```bash
# Set up log rotation
logrotate -f logrotate.conf

# Monitor system resources
watch -n 5 'ps aux | grep python3'

# Check disk space
df -h
```

## Additional Resources

### Documentation Links
- [System Architecture](../architecture/)
- [Component Documentation](../components/)
- [API Documentation](../api/)
- [User Guide](../user-guide/)
- [Developer Guide](../developer/)

### External Resources
- [Python Documentation](https://docs.python.org/3/)
- [NumPy Troubleshooting](https://numpy.org/doc/stable/user/troubleshooting.html)
- [LibROSA Documentation](https://librosa.org/doc/)
- [FastAPI Troubleshooting](https://fastapi.tiangolo.com/tutorial/dependencies/)

---

**Last Updated**: 2026-05-06  
**Troubleshooting Guide Version**: 1.0.0  
**Status**: Production Ready
