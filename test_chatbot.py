"""
Quick test script to verify chatbot integration
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from chatbot import chatbot
    print("[OK] Chatbot module imported successfully")
    
    # Test chatbot response
    test_response = chatbot.get_response("hello")
    print(f"[OK] Chatbot responds to greetings: {test_response[:50]}...")
    
    test_response2 = chatbot.get_response("tell me about battery charging")
    print(f"[OK] Chatbot responds to queries: {test_response2[:50]}...")
    
    print("\n[SUCCESS] Chatbot integration is working correctly!")
    print("\nTo access the chatbot:")
    print("1. Start the Flask app: python app/app.py")
    print("2. Open browser: http://127.0.0.1:5000/chatbot")
    print("3. Or click the 'Chatbot' link in the navbar")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
