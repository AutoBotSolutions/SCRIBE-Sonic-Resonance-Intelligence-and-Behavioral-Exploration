"""
Configuration Management for SCRIBE System
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass

@dataclass
class AudioConfig:
    """Audio system configuration"""
    sample_rate: int = 44100
    channels: int = 1
    chunk_size: int = 1024
    format: str = "float32"
    device_index: Optional[int] = None

@dataclass
class ProcessingConfig:
    """Signal processing configuration"""
    window_size: int = 2048
    hop_length: int = 512
    n_fft: int = 2048
    n_mels: int = 128
    fmin: float = 20.0
    fmax: float = 20000.0

@dataclass
class AIConfig:
    """AI interpretation configuration"""
    confidence_threshold: float = 0.7
    pattern_matching_threshold: float = 0.8
    anomaly_detection_threshold: float = 2.0
    learning_rate: float = 0.01
    model_update_frequency: int = 100

@dataclass
class DatabaseConfig:
    """Database configuration"""
    path: str = "scribe_learning.db"
    backup_enabled: bool = True
    backup_interval: int = 3600  # seconds

class Config:
    """Main configuration manager for SCRIBE system"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._find_config_file()
        self.config_data = {}
        
        # Load configuration
        self._load_config()
        
        # Initialize sub-configurations
        self.audio = AudioConfig(**self.config_data.get('audio', {}))
        self.processing = ProcessingConfig(**self.config_data.get('processing', {}))
        self.ai = AIConfig(**self.config_data.get('ai', {}))
        self.database = DatabaseConfig(**self.config_data.get('database', {}))
    
    def _find_config_file(self) -> str:
        """Find configuration file in standard locations"""
        possible_paths = [
            "config.json",
            "scribe_config.json",
            os.path.expanduser("~/.scribe/config.json"),
            "/etc/scribe/config.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Create default config if none found
        default_path = "config.json"
        self._create_default_config(default_path)
        return default_path
    
    def _create_default_config(self, path: str):
        """Create default configuration file"""
        default_config = {
            "audio": {
                "sample_rate": 44100,
                "channels": 1,
                "chunk_size": 1024,
                "format": "float32",
                "device_index": None
            },
            "processing": {
                "window_size": 2048,
                "hop_length": 512,
                "n_fft": 2048,
                "n_mels": 128,
                "fmin": 20.0,
                "fmax": 20000.0
            },
            "ai": {
                "confidence_threshold": 0.7,
                "pattern_matching_threshold": 0.8,
                "anomaly_detection_threshold": 2.0,
                "learning_rate": 0.01,
                "model_update_frequency": 100
            },
            "database": {
                "path": "scribe_learning.db",
                "backup_enabled": True,
                "backup_interval": 3600
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "scribe.log"
            }
        }
        
        with open(path, 'w') as f:
            json.dump(default_config, f, indent=2)
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config_data = json.load(f)
            else:
                self.config_data = {}
        except Exception as e:
            print(f"Warning: Could not load config file {self.config_file}: {e}")
            self.config_data = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config_data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    @property
    def default_signal_config(self) -> Dict[str, Any]:
        """Get default signal configuration for scanning"""
        return {
            'signal_type': 'sine',
            'frequency': 440.0,
            'duration': 2.0,
            'amplitude': 0.5
        }
    
    def __getitem__(self, key: str) -> Any:
        """Dictionary-style access"""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any):
        """Dictionary-style assignment"""
        self.set(key, value)
