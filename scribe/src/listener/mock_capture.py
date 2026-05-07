"""
Mock Audio Capture System for Testing
Fallback when PyAudio is not available
"""

import numpy as np
import asyncio
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CaptureConfig:
    """Configuration for audio capture"""
    sample_rate: int = 44100
    channels: int = 1
    chunk_size: int = 1024
    device_index: Optional[int] = None

class MockMicroListeningModule:
    """Mock audio capture for testing without audio hardware"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Mock audio parameters
        self.sample_rate = config.get('sample_rate', 44100)
        self.channels = config.get('channels', 1)
        self.chunk_size = config.get('chunk_size', 1024)
        self.device_index = config.get('device_index', None)
        
        self.is_initialized = False
        self.is_capturing = False
        
        self.logger.info("Mock Micro Listening Module created")
    
    async def initialize(self):
        """Initialize mock audio capture system"""
        self.logger.info("🎙️ Initializing mock audio capture...")
        await asyncio.sleep(0.1)  # Simulate initialization time
        self.is_initialized = True
        self.logger.info("✅ Mock Micro Listening Module initialized")
    
    async def cleanup(self):
        """Cleanup audio resources"""
        self.is_capturing = False
        self.is_initialized = False
        self.logger.info("Mock Micro Listening Module cleaned up")
    
    async def capture_response(self, duration: float = 2.0, 
                              start_immediately: bool = True) -> Dict[str, Any]:
        """Capture mock environmental response"""
        if not self.is_initialized:
            raise RuntimeError("Listening module not initialized")
        
        if self.is_capturing:
            raise RuntimeError("Already capturing audio")
        
        capture_start = datetime.now()
        self.logger.info(f"🎙️ Starting mock audio capture for {duration}s")
        
        try:
            self.is_capturing = True
            
            # Generate mock response signal
            total_samples = int(duration * self.sample_rate)
            t = np.linspace(0, duration, total_samples)
            
            # Create realistic mock response based on resonance principles
            # Simulate room response with multiple reflections
            direct_signal = 0.8 * np.sin(2 * np.pi * 440 * t)  # Direct response
            
            # Add reflections (delayed and attenuated copies)
            reflection1 = 0.4 * np.sin(2 * np.pi * 440 * (t - 0.05))
            reflection2 = 0.2 * np.sin(2 * np.pi * 440 * (t - 0.08))
            reflection3 = 0.1 * np.sin(2 * np.pi * 440 * (t - 0.12))
            
            # Combine with proper masking for delays
            response_signal = direct_signal.copy()
            
            # Add reflections with proper timing
            delay_samples1 = int(0.05 * self.sample_rate)
            delay_samples2 = int(0.08 * self.sample_rate)
            delay_samples3 = int(0.12 * self.sample_rate)
            
            if delay_samples1 < total_samples:
                response_signal[delay_samples1:] += reflection1[:total_samples-delay_samples1]
            if delay_samples2 < total_samples:
                response_signal[delay_samples2:] += reflection2[:total_samples-delay_samples2]
            if delay_samples3 < total_samples:
                response_signal[delay_samples3:] += reflection3[:total_samples-delay_samples3]
            
            # Add some noise for realism
            noise = 0.02 * np.random.randn(total_samples)
            response_signal += noise
            
            # Apply exponential decay
            decay_envelope = np.exp(-t * 2)  # 2-second decay constant
            response_signal *= decay_envelope
            
            # Add some harmonic content
            harmonic = 0.3 * np.sin(2 * np.pi * 880 * t)  # 2nd harmonic
            response_signal += harmonic * decay_envelope
            
            # Normalize to prevent clipping
            response_signal = response_signal / np.max(np.abs(response_signal)) * 0.8
            
            # Simulate capture processing time
            await asyncio.sleep(duration * 0.1)  # Simulate real-time capture
            
            # Create capture metadata
            capture_metadata = {
                'timestamp': capture_start.isoformat(),
                'duration': duration,
                'sample_rate': self.sample_rate,
                'channels': self.channels,
                'samples_captured': len(response_signal),
                'chunks_processed': total_samples // self.chunk_size,
                'device_index': self.device_index,
                'amplitude_stats': self._calculate_amplitude_stats(response_signal),
                'frequency_spectrum': self._calculate_frequency_spectrum(response_signal)
            }
            
            capture_duration = (datetime.now() - capture_start).total_seconds()
            self.logger.info(f"✅ Mock audio capture completed in {capture_duration:.2f}s")
            self.logger.debug(f"Captured {len(response_signal)} samples")
            
            return {
                'audio_data': response_signal,
                'metadata': capture_metadata
            }
            
        except Exception as e:
            self.logger.error(f"Mock audio capture failed: {e}")
            raise
        finally:
            self.is_capturing = False
    
    def _calculate_amplitude_stats(self, audio_array: np.ndarray) -> Dict[str, float]:
        """Calculate amplitude statistics for captured audio"""
        if len(audio_array) == 0:
            return {'rms': 0.0, 'peak': 0.0, 'crest_factor': 0.0}
        
        rms = np.sqrt(np.mean(audio_array ** 2))
        peak = np.max(np.abs(audio_array))
        crest_factor = peak / rms if rms > 0 else 0.0
        
        return {
            'rms': float(rms),
            'peak': float(peak),
            'crest_factor': float(crest_factor),
            'dynamic_range': float(20 * np.log10(peak / rms)) if rms > 0 else 0.0
        }
    
    def _calculate_frequency_spectrum(self, audio_array: np.ndarray) -> Dict[str, Any]:
        """Calculate basic frequency spectrum information"""
        if len(audio_array) == 0:
            return {'dominant_frequency': 0.0, 'spectral_centroid': 0.0}
        
        try:
            # Compute FFT
            fft_data = np.fft.fft(audio_array)
            freqs = np.fft.fftfreq(len(audio_array), 1/self.sample_rate)
            
            # Get magnitude spectrum (only positive frequencies)
            magnitude = np.abs(fft_data[:len(freqs)//2])
            freqs_positive = freqs[:len(freqs)//2]
            
            # Find dominant frequency
            dominant_freq_idx = np.argmax(magnitude)
            dominant_frequency = freqs_positive[dominant_freq_idx]
            
            # Calculate spectral centroid
            spectral_centroid = np.sum(freqs_positive * magnitude) / np.sum(magnitude)
            
            return {
                'dominant_frequency': float(dominant_frequency),
                'spectral_centroid': float(spectral_centroid),
                'spectral_energy': float(np.sum(magnitude ** 2))
            }
            
        except Exception as e:
            self.logger.error(f"Frequency spectrum calculation error: {e}")
            return {'dominant_frequency': 0.0, 'spectral_centroid': 0.0}
    
    async def get_status(self) -> Dict[str, Any]:
        """Get listening module status"""
        return {
            'initialized': self.is_initialized,
            'capturing': self.is_capturing,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'chunk_size': self.chunk_size,
            'device_index': self.device_index,
            'stream_active': False,
            'mock_mode': True
        }
