# SCRIBE Configuration Guide

## ⚙️ Configuration Overview

The SCRIBE system uses a comprehensive configuration system that allows fine-tuning of all aspects of the resonance analysis pipeline. This guide covers all configuration options, their effects, and best practices for different use cases.

## 📁 Configuration Files

### Primary Configuration
- **`config.json`** - Main system configuration
- **`default_config.py`** - Default values and fallbacks
- **Environment variables** - Runtime overrides

### Configuration Hierarchy
```
Environment Variables (highest priority)
    ↓
config.json (user overrides)
    ↓
default_config.py (system defaults)
    ↓
Component defaults (fallback values)
```

## 🔧 Complete Configuration Reference

### System Configuration
```json
{
  "system": {
    "production_mode": false,
    "debug_mode": false,
    "log_level": "INFO",
    "max_concurrent_scans": 5,
    "scan_timeout": 30.0,
    "cleanup_interval": 3600,
    "max_history": 1000
  }
}
```

#### System Parameters
- **`production_mode`** (boolean): Enable production optimizations
- **`debug_mode`** (boolean): Enable debug logging and features
- **`log_level`** (string): Logging level (DEBUG, INFO, WARNING, ERROR)
- **`max_concurrent_scans`** (integer): Maximum simultaneous scans
- **`scan_timeout`** (float): Maximum scan duration in seconds
- **`cleanup_interval`** (integer): Cleanup interval in seconds
- **`max_history`** (integer): Maximum scan history entries

### Audio Configuration
```json
{
  "audio": {
    "sample_rate": 44100,
    "channels": 1,
    "chunk_size": 1024,
    "format": "float32",
    "use_real_audio": true,
    "device_index": null,
    "latency": "low",
    "buffer_size": 4096
  }
}
```

#### Audio Parameters
- **`sample_rate`** (integer): Audio sample rate in Hz (22050, 44100, 48000, 96000)
- **`channels`** (integer): Number of audio channels (1=mono, 2=stereo)
- **`chunk_size`** (integer): Audio buffer size (512, 1024, 2048, 4096)
- **`format`** (string): Audio format (int16, int32, float32)
- **`use_real_audio`** (boolean): Use real audio hardware
- **`device_index`** (integer): Specific audio device index
- **`latency`** (string): Audio latency setting (low, medium, high)
- **`buffer_size`** (integer): Audio buffer size in samples

### Signal Processing Configuration
```json
{
  "processing": {
    "window_size": 2048,
    "hop_length": 512,
    "n_fft": 2048,
    "n_mels": 128,
    "fmin": 50.0,
    "fmax": 20000.0,
    "window_type": "hann",
    "normalize": true,
    "pre_emphasis": 0.97
  }
}
```

#### Processing Parameters
- **`window_size`** (integer): FFT window size (256, 512, 1024, 2048, 4096)
- **`hop_length`** (integer): Hop size for overlapping windows
- **`n_fft`** (integer): FFT size (power of 2)
- **`n_mels`** (integer): Number of mel frequency bands
- **`fmin`** (float): Minimum frequency for analysis
- **`fmax`** (float): Maximum frequency for analysis
- **`window_type`** (string): Window function (hann, hamming, blackman)
- **`normalize`** (boolean): Normalize audio signals
- **`pre_emphasis`** (float): Pre-emphasis filter coefficient

### AI Configuration
```json
{
  "ai": {
    "confidence_threshold": 0.7,
    "anomaly_threshold": 0.3,
    "learning_rate": 0.01,
    "max_patterns": 1000,
    "pattern_adaptation": true,
    "use_ml_models": true,
    "model_path": "models/",
    "feature_selection": true
  }
}
```

#### AI Parameters
- **`confidence_threshold`** (float): Minimum confidence for results (0.0-1.0)
- **`anomaly_threshold`** (float): Anomaly detection threshold (0.0-1.0)
- **`learning_rate`** (float): Learning rate for adaptation (0.001-0.1)
- **`max_patterns`** (integer): Maximum stored patterns
- **`pattern_adaptation`** (boolean): Enable pattern learning
- **`use_ml_models`** (boolean): Use machine learning models
- **`model_path`** (string): Path to ML model files
- **`feature_selection`** (boolean): Enable feature selection

### API Configuration
```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "reload": false,
    "access_log": true,
    "cors_origins": ["*"],
    "rate_limiting": true,
    "max_requests_per_minute": 100,
    "request_timeout": 30.0,
    "max_request_size": 1048576
  }
}
```

