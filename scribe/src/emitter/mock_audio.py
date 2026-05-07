"""
Mock Audio System for Testing
Fallback when PyAudio is not available
"""

import numpy as np
import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class SignalConfig:
    """Configuration for resonance signal generation"""
    signal_type: str = "sine"
    frequency: float = 440.0
    duration: float = 2.0
    sample_rate: int = 44100
    amplitude: float = 0.5

class MockResonanceEmissionEngine:
    """Mock resonance emission engine for testing without audio hardware"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
        
        # Mock audio parameters
        self.sample_rate = config.get('sample_rate', 44100)
        self.channels = config.get('channels', 1)
        
        self.logger.info("Mock Resonance Emission Engine created")
    
    async def initialize(self):
        """Initialize mock audio system"""
        self.logger.info("🔧 Initializing mock audio system...")
        await asyncio.sleep(0.1)  # Simulate initialization time
        self.is_initialized = True
        self.logger.info("✅ Mock Resonance Emission Engine initialized")
    
    async def cleanup(self):
        """Cleanup mock audio resources"""
        self.is_initialized = False
        self.logger.info("Mock Resonance Emission Engine cleaned up")
    
    def generate_sine_wave(self, config: SignalConfig) -> np.ndarray:
        """Generate sine wave signal"""
        t = np.linspace(0, config.duration, int(self.sample_rate * config.duration))
        signal = config.amplitude * np.sin(2 * np.pi * config.frequency * t)
        return signal.astype(np.float32)
    
    def generate_frequency_sweep(self, config: SignalConfig) -> np.ndarray:
        """Generate frequency sweep signal"""
        t = np.linspace(0, config.duration, int(self.sample_rate * config.duration))
        sweep_rate = (20000 / 20) ** (1 / config.duration)
        instantaneous_freq = 20 * (sweep_rate ** t)
        phase = 2 * np.pi * np.cumsum(instantaneous_freq) / self.sample_rate
        signal = config.amplitude * np.sin(phase)
        return signal.astype(np.float32)
    
    def generate_pulse_burst(self, config: SignalConfig) -> np.ndarray:
        """Generate pulse burst signal"""
        samples_per_pulse = int(self.sample_rate * 0.01)
        silence_samples = int(self.sample_rate * 0.1)
        
        pulse = np.sin(2 * np.pi * config.frequency * np.linspace(0, 0.01, samples_per_pulse))
        pulse = config.amplitude * pulse.astype(np.float32)
        silence = np.zeros(silence_samples, dtype=np.float32)
        
        signal_parts = []
        for i in range(5):  # 5 pulses
            signal_parts.extend([pulse, silence])
        
        if signal_parts:
            signal_parts.pop()
        
        return np.concatenate(signal_parts)
    
    def generate_harmonic_stack(self, config: SignalConfig) -> np.ndarray:
        """Generate harmonic stack"""
        harmonic_freqs = [
            config.frequency,
            config.frequency * 2,
            config.frequency * 3,
            config.frequency * 5,
        ]
        
        t = np.linspace(0, config.duration, int(self.sample_rate * config.duration))
        signal = np.zeros_like(t)
        
        for i, freq in enumerate(harmonic_freqs):
            harmonic_amp = config.amplitude / (i + 1)
            signal += harmonic_amp * np.sin(2 * np.pi * freq * t)
        
        signal = signal / np.max(np.abs(signal)) * config.amplitude
        return signal.astype(np.float32)
    
    async def emit_signals(self, signal_configs: List[SignalConfig]) -> List[Dict[str, Any]]:
        """Emit mock signals"""
        if not self.is_initialized:
            raise RuntimeError("Emission engine not initialized")
        
        emitted_signals = []
        
        for config in signal_configs:
            try:
                # Generate signal based on type
                if config.signal_type == "sine":
                    signal_data = self.generate_sine_wave(config)
                elif config.signal_type == "sweep":
                    signal_data = self.generate_frequency_sweep(config)
                elif config.signal_type == "pulse":
                    signal_data = self.generate_pulse_burst(config)
                elif config.signal_type == "harmonic":
                    signal_data = self.generate_harmonic_stack(config)
                else:
                    raise ValueError(f"Unknown signal type: {config.signal_type}")
                
                # Mock signal emission (simulate processing time)
                await asyncio.sleep(0.01)
                
                signal_info = {
                    'type': config.signal_type,
                    'frequency': config.frequency,
                    'duration': config.duration,
                    'amplitude': config.amplitude,
                    'sample_rate': self.sample_rate,
                    'samples': len(signal_data),
                    'timestamp': asyncio.get_event_loop().time()
                }
                
                emitted_signals.append(signal_info)
                self.logger.debug(f"Mock emitted {config.signal_type} signal at {config.frequency}Hz")
                
                await asyncio.sleep(0.01)
                
            except Exception as e:
                self.logger.error(f"Failed to emit signal: {e}")
                raise
        
        return emitted_signals
    
    async def get_status(self) -> Dict[str, Any]:
        """Get emission engine status"""
        return {
            'initialized': self.is_initialized,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'audio_devices': 'Mock System',
            'stream_active': False,
            'mock_mode': True
        }
