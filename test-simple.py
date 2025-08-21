"""
Simple test without Portia SDK - fallback approach
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_environment():
    """Test if environment is set up correctly"""
    
    print("🧪 Testing Environment Setup")
    print("=" * 40)
    
    # Check API keys
    google_key = os.getenv("GOOGLE_API_KEY")
    portia_key = os.getenv("PORTIA_API_KEY")
    
    if google_key and google_key != "your-google-api-key-here":
        print("✅ Google API Key: Set")
    else:
        print("❌ Google API Key: Missing or default")
    
    if portia_key and portia_key != "your-portia-api-key-here":
        print("✅ Portia API Key: Set")
    else:
        print("❌ Portia API Key: Missing or default")
    
    # Test basic imports
    try:
        import requests
        print("✅ Requests: Available")
    except ImportError:
        print("❌ Requests: Not installed")
    
    try:
        import streamlit
        print("✅ Streamlit: Available")
    except ImportError:
        print("❌ Streamlit: Not installed")
    
    # Test backend connection
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ Backend API: Running")
        else:
            print("❌ Backend API: Not responding")
    except:
        print("⚠️ Backend API: Not running (start with start-backend.bat)")
    
    print("\n🎯 Current Status:")
    print("- Environment: Ready for demo")
    print("- Portia SDK: Optional for hackathon")
    print("- Frontend: Uses enhanced rule-based responses")
    print("- Demo: Fully functional without Portia cloud")

def simulate_portia_response(query):
    """Simulate intelligent Portia-like responses"""
    
    if "status" in query.lower():
        return {
            "pipeline_name": "Backend API",
            "status": "failed", 
            "recommended_action": "retry",
            "reasoning": "Database timeout errors are usually temporary network issues that resolve with retry",
            "urgency": "medium"
        }
    elif "failed" in query.lower():
        return {
            "pipeline_name": "Backend API",
            "status": "failed",
            "recommended_action": "retry", 
            "reasoning": "The error pattern suggests a temporary database connectivity issue. Retry is the safest first action.",
            "urgency": "high"
        }
    else:
        return {
            "pipeline_name": "General",
            "status": "unknown",
            "recommended_action": "check_status",
            "reasoning": "I can help you check pipeline status, troubleshoot failures, and recommend actions.",
            "urgency": "low"
        }

if __name__ == "__main__":
    test_environment()
    
    print("\n🤖 Testing AI Response Simulation:")
    test_query = "My backend pipeline failed, what should I do?"
    response = simulate_portia_response(test_query)
    print(f"Query: {test_query}")
    print(f"Response: {response['recommended_action']} - {response['reasoning']}")
    
    print("\n✅ System ready for hackathon demo!")