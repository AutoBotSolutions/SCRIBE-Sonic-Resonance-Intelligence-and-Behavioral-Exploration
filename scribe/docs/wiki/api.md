# SCRIBE API Documentation

## 🌐 API Overview

The SCRIBE Resonance AI System provides a comprehensive REST API for external integration and programmatic access to all system capabilities.

## 🚀 Quick Start

### Starting the API Server
```bash
./start_api.sh
```

The API server will start on `http://localhost:8000`

### Interactive Documentation
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)
Visit `http://localhost:8000/redoc` for alternative documentation (ReDoc)

## 📋 API Endpoints

### 🔍 System Information

#### `GET /`
Get basic API information and system status.

**Response**:
```json
{
  "name": "SCRIBE Resonance AI API",
  "version": "1.0.0",
  "description": "REST API for SCRIBE Resonance Intelligence System",
  "status": "operational",
  "docs": "/docs"
}
```

#### `GET /health`
Health check endpoint for monitoring.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-06T19:00:00Z",
  "service": "scribe-api",
  "version": "1.0.0"
}
```

#### `GET /status`
Get comprehensive system status.

**Response**:
```json
{
  "system_running": true,
  "scan_count": 5,
  "components": {
    "emission_engine": "operational",
    "listening_module": "operational",
    "signal_processor": "operational",
    "interpretation_engine": "operational",
    "feedback_loop": "operational"
  },
  "timestamp": "2026-05-06T19:00:00Z"
}
```

### 🔬 Scan Operations

#### `POST /scan`
Perform a resonance scan with specified parameters.

**Request Body**:
```json
{
  "signal_type": "sine",
  "frequency": 440.0,
  "duration": 2.0,
  "amplitude": 0.5
}
```

**Parameters**:
- `signal_type` (string): Type of signal to emit (`sine`, `sweep`, `pulse`, `harmonic`)
- `frequency` (float): Frequency in Hz (20.0 - 20000.0)
- `duration` (float): Duration in seconds (0.1 - 10.0)
- `amplitude` (float): Amplitude (0.0 - 1.0)

**Response**:
```json
{
  "scan_id": 123,
  "timestamp": "2026-05-06T19:00:00Z",
  "signals": [
    {
      "type": "sine",
      "frequency": 440.0,
      "duration": 2.0,
      "amplitude": 0.5
    }
  ],
  "interpretation": {
    "insights": [
      "Resonance peak detected at 440Hz with moderate Q-factor",
      "Environment shows stable acoustic properties"
    ],
    "confidence_scores": {
      "overall": 0.85,
      "material_matching": 0.90,
      "environment_matching": 0.80
    },
    "pattern_matches": {
      "materials": [
        {
          "material": "wood",
          "confidence": 0.90
        }
      ]
    }
  },
  "features": {
    "time_domain": {
      "rms": 0.12,
      "peak": 0.45
    },
    "frequency_domain": {
      "dominant_frequency": 440.0,
      "spectral_centroid": 1200.0
    }
  },
  "processing_time": 1.23
}
```

#### `GET /scans`
Get scan history with optional pagination.

**Query Parameters**:
- `limit` (integer): Maximum number of scans to return (default: 10)
- `offset` (integer): Offset for pagination (default: 0)

**Response**:
```json
{
  "scans": [
    {
      "scan_id": 123,
      "timestamp": "2026-05-06T19:00:00Z",
      "confidence": 0.85,
      "insights_count": 2
    }
  ],
  "total_count": 25,
  "limit": 10,
  "offset": 0
}
```

#### `GET /scans/{scan_id}`
Get detailed information about a specific scan.

**Path Parameters**:
- `scan_id` (integer): Unique identifier for the scan

**Response**:
```json
{
  "scan_id": 123,
  "timestamp": "2026-05-06T19:00:00Z",
  "signals": [...],
  "interpretation": {...},
  "features": {...},
  "processing_time": 1.23
}
```

### 📚 Learning & Feedback

#### `POST /feedback`
Submit user feedback for scan results.

**Request Body**:
```json
{
  "scan_id": 123,
  "feedback_type": "material_correction",
  "feedback_data": {
    "correct_material": "metal",
    "confidence": 0.95
  }
}
```

**Parameters**:
- `scan_id` (integer): ID of the scan to provide feedback for
- `feedback_type` (string): Type of feedback (`material_correction`, `environment_correction`, `state_correction`, `rating`)
- `feedback_data` (object): Feedback-specific data

**Response**:
```json
{
  "feedback_id": 456,
  "scan_id": 123,
  "status": "processed",
  "message": "Feedback recorded successfully"
}
```

#### `GET /learning/insights`
Get learning insights and statistics.

**Response**:
```json
{
  "total_scans": 150,
  "total_feedback": 25,
  "recent_performance": {
    "avg_confidence": 0.82,
    "accuracy_rate": 0.88
  },
  "top_adapted_patterns": [
    {
      "pattern": "wood_resonance",
      "adaptations": 5,
      "accuracy_improvement": 0.15
    }
  ],
  "feedback_trends": {
    "material_corrections": 12,
    "environment_corrections": 8,
    "state_corrections": 5
  }
}
```

#### `GET /learning/patterns`
Get adapted patterns from the learning system.

**Response**:
```json
{
  "patterns": [
    {
      "pattern_id": "wood_resonance_440hz",
      "type": "material",
      "confidence": 0.92,
      "adaptations": 3,
      "last_updated": "2026-05-06T18:45:00Z"
    }
  ],
  "total_patterns": 15
}
```

### 📊 Analytics & Metrics

#### `POST /compare`
Compare multiple scans.

**Request Body**:
```json
{
  "scan_ids": [123, 124, 125]
}
```

**Response**:
```json
{
  "comparison": {
    "scan_count": 3,
    "time_range": {
      "start": "2026-05-06T18:00:00Z",
      "end": "2026-05-06T19:00:00Z"
    },
    "changes": [
      {
        "type": "frequency_shift",
        "description": "Dominant frequency shifted from 440Hz to 445Hz",
        "significance": 0.75
      }
    ],
    "stability_score": 0.85
  }
}
```

#### `GET /metrics`
Get system performance metrics.

**Response**:
```json
{
  "system_metrics": {
    "uptime": 3600,
    "scan_count": 25,
    "avg_scan_duration": 1.2,
    "error_rate": 0.02
  },
  "performance_metrics": {
    "avg_confidence": 0.82,
    "accuracy_rate": 0.88,
    "processing_efficiency": 0.95
  },
  "resource_metrics": {
    "cpu_usage": 0.35,
    "memory_usage": 0.42,
    "disk_usage": 0.15
  }
}
```

## 🔐 Authentication

Currently, the SCRIBE API operates without authentication for development and testing purposes. Production deployments should implement appropriate authentication mechanisms.

## 🚨 Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "SCAN_FAILED",
    "message": "Failed to perform resonance scan",
    "details": "Audio capture timeout",
    "timestamp": "2026-05-06T19:00:00Z"
  }
}
```

