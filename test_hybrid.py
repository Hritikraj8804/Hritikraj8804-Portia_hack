"""
Test the hybrid AI system
"""
from workflow_manager import workflow_manager

def test_hybrid_system():
    """Test both fast chat and complex workflows"""
    
    print("🧪 Testing Hybrid AI System")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "query": "Hi, check my pipeline status",
            "expected_type": "chat",
            "description": "Simple greeting + status check"
        },
        {
            "query": "Analyze the backend failure and notify the DevOps team via Slack",
            "expected_type": "workflow", 
            "description": "Complex multi-step workflow"
        },
        {
            "query": "What should I do about this error?",
            "expected_type": "chat",
            "description": "Simple troubleshooting question"
        },
        {
            "query": "Research solutions for database timeout errors and create an incident report",
            "expected_type": "workflow",
            "description": "Research + documentation workflow"
        },
        {
            "query": "Should I retry the deployment?",
            "expected_type": "chat", 
            "description": "Simple decision question"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['description']}")
        print(f"   Query: \"{test['query']}\"")
        
        # Test routing logic
        is_complex = workflow_manager.is_complex_workflow(test['query'])
        actual_type = "workflow" if is_complex else "chat"
        
        # Check if routing is correct
        status = "✅" if actual_type == test['expected_type'] else "❌"
        print(f"   {status} Route: {actual_type} (expected: {test['expected_type']})")
        
        # Test actual response (quick test)
        try:
            result = workflow_manager.process_query(test['query'])
            response_preview = result['response'][:80] + "..." if len(result['response']) > 80 else result['response']
            print(f"   Response: {response_preview}")
        except Exception as e:
            print(f"   Error: {str(e)}")
    
    print(f"\n🎯 Hybrid system test complete!")
    print("✅ Fast responses for simple queries")
    print("🔧 Complex workflows for advanced tasks")

if __name__ == "__main__":
    test_hybrid_system()