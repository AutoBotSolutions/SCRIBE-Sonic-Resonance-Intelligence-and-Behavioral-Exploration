# SCRIBE Tutorials and Examples

## Tutorial Overview

This section provides comprehensive tutorials and practical examples for using the SCRIBE Resonance AI System. From basic getting started guides to advanced use cases, these tutorials will help you master resonance analysis.

## Getting Started Tutorials

### Tutorial 1: First Resonance Scan
**Objective**: Perform your first resonance analysis and understand the results

#### Step 1: Start the System
```bash
# Start interactive mode
./start_interactive.sh
```

#### Step 2: Basic Scan
```
SCRIBE> /scan
```

#### Step 3: Understand Results
```
Scan completed with 85% confidence

Key Findings:
• Resonance peak detected at 440Hz with moderate Q-factor
• Environment shows stable acoustic properties
• Material characteristics suggest wooden surface
• No significant anomalies detected

Material: Wood (90% confidence)
Environment: Room (80% confidence)
State: Stable (85% confidence)
```

#### Step 4: Natural Language Query
```
SCRIBE> What did you detect?
```

### Tutorial 2: Custom Signal Parameters
**Objective**: Learn to customize scan parameters for specific analysis

#### Frequency-Specific Analysis
```
SCRIBE> /scan --type=sine --frequency=1000 --duration=3
```

#### Material Analysis Setup
```
SCRIBE> /scan --type=sine --frequency=440 --duration=2 --amplitude=0.8
```

#### Broad Spectrum Analysis
```
SCRIBE> /scan --type=sweep --duration=5
```

### Tutorial 3: Feedback and Learning
**Objective**: Help the system learn from your corrections

#### Provide Material Feedback
```
SCRIBE> /scan
SCRIBE> /feedback material oak
```

#### Rate Scan Accuracy
```
SCRIBE> /feedback rating 5
```

#### Check Learning Progress
```
SCRIBE> What have you learned?
```

## Advanced Tutorials

### Tutorial 4: Material Identification
**Objective**: Accurately identify materials using resonance analysis

#### Setup for Material Analysis
```python
# Configure for material detection
config = {
    "processing": {
        "window_size": 2048,
        "fmin": 100.0,
        "fmax": 5000.0
    },
    "ai": {
        "confidence_threshold": 0.8,
        "pattern_adaptation": true
    }
}
```

#### Material Detection Scan
```
SCRIBE> /scan --type=sine --frequency=440 --duration=2
SCRIBE> What material is this?
```

#### Comparative Analysis
```
SCRIBE> /scan --type=sine --frequency=440 --duration=2
SCRIBE> /scan --type=sine --frequency=880 --duration=2
SCRIBE> Compare these scans
```

### Tutorial 5: Environmental Analysis
**Objective**: Analyze room acoustics and environmental properties

#### Room Acoustic Profile
```
SCRIBE> /scan --type=sweep --duration=5
SCRIBE> How reverberant is this room?
SCRIBE> What are the room modes?
```

#### Environmental Comparison
```
SCRIBE> /scan --type=sweep --duration=3
# Move to different location
SCRIBE> /scan --type=sweep --duration=3
SCRIBE> Compare to previous scan
```

### Tutorial 6: Structural Analysis
**Objective**: Detect structural resonances and anomalies

#### Structural Resonance Detection
```
SCRIBE> /scan --type=pulse --duration=1
SCRIBE> Are there any structural resonances?
SCRIBE> Detect any anomalies
```

#### Time-Based Analysis
```
SCRIBE> /scan --type=sine --frequency=100 --duration=3
# Wait 10 minutes
SCRIBE> /scan --type=sine --frequency=100 --duration=3
SCRIBE> What changed since the last scan?
```

## Programming Tutorials

### Tutorial 7: Python API Integration
**Objective**: Use SCRIBE programmatically with Python

#### Basic API Usage
```python
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

# Perform scan
def perform_scan(frequency=440, duration=2.0):
    response = requests.post(f"{BASE_URL}/scan", json={
        "signal_type": "sine",
        "frequency": frequency,
        "duration": duration
    })
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Scan failed: {response.text}")

# Get results
result = perform_scan()
print(f"Confidence: {result['interpretation']['confidence_scores']['overall']:.1%}")
print(f"Insights: {len(result['interpretation']['insights'])}")
```

