"""
Test the updated routing logic
"""
from workflow_manager import workflow_manager

def test_routing_logic():
    """Test which queries go to Portia vs Gemini"""
    
    print("🧪 Testing Updated Routing Logic")
    print("=" * 50)
    
    test_cases = [
        # Should use Portia (pipeline-related)
        ("Check my pipeline status", True, "Pipeline status check"),
        ("What's my GitHub repository status?", True, "GitHub repo query"),
        ("My deployment failed, help me", True, "Deployment failure"),
        ("Check the CI/CD workflow", True, "CI/CD workflow query"),
        
        # Should use Gemini (simple chat)
        ("Hi there!", False, "Simple greeting"),
        ("What is DevOps?", False, "General question"),
        ("Should I retry?", False, "Simple decision"),
        ("Thanks for the help", False, "Acknowledgment"),
        
        # Should use Portia (complex workflows)
        ("Analyze failure and notify team", True, "Complex workflow"),
        ("Research solutions for database timeout", True, "Research workflow"),
    ]
    
    for query, expected_portia, description in test_cases:
        is_complex = workflow_manager.is_complex_workflow(query)
        route = "Portia" if is_complex else "Gemini"
        expected_route = "Portia" if expected_portia else "Gemini"
        
        status = "✅" if is_complex == expected_portia else "❌"
        
        print(f"\n{status} {description}")
        print(f"   Query: \"{query}\"")
        print(f"   Route: {route} (expected: {expected_route})")
    
    print(f"\n🎯 Routing test complete!")

if __name__ == "__main__":
    test_routing_logic()