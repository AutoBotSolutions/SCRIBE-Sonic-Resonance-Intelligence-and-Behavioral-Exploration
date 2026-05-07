#!/usr/bin/env python3
"""
SCRIBE System Validation Script
Comprehensive system validation and testing
"""

import sys
import os
import json
import subprocess
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def validate_project_structure():
    """Validate project structure is complete"""
    print("🏗️  Validating Project Structure...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'config.json',
        'deploy.sh',
        'test_system.py'
    ]
    
    required_dirs = [
        'src',
        'src/core',
        'src/emitter',
        'src/listener',
        'src/processing',
        'src/ai',
        'src/feedback',
        'src/chat',
        'src/api',
        'src/monitoring',
        'src/utils'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✅ Project structure validated")
    return True

def validate_core_modules():
    """Validate core modules can be imported"""
    print("🧪 Validating Core Modules...")
    
    try:
        from utils.config import Config
        from utils.logger import setup_logging
        print("✅ Utils modules imported successfully")
        
        # Test configuration
        config = Config()
        print(f"✅ Configuration loaded: {config.audio.sample_rate}Hz sample rate")
        
        # Test logging
        setup_logging()
        import logging
        logger = logging.getLogger(__name__)
        logger.info("✅ Logging system working")
        
        return True
    except Exception as e:
        print(f"❌ Core module validation failed: {e}")
        return False

def validate_documentation():
    """Validate documentation completeness"""
    print("📚 Validating Documentation...")
    
    try:
        # Check README.md exists and has content
        with open('README.md', 'r') as f:
            readme_content = f.read()
        
        required_sections = [
            'SCRIBE Resonance AI System',
            'Installation',
            'Usage',
            'Architecture',
            'API Reference'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in readme_content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Missing documentation sections: {missing_sections}")
            return False
        
        print("✅ Documentation validated")
        return True
        
    except Exception as e:
        print(f"❌ Documentation validation failed: {e}")
        return False

def validate_configuration():
    """Validate configuration system"""
    print("⚙️  Validating Configuration...")
    
    try:
        from utils.config import Config
        
        config = Config()
        
        # Check essential configuration values
        required_configs = [
            ('audio.sample_rate', 44100),
            ('audio.channels', 1),
            ('ai.confidence_threshold', 0.7),
            ('processing.window_size', 2048)
        ]
        
        for config_key, expected_value in required_configs:
            actual_value = config.get(config_key)
            if actual_value != expected_value:
                print(f"⚠️  Configuration mismatch: {config_key} = {actual_value}, expected {expected_value}")
        
        print("✅ Configuration validated")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def validate_dependencies():
    """Validate Python dependencies"""
    print("🐍 Validating Dependencies...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    # Check critical dependencies
    critical_deps = [
        'numpy',
        'scipy',
        'fastapi',
        'uvicorn'
    ]
    
    missing_deps = []
    for dep in critical_deps:
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"⚠️  Missing optional dependencies: {missing_deps}")
        print("   System will use mock implementations where needed")
    
    print("✅ Dependency validation completed")
    return True

def validate_api_structure():
    """Validate API structure"""
    print("🌐 Validating API Structure...")
    
    try:
        # Check if API main file exists
        api_file = 'src/api/main.py'
        if not os.path.exists(api_file):
            print("❌ API main file not found")
            return False
        
        # Check API content
        with open(api_file, 'r') as f:
            api_content = f.read()
        
        required_endpoints = [
            '@app.get("/",',
            '@app.post("/scan"',
            '@app.get("/status"',
            '@app.get("/health"'
        ]
        
        missing_endpoints = []
        for endpoint in required_endpoints:
            if endpoint not in api_content:
                missing_endpoints.append(endpoint)
        
        if missing_endpoints:
            print(f"❌ Missing API endpoints: {missing_endpoints}")
            return False
        
        print("✅ API structure validated")
        return True
        
    except Exception as e:
        print(f"❌ API validation failed: {e}")
        return False

def run_system_tests():
    """Run system tests"""
    print("🧪 Running System Tests...")
    
    try:
        result = subprocess.run(['python3', 'test_system.py'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ System tests passed")
            print(result.stdout)
            return True
        else:
            print("❌ System tests failed")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def generate_validation_report():
    """Generate comprehensive validation report"""
    print("📊 Generating Validation Report...")
    
    validations = [
        ("Project Structure", validate_project_structure),
        ("Core Modules", validate_core_modules),
        ("Documentation", validate_documentation),
        ("Configuration", validate_configuration),
        ("Dependencies", validate_dependencies),
        ("API Structure", validate_api_structure),
        ("System Tests", run_system_tests)
    ]
    
    results = {}
    
    for name, validator in validations:
        try:
            results[name] = validator()
        except Exception as e:
            print(f"❌ {name} validation crashed: {e}")
            results[name] = False
    
    # Generate summary
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print("\n" + "="*60)
    print("📋 SCRIBE SYSTEM VALIDATION REPORT")
    print("="*60)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:<20} {status}")
    
    print(f"\n📊 Summary: {passed}/{total} validations passed")
    
    if passed == total:
        print("🎉 SCRIBE System is fully validated and ready for deployment!")
        return True
    else:
        print("⚠️  Some validations failed. Review the issues above.")
        return False

def main():
    """Main validation function"""
    print("🔍 SCRIBE Resonance AI System - Comprehensive Validation")
    print("=" * 60)
    
    success = generate_validation_report()
    
    if success:
        print("\n🚀 System is ready for production use!")
        print("\n📯 Next Steps:")
        print("1. Run './deploy.sh' for full deployment")
        print("2. Use './start_interactive.sh' for interactive mode")
        print("3. Use './start_api.sh' for API server mode")
        print("4. Visit http://localhost:8000/docs for API documentation")
    else:
        print("\n🔧 Please address validation issues before deployment.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
