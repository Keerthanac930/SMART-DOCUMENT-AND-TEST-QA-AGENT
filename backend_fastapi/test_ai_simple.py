"""
Simple test to check which Gemini models are available
"""
import google.generativeai as genai
from config import settings

def test_gemini_models():
    """Test which Gemini models work"""
    
    api_key = settings.google_gemini_api_key or settings.google_ai_api_key
    if not api_key:
        print("❌ No API key configured")
        return
    
    genai.configure(api_key=api_key)
    
    # List of models to try
    models_to_try = [
        'gemini-2.0-flash-exp',
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-1.5-flash-latest',
        'gemini-pro',
        'models/gemini-pro',
    ]
    
    print("Testing Gemini models...")
    print("=" * 60)
    
    working_model = None
    
    for model_name in models_to_try:
        try:
            print(f"\nTrying: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello'")
            if response and response.text:
                print(f"  ✓ SUCCESS - Response: {response.text[:50]}")
                if not working_model:
                    working_model = model_name
            else:
                print(f"  ✗ No response")
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                print(f"  ✗ Model not found")
            else:
                print(f"  ✗ Error: {error_msg[:100]}")
    
    print("\n" + "=" * 60)
    if working_model:
        print(f"✓ Recommended model: {working_model}")
    else:
        print("❌ No working models found")
    
    # List available models
    print("\n" + "=" * 60)
    print("Listing available models from API...")
    try:
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    test_gemini_models()

