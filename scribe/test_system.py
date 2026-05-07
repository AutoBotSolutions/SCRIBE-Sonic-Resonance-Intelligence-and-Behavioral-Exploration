#!/usr/bin/env python3
"""
Simple test for SCRIBE system without external dependencies
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test basic imports"""
    try:
        from utils.config import Config
        print("✅ Config import successful")
        
        from utils.logger import setup_logging
        print("✅ Logger import successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test configuration system"""
    try:
        from utils.config import Config
        config = Config()
        print(f"✅ Config created successfully")
        print(f"   Sample rate: {config.audio.sample_rate}")
        print(f"   Confidence threshold: {config.ai.confidence_threshold}")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_logging():
    """Test logging system"""
    try:
        from utils.logger import setup_logging
        setup_logging()
        import logging
        logger = logging.getLogger(__name__)
        logger.info("✅ Logging test successful")
        return True
    except Exception as e:
        print(f"❌ Logging test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 SCRIBE System Test Suite")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Logging", test_logging),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
    else:
        print("⚠️ Some tests failed. Check dependencies.")

if __name__ == "__main__":
    main()
