"""
Portia workflow examples for complex DevOps tasks
"""

def get_workflow_examples():
    """Examples of complex queries that should trigger Portia workflows"""
    
    return {
        "github_analysis": {
            "query": "Check my GitHub repository pipeline status and analyze any failures",
            "expected_tools": ["GitHub"],
            "description": "Uses GitHub tool to get real pipeline data"
        },
        
        "error_research": {
            "query": "Research solutions for database timeout errors in CI/CD pipelines",
            "expected_tools": ["Tavily"],
            "description": "Uses Tavily to research specific error solutions"
        },
        
        "team_notification": {
            "query": "Analyze the backend failure and notify the DevOps team via Slack",
            "expected_tools": ["GitHub", "Slack"],
            "description": "Multi-tool workflow: analyze + notify"
        },
        
        "full_workflow": {
            "query": "Investigate the deployment failure, research solutions, and create an incident report for the team",
            "expected_tools": ["GitHub", "Tavily", "Slack"],
            "description": "Complete DevOps incident response workflow"
        },
        
        "escalation_workflow": {
            "query": "The pipeline has failed 3 times, escalate to DevOps team with full analysis",
            "expected_tools": ["GitHub", "Tavily", "Slack"],
            "description": "Escalation with comprehensive analysis"
        }
    }

def test_workflow_triggers():
    """Test which queries should trigger Portia workflows"""
    
    print("🔧 Testing Portia Workflow Triggers")
    print("=" * 50)
    
    examples = get_workflow_examples()
    
    for name, example in examples.items():
        print(f"\n📋 {name.replace('_', ' ').title()}")
        print(f"   Query: {example['query']}")
        print(f"   Expected Tools: {', '.join(example['expected_tools'])}")
        print(f"   Description: {example['description']}")
    
    print(f"\n🎯 These queries should use Portia workflows with real tools!")
    print("✅ Simple questions use fast Gemini chat")
    print("🔧 Complex workflows use Portia + GitHub/Slack/Tavily")

if __name__ == "__main__":
    test_workflow_triggers()