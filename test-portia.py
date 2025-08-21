"""
Test Portia SDK integration
Run this to verify everything works
"""
from portia_integration import test_portia_integration

if __name__ == "__main__":
    print("🧪 Testing Portia SDK Integration")
    print("Make sure your .env file has:")
    print("- GOOGLE_API_KEY=your-key")
    print("- PORTIA_API_KEY=your-key")
    print()
    
    test_portia_integration()