#### API Parameters
- **`host`** (string): API server host
- **`port`** (integer): API server port
- **`workers`** (integer): Number of worker processes
- **`reload`** (boolean): Enable auto-reload for development
- **`access_log`** (boolean): Enable access logging
- **`cors_origins`** (array): Allowed CORS origins
- **`rate_limiting`** (boolean): Enable rate limiting
- **`max_requests_per_minute`** (integer): Rate limit per minute
- **`request_timeout`** (float): Request timeout in seconds
- **`max_request_size`** (integer): Maximum request size in bytes

### Database Configuration
```json
{
  "database": {
    "type": "sqlite",
    "path": "scribe_learning.db",
    "backup_interval": 3600,
    "max_backups": 7,
    "connection_pool_size": 5,
    "query_timeout": 10.0,
    "enable_wal": true,
    "vacuum_interval": 86400
  }
}
```

#### Database Parameters
- **`type`** (string): Database type (sqlite, postgresql, mysql)
- **`path`** (string): Database file path
- **`backup_interval`** (integer): Backup interval in seconds
- **`max_backups`** (integer): Maximum backup files to keep
- **`connection_pool_size`** (integer): Database connection pool size
- **`query_timeout`** (float): Query timeout in seconds
- **`enable_wal`** (boolean): Enable WAL mode (SQLite)
- **`vacuum_interval`** (integer): Vacuum interval in seconds

### Monitoring Configuration
```json
{
  "monitoring": {
    "enable_metrics": true,
    "prometheus_port": 8001,
    "metrics_interval": 10,
    "health_check_interval": 30,
    "performance_tracking": true,
    "alert_thresholds": {
      "scan_duration": 5.0,
      "confidence_score": 0.5,
      "error_rate": 0.05,
      "memory_usage": 0.8,
      "cpu_usage": 0.9
    },
    "log_retention_days": 30
  }
}
```

#### Monitoring Parameters
- **`enable_metrics`** (boolean): Enable metrics collection
- **`prometheus_port`** (integer): Prometheus metrics port
- **`metrics_interval`** (integer): Metrics collection interval in seconds
- **`health_check_interval`** (integer): Health check interval in seconds
- **`performance_tracking`** (boolean): Enable performance tracking
- **`alert_thresholds`** (object): Alert threshold values
- **`log_retention_days`** (integer): Log retention period in days

### Security Configuration
```json
{
  "security": {
    "api_key_required": false,
    "api_key": "your-secret-key",
    "ssl_required": false,
    "cert_path": "/path/to/cert.pem",
    "key_path": "/path/to/key.pem",
    "allowed_ips": ["0.0.0.0/0"],
    "max_login_attempts": 5,
    "session_timeout": 3600,
    "encrypt_database": false
  }
}
```

#### Security Parameters
- **`api_key_required`** (boolean): Require API key authentication
- **`api_key`** (string): API key for authentication
- **`ssl_required`** (boolean): Require SSL/TLS
- **`cert_path`** (string): SSL certificate path
- **`key_path`** (string): SSL private key path
- **`allowed_ips`** (array): Allowed IP addresses
- **`max_login_attempts`** (integer): Maximum login attempts
- **`session_timeout`** (integer): Session timeout in seconds
- **`encrypt_database`** (boolean): Encrypt database

## 🎯 Configuration Profiles

### Development Profile
```json
{
  "system": {
    "production_mode": false,
    "debug_mode": true,
    "log_level": "DEBUG"
  },
  "audio": {
    "use_real_audio": false
  },
  "api": {
    "reload": true,
    "access_log": true
  },
  "monitoring": {
    "enable_metrics": false
  }
}
```

### Production Profile
```json
{
  "system": {
    "production_mode": true,
    "debug_mode": false,
    "log_level": "INFO"
  },
  "audio": {
    "use_real_audio": true,
    "buffer_size": 8192
  },
  "api": {
    "workers": 8,
    "reload": false
  },
  "monitoring": {
    "enable_metrics": true,
    "performance_tracking": true
  },
  "security": {
    "api_key_required": true,
    "ssl_required": true
  }
}
```

### High Performance Profile
```json
{
  "audio": {
    "sample_rate": 96000,
    "chunk_size": 4096,
    "buffer_size": 16384
  },
  "processing": {
    "window_size": 4096,
    "n_fft": 4096
  },
  "system": {
    "max_concurrent_scans": 10
  },
  "api": {
    "workers": 16
  }
}
```

