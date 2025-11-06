"""
Quick test to verify .env loading and Gemini connection
"""

import os
from dotenv import load_dotenv

def quick_test():
    print("🚀 Quick Test - Auto-loading API Key")
    print("=" * 40)
    
    # Load .env file
    load_dotenv()
    
    # Check if API key exists
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file!")
        print("💡 Make sure your .env file contains:")
        print("   GEMINI_API_KEY=your_actual_api_key")
        return False
    
    print(f"✅ API key found")
    
    # Test Gemini connection
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        
        # Try the working model we found earlier
        model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')
        response = model.generate_content("Say hello!")
        
        print("✅ Gemini connection successful!")
        print(f"Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = quick_test()
    
    if success:
        print("\n🎉 Everything is working! You can now run:")
        print("   python test_with_sample.py")
        print("   streamlit run rag_app.py")
    else:
        print("\n🔧 Please fix the issues above first.")