### Common Error Codes
- `SCAN_FAILED` - Scan operation failed
- `INVALID_PARAMETERS` - Invalid request parameters
- `SYSTEM_ERROR` - Internal system error
- `RESOURCE_UNAVAILABLE` - System resource not available
- `NOT_FOUND` - Requested resource not found

## 🔄 Rate Limiting

The API implements rate limiting to ensure system stability:
- **Scan operations**: 10 requests per minute
- **Data retrieval**: 100 requests per minute
- **Feedback submission**: 50 requests per minute

## 📝 Request Examples

### Perform a Basic Scan
```bash
curl -X POST "http://localhost:8000/scan" \
  -H "Content-Type: application/json" \
  -d '{
    "signal_type": "sine",
    "frequency": 440.0,
    "duration": 2.0
  }'
```

### Get System Status
```bash
curl -X GET "http://localhost:8000/status"
```

### Submit Feedback
```bash
curl -X POST "http://localhost:8000/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "scan_id": 123,
    "feedback_type": "material_correction",
    "feedback_data": {
      "correct_material": "metal"
    }
  }'
```

## 🛠️ SDK Examples

### Python Example
```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Perform scan
response = requests.post(f"{BASE_URL}/scan", json={
    "signal_type": "sine",
    "frequency": 440.0,
    "duration": 2.0
})

if response.status_code == 200:
    scan_result = response.json()
    print(f"Scan completed with {scan_result['interpretation']['confidence_scores']['overall']:.1%} confidence")
```

### JavaScript Example
```javascript
// Perform scan
const response = await fetch('http://localhost:8000/scan', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    signal_type: 'sine',
    frequency: 440.0,
    duration: 2.0
  })
});

const scanResult = await response.json();
console.log(`Scan completed: ${scanResult.interpretation.confidence_scores.overall}`);
```

## 📊 WebSocket Support (Planned)

Future versions will include WebSocket support for real-time updates:
- Live scan progress
- Real-time status updates
- Streaming analytics data

## 🔍 Testing the API

### Using curl
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test scan endpoint
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"signal_type": "sine", "frequency": 440.0, "duration": 2.0}'
```

### Using Python requests
```python
import requests

# Test API
response = requests.get("http://localhost:8000/health")
print(f"API Status: {response.json()['status']}")
```

## 📚 Additional Resources

- [Interactive API Documentation](http://localhost:8000/docs)
- [Component Documentation](../components/)
- [System Architecture](../architecture/)
- [User Guide](../user-guide/)

---

**Last Updated**: 2026-05-06  
**API Version**: 1.0.0  
**Status**: Production Ready