#### Advanced API Integration
```python
import asyncio
import aiohttp

class ScribeClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    async def scan(self, signal_type="sine", frequency=440, duration=2.0):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/scan", json={
                "signal_type": signal_type,
                "frequency": frequency,
                "duration": duration
            }) as response:
                return await response.json()
    
    async def get_status(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/status") as response:
                return await response.json()
    
    async def compare_scans(self, scan_ids):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/compare", json=scan_ids) as response:
                return await response.json()

# Usage
async def main():
    client = ScribeClient()
    
    # Perform multiple scans
    scans = []
    for freq in [220, 440, 880]:
        result = await client.scan(frequency=freq)
        scans.append(result)
    
    # Compare results
    comparison = await client.compare_scans([scan['scan_id'] for scan in scans])
    print(f"Comparison: {comparison}")

asyncio.run(main())
```

### Tutorial 8: Real-time Analysis
**Objective**: Implement real-time resonance monitoring

#### Real-time Monitoring Script
```python
import asyncio
import time
from scribe_client import ScribeClient

class RealTimeMonitor:
    def __init__(self, interval=60):
        self.client = ScribeClient()
        self.interval = interval
        self.baseline = None
    
    async def establish_baseline(self):
        """Establish baseline resonance profile"""
        print("Establishing baseline...")
        self.baseline = await self.client.scan(frequency=440, duration=3)
        print(f"Baseline established: {self.baseline['interpretation']['confidence_scores']['overall']:.1%}")
    
    async def monitor_continuously(self):
        """Continuously monitor for changes"""
        while True:
            try:
                current = await self.client.scan(frequency=440, duration=2)
                
                # Compare with baseline
                comparison = await self.client.compare_scans([
                    self.baseline['scan_id'], 
                    current['scan_id']
                ])
                
                # Check for significant changes
                if comparison['stability_score'] < 0.7:
                    print(f"Significant change detected! Stability: {comparison['stability_score']:.1%}")
                    print(f"Changes: {len(comparison['changes'])}")
                
                await asyncio.sleep(self.interval)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(10)

# Usage
monitor = RealTimeMonitor(interval=30)
await monitor.establish_baseline()
await monitor.monitor_continuously()
```

## Use Case Examples

### Use Case 1: Musical Instrument Analysis
**Objective**: Analyze musical instrument acoustics

#### Guitar Analysis
```python
# Configure for instrument analysis
instrument_config = {
    "audio": {
        "sample_rate": 48000,
        "chunk_size": 2048
    },
    "processing": {
        "fmin": 80.0,
        "fmax": 8000.0,
        "window_size": 4096
    }
}

# Analyze guitar strings
string_frequencies = [82.4, 110.0, 146.8, 196.0, 246.9, 329.6]  # E-A-D-G-B-E

for freq in string_frequencies:
    result = await client.scan(frequency=freq, duration=3)
    print(f"String {freq}Hz: {result['interpretation']['confidence_scores']['overall']:.1%}")
```

#### Piano Analysis
```python
# Piano frequency range analysis
piano_frequencies = [27.5, 55.0, 110.0, 220.0, 440.0, 880.0, 1760.0, 3520.0]

for freq in piano_frequencies:
    result = await client.scan(frequency=freq, type="sine", duration=2)
    harmonics = result['features']['harmonics']
    print(f"Note {freq}Hz: {len(harmonics['harmonics'])} harmonics detected")
```

### Use Case 2: Room Acoustics Analysis
**Objective**: Optimize room acoustics for recording

#### Room Acoustic Profiling
```python
# Comprehensive room analysis
async def analyze_room():
    # Low frequency response
    low_freq = await client.scan(frequency=100, duration=5, type="sine")
    
    # Mid frequency response
    mid_freq = await client.scan(frequency=1000, duration=3, type="sine")
    
    # High frequency response
    high_freq = await client.scan(frequency=8000, duration=2, type="sine")
    
    # Full spectrum sweep
    full_spectrum = await client.scan(duration=10, type="sweep")
    
    # Analyze results
    analyses = [low_freq, mid_freq, high_freq, full_spectrum]
    
    for i, analysis in enumerate(analyses):
        features = analysis['features']
        print(f"Analysis {i+1}:")
        print(f"  RMS: {features['time_domain']['rms']:.3f}")
        print(f"  Spectral centroid: {features['frequency_domain']['spectral_centroid']:.1f} Hz")
        print(f"  Confidence: {analysis['interpretation']['confidence_scores']['overall']:.1%}")

await analyze_room()
```

### Use Case 3: Material Testing
**Objective**: Identify and test material properties

