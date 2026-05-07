"""
Micro Listening Module
Captures environmental acoustic responses with high precision
"""

import numpy as np
import pyaudio
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
    format: int = pyaudio.paFloat32
    chunk_size: int = 1024
    device_index: Optional[int] = None  # None = default device

class MicroListeningModule:
    """High-precision audio capture for environmental responses"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Audio input setup
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_initialized = False
        self.is_capturing = False
        
        # Capture parameters
        self.sample_rate = config.get('sample_rate', 44100)
        self.channels = config.get('channels', 1)
        self.chunk_size = config.get('chunk_size', 1024)
        self.format = pyaudio.paFloat32
        
        # Device selection
        self.device_index = self._select_best_input_device()
        
        self.logger.info("Micro Listening Module created")
    
    def _select_best_input_device(self) -> Optional[int]:
        """Select the best available input device"""
        try:
            device_count = self.audio.get_device_count()
            best_device = None
            max_channels = 0
            
            for i in range(device_count):
                device_info = self.audio.get_device_info_by_index(i)
                
                # Look for devices with input channels
                if device_info['maxInputChannels'] > 0:
                    self.logger.debug(f"Input device {i}: {device_info['name']}")
                    
                    # Prefer devices with more channels and higher sample rates
                    if (device_info['maxInputChannels'] >= max_channels and 
                        device_info['defaultSampleRate'] >= self.sample_rate):
                        best_device = i
                        max_channels = device_info['maxInputChannels']
            
            if best_device is not None:
                device_info = self.audio.get_device_info_by_index(best_device)
                self.logger.info(f"Selected input device: {device_info['name']}")
                return best_device
            else:
                self.logger.warning("No suitable input device found, using default")
                return None
                
        except Exception as e:
            self.logger.error(f"Error selecting input device: {e}")
            return None
    
    async def initialize(self):
        """Initialize audio capture system"""
        try:
            # Test device capabilities
            if self.device_index is not None:
                device_info = self.audio.get_device_info_by_index(self.device_index)
                self.logger.info(f"Using device: {device_info['name']}")
                self.logger.info(f"Max input channels: {device_info['maxInputChannels']}")
                self.logger.info(f"Default sample rate: {device_info['defaultSampleRate']}")
            
            # Create input stream
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=self.chunk_size
            )
            
            self.is_initialized = True
            self.logger.info("✅ Micro Listening Module initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize listening module: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup audio resources"""
        self.is_capturing = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        self.audio.terminate()
        self.is_initialized = False
        self.logger.info("Micro Listening Module cleaned up")
    
    async def capture_response(self, duration: float = 2.0, 
                              start_immediately: bool = True) -> Dict[str, Any]:
        """
        Capture environmental acoustic response
        
        Args:
            duration: Capture duration in seconds
            start_immediately: If False, wait for signal detection
            
        Returns:
            Dictionary containing captured audio data and metadata
        """
        if not self.is_initialized:
            raise RuntimeError("Listening module not initialized")
        
        if self.is_capturing:
            raise RuntimeError("Already capturing audio")
        
        capture_start = datetime.now()
        self.logger.info(f"🎙️ Starting audio capture for {duration}s")
        
        try:
            self.is_capturing = True
            
            # Calculate number of chunks to capture
            total_chunks = int((duration * self.sample_rate) / self.chunk_size)
            
            # Capture audio data
            audio_data = []
            
            def read_callback():
                """Read audio data from stream"""
                try:
                    data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_data.append(data)
                    return len(audio_data) < total_chunks
                except Exception as e:
                    self.logger.error(f"Audio read error: {e}")
                    return False
            
            # Run capture in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            
            if start_immediately:
                # Start capture immediately
                await loop.run_in_executor(None, self._capture_loop, read_callback)
            else:
                # Wait for signal detection before starting
                await self._wait_for_signal_threshold()
                await loop.run_in_executor(None, self._capture_loop, read_callback)
            
            # Convert captured data to numpy array
            if audio_data:
                raw_audio = b''.join(audio_data)
                audio_array = np.frombuffer(raw_audio, dtype=np.float32)
            else:
                audio_array = np.array([], dtype=np.float32)
            
            # Create capture metadata
            capture_metadata = {
                'timestamp': capture_start.isoformat(),
                'duration': duration,
                'sample_rate': self.sample_rate,
                'channels': self.channels,
                'samples_captured': len(audio_array),
                'chunks_processed': len(audio_data),
                'device_index': self.device_index,
                'amplitude_stats': self._calculate_amplitude_stats(audio_array),
                'frequency_spectrum': self._calculate_frequency_spectrum(audio_array)
            }
            
            capture_duration = (datetime.now() - capture_start).total_seconds()
            self.logger.info(f"✅ Audio capture completed in {capture_duration:.2f}s")
            self.logger.debug(f"Captured {len(audio_array)} samples")
            
            return {
                'audio_data': audio_array,
                'metadata': capture_metadata
            }
            
        except Exception as e:
            self.logger.error(f"Audio capture failed: {e}")
            raise
        finally:
            self.is_capturing = False
    
    def _capture_loop(self, read_callback):
        """Synchronous capture loop for thread pool execution"""
        try:
            while read_callback():
                pass
        except Exception as e:
            self.logger.error(f"Capture loop error: {e}")
            raise
    
    async def _wait_for_signal_threshold(self, threshold: float = 0.01, 
                                        timeout: float = 5.0):
        """Wait for audio signal to exceed threshold before capturing"""
        self.logger.debug("Waiting for signal threshold...")
        
        start_time = asyncio.get_event_loop().time()
        
        while True:
            # Read a small chunk to check signal level
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                audio_chunk = np.frombuffer(data, dtype=np.float32)
                
                # Calculate RMS amplitude
                rms = np.sqrt(np.mean(audio_chunk ** 2))
                
                if rms > threshold:
                    self.logger.debug(f"Signal detected: {rms:.4f}")
                    break
                
                # Check timeout
                if (asyncio.get_event_loop().time() - start_time) > timeout:
                    self.logger.warning("Signal detection timeout, proceeding anyway")
                    break
                
                # Small delay before next check
                await asyncio.sleep(0.01)
                
            except Exception as e:
                self.logger.error(f"Signal detection error: {e}")
                break
    
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
            'stream_active': self.stream.is_active() if self.stream else False
        }
