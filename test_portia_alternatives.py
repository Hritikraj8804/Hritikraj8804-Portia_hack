#!/usr/bin/env python3
"""
Test if Portia API key works with alternative AI services
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_alternative_services():
    """Test if Portia key works with other AI services"""
    portia_api_key = os.getenv('PORTIA_API_KEY')
    
    if not portia_api_key:
        print("ERROR: PORTIA_API_KEY not found")
        return False
    
    print(f"Testing API Key: {portia_api_key}")
    
    # Test with different AI service endpoints that might use Portia keys
    test_configs = [
        {
            'name': 'Anthropic Claude',
            'url': 'https://api.anthropic.com/v1/messages',
            'headers': {
                'x-api-key': portia_api_key,
                'anthropic-version': '2023-06-01',
                'Content-Type': 'application/json'
            },
            'data': {
                'model': 'claude-3-sonnet-20240229',
                'max_tokens': 50,
                'messages': [{'role': 'user', 'content': 'Hello'}]
            }
        },
        {
            'name': 'Cohere',
            'url': 'https://api.cohere.ai/v1/generate',
            'headers': {
                'Authorization': f'Bearer {portia_api_key}',
                'Content-Type': 'application/json'
            },
            'data': {
                'model': 'command',
                'prompt': 'Hello',
                'max_tokens': 50
            }
        },
        {
            'name': 'Hugging Face',
            'url': 'https://api-inference.huggingface.co/models/gpt2',
            'headers': {
                'Authorization': f'Bearer {portia_api_key}',
                'Content-Type': 'application/json'
            },
            'data': {
                'inputs': 'Hello'
            }
        },
        {
            'name': 'Together AI',
            'url': 'https://api.together.xyz/inference',
            'headers': {
                'Authorization': f'Bearer {portia_api_key}',
                'Content-Type': 'application/json'
            },
            'data': {
                'model': 'togethercomputer/RedPajama-INCITE-Chat-3B-v1',
                'prompt': 'Hello',
                'max_tokens': 50
            }
        }
    ]
    
    for config in test_configs:
        print(f"\nTesting {config['name']}...")
        try:
            response = requests.post(
                config['url'],
                headers=config['headers'],
                json=config['data'],
                timeout=10
            )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"  SUCCESS! Response: {result}")
                return True
            elif response.status_code in [401, 403]:
                print(f"  Auth failed: {response.text[:100]}")
            else:
                print(f"  Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"  Connection error: {str(e)[:100]}")
    
    # Test if it's a custom Portia service with different base URLs
    portia_urls = [
        'https://portia-ai.herokuapp.com/api/chat',
        'https://portia.ngrok.io/api/chat',
        'https://api.portia.dev/chat',
        'https://portia-api.vercel.app/api/chat'
    ]
    
    print(f"\nTesting custom Portia endpoints...")
    for url in portia_urls:
        print(f"  Testing: {url}")
        try:
            headers = {
                'Authorization': f'Bearer {portia_api_key}',
                'Content-Type': 'application/json'
            }
            data = {'message': 'Hello', 'max_tokens': 50}
            
            response = requests.post(url, headers=headers, json=data, timeout=5)
            print(f"    Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"    SUCCESS! Response: {result}")
                return True
                
        except Exception as e:
            print(f"    Error: {str(e)[:50]}")
    
    return False

if __name__ == "__main__":
    print("Testing Portia API Key with Alternative Services")
    print("=" * 50)
    
    success = test_alternative_services()
    
    if success:
        print("\nSUCCESS: Found working configuration!")
    else:
        print("\nNo working configuration found.")
        print("The Portia API key might be for a service not tested here.")