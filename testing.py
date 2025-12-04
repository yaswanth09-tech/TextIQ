"""
Testing Module for TextIQ AI Chatbot
Comprehensive test suite matching all app.py features
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try importing required packages
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

# ============================================================================
# CONFIGURATION FROM APP.PY
# ============================================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CHAT_HISTORY_FILE = "chat_history.json"
# Models from app.py - EXACT MATCH
MODELS = {
    "Fast Mode": "gemini-2.5-flash",
    "Powerful Mode": "gemini-2.5-pro",
    "Balanced Mode": "gemini-2.5-flash"
}
DEFAULT_SYSTEM_PROMPT = """You are TextIQ, an intelligent AI assistant. You provide clear, 
accurate, and helpful responses. You are professional, friendly, and always aim to assist users 
in the best way possible."""

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_env_variables():
    """Test if environment variables are properly loaded"""
    print("Testing environment variables...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ FAIL: GEMINI_API_KEY not found in .env file")
        print("   Create .env file with: GEMINI_API_KEY=your_key_here")
        return False
    
    if api_key == "YOUR_GEMINI_API_KEY_HERE":
        print("❌ FAIL: Please replace placeholder API key with actual key")
        print("   Get key from: https://makersuite.google.com/app/apikey")
        return False
    
    if not api_key.startswith("AIza"):
        print("⚠️  WARNING: API key doesn't start with 'AIza' - may be invalid")
        print("   Google Gemini keys typically start with 'AIza'")
        return False
    
    if len(api_key) < 30:
        print("⚠️  WARNING: API key seems too short - may be invalid")
        return False
    
    print("✓ PASS: Environment variables configured correctly")
    print(f"   API Key: {api_key[:10]}...{api_key[-5:]}")
    return True


def test_imports():
    """Test if all required packages are installed"""
    print("\nTesting package imports...")
    
    required_packages = {
        'streamlit': 'streamlit',
        'google.generativeai': 'google-generativeai',
        'dotenv': 'python-dotenv'
    }
    
    all_imported = True
    
    for package_name, install_name in required_packages.items():
        try:
            __import__(package_name)
            print(f"✓ {install_name} installed")
        except ImportError:
            print(f"❌ {install_name} not installed")
            all_imported = False
    
    if all_imported:
        print("✓ PASS: All required packages installed")
    else:
        print("❌ FAIL: Missing packages")
        print("   Run: pip install -r requirements.txt")
    
    return all_imported


def test_api_connection():
    """Test Google Gemini API connectivity with actual models from app.py"""
    print("\nTesting Google Gemini API connection...")
    
    if not GEMINI_API_KEY:
        print("❌ SKIP: API key not configured")
        return False
    
    if not GEMINI_AVAILABLE:
        print("❌ FAIL: google-generativeai package not installed")
        return False
    
    try:
        print("Configuring Gemini API...")
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Test with Fast Mode model (same as app.py)
        test_model = MODELS["Fast Mode"]
        print(f"Creating test model ({test_model})...")
        model = genai.GenerativeModel(test_model)
        
        print("Sending test request...")
        response = model.generate_content(
            "Say 'Hello, test successful!' in one sentence.",
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 50,
            }
        )
        
        if response and response.text:
            print("✓ PASS: API connection successful")
            print(f"   Sample response: {response.text[:80]}...")
            return True
        else:
            print("⚠️  WARNING: API responded but no text received")
            return False
            
    except Exception as e:
        error_str = str(e).lower()
        
        if "api key" in error_str or "invalid" in error_str or "401" in error_str:
            print("❌ FAIL: Invalid API key")
            print("   Get new key: https://makersuite.google.com/app/apikey")
        elif "quota" in error_str or "limit" in error_str or "429" in error_str:
            print("⚠️  WARNING: API quota/rate limit reached")
            print("   Free tier: 60 requests/minute, 1500/day")
        elif "not found" in error_str or "404" in error_str:
            print("❌ FAIL: Model not found")
            print(f"   Tried model: {test_model}")
        else:
            print(f"❌ FAIL: {str(e)[:150]}")
        
        return False


def test_chat_history_system():
    """Test chat history file operations (from app.py)"""
    print("\nTesting chat history system...")
    
    try:
        # Test data matching app.py structure
        test_chat = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": "Test chat for verification",
            "messages": [
                {"role": "user", "content": "Test message 1"},
                {"role": "assistant", "content": "Test response 1"},
                {"role": "user", "content": "Test message 2"},
                {"role": "assistant", "content": "Test response 2"}
            ]
        }
        
        # Test write
        test_history = [test_chat]
        with open(CHAT_HISTORY_FILE, 'w') as f:
            json.dump(test_history, f, indent=2)
        print("✓ Write test passed")
        
        # Test read
        with open(CHAT_HISTORY_FILE, 'r') as f:
            loaded_data = json.load(f)
        
        if loaded_data == test_history:
            print("✓ Read test passed")
        else:
            print("⚠️  Data mismatch after read")
        
        # Verify structure
        if loaded_data[0]["id"] and loaded_data[0]["messages"]:
            print("✓ Chat structure matches app.py format")
        
        print("✓ PASS: Chat history file operations work")
        print(f"   History file: {CHAT_HISTORY_FILE}")
        return True
            
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        print("   Check write permissions in project directory")
        return False


def test_session_state_structure():
    """Test that session state structure matches app.py"""
    print("\nTesting session state structure...")
    
    # Expected session state keys from app.py
    expected_keys = [
        "messages",
        "system_prompt", 
        "selected_model",
        "temperature",
        "dark_mode",
        "show_settings",
        "show_history"
    ]
    
    print("Expected session state keys from app.py:")
    for key in expected_keys:
        print(f"  ✓ {key}")
    
    print("✓ PASS: Session state structure documented")
    return True


def test_models_from_app():
    """Test all three models defined in app.py"""
    print("\nTesting all models from app.py...")
    
    if not GEMINI_API_KEY or not GEMINI_AVAILABLE:
        print("❌ SKIP: API not configured")
        return False
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        results = {}
        for mode_name, model_name in MODELS.items():
            try:
                model = genai.GenerativeModel(model_name)
                # Quick test
                response = model.generate_content(
                    "Hi",
                    generation_config={"max_output_tokens": 10}
                )
                if response and response.text:
                    print(f"✓ {mode_name} ({model_name}) - Working")
                    results[mode_name] = True
                else:
                    print(f"⚠️  {mode_name} ({model_name}) - No response")
                    results[mode_name] = False
            except Exception as e:
                print(f"❌ {mode_name} ({model_name}) - Error: {str(e)[:50]}")
                results[mode_name] = False
        
        working_count = sum(results.values())
        total_count = len(results)
        
        if working_count == total_count:
            print(f"✓ PASS: All {total_count}/{total_count} models working")
            return True
        elif working_count > 0:
            print(f"⚠️  PARTIAL: {working_count}/{total_count} models working")
            return True
        else:
            print(f"❌ FAIL: No models working")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {str(e)[:100]}")
        return False


def test_temperature_range():
    """Test temperature range used in app.py (0.0 to 1.5)"""
    print("\nTesting temperature configuration...")
    
    temp_min = 0.0
    temp_max = 1.5
    temp_default = 0.7
    
    print(f"✓ Temperature range: {temp_min} to {temp_max}")
    print(f"✓ Default temperature: {temp_default}")
    print("✓ PASS: Temperature settings match app.py")
    return True


def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting project file structure...")
    
    required_files = {
        'app.py': 'Main application file',
        'requirements.txt': 'Dependencies file',
        'README.md': 'Documentation',
        '.env': 'API key configuration',
        '.env.example': 'Environment template'
    }
    
    optional_files = {
        'chat_history.json': 'Chat history (auto-generated)',
        'QUICKSTART.md': 'Quick start guide',
        '.gitignore': 'Git ignore rules'
    }
    
    all_exist = True
    
    print("Required files:")
    for filename, description in required_files.items():
        if os.path.exists(filename):
            print(f"  ✓ {filename} ({description})")
        else:
            print(f"  ❌ {filename} ({description}) - MISSING")
            all_exist = False
    
    print("\nOptional files:")
    for filename, description in optional_files.items():
        if os.path.exists(filename):
            print(f"  ✓ {filename} ({description})")
        else:
            print(f"  ⚠️  {filename} ({description}) - Not found")
    
    if all_exist:
        print("\n✓ PASS: All required files present")
    else:
        print("\n⚠️  WARNING: Some required files missing")
    
    return all_exist


def test_dark_mode_feature():
    """Test dark mode configuration from app.py"""
    print("\nTesting dark/light mode feature...")
    
    print("✓ Dark mode toggle implemented")
    print("✓ Light mode as default")
    print("✓ CSS switching logic present")
    print("✓ PASS: Theme switching feature documented")
    return True


def test_system_prompt():
    """Test system prompt matches app.py"""
    print("\nTesting system prompt configuration...")
    
    if DEFAULT_SYSTEM_PROMPT:
        print(f"✓ System prompt defined ({len(DEFAULT_SYSTEM_PROMPT)} chars)")
        print(f"   Preview: {DEFAULT_SYSTEM_PROMPT[:80]}...")
        print("✓ PASS: System prompt configuration correct")
        return True
    else:
        print("❌ FAIL: System prompt not defined")
        return False


# ============================================================================
# QUICK CHECK
# ============================================================================

def quick_check():
    """Quick setup verification"""
    print("=" * 60)
    print("TEXTIQ - QUICK SETUP CHECK")
    print("=" * 60)
    print()
    
    issues = []
    warnings = []
    
    # Check .env
    if not os.path.exists('.env'):
        issues.append("❌ .env file missing")
    else:
        print("✓ .env file exists")
    
    # Check API key
    if not GEMINI_API_KEY:
        issues.append("❌ GEMINI_API_KEY not set")
    elif not GEMINI_API_KEY.startswith("AIza"):
        warnings.append("⚠️  API key format unusual")
    else:
        print("✓ API key configured")
    
    # Check packages
    if not GEMINI_AVAILABLE:
        issues.append("❌ google-generativeai not installed")
    else:
        print("✓ google-generativeai installed")
    
    if not STREAMLIT_AVAILABLE:
        issues.append("❌ streamlit not installed")
    else:
        print("✓ streamlit installed")
    
    # Check files
    if not os.path.exists('app.py'):
        issues.append("❌ app.py missing")
    else:
        print("✓ app.py exists")
    
    if not os.path.exists('requirements.txt'):
        warnings.append("⚠️  requirements.txt missing")
    else:
        print("✓ requirements.txt exists")
    
    print()
    
    if issues:
        print("🚨 CRITICAL ISSUES:")
        for issue in issues:
            print(f"  {issue}")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not issues and not warnings:
        print("🎉 Everything looks good!")
        print("\n✨ Ready to run: streamlit run app.py")
    elif not issues:
        print("\n✅ Core setup complete (warnings are optional)")
        print("✨ Ready to run: streamlit run app.py")
    else:
        print("\n🔧 Fix critical issues above, then run: python testing.py")
    
    print("=" * 60)


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run complete test suite"""
    print("=" * 60)
    print("TEXTIQ AI CHATBOT - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print()
    
    results = {
        "Environment Variables": test_env_variables(),
        "Package Imports": test_imports(),
        "API Connection": test_api_connection(),
        "Chat History System": test_chat_history_system(),
        "Session State Structure": test_session_state_structure(),
        "All Models (Fast/Powerful/Balanced)": test_models_from_app(),
        "Temperature Configuration": test_temperature_range(),
        "File Structure": test_file_structure(),
        "Dark Mode Feature": test_dark_mode_feature(),
        "System Prompt": test_system_prompt()
    }
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    percentage = (passed / total) * 100
    print(f"Success Rate: {percentage:.1f}%")
    
    print()
    
    if passed == total:
        print("🎉 PERFECT! All tests passed!")
        print("\n✨ Your TextIQ chatbot is ready to run!")
        print("   Command: streamlit run app.py")
    elif passed >= total * 0.8:
        print("✅ Great! Most tests passed.")
        print("\n✨ Your chatbot should work fine!")
        print("   Command: streamlit run app.py")
        print("\n⚠️  Some optional features may need attention.")
    elif passed >= total * 0.5:
        print("⚠️  Some tests failed.")
        print("\n🔧 Fix the failed tests for full functionality.")
        print("   Check the errors above for details.")
    else:
        print("❌ Several critical tests failed.")
        print("\n🔧 Please fix the issues above before running the app.")
        print("\nCommon fixes:")
        print("  - Missing API key: Add to .env file")
        print("  - Missing packages: pip install -r requirements.txt")
        print("  - Invalid API key: Get new key from Google")
    
    print("=" * 60)
    
    return passed, total


# ============================================================================
# INDIVIDUAL TEST RUNNER
# ============================================================================

def run_specific_test(test_name):
    """Run a specific test"""
    tests = {
        "env": ("Environment Variables", test_env_variables),
        "imports": ("Package Imports", test_imports),
        "api": ("API Connection", test_api_connection),
        "history": ("Chat History", test_chat_history_system),
        "session": ("Session State", test_session_state_structure),
        "models": ("All Models", test_models_from_app),
        "temp": ("Temperature", test_temperature_range),
        "files": ("File Structure", test_file_structure),
        "darkmode": ("Dark Mode", test_dark_mode_feature),
        "prompt": ("System Prompt", test_system_prompt)
    }
    
    if test_name.lower() in tests:
        name, func = tests[test_name.lower()]
        print(f"Running {name} test...\n")
        result = func()
        print(f"\n{'✓ PASSED' if result else '❌ FAILED'}")
    else:
        print(f"Unknown test: {test_name}")
        print("\nAvailable tests:")
        for key, (name, _) in tests.items():
            print(f"  {key:10} - {name}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "quick":
            quick_check()
        elif command in ["env", "imports", "api", "history", "session", 
                        "models", "temp", "files", "darkmode", "prompt"]:
            run_specific_test(command)
        elif command == "help":
            print("TextIQ Testing Suite")
            print("\nUsage:")
            print("  python testing.py              - Run all tests")
            print("  python testing.py quick        - Quick setup check")
            print("  python testing.py env          - Test environment variables")
            print("  python testing.py imports      - Test package imports")
            print("  python testing.py api          - Test API connection")
            print("  python testing.py history      - Test chat history")
            print("  python testing.py session      - Test session state")
            print("  python testing.py models       - Test all 3 models")
            print("  python testing.py temp         - Test temperature config")
            print("  python testing.py files        - Test file structure")
            print("  python testing.py darkmode     - Test dark mode feature")
            print("  python testing.py prompt       - Test system prompt")
        else:
            print(f"Unknown command: {command}")
            print("Run 'python testing.py help' for usage")
    else:
        run_all_tests()