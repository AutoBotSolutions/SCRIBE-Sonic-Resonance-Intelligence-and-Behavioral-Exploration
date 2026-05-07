"""
SCRIBE System Controller
Central coordination for all system components
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Try to import real audio components, fall back to mock if not available
try:
    from emitter.tone_generator import ResonanceEmissionEngine, SignalConfig
    from listener.mic_capture import MicroListeningModule
    AUDIO_AVAILABLE = True
except ImportError as e:
    if 'pyaudio' in str(e).lower():
        from emitter.mock_audio import MockResonanceEmissionEngine as ResonanceEmissionEngine, SignalConfig
        from listener.mock_capture import MockMicroListeningModule as MicroListeningModule
        AUDIO_AVAILABLE = False
    else:
        raise
from processing.fft_analyzer import SignalProcessingLayer
from ai.interpreter import ResonanceInterpretationEngine
from feedback.learning_system import FeedbackLoop

class ScribeSystemController:
    """Main system controller for SCRIBE resonance intelligence"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize all system components
        self.emission_engine = ResonanceEmissionEngine(config)
        self.listening_module = MicroListeningModule(config)
        self.signal_processor = SignalProcessingLayer(config)
        self.interpretation_engine = ResonanceInterpretationEngine(config)
        self.feedback_loop = FeedbackLoop(config)
        
        # System state
        self.is_running = False
        self.current_scan_data = None
        self.scan_history = []
        
        # Log audio system status
        if AUDIO_AVAILABLE:
            self.logger.info("SCRIBE System Controller initialized with real audio system")
        else:
            self.logger.info("SCRIBE System Controller initialized with mock audio system")
    
    async def start(self):
        """Start all system components"""
        self.logger.info("Starting SCRIBE system components...")
        
        try:
            await self.emission_engine.initialize()
            await self.listening_module.initialize()
            await self.signal_processor.initialize()
            await self.interpretation_engine.initialize()
            await self.feedback_loop.initialize()
            
            self.is_running = True
            self.logger.info("✅ All SCRIBE components started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start system: {e}")
            raise
    
    async def stop(self):
        """Stop all system components"""
        self.logger.info("Stopping SCRIBE system...")
        self.is_running = False
        
        await asyncio.gather(
            self.emission_engine.cleanup(),
            self.listening_module.cleanup(),
            self.signal_processor.cleanup(),
            self.interpretation_engine.cleanup(),
            self.feedback_loop.cleanup(),
            return_exceptions=True
        )
        
        self.logger.info("SCRIBE system stopped")
    
    async def perform_resonance_scan(self, scan_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform a complete resonance scan cycle
        1. Emit resonance signals
        2. Capture environmental response
        3. Process signals
        4. Interpret patterns
        5. Store results for learning
        """
        if not self.is_running:
            raise RuntimeError("System not running")
        
        scan_start = datetime.now()
        self.logger.info(f"🔊 Starting resonance scan at {scan_start}")
        
        try:
            # Step 1: Generate resonance signals
            signal_config_dict = scan_config or self.config.default_signal_config
            
            # Convert dict to SignalConfig object
            signal_config = SignalConfig(
                signal_type=signal_config_dict.get('signal_type', 'sine'),
                frequency=signal_config_dict.get('frequency', 440.0),
                duration=signal_config_dict.get('duration', 2.0),
                amplitude=signal_config_dict.get('amplitude', 0.5)
            )
            
            emitted_signals = await self.emission_engine.emit_signals([signal_config])
            
            # Step 2: Capture environmental response
            response_data = await self.listening_module.capture_response(
                duration=signal_config.duration
            )
            
            # Step 3: Process signals and extract features
            processed_features = await self.signal_processor.analyze_signal(
                response_data, emitted_signals
            )
            
            # Step 4: AI interpretation of resonance patterns
            interpretation = await self.interpretation_engine.interpret_resonance(
                processed_features, scan_history=self.scan_history[-10:]  # Last 10 scans
            )
            
            # Step 5: Store for learning loop
            scan_result = {
                'timestamp': scan_start.isoformat(),
                'signals': emitted_signals,
                'response': response_data,
                'features': processed_features,
                'interpretation': interpretation,
                'config': signal_config
            }
            
            await self.feedback_loop.store_scan_result(scan_result)
            self.scan_history.append(scan_result)
            
            # Keep only last 100 scans in memory
            if len(self.scan_history) > 100:
                self.scan_history = self.scan_history[-100:]
            
            self.current_scan_data = scan_result
            
            scan_duration = (datetime.now() - scan_start).total_seconds()
            self.logger.info(f"✅ Resonance scan completed in {scan_duration:.2f}s")
            
            return scan_result
            
        except Exception as e:
            self.logger.error(f"Resonance scan failed: {e}")
            raise
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and health"""
        return {
            'system_running': self.is_running,
            'components': {
                'emission_engine': await self.emission_engine.get_status(),
                'listening_module': await self.listening_module.get_status(),
                'signal_processor': await self.signal_processor.get_status(),
                'interpretation_engine': await self.interpretation_engine.get_status(),
                'feedback_loop': await self.feedback_loop.get_status(),
            },
            'scan_count': len(self.scan_history),
            'last_scan': self.current_scan_data.get('timestamp') if self.current_scan_data else None
        }
    
    def get_scan_history(self, limit: int = 10) -> list:
        """Get recent scan history"""
        return self.scan_history[-limit:] if self.scan_history else []