### Low Resource Profile
```json
{
  "audio": {
    "sample_rate": 22050,
    "chunk_size": 512,
    "buffer_size": 1024
  },
  "processing": {
    "window_size": 512,
    "n_fft": 512
  },
  "system": {
    "max_concurrent_scans": 2,
    "max_history": 100
  },
  "monitoring": {
    "enable_metrics": false
  }
}
```

## 🔧 Configuration Management

### Loading Configuration
```python
from utils.config import Config

# Load default configuration
config = Config()

# Load from file
config = Config.from_file("custom_config.json")

# Load with profile
config = Config(profile="production")

# Override specific values
config.audio.sample_rate = 48000
config.ai.confidence_threshold = 0.8
```

### Environment Variables
```bash
# System settings
export SCRIBE_DEBUG=true
export SCRIBE_LOG_LEVEL=DEBUG

# Audio settings
export SCRIBE_AUDIO_SAMPLE_RATE=48000
export SCRIBE_AUDIO_USE_REAL_AUDIO=false

# API settings
export SCRIBE_API_PORT=8080
export SCRIBE_API_WORKERS=8

# Database settings
export SCRIBE_DB_PATH=/data/scribe.db
```

### Configuration Validation
```python
from utils.config import Config

config = Config()

# Validate configuration
errors = config.validate()
if errors:
    print("Configuration errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Configuration is valid")

# Check specific section
if config.audio.sample_rate not in [22050, 44100, 48000, 96000]:
    raise ValueError("Invalid sample rate")
```

## 🎛️ Advanced Configuration

### Custom Signal Types
```json
{
  "custom_signals": {
    "chirp": {
      "type": "frequency_modulated",
      "start_freq": 100,
      "end_freq": 10000,
      "duration": 2.0,
      "modulation_rate": 10.0
    },
    "noise_burst": {
      "type": "white_noise",
      "bandwidth": "full",
      "duration": 0.5,
      "envelope": "exponential"
    }
  }
}
```

### Feature Extraction Configuration
```json
{
  "features": {
    "time_domain": {
      "enabled": true,
      "metrics": ["rms", "peak", "crest_factor", "zero_crossing_rate"]
    },
    "frequency_domain": {
      "enabled": true,
      "metrics": ["spectral_centroid", "spectral_bandwidth", "spectral_rolloff"]
    },
    "harmonic_analysis": {
      "enabled": true,
      "max_harmonics": 10,
      "harmonic_tolerance": 0.05
    },
    "envelope_analysis": {
      "enabled": true,
      "attack_threshold": 0.01,
      "decay_threshold": 0.01
    }
  }
}
```

### Machine Learning Configuration
```json
{
  "ml": {
    "algorithms": {
      "material_classification": {
        "model_type": "random_forest",
        "n_estimators": 100,
        "max_depth": 10,
        "feature_importance_threshold": 0.01
      },
      "anomaly_detection": {
        "model_type": "isolation_forest",
        "contamination": 0.1,
        "n_estimators": 50
      }
    },
    "training": {
      "cross_validation_folds": 5,
      "test_size": 0.2,
      "random_state": 42,
      "feature_scaling": true
    }
  }
}
```

## 🔄 Dynamic Configuration

### Runtime Configuration Updates
```python
from utils.config import Config

config = Config()

# Update configuration at runtime
config.update({
    "audio": {"sample_rate": 48000},
    "ai": {"confidence_threshold": 0.8}
})

# Save configuration
config.save("updated_config.json")

# Reload configuration
config.reload()
```

### Configuration Hot Reload
```python
import asyncio
from utils.config import Config

class ConfigManager:
    def __init__(self):
        self.config = Config()
        self.config_file = "config.json"
        self.last_modified = 0
    
    async def watch_config(self):
        """Watch for configuration changes"""
        while True:
            try:
                current_modified = os.path.getmtime(self.config_file)
                if current_modified > self.last_modified:
                    self.config.reload()
                    self.last_modified = current_modified
                    print("Configuration reloaded")
            except FileNotFoundError:
                pass
            await asyncio.sleep(1)
```

## 📊 Performance Tuning

### Audio Performance
```json
{
  "audio": {
    "sample_rate": 44100,
    "chunk_size": 1024,
    "buffer_size": 4096,
    "latency": "low"
  }
}
```

**Optimization Tips:**
- Increase `chunk_size` for better performance
- Use `latency: "high"` for stability
- Reduce `sample_rate` for CPU savings

