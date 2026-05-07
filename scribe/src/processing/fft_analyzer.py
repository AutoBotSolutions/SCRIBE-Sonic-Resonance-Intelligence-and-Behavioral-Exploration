"""
Signal Processing Layer
Converts raw audio into meaningful features using FFT and analysis techniques
"""

import numpy as np
import scipy.signal
import librosa
import asyncio
import logging
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProcessingConfig:
    """Configuration for signal processing"""
    sample_rate: int = 44100
    window_size: int = 2048
    hop_length: int = 512
    n_fft: int = 2048
    n_mels: int = 128
    fmin: float = 20.0
    fmax: float = 20000.0

class SignalProcessingLayer:
    """Advanced signal processing for resonance analysis"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Processing parameters
        self.sample_rate = config.get('sample_rate', 44100)
        self.window_size = config.get('window_size', 2048)
        self.hop_length = config.get('hop_length', 512)
        self.n_fft = config.get('n_fft', 2048)
        self.n_mels = config.get('n_mels', 128)
        
        # Frequency range (adjusted to be compatible with frame_length)
        self.fmin = config.get('fmin', 50.0)  # Increased to avoid librosa error
        self.fmax = config.get('fmax', 20000.0)
        
        # Analysis windows
        self.window = scipy.signal.windows.hann(self.window_size)
        
        self.is_initialized = False
        self.logger.info("Signal Processing Layer created")
    
    async def initialize(self):
        """Initialize processing components"""
        try:
            # Test FFT computation
            test_signal = np.random.randn(self.sample_rate).astype(np.float32)
            _ = self.compute_fft(test_signal)
            
            self.is_initialized = True
            self.logger.info("✅ Signal Processing Layer initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize signal processing: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup processing resources"""
        self.is_initialized = False
        self.logger.info("Signal Processing Layer cleaned up")
    
    async def analyze_signal(self, response_data: Dict[str, Any], 
                           emitted_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive signal analysis
        
        Args:
            response_data: Captured audio response from environment
            emitted_signals: List of emitted signal metadata
            
        Returns:
            Dictionary containing extracted features and analysis results
        """
        if not self.is_initialized:
            raise RuntimeError("Signal processing not initialized")
        
        analysis_start = datetime.now()
        self.logger.info("🔍 Starting signal analysis...")
        
        try:
            audio_array = response_data['audio_data']
            metadata = response_data['metadata']
            
            if len(audio_array) == 0:
                self.logger.warning("Empty audio data received")
                return self._empty_analysis_result()
            
            # Perform comprehensive analysis
            analysis_results = {}
            
            # 1. Basic time-domain analysis
            analysis_results['time_domain'] = await self._analyze_time_domain(audio_array)
            
            # 2. Frequency domain analysis
            analysis_results['frequency_domain'] = await self._analyze_frequency_domain(audio_array)
            
            # 3. Spectrographic analysis
            analysis_results['spectrogram'] = await self._analyze_spectrogram(audio_array)
            
            # 4. Resonance peak analysis
            analysis_results['resonance_peaks'] = await self._analyze_resonance_peaks(audio_array)
            
            # 5. Harmonic analysis
            analysis_results['harmonics'] = await self._analyze_harmonics(audio_array)
            
            # 6. Envelope and decay analysis
            analysis_results['envelope'] = await self._analyze_envelope(audio_array)
            
            # 7. Comparative analysis with emitted signals
            analysis_results['signal_response'] = await self._analyze_signal_response(
                audio_array, emitted_signals
            )
            
            # 8. Noise and distortion analysis
            analysis_results['noise_analysis'] = await self._analyze_noise(audio_array)
            
            # Add processing metadata
            analysis_results['processing_metadata'] = {
                'analysis_timestamp': analysis_start.isoformat(),
                'input_samples': len(audio_array),
                'sample_rate': self.sample_rate,
                'processing_time': (datetime.now() - analysis_start).total_seconds()
            }
            
            processing_time = (datetime.now() - analysis_start).total_seconds()
            self.logger.info(f"✅ Signal analysis completed in {processing_time:.3f}s")
            
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"Signal analysis failed: {e}")
            raise
    
    def compute_fft(self, signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute FFT of signal"""
        # Take a segment of the signal for FFT analysis
        if len(signal) >= self.window_size:
            # Take the first window_size samples
            signal_segment = signal[:self.window_size]
            windowed = signal_segment * self.window
        else:
            # Pad signal if it's shorter than window_size
            padded_signal = np.zeros(self.window_size)
            padded_signal[:len(signal)] = signal
            windowed = padded_signal * self.window
        
        # Compute FFT
        fft_data = np.fft.fft(windowed, n=self.n_fft)
        freqs = np.fft.fftfreq(self.n_fft, 1/self.sample_rate)
        
        # Return only positive frequencies
        positive_freqs = freqs[:self.n_fft//2]
        positive_fft = np.abs(fft_data[:self.n_fft//2])
        
        return positive_freqs, positive_fft
    
    async def _analyze_time_domain(self, audio: np.ndarray) -> Dict[str, Any]:
        """Analyze time-domain characteristics"""
        # Basic statistics
        rms = np.sqrt(np.mean(audio ** 2))
        peak = np.max(np.abs(audio))
        crest_factor = peak / rms if rms > 0 else 0
        
        # Zero crossing rate
        zero_crossings = np.sum(np.diff(np.sign(audio)) != 0) / len(audio)
        
        # Temporal centroid
        time_axis = np.arange(len(audio)) / self.sample_rate
        temporal_centroid = np.sum(time_axis * np.abs(audio)) / np.sum(np.abs(audio))
        
        return {
            'rms': float(rms),
            'peak': float(peak),
            'crest_factor': float(crest_factor),
            'zero_crossing_rate': float(zero_crossings),
            'temporal_centroid': float(temporal_centroid),
            'dynamic_range_db': float(20 * np.log10(peak / rms)) if rms > 0 else 0.0
        }
    
    async def _analyze_frequency_domain(self, audio: np.ndarray) -> Dict[str, Any]:
        """Analyze frequency-domain characteristics"""
        freqs, magnitude = self.compute_fft(audio[:self.window_size])
        
        # Find peaks
        peaks, properties = scipy.signal.find_peaks(magnitude, height=np.max(magnitude) * 0.1)
        peak_freqs = freqs[peaks]
        peak_magnitudes = magnitude[peaks]
        
        # Sort peaks by magnitude
        peak_indices = np.argsort(peak_magnitudes)[::-1]
        top_peaks = [(float(peak_freqs[i]), float(peak_magnitudes[i])) 
                     for i in peak_indices[:10]]
        
        # Spectral centroid
        spectral_centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
        
        # Spectral bandwidth
        spectral_bandwidth = np.sqrt(np.sum(((freqs - spectral_centroid) ** 2) * magnitude) / np.sum(magnitude))
        
        # Spectral rolloff (frequency below which 85% of energy is contained)
        cumsum_energy = np.cumsum(magnitude)
        rolloff_idx = np.where(cumsum_energy >= 0.85 * cumsum_energy[-1])[0]
        spectral_rolloff = freqs[rolloff_idx[0]] if len(rolloff_idx) > 0 else freqs[-1]
        
        return {
            'spectral_centroid': float(spectral_centroid),
            'spectral_bandwidth': float(spectral_bandwidth),
            'spectral_rolloff': float(spectral_rolloff),
            'dominant_frequency': float(top_peaks[0][0]) if top_peaks else 0.0,
            'peak_frequencies': top_peaks,
            'total_energy': float(np.sum(magnitude ** 2))
        }
    
    async def _analyze_spectrogram(self, audio: np.ndarray) -> Dict[str, Any]:
        """Analyze spectrogram features"""
        # Compute spectrogram
        frequencies, times, Sxx = scipy.signal.spectrogram(
            audio, fs=self.sample_rate, window='hann', 
            nperseg=self.window_size, noverlap=self.window_size - self.hop_length
        )
        
        # Convert to dB
        Sxx_db = 10 * np.log10(Sxx + 1e-10)
        
        # Mel spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=audio, sr=self.sample_rate, n_mels=self.n_mels,
            fmin=self.fmin, fmax=self.fmax
        )
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Spectral features over time
        spectral_centroid_time = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
        spectral_bandwidth_time = librosa.feature.spectral_bandwidth(y=audio, sr=self.sample_rate)[0]
        spectral_rolloff_time = librosa.feature.spectral_rolloff(y=audio, sr=self.sample_rate)[0]
        
        return {
            'spectrogram_shape': Sxx.shape,
            'spectrogram_mean_db': float(np.mean(Sxx_db)),
            'spectrogram_std_db': float(np.std(Sxx_db)),
            'mel_spectrogram_shape': mel_spec_db.shape,
            'spectral_centroid_mean': float(np.mean(spectral_centroid_time)),
            'spectral_centroid_std': float(np.std(spectral_centroid_time)),
            'spectral_bandwidth_mean': float(np.mean(spectral_bandwidth_time)),
            'spectral_rolloff_mean': float(np.mean(spectral_rolloff_time))
        }
    
    async def _analyze_resonance_peaks(self, audio: np.ndarray) -> Dict[str, Any]:
        """Identify and analyze resonance peaks"""
        freqs, magnitude = self.compute_fft(audio[:self.window_size])
        
        # Find prominent peaks
        peaks, properties = scipy.signal.find_peaks(
            magnitude, height=np.max(magnitude) * 0.05, 
            distance=10, width=5
        )
        
        resonance_peaks = []
        for peak_idx in peaks:
            peak_freq = freqs[peak_idx]
            peak_mag = magnitude[peak_idx]
            
            # Estimate Q factor (quality factor)
            half_max = peak_mag / 2
            left_idx = peak_idx
            right_idx = peak_idx
            
            while left_idx > 0 and magnitude[left_idx] > half_max:
                left_idx -= 1
            while right_idx < len(magnitude) - 1 and magnitude[right_idx] > half_max:
                right_idx += 1
            
            bandwidth = freqs[right_idx] - freqs[left_idx]
            q_factor = peak_freq / bandwidth if bandwidth > 0 else 0
            
            resonance_peaks.append({
                'frequency': float(peak_freq),
                'magnitude': float(peak_mag),
                'q_factor': float(q_factor),
                'bandwidth': float(bandwidth)
            })
        
        # Sort by magnitude
        resonance_peaks.sort(key=lambda x: x['magnitude'], reverse=True)
        
        return {
            'resonance_peaks': resonance_peaks[:20],  # Top 20 peaks
            'peak_count': len(resonance_peaks),
            'dominant_resonance': resonance_peaks[0] if resonance_peaks else None
        }
    
    async def _analyze_harmonics(self, audio: np.ndarray) -> Dict[str, Any]:
        """Analyze harmonic content"""
        # Find fundamental frequency
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio, fmin=self.fmin, fmax=self.fmax, sr=self.sample_rate
        )
        
        # Remove NaN values
        valid_f0 = f0[~np.isnan(f0)]
        
        if len(valid_f0) > 0:
            fundamental_freq = np.median(valid_f0)
            
            # Find harmonic peaks
            freqs, magnitude = self.compute_fft(audio[:self.window_size])
            
            # Look for peaks at harmonic frequencies
            harmonic_peaks = []
            for n in range(1, 11):  # First 10 harmonics
                harmonic_freq = fundamental_freq * n
                if harmonic_freq <= self.fmax:
                    # Find nearest peak
                    idx = np.argmin(np.abs(freqs - harmonic_freq))
                    if magnitude[idx] > np.max(magnitude) * 0.05:
                        harmonic_peaks.append({
                            'harmonic_number': n,
                            'frequency': float(freqs[idx]),
                            'magnitude': float(magnitude[idx]),
                            'theoretical_frequency': float(harmonic_freq)
                        })
        else:
            fundamental_freq = 0
            harmonic_peaks = []
        
        # Harmonic-to-noise ratio
        hnr = librosa.effects.harmonic(audio)
        noise = audio - hnr
        hnr_ratio = np.sum(hnr ** 2) / (np.sum(noise ** 2) + 1e-10)
        
        return {
            'fundamental_frequency': float(fundamental_freq),
            'harmonic_peaks': harmonic_peaks,
            'harmonic_count': len(harmonic_peaks),
            'harmonic_to_noise_ratio': float(hnr_ratio)
        }
    
    async def _analyze_envelope(self, audio: np.ndarray) -> Dict[str, Any]:
        """Analyze signal envelope and decay characteristics"""
        # Compute envelope using Hilbert transform
        analytic_signal = scipy.signal.hilbert(audio)
        envelope = np.abs(analytic_signal)
        
        # Find attack and decay times
        envelope_normalized = envelope / np.max(envelope)
        
        # Attack time (time to reach 90% of peak)
        attack_idx = np.where(envelope_normalized >= 0.9)[0]
        attack_time = attack_idx[0] / self.sample_rate if len(attack_idx) > 0 else 0
        
        # Decay time (time to drop to 10% of peak after peak)
        peak_idx = np.argmax(envelope)
        decay_start_idx = peak_idx + np.where(envelope_normalized[peak_idx:] <= 0.1)[0]
        decay_time = decay_start_idx[0] / self.sample_rate if len(decay_start_idx) > 0 else 0
        
        # Exponential decay fitting
        try:
            from scipy.optimize import curve_fit
            
            def exp_decay(t, a, b):
                return a * np.exp(-b * t)
            
            if decay_time > 0:
                t_decay = np.arange(peak_idx, min(peak_idx + int(decay_time * self.sample_rate), len(envelope))) / self.sample_rate
                env_decay = envelope[peak_idx:len(t_decay) + peak_idx]
                
                if len(t_decay) > 10:
                    popt, _ = curve_fit(exp_decay, t_decay, env_decay, p0=[envelope[peak_idx], 1])
                    decay_rate = popt[1]
                    decay_constant = 1 / decay_rate if decay_rate > 0 else 0
                else:
                    decay_constant = 0
            else:
                decay_constant = 0
        except:
            decay_constant = 0
        
        return {
            'attack_time': float(attack_time),
            'decay_time': float(decay_time),
            'decay_constant': float(decay_constant),
            'envelope_peak': float(np.max(envelope)),
            'envelope_mean': float(np.mean(envelope))
        }
    
    async def _analyze_signal_response(self, audio: np.ndarray, 
                                     emitted_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze response characteristics relative to emitted signals"""
        if not emitted_signals:
            return {'response_quality': 0.0, 'signal_correlation': 0.0}
        
        # Get dominant emitted frequency
        emitted_freqs = [s.get('frequency', 440) for s in emitted_signals]
        dominant_emitted = emitted_freqs[0] if emitted_freqs else 440
        
        # Analyze response at emitted frequencies
        freqs, magnitude = self.compute_fft(audio[:self.window_size])
        
        # Find response at emitted frequencies
        response_magnitudes = []
        for freq in emitted_freqs:
            idx = np.argmin(np.abs(freqs - freq))
            response_magnitudes.append(float(magnitude[idx]))
        
        # Calculate signal-to-response correlation
        avg_response = np.mean(response_magnitudes)
        noise_floor = np.median(magnitude)
        signal_to_noise = avg_response / noise_floor if noise_floor > 0 else 0
        
        return {
            'dominant_emitted_frequency': float(dominant_emitted),
            'response_magnitudes': response_magnitudes,
            'average_response': float(avg_response),
            'signal_to_noise_ratio': float(signal_to_noise),
            'response_quality': float(min(1.0, signal_to_noise / 10))  # Normalized 0-1
        }
    
    async def _analyze_noise(self, audio: np.ndarray) -> Dict[str, Any]:
        """Analyze noise and distortion characteristics"""
        # Total harmonic distortion
        try:
            fundamental_freq, harmonic_peaks = await self._estimate_fundamental_and_harmonics(audio)
            
            if fundamental_freq > 0:
                # Calculate THD
                harmonic_power = 0
                for peak in harmonic_peaks[:5]:  # First 5 harmonics
                    harmonic_power += peak['magnitude'] ** 2
                
                fundamental_power = harmonic_peaks[0]['magnitude'] ** 2 if harmonic_peaks else 0
                thd = np.sqrt(harmonic_power) / np.sqrt(fundamental_power) if fundamental_power > 0 else 0
            else:
                thd = 0
        except:
            thd = 0
        
        # Noise estimation (high-frequency content)
        freqs, magnitude = self.compute_fft(audio[:self.window_size])
        noise_freq_mask = freqs > 10000  # High frequencies as noise estimate
        noise_level = np.mean(magnitude[noise_freq_mask]) if np.any(noise_freq_mask) else 0
        
        return {
            'total_harmonic_distortion': float(thd),
            'noise_level': float(noise_level),
            'signal_to_noise': float(np.max(magnitude) / noise_level) if noise_level > 0 else 0
        }
    
    async def _estimate_fundamental_and_harmonics(self, audio: np.ndarray) -> Tuple[float, List[Dict]]:
        """Estimate fundamental frequency and harmonics"""
        try:
            f0, voiced_flag, voiced_probs = librosa.pyin(
                audio, fmin=self.fmin, fmax=self.fmax, sr=self.sample_rate
            )
            
            valid_f0 = f0[~np.isnan(f0)]
            fundamental = np.median(valid_f0) if len(valid_f0) > 0 else 0
            
            # Find harmonic peaks
            freqs, magnitude = self.compute_fft(audio[:self.window_size])
            harmonic_peaks = []
            
            for n in range(1, 11):
                harmonic_freq = fundamental * n
                if harmonic_freq <= self.fmax:
                    idx = np.argmin(np.abs(freqs - harmonic_freq))
                    harmonic_peaks.append({
                        'frequency': float(freqs[idx]),
                        'magnitude': float(magnitude[idx])
                    })
            
            return fundamental, harmonic_peaks
        except:
            return 0, []
    
    def _empty_analysis_result(self) -> Dict[str, Any]:
        """Return empty analysis result for empty input"""
        return {
            'time_domain': {'rms': 0.0, 'peak': 0.0},
            'frequency_domain': {'spectral_centroid': 0.0},
            'spectrogram': {'spectrogram_shape': (0, 0)},
            'resonance_peaks': {'resonance_peaks': [], 'peak_count': 0},
            'harmonics': {'fundamental_frequency': 0.0, 'harmonic_peaks': []},
            'envelope': {'attack_time': 0.0, 'decay_time': 0.0},
            'signal_response': {'response_quality': 0.0},
            'noise_analysis': {'total_harmonic_distortion': 0.0},
            'processing_metadata': {'input_samples': 0}
        }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get signal processing status"""
        return {
            'initialized': self.is_initialized,
            'sample_rate': self.sample_rate,
            'window_size': self.window_size,
            'hop_length': self.hop_length,
            'n_fft': self.n_fft,
            'frequency_range': (self.fmin, self.fmax)
        }
