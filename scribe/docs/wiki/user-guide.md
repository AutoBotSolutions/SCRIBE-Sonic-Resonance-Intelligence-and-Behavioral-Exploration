# SCRIBE User Guide

## 👋 Welcome to SCRIBE

The SCRIBE (Sonic Resonance Intelligence and Behavioral Exploration) system is an advanced resonance intelligence platform that analyzes environments through acoustic signals. This guide will help you get started and make the most of SCRIBE's capabilities.

## 🚀 Quick Start

### Starting the System

#### Interactive Mode (Recommended for Beginners)
```bash
./start_interactive.sh
```

#### API Server Mode
```bash
./start_api.sh
```

#### Full Deployment
```bash
./deploy.sh
```

### Your First Scan

Once the system starts, you'll see the chat interface:

```
🔍 SCRIBE> 
```

Type `help` to see available commands, or simply ask:

```
🔍 SCRIBE> What did you detect?
```

The system will perform a resonance scan and provide insights about the environment.

## 💬 Chat Interface Commands

### Basic Commands

#### `/scan` - Perform Resonance Analysis
```
🔍 SCRIBE> /scan
```
Performs a complete resonance scan with default parameters.

#### `/scan --type=sine --frequency=440 --duration=2` - Custom Scan
```
🔍 SCRIBE> /scan --type=sine --frequency=440 --duration=2
```
Performs a scan with custom parameters.

#### `/status` - Check System Health
```
🔍 SCRIBE> /status
```
Shows current system status and component health.

#### `/help` - Show Available Commands
```
🔍 SCRIBE> /help
```
Displays all available commands and usage examples.

#### `/history` - View Scan History
```
🔍 SCRIBE> /history
```
Shows recent scans and their results.

### Feedback Commands

#### `/feedback material wood` - Correct Material Identification
```
🔍 SCRIBE> /feedback material wood
```
Tells the system the correct material for the last scan.

#### `/feedback rating 5` - Rate Scan Accuracy
```
🔍 SCRIBE> /feedback rating 5
```
Rates the accuracy of the last scan (1-5 scale).

#### `/feedback environment room` - Correct Environment Type
```
🔍 SCRIBE> /feedback environment room
```
Corrects the environment classification.

## 🗣️ Natural Language Interaction

SCRIBE understands natural language queries. Here are some examples:

### Environment Analysis
```
🔍 SCRIBE> What did you detect?
🔍 SCRIBE> Is this environment stable?
🔍 SCRIBE> What materials are present?
🔍 SCRIBE> Analyze the acoustic properties
```

### Comparison Questions
```
🔍 SCRIBE> Compare this scan to the previous one
🔍 SCRIBE> What changed since the last scan?
🔍 SCRIBE> How does this environment compare to a room?
```

### System Information
```
🔍 SCRIBE> How confident are you in your analysis?
🔍 SCRIBE> What frequency ranges did you analyze?
🔍 SCRIBE> Show me the resonance peaks
```

### Learning and Feedback
```
🔍 SCRIBE> What have you learned from previous scans?
🔍 SCRIBE> How accurate have your predictions been?
🔍 SCRIBE> What patterns do you recognize?
```

## 📊 Understanding Scan Results

### Confidence Scores
SCRIBE provides confidence scores for different aspects of analysis:

- **Overall Confidence**: General accuracy of the interpretation
- **Material Matching**: Confidence in material identification
- **Environment Matching**: Confidence in environment classification
- **State Matching**: Confidence in state assessment
- **Anomaly Detection**: Confidence in anomaly identification

### Typical Insights
```
✅ Scan completed with 85% confidence

🔍 Key Findings:
• Resonance peak detected at 440Hz with moderate Q-factor
• Environment shows stable acoustic properties
• Material characteristics suggest wooden surface
• No significant anomalies detected

🪵 Material: Wood (90% confidence)
🏠 Environment: Room (80% confidence)
⚖️ State: Stable (85% confidence)
```

### Feature Types
SCRIBE analyzes multiple acoustic features:

- **Time Domain**: RMS, peak levels, zero crossings
- **Frequency Domain**: Dominant frequencies, spectral centroid
- **Resonance Peaks**: Frequency peaks and Q-factors
- **Harmonics**: Harmonic content and ratios
- **Envelope**: Attack and decay characteristics
- **Noise Profile**: Background noise characteristics

## 🔧 Advanced Usage

### Custom Signal Parameters

#### Signal Types
- `sine`: Pure tone at single frequency
- `sweep`: Frequency sweep from low to high
- `pulse`: Short pulse bursts
- `harmonic`: Multiple frequency harmonics

#### Parameter Ranges
- **Frequency**: 20Hz - 20,000Hz
- **Duration**: 0.1s - 10s
- **Amplitude**: 0.0 - 1.0

### Example Custom Scans
```
# Low frequency sweep
🔍 SCRIBE> /scan --type=sweep --frequency=100 --duration=5

# High frequency analysis
🔍 SCRIBE> /scan --type=sine --frequency=8000 --duration=1

# Harmonic stack
🔍 SCRIBE> /scan --type=harmonic --frequency=440 --duration=3
```

