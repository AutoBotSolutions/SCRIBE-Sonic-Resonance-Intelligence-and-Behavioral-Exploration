#!/usr/bin/env python3
"""
SCRIBE Resonance AI System
Main entry point for the resonance intelligence system

Architecture:
- Resonance Emission Engine -> generates acoustic signals
- Micro Listening Module -> captures environmental responses
- Signal Processing Layer -> FFT and feature extraction
- Resonance Interpretation Engine -> AI pattern recognition
- Chat Interface -> user interaction
- Feedback Loop -> continuous learning
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from core.system_controller import ScribeSystemController
from chat.interface import ChatInterface
from utils.config import Config
from utils.logger import setup_logging

def main():
    """Main entry point for SCRIBE system"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("🧠 SCRIBE Resonance AI System Starting...")
    
    try:
        # Load configuration
        config = Config()
        
        # Initialize system controller
        system = ScribeSystemController(config)
        
        # Initialize chat interface
        chat_interface = ChatInterface(system)
        
        # Start the system
        asyncio.run(chat_interface.start())
        
    except KeyboardInterrupt:
        logger.info("System shutdown requested by user")
    except Exception as e:
        logger.error(f"System error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
