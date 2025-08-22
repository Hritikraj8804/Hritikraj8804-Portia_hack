"""
Test response speed with fixed routing
"""
import time
from workflow_manager import workflow_manager

def test_response_speed():
    """Test response times for different query types"""
    
    print("⚡ Testing Response Speed")
    print("=" * 40)
    
    test_cases = [
        {
            "query": "Hi, check my pipeline status",
            "expected": "fast_chat",
            "description": "Simple status check"
        },
        {
            "query": "Should I retry the deployment?", 
            "expected": "fast_chat",
            "description": "Simple decision question"
        },
        {
            "query": "Analyze the backend failure and notify the DevOps team via Slack",
            "expected": "workflow",
            "description": "Complex multi-tool workflow"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['description']}")
        print(f"   Query: \"{test['query']}\"")
        
        # Time the response
        start_time = time.time()
        
        try:
            result = workflow_manager.process_query(test['query'])
            end_time = time.time()
            
            response_time = round(end_time - start_time, 2)
            response_type = result.get('type', 'unknown')
            
            # Check speed expectations
            if response_type == 'fast_chat' and response_time < 5:
                speed_status = "✅ FAST"
            elif response_type == 'workflow' and response_time < 20:
                speed_status = "✅ ACCEPTABLE"
            else:
                speed_status = "❌ SLOW"
            
            print(f"   {speed_status} Response time: {response_time}s")
            print(f"   Type: {response_type}")
            print(f"   Preview: {result['response'][:60]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n🎯 Speed test complete!")
    print("Expected: Simple queries < 5s, Complex workflows < 20s")

if __name__ == "__main__":
    test_response_speed()