#### Material Comparison
```python
# Test different materials
materials = ["wood", "metal", "plastic", "glass"]

async def test_materials():
    results = {}
    
    for material in materials:
        print(f"Testing {material}...")
        
        # Perform scan
        result = await client.scan(frequency=440, duration=3)
        
        # Store results
        results[material] = {
            'confidence': result['interpretation']['confidence_scores']['overall'],
            'features': result['features'],
            'insights': result['interpretation']['insights']
        }
        
        # Provide feedback
        await client.add_feedback(
            scan_id=result['scan_id'],
            feedback_type="material_correction",
            feedback_data={"correct_material": material}
        )
    
    # Compare results
    print("\nMaterial Comparison:")
    for material, data in results.items():
        print(f"{material}: {data['confidence']:.1%} confidence")
        print(f"  Insights: {len(data['insights'])}")

await test_materials()
```

### Use Case 4: Quality Control
**Objective**: Use resonance analysis for quality control

#### Manufacturing Quality Check
```python
class QualityController:
    def __init__(self, client):
        self.client = client
        self.baseline = None
    
    async def establish_baseline(self, sample_count=10):
        """Establish quality baseline"""
        print("Establishing quality baseline...")
        
        scans = []
        for i in range(sample_count):
            scan = await self.client.scan(frequency=440, duration=2)
            scans.append(scan)
        
        # Calculate baseline metrics
        confidences = [s['interpretation']['confidence_scores']['overall'] for s in scans]
        self.baseline = {
            'mean_confidence': sum(confidences) / len(confidences),
            'std_confidence': (sum((c - sum(confidences)/len(confidences))**2 for c in confidences) / len(confidences))**0.5
        }
        
        print(f"Baseline: {self.baseline['mean_confidence']:.1%} ± {self.baseline['std_confidence']:.1%}")
    
    async def check_quality(self, threshold=0.8):
        """Check if sample meets quality standards"""
        scan = await self.client.scan(frequency=440, duration=2)
        confidence = scan['interpretation']['confidence_scores']['overall']
        
        # Check against baseline
        deviation = abs(confidence - self.baseline['mean_confidence'])
        std_devs = deviation / self.baseline['std_confidence']
        
        # Quality assessment
        if confidence >= threshold and std_devs <= 2:
            return True, "PASS"
        elif confidence >= threshold - 0.1:
            return False, "MARGINAL"
        else:
            return False, "FAIL"

# Usage
qc = QualityController(client)
await qc.establish_baseline()

# Check samples
for i in range(5):
    passed, status = await qc.check_quality()
    print(f"Sample {i+1}: {status}")
```

## Integration Examples

### Integration with IoT Devices
```python
import asyncio
import json
from scribe_client import ScribeClient

class IoTIntegration:
    def __init__(self):
        self.client = ScribeClient()
        self.device_registry = {}
    
    async def register_device(self, device_id, location, device_type):
        """Register IoT device for monitoring"""
        self.device_registry[device_id] = {
            'location': location,
            'type': device_type,
            'baseline': None,
            'last_scan': None
        }
        
        # Establish baseline
        baseline = await self.client.scan(frequency=440, duration=3)
        self.device_registry[device_id]['baseline'] = baseline
        
        print(f"Device {device_id} registered at {location}")
    
    async def monitor_device(self, device_id):
        """Monitor specific device"""
        if device_id not in self.device_registry:
            raise ValueError(f"Device {device_id} not registered")
        
        device = self.device_registry[device_id]
        current_scan = await self.client.scan(frequency=440, duration=2)
        
        # Compare with baseline
        comparison = await self.client.compare_scans([
            device['baseline']['scan_id'],
            current_scan['scan_id']
        ])
        
        # Check for anomalies
        if comparison['stability_score'] < 0.7:
            alert = {
                'device_id': device_id,
                'location': device['location'],
                'stability_score': comparison['stability_score'],
                'changes': comparison['changes'],
                'timestamp': current_scan['timestamp']
            }
            
            # Send alert (implementation depends on your alert system)
            await self.send_alert(alert)
        
        device['last_scan'] = current_scan
        return comparison
    
    async def send_alert(self, alert):
        """Send alert to monitoring system"""
        print(f"ALERT: {alert['device_id']} at {alert['location']} - Stability: {alert['stability_score']:.1%}")
        # Implementation: Send to your monitoring system

# Usage
iot = IoTIntegration()
await iot.register_device("sensor_001", "factory_floor_a", "vibration_sensor")
await iot.register_device("sensor_002", "factory_floor_b", "vibration_sensor")

# Continuous monitoring
while True:
    for device_id in iot.device_registry:
        await iot.monitor_device(device_id)
    await asyncio.sleep(60)  # Check every minute
```

