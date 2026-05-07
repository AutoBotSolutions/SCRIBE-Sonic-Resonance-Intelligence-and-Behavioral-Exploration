"""
Resonance Emission Engine
Generates controlled acoustic signals for environmental probing
"""

import numpy as np
import pyaudio
import asyncio
import logging
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

@dataclass
class SignalConfig:
    """Configuration for resonance signal generation"""
    signal_type: str = "sine"  # sine, sweep, pulse, harmonic
    frequency: float = 440.0  # Hz
    duration: float = 2.0  # seconds
    sample_rate: int = 44100  # Hz
    amplitude: float = 0.5  # 0.0 to 1.0
    sweep_start: float = 20.0  # Hz (for sweep signals)
    sweep_end: float = 20000.0  # Hz (for sweep signals)
    pulse_count: int = 5  # (for pulse signals)
    harmonic_frequencies: List[float] = None  # (for harmonic signals)

class ResonanceEmissionEngine:
    """Generates resonance signals for environmental probing"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Audio output setup
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_initialized = False
        
        # Signal parameters
        self.sample_rate = config.get('sample_rate', 44100)
        self.channels = config.get('channels', 1)
        self.format = pyaudio.paFloat32
        
        self.logger.info("Resonance Emission Engine created")
    
    async def initialize(self):
        """Initialize audio output system"""
        try:
            # Test audio device availability
            device_count = self.audio.get_device_count()
            self.logger.info(f"Found {device_count} audio devices")
            
            # Create output stream
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=1024
            )
            
            self.is_initialized = True
            self.logger.info("✅ Resonance Emission Engine initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize emission engine: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup audio resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        self.is_initialized = False
        self.logger.info("Resonance Emission Engine cleaned up")
    
    def generate_sine_wave(self, config: SignalConfig) -> np.ndarray:
        """Generate pure sine wave signal"""
        t = np.linspace(0, config.duration, int(self.sample_rate * config.duration))
        signal = config.amplitude * np.sin(2 * np.pi * config.frequency * t)
        return signal.astype(np.float32)
    
    def generate_frequency_sweep(self, config: SignalConfig) -> np.ndarray:
        """Generate frequency sweep (chirp) signal"""
        t = np.linspace(0, config.duration, int(self.sample_rate * config.duration))
        
        # Logarithmic sweep from sweep_start to sweep_end
        sweep_rate = (config.sweep_end / config.sweep_start) ** (1 / config.duration)
        instantaneous_freq = config.sweep_start * (sweep_rate ** t)
        
        # Generate sweep signal
        phase = 2 * np.pi * np.cumsum(instantaneous_freq) / self.sample_rate
        signal = config.amplitude * np.sin(phase)
        
        return signal.astype(np.float32)
    
    def generate_pulse_burst(self, config: SignalConfig) -> np.ndarray:
        """Generate pulsed burst signals"""
        samples_per_pulse = int(self.sample_rate * 0.01)  # 10ms pulses
        silence_samples = int(self.sample_rate * 0.1)  # 100ms between pulses
        
        pulse = np.sin(2 * np.pi * config.frequency * np.linspace(0, 0.01, samples_per_pulse))
        pulse = config.amplitude * pulse.astype(np.float32)
        
        silence = np.zeros(silence_samples, dtype=np.float32)
        
        # Create pulse train
        signal_parts = []
        for i in range(config.pulse_count):
            signal_parts.extend([pulse, silence])
        
        # Remove final silence
        if signal_parts:
            signal_parts.pop()
        
        return np.concatenate(signal_parts)
    
    def generate_harmonic_stack(self, config: SignalConfig) -> np.ndarray:
        """Generate multi-tone harmonic stack"""
        if not config.harmonic_frequencies:
            # Default harmonic series based on fundamental frequency
            config.harmonic_frequencies = [
                config.frequency,  # Fundamental
                config.frequency * 2,  # 2nd harmonic
                config.frequency * 3,  # 3rd harmonic
                config.frequency * 5,  # 5th harmonic
            ]
        
        t = np.linspace(0, config.duration, int(self.sample_rate * config.duration))
        signal = np.zeros_like(t)
        
        # Sum harmonics with decreasing amplitude
        for i, freq in enumerate(config.harmonic_frequencies):
            harmonic_amp = config.amplitude / (i + 1)  # Decreasing amplitude
            signal += harmonic_amp * np.sin(2 * np.pi * freq * t)
        
        # Normalize to prevent clipping
        signal = signal / np.max(np.abs(signal)) * config.amplitude
        
        return signal.astype(np.float32)
    
    async def emit_signals(self, signal_configs: List[SignalConfig]) -> List[Dict[str, Any]]:
        """Emit multiple resonance signals"""
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
                
                # Emit signal through audio output
                await self._emit_signal(signal_data)
                
                # Record signal metadata
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
                self.logger.debug(f"Emitted {config.signal_type} signal at {config.frequency}Hz")
                
                # Small delay between signals
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Failed to emit signal: {e}")
                raise
        
        return emitted_signals
    
    async def _emit_signal(self, signal_data: np.ndarray):
        """Emit signal data through audio stream"""
        def write_signal():
            self.stream.write(signal_data.tobytes())
        
        # Run blocking audio write in thread pool
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, write_signal)
    
    async def get_status(self) -> Dict[str, Any]:
        """Get emission engine status"""
        return {
            'initialized': self.is_initialized,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'audio_devices': self.audio.get_device_count(),
            'stream_active': self.stream.is_active() if self.stream else False
        }