### Processing Performance
```json
{
  "processing": {
    "window_size": 2048,
    "hop_length": 512,
    "n_fft": 2048,
    "normalize": false
  }
}
```

**Optimization Tips:**
- Increase `window_size` for better frequency resolution
- Disable `normalize` for faster processing
- Use smaller `n_fft` for faster FFT

### System Performance
```json
{
  "system": {
    "max_concurrent_scans": 5,
    "scan_timeout": 30.0,
    "cleanup_interval": 3600
  }
}
```

**Optimization Tips:**
- Increase `max_concurrent_scans` for throughput
- Reduce `scan_timeout` for faster failure detection
- Decrease `cleanup_interval` for more frequent cleanup

## 🔍 Configuration Debugging

### Configuration Diagnostics
```python
from utils.config import Config

config = Config()

# Print all configuration
print("Current configuration:")
print(config.to_json(indent=2))

# Check specific sections
print(f"Audio sample rate: {config.audio.sample_rate}")
print(f"AI confidence threshold: {config.ai.confidence_threshold}")

# Validate configuration
errors = config.validate()
if errors:
    print("Configuration errors found:")
    for error in errors:
        print(f"  - {error}")
```

### Common Configuration Issues

#### Sample Rate Mismatch
```json
{
  "audio": {
    "sample_rate": 48000
  },
  "processing": {
    "fmin": 20.0,
    "fmax": 20000.0
  }
}
```
**Issue**: Processing frequency range incompatible with sample rate
**Fix**: Adjust `fmax` to be less than half the sample rate

#### Memory Usage
```json
{
  "processing": {
    "window_size": 8192,
    "n_fft": 8192
  }
}
```
**Issue**: Large FFT sizes consume significant memory
**Fix**: Reduce window size or enable memory optimization

#### Performance Bottlenecks
```json
{
  "system": {
    "max_concurrent_scans": 20
  }
}
```
**Issue**: Too many concurrent scans overwhelm system
**Fix**: Reduce concurrent scans or increase system resources

## 📚 Configuration Best Practices

### Development Environment
```json
{
  "system": {
    "debug_mode": true,
    "log_level": "DEBUG"
  },
  "audio": {
    "use_real_audio": false
  },
  "monitoring": {
    "enable_metrics": false
  }
}
```

### Production Environment
```json
{
  "system": {
    "production_mode": true,
    "debug_mode": false,
    "log_level": "INFO"
  },
  "security": {
    "api_key_required": true,
    "ssl_required": true
  },
  "monitoring": {
    "enable_metrics": true
  }
}
```

### Testing Environment
```json
{
  "system": {
    "debug_mode": true,
    "log_level": "INFO"
  },
  "audio": {
    "use_real_audio": false
  },
  "database": {
    "type": "sqlite",
    "path": ":memory:"
  }
}
```

## 🔧 Configuration Templates

### Basic Configuration Template
```json
{
  "system": {
    "production_mode": false,
    "debug_mode": false,
    "log_level": "INFO"
  },
  "audio": {
    "sample_rate": 44100,
    "channels": 1,
    "use_real_audio": true
  },
  "processing": {
    "window_size": 2048,
    "fmin": 50.0,
    "fmax": 20000.0
  },
  "ai": {
    "confidence_threshold": 0.7,
    "learning_rate": 0.01
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

### Advanced Configuration Template
```json
{
  "system": {
    "production_mode": true,
    "debug_mode": false,
    "log_level": "INFO",
    "max_concurrent_scans": 5,
    "scan_timeout": 30.0
  },
  "audio": {
    "sample_rate": 44100,
    "channels": 1,
    "chunk_size": 1024,
    "use_real_audio": true,
    "latency": "low"
  },
  "processing": {
    "window_size": 2048,
    "hop_length": 512,
    "n_fft": 2048,
    "fmin": 50.0,
    "fmax": 20000.0,
    "normalize": true
  },
  "ai": {
    "confidence_threshold": 0.7,
    "anomaly_threshold": 0.3,
    "learning_rate": 0.01,
    "pattern_adaptation": true
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "rate_limiting": true,
    "max_requests_per_minute": 100
  },
  "monitoring": {
    "enable_metrics": true,
    "prometheus_port": 8001,
    "performance_tracking": true
  },
  "security": {
    "api_key_required": false,
    "ssl_required": false
  }
}
```

---

**Last Updated**: 2026-05-06  
**Configuration Guide Version**: 1.0.0  
**Status**: Production Ready