### Integration with Data Analytics
```python
import pandas as pd
import matplotlib.pyplot as plt
from scribe_client import ScribeClient

class AnalyticsIntegration:
    def __init__(self, client):
        self.client = client
        self.data = []
    
    async def collect_scan_data(self, duration_hours=24):
        """Collect scan data over time period"""
        end_time = time.time()
        start_time = end_time - (duration_hours * 3600)
        
        # Get scan history
        history = await self.client.get_scan_history(limit=1000)
        
        # Filter by time range
        filtered_scans = [
            scan for scan in history['scans']
            if start_time <= scan['timestamp'] <= end_time
        ]
        
        self.data = filtered_scans
        print(f"Collected {len(self.data)} scans over {duration_hours} hours")
    
    def analyze_trends(self):
        """Analyze trends in scan data"""
        if not self.data:
            print("No data available for analysis")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(self.data)
        
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        
        # Analyze confidence trends
        hourly_confidence = df.groupby('hour')['confidence'].mean()
        
        print("Hourly Confidence Trends:")
        for hour, confidence in hourly_confidence.items():
            print(f"  Hour {hour}: {confidence:.1%}")
        
        # Plot trends
        plt.figure(figsize=(12, 6))
        
        plt.subplot(2, 2, 1)
        plt.plot(df['timestamp'], df['confidence'])
        plt.title('Confidence Over Time')
        plt.ylabel('Confidence')
        
        plt.subplot(2, 2, 2)
        hourly_confidence.plot(kind='bar')
        plt.title('Average Confidence by Hour')
        plt.ylabel('Confidence')
        plt.xlabel('Hour')
        
        plt.subplot(2, 2, 3)
        df['confidence'].hist(bins=20)
        plt.title('Confidence Distribution')
        plt.xlabel('Confidence')
        plt.ylabel('Frequency')
        
        plt.subplot(2, 2, 4)
        df.boxplot(column='confidence', by='hour')
        plt.title('Confidence by Hour')
        plt.ylabel('Confidence')
        
        plt.tight_layout()
        plt.show()
    
    def generate_report(self):
        """Generate analytics report"""
        if not self.data:
            return "No data available"
        
        df = pd.DataFrame(self.data)
        
        report = f"""
# SCRIBE Analytics Report

## Summary Statistics
- Total Scans: {len(df)}
- Average Confidence: {df['confidence'].mean():.1%}
- Confidence Std Dev: {df['confidence'].std():.1%}
- Min Confidence: {df['confidence'].min():.1%}
- Max Confidence: {df['confidence'].max():.1%}

## Time Analysis
- Time Range: {df['timestamp'].min()} to {df['timestamp'].max()}
- Average Scans per Hour: {len(df) / ((df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600):.1f}

## Quality Metrics
- Scans Above 80% Confidence: {len(df[df['confidence'] > 0.8])} ({len(df[df['confidence'] > 0.8])/len(df):.1%})
- Scans Below 50% Confidence: {len(df[df['confidence'] < 0.5])} ({len(df[df['confidence'] < 0.5])/len(df):.1%})

## Recommendations
"""
        
        # Add recommendations based on data
        if df['confidence'].mean() < 0.7:
            report += "- Average confidence is below 70%. Consider environmental improvements.\n"
        
        if df['confidence'].std() > 0.2:
            report += "- High variance in confidence. Check for environmental inconsistencies.\n"
        
        return report

# Usage
analytics = AnalyticsIntegration(client)
await analytics.collect_scan_data(duration_hours=24)
analytics.analyze_trends()
print(analytics.generate_report())
```

## Best Practices

### Scan Optimization
1. **Choose appropriate frequencies** for your target analysis
2. **Use sufficient duration** for accurate results (2-5 seconds)
3. **Minimize background noise** during scans
4. **Maintain consistent positioning** for comparative analysis

### Data Management
1. **Regularly back up** learning database
2. **Monitor system performance** and adjust parameters
3. **Provide consistent feedback** to improve accuracy
4. **Document scan conditions** for reproducibility

### Integration Tips
1. **Handle errors gracefully** in API calls
2. **Implement rate limiting** for high-frequency scanning
3. **Cache results** when appropriate
4. **Monitor system resources** during operation

---

**Last Updated**: 2026-05-06  
**Tutorials Version**: 1.0.0  
**Status**: Production Ready
