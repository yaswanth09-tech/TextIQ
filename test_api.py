"""
Simple API Key Tester
Run this to check if your Gemini API key works
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("=" * 60)
print("GEMINI API KEY TESTER")
print("=" * 60)

# Check if package is installed
print("\n1. Checking google-generativeai package...")
try:
    import google.generativeai as genai
    print("   ✅ Package installed")
except ImportError:
    print("   ❌ Package NOT installed")
    print("   Run: pip install google-generativeai")
    exit(1)

# Check API key
print("\n2. Checking API key...")
api_key = os.getenv("GEMINI_API_KEY", "")

if not api_key:
    print("   ❌ No API key found in .env file")
    print("\n   Create .env file with:")
    print("   GEMINI_API_KEY=your_key_here")
    exit(1)

if len(api_key) < 20:
    print("   ❌ API key too short")
    print(f"   Current key: {api_key}")
    exit(1)

print(f"   ✅ API key found: {api_key[:10]}...")

# Test API connection
print("\n3. Testing API connection...")
try:
    genai.configure(api_key=api_key)
    
    # Try listing models
    print("   Attempting to list available models...")
    models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            models.append(m.name)
    
    if models:
        print(f"   ✅ SUCCESS! Found {len(models)} models")
        print("\n   Available models:")
        for model in models[:5]:  # Show first 5
            print(f"   - {model}")
        if len(models) > 5:
            print(f"   ... and {len(models) - 5} more")
    else:
        print("   ⚠️  Connected but no models available")
        print("   Your API key might need activation")
        
except Exception as e:
    error_str = str(e).lower()
    print(f"   ❌ FAILED: {str(e)[:100]}")
    
    print("\n   Possible solutions:")
    if "api" in error_str and "key" in error_str:
        print("   - API key is invalid")
        print("   - Get new key: https://aistudio.google.com/app/apikey")
    elif "quota" in error_str or "429" in error_str:
        print("   - Rate limit exceeded")
        print("   - Wait a few minutes or get new API key")
    else:
        print("   - Check internet connection")
        print("   - Update package: pip install --upgrade google-generativeai")
    exit(1)

# Test actual generation
print("\n4. Testing message generation...")
try:
    # Use first available model
    model_name = models[0].replace("models/", "")
    model = genai.GenerativeModel(model_name)
    
    print(f"   Using model: {model_name}")
    print("   Sending test message: 'Say hi'")
    
    response = model.generate_content("Say hi")
    
    print(f"   ✅ Response received: {response.text[:50]}...")
    
except Exception as e:
    print(f"   ❌ Generation failed: {str(e)[:100]}")
    
    error_str = str(e).lower()
    if "quota" in error_str or "429" in error_str:
        print("\n   Your API key hit the rate limit!")
        print("   Solutions:")
        print("   1. Wait a few minutes")
        print("   2. Get new free API key")
    exit(1)

# All tests passed!
print("\n" + "=" * 60)
print("🎉 ALL TESTS PASSED!")
print("=" * 60)
print("\nYour API key is working correctly!")
print("You can now run your chatbot:")
print("  streamlit run app.py")
print("=" * 60)