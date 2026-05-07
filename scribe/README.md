# SCRIBE Resonance AI System

🧠 **SCRIBE** is a revolutionary resonance intelligence system that actively explores and understands environments through sophisticated signal-response analysis.

## Overview

SCRIBE emits controlled acoustic signals, captures environmental responses, and uses advanced AI to interpret resonance patterns for material identification, environmental analysis, and anomaly detection.

## System Architecture

```
SCRIBE System Architecture:
├── Resonance Emission Engine     → Generates acoustic signals
├── Micro Listening Module        → Captures environmental responses  
├── Signal Processing Layer       → FFT and feature extraction
├── Resonance Interpretation Engine → AI pattern recognition
├── Chat Interface               → User interaction
└── Feedback Loop                → Continuous learning
```

## Features

### 🔍 Active Sensing
- Multi-frequency resonance signals (20Hz - 20kHz)
- Adaptive signal modulation
- Real-time signal optimization

### 🧠 Intelligent Analysis
- Machine learning interpretation (98.7% accuracy target)
- Real-time processing (1.2ms latency target)
- Pattern recognition and anomaly detection

### 💬 Conversational Interface
- Natural language interaction
- Command-based control
- Real-time feedback and insights

### 📚 Continuous Learning
- User feedback integration
- Pattern adaptation
- Performance optimization

## Installation

### Prerequisites
- Python 3.8+
- Audio input/output device
- 4GB+ RAM recommended

### Setup

1. **Clone and setup:**
```bash
cd /home/robbie/Desktop/scribe/scribe
pip install -r requirements.txt
```

2. **Install system dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-dev

# macOS
brew install portaudio

# Windows
# Install from http://www.portaudio.com/download.html
```

3. **Run the system:**
```bash
python main.py
```

## Usage

### Interactive Mode
```bash
python main.py
```

### Basic Commands
- `/scan` - Perform resonance scan
- `/status` - Show system status
- `/history` - View scan history
- `/help` - Show all commands

### Natural Language
- "What did you detect?"
- "Is this environment stable?"
- "What changed since the last scan?"
- "Scan the room"

### Feedback System
- `/feedback material wood` - Correct material identification
- `/feedback rating 5` - Rate interpretation accuracy
- `/feedback environment large_room` - Correct environment type

## Configuration

Edit `config.json` to customize:

```json
{
  "audio": {
    "sample_rate": 44100,
    "channels": 1,
    "chunk_size": 1024
  },
  "ai": {
    "confidence_threshold": 0.7,
    "learning_rate": 0.01
  },
  "processing": {
    "window_size": 2048,
    "fmin": 20.0,
    "fmax": 20000.0
  }
}
```

## Technical Specifications

### Signal Generation
- **Types**: Sine waves, frequency sweeps, pulse bursts, harmonic stacks
- **Range**: 20Hz - 20kHz
- **Precision**: 32-bit float

### Analysis Capabilities
- **FFT Analysis**: 2048-point window
- **Spectrogram**: Time-frequency analysis
- **Resonance Peaks**: Q-factor calculation
- **Harmonic Analysis**: HNR calculation
- **Envelope Analysis**: Attack/decay times

### AI Interpretation
- **Pattern Matching**: Material, environment, state recognition
- **Anomaly Detection**: Statistical deviation analysis
- **Temporal Analysis**: Change detection over time
- **Confidence Scoring**: Multi-factor confidence calculation

## Development

### Project Structure
```
scribe/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── config.json            # Configuration
├── src/
│   ├── core/              # System controller
│   ├── emitter/           # Signal generation
│   ├── listener/          # Audio capture
│   ├── processing/        # Signal analysis
│   ├── ai/                # Interpretation engine
│   ├── feedback/          # Learning system
│   ├── chat/              # User interface
│   └── utils/             # Utilities
└── docs/                  # Documentation
```

### Adding New Features

1. **New Signal Types**: Add to `emitter/tone_generator.py`
2. **Analysis Methods**: Add to `processing/fft_analyzer.py`
3. **Pattern Recognition**: Add to `ai/interpreter.py`
4. **Commands**: Add to `chat/interface.py`

## Performance Targets

- **System Availability**: 99.98%
- **Response Time**: 1.2ms average
- **Accuracy**: 98.7%
- **Throughput**: 1,250 requests/second
- **Error Rate**: 0.02%

## Troubleshooting

### Audio Issues
```bash
# Check available devices
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"

# Test audio capture
python -c "import pyaudio; import numpy as np; p = pyaudio.PyAudio(); stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True); data = stream.read(1024); print(f'Captured {len(data)} bytes')"
```

### Performance Issues
- Reduce `chunk_size` in config for lower latency
- Increase `window_size` for better frequency resolution
- Disable unused features in configuration

### Learning Issues
- Clear database: `rm scribe_learning.db`
- Reset patterns: Delete pattern_adaptations table
- Check feedback: Review user_feedback table

## API Reference

### Core Classes

- `ScribeSystemController`: Main system coordination
- `ResonanceEmissionEngine`: Signal generation
- `MicroListeningModule`: Audio capture
- `SignalProcessingLayer`: Feature extraction
- `ResonanceInterpretationEngine`: AI interpretation
- `FeedbackLoop`: Learning system
- `ChatInterface`: User interaction

### Key Methods

```python
# Perform scan
result = await system.perform_resonance_scan(config)

# Get system status
status = await system.get_system_status()

# Add user feedback
await feedback_loop.add_user_feedback(scan_id, "material", {"correct_material": "wood"})
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

This project is proprietary software. All rights reserved.

## Support

For technical support and questions, please refer to the documentation in the `docs/` directory or contact the development team.

---

**SCRIBE** - *Resonance Intelligence for Environmental Understanding*
