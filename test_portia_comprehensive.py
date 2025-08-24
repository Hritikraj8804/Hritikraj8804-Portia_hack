#!/usr/bin/env python3
"""
Comprehensive Portia API test - find the correct endpoint and format
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_portia_comprehensive():
    """Test all possible Portia API configurations"""
    portia_api_key = os.getenv('PORTIA_API_KEY')
    
    if not portia_api_key:
        print("ERROR: PORTIA_API_KEY not found")
        return False
    
    print(f"API Key: {portia_api_key}")
    
    # Test different authentication formats
    auth_formats = [
        {'Authorization': f'Bearer {portia_api_key}'},
        {'Authorization': f'Token {portia_api_key}'},
        {'X-API-Key': portia_api_key},
        {'api-key': portia_api_key}
    ]
    
    # Test different endpoints and data formats
    test_configs = [
        # OpenAI-style endpoints
        {
            'url': 'https://api.openai.com/v1/chat/completions',
            'data': {
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': 'Hello'}],
                'max_tokens': 50
            }
        },
        # Portia-specific endpoints
        {
            'url': 'https://portia.ai/api/chat',
            'data': {'message': 'Hello', 'max_tokens': 50}
        },
        {
            'url': 'https://api.portia.com/v1/chat',
            'data': {'prompt': 'Hello', 'max_tokens': 50}
        },
        {
            'url': 'https://portia-api.com/v1/completions',
            'data': {'prompt': 'Hello', 'max_tokens': 50}
        },
        # Try with different subdomains
        {
            'url': 'https://chat.portia.ai/api/v1/completions',
            'data': {'prompt': 'Hello', 'max_tokens': 50}
        }
    ]
    
    for i, config in enumerate(test_configs):
        print(f"\nTest {i+1}: {config['url']}")
        
        for j, headers in enumerate(auth_formats):
            print(f"  Auth format {j+1}: {list(headers.keys())[0]}")
            
            try:
                headers['Content-Type'] = 'application/json'
                response = requests.post(
                    config['url'], 
                    headers=headers, 
                    json=config['data'], 
                    timeout=10
                )
                
                print(f"    Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"    SUCCESS! Response: {result}")
                    return True
                elif response.status_code in [401, 403]:
                    print(f"    Auth issue: {response.text[:100]}")
                else:
                    print(f"    Error: {response.text[:100]}")
                    
            except requests.exceptions.ConnectionError as e:
                if "Failed to resolve" in str(e):
                    print(f"    DNS resolution failed")
                else:
                    print(f"    Connection error: {str(e)[:50]}")
            except Exception as e:
                print(f"    Error: {str(e)[:50]}")
    
    # Test if it's actually an OpenAI proxy
    print(f"\nTesting if Portia key works with OpenAI API...")
    try:
        headers = {
            'Authorization': f'Bearer {portia_api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': 'Hello from Portia test'}],
            'max_tokens': 50
        }
        
        response = requests.post('https://api.openai.com/v1/chat/completions', 
                               headers=headers, json=data, timeout=10)
        
        print(f"OpenAI API Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS! Portia key works with OpenAI: {result}")
            return True
        else:
            print(f"OpenAI API Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"OpenAI API Error: {e}")
    
    return False

if __name__ == "__main__":
    print("Comprehensive Portia API Test")
    print("=" * 50)
    
    success = test_portia_comprehensive()
    
    if success:
        print("\nSUCCESS: Found working Portia API configuration!")
    else:
        print("\nWARNING: No working Portia API configuration found.")
        print("The API key might be for a different service or format.")