### Batch Operations
For multiple scans, use the API or scripting:

```python
import requests

# Perform multiple scans
frequencies = [220, 440, 880, 1760]
for freq in frequencies:
    response = requests.post('http://localhost:8000/scan', json={
        'signal_type': 'sine',
        'frequency': freq,
        'duration': 2.0
    })
    print(f"Scan at {freq}Hz: {response.json()['interpretation']['confidence_scores']['overall']:.1%}")
```

## 📚 Best Practices

### Getting Accurate Results

1. **Environment Setup**: Minimize background noise during scans
2. **Consistent Positioning**: Keep the microphone/sensor in the same position
3. **Multiple Scans**: Perform several scans to establish baseline
4. **Provide Feedback**: Help the system learn by providing corrections

### Optimal Scan Parameters

#### Material Analysis
- **Frequency**: 200Hz - 2000Hz (resonance range)
- **Duration**: 2-3 seconds
- **Signal Type**: Sine or sweep

#### Environment Analysis
- **Frequency**: 100Hz - 5000Hz (broad range)
- **Duration**: 3-5 seconds
- **Signal Type**: Sweep or harmonic

#### Anomaly Detection
- **Frequency**: Full range (20Hz - 20kHz)
- **Duration**: 5+ seconds
- **Signal Type**: Sweep or pulse

### Interpreting Results

#### High Confidence (>80%)
- Results are reliable
- Material/environment identification is accurate
- Can be used for critical decisions

#### Medium Confidence (50-80%)
- Results are moderately reliable
- May need additional scans for confirmation
- Good for general analysis

#### Low Confidence (<50%)
- Results are uncertain
- Environmental factors may be interfering
- Recommend improving conditions and rescanning

## 🎯 Use Cases

### Material Identification
```
🔍 SCRIBE> /scan --type=sine --frequency=440 --duration=2
🔍 SCRIBE> What material is this?
🔍 SCRIBE> /feedback material oak if it's wood
```

### Room Acoustics
```
🔍 SCRIBE> /scan --type=sweep --duration=5
🔍 SCRIBE> How reverberant is this room?
🔍 SCRIBE> What are the room modes?
```

### Structural Analysis
```
🔍 SCRIBE> /scan --type=pulse --duration=1
🔍 SCRIBE> Are there any structural resonances?
🔍 SCRIBE> Compare to previous scan
```

### Environmental Monitoring
```
🔍 SCRIBE> /scan --type=harmonic --duration=3
🔍 SCRIBE> Has anything changed recently?
🔍 SCRIBE> /feedback rating 5
```

## 🔍 Troubleshooting

### Common Issues

#### Low Confidence Results
- **Cause**: Noisy environment or poor signal
- **Solution**: Reduce background noise, increase duration

#### System Not Responding
- **Cause**: System busy or error
- **Solution**: Check `/status`, restart if needed

#### Inconsistent Results
- **Cause**: Variable conditions
- **Solution**: Multiple scans, provide feedback

### Getting Help

1. **Use `/help`**: Shows all available commands
2. **Check `/status`**: Verify system health
3. **Review `/history`**: Look for patterns in results
4. **Provide Feedback**: Help the system learn

## 📖 Advanced Topics

### Understanding Resonance

Resonance occurs when an object vibrates at its natural frequency. SCRIBE:
1. Emits controlled acoustic signals
2. Measures the environmental response
3. Analyzes resonance patterns
4. Identifies materials and properties

### Signal Processing

SCRIBE uses advanced signal processing:
- **FFT Analysis**: Frequency domain transformation
- **Spectrogram**: Time-frequency representation
- **Peak Detection**: Resonance frequency identification
- **Envelope Analysis**: Temporal characteristics

### Machine Learning

The system learns from:
- **User Feedback**: Corrections and ratings
- **Pattern Recognition**: Repeated signatures
- **Adaptation**: Improves over time

## 🔗 External Resources

- [API Documentation](../api/)
- [Component Details](../components/)
- [System Architecture](../architecture/)
- [Troubleshooting Guide](../troubleshooting/)

## 💡 Tips and Tricks

### Power User Commands
```
# Quick material check
🔍 SCRIBE> /scan && what material is this?

# Environment comparison
🔍 SCRIBE> /scan --type=sweep && compare to last scan

# Learning check
🔍 SCRIBE> /feedback rating 5 && what have you learned?
```

### Keyboard Shortcuts
- **Up Arrow**: Previous commands
- **Tab**: Command completion (if supported)
- **Ctrl+C**: Exit the system

### Scripting Examples
Create a file `scan_script.txt`:
```
/scan --type=sine --frequency=440 --duration=2
what material is this?
/feedback material wood
/scan --type=sweep --duration=3
how reverberant is this room?
```

Run with:
```bash
cat scan_script.txt | ./start_interactive.sh
```

---

**Last Updated**: 2026-05-06  
**Guide Version**: 1.0.0  
**Status**: Production Ready
