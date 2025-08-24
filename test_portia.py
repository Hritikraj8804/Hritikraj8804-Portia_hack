#!/usr/bin/env python3
"""
Test Portia API connection and response
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_portia_api():
    """Test Portia API connection"""
    portia_api_key = os.getenv('PORTIA_API_KEY')
    
    if not portia_api_key:
        print("❌ PORTIA_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key found: {portia_api_key[:10]}...")
    
    headers = {
        'Authorization': f'Bearer {portia_api_key}',
        'Content-Type': 'application/json'
    }
    
    # Test data for different API formats
    test_data = [
        {
            'prompt': 'Hello, this is a test message',
            'max_tokens': 50,
            'temperature': 0.7
        },
        {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': 'Hello, this is a test message'}],
            'max_tokens': 50
        }
    ]
    
    # Test different possible endpoints
    endpoints = [
        'https://api.portia.dev/v1/completions',
        'https://api.getportia.com/v1/chat/completions',
        'https://api.portia.ai/v1/chat/completions',
        'https://portia.ai/api/v1/chat/completions'
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing endpoint: {endpoint}")
        for i, data in enumerate(test_data):
            try:
                print(f"  Trying data format {i+1}...")
                response = requests.post(endpoint, headers=headers, json=data, timeout=10)
                print(f"  Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"  ✅ SUCCESS! Response: {result}")
                    return True
                else:
                    print(f"  ❌ Error Response: {response.text[:200]}")
                    
            except Exception as e:
                print(f"  ❌ Connection Error: {e}")
                continue
    
    return False

if __name__ == "__main__":
    print("🚀 Testing Portia API Connection")
    print("=" * 40)
    
    success = test_portia_api()
    
    if success:
        print("\n🎉 Portia API is working!")
    else:
        print("\n⚠️ Portia API connection failed. Check your API key and endpoint.")