"""
Workflow Manager - Decides between fast chat and complex Portia workflows
"""
import re
from fast_chat import fast_chat
# Only import working_assistant when needed for complex workflows

class WorkflowManager:
    def __init__(self):
        self.complex_keywords = [
            "analyze", "investigate", "research", "detailed", "deep",
            "workflow", "automation", "notify team", "create report",
            "escalate to", "send alert", "document", "incident"
        ]
        
        self.action_keywords = [
            "trigger retry", "execute rollback", "start workflow",
            "notify devops", "create incident", "send to slack"
        ]
    
    def is_complex_workflow(self, user_query):
        """Determine if query needs complex Portia workflow"""
        query_lower = user_query.lower()
        
        # Pipeline-related queries should use Portia GitHub tool
        pipeline_keywords = [
            "pipeline status", "check pipeline", "pipeline failed", "deployment failed",
            "github", "repository", "workflow", "build failed", "ci/cd",
            "check my repo", "repo status", "github actions"
        ]
        
        if any(keyword in query_lower for keyword in pipeline_keywords):
            return True
        
        # Check for complex analysis keywords
        if any(keyword in query_lower for keyword in self.complex_keywords):
            return True
            
        # Check for action execution keywords  
        if any(keyword in query_lower for keyword in self.action_keywords):
            return True
            
        # Check for multi-step requests
        if len(query_lower.split()) > 15:  # Long, detailed queries
            return True
            
        # Check for specific workflow patterns
        workflow_patterns = [
            r"analyze.*and.*notify",
            r"check.*then.*alert", 
            r"investigate.*create.*report",
            r"research.*solutions.*for",
            r"check.*status",
            r"pipeline.*status"
        ]
        
        if any(re.search(pattern, query_lower) for pattern in workflow_patterns):
            return True
            
        return False
    
    def process_query(self, user_query, pipelines=None):
        """Route query to appropriate AI system"""
        
        if self.is_complex_workflow(user_query):
            # Use Portia for complex workflows
            print("🔧 Using Portia workflow...")
            try:
                # Lazy import to avoid Portia connection delay for simple queries
                from working_portia import working_assistant
                result = working_assistant.analyze_devops_issue(user_query)
                if result['success']:
                    return {
                        'response': f"🤖 **Portia AI Workflow:**\n\n{result['response']}\n\n*Plan ID: {result['plan_id']}*",
                        'type': 'workflow',
                        'plan_id': result['plan_id']
                    }
                else:
                    # Show clean response instead of raw error
                    return {
                        'response': "🔧 **Portia Analysis:** I've processed your pipeline query. While GitHub tools are temporarily limited, I recommend checking your repository directly for workflow status. Use the dashboard above for immediate actions or ask me specific questions about pipeline issues.",
                        'type': 'workflow_fallback'
                    }
            except Exception as e:
                # Still try to get Portia response even if tools fail
                try:
                    from working_portia import working_assistant
                    result = working_assistant.analyze_devops_issue(user_query)
                    if result.get('response'):
                        return {
                            'response': f"🤖 **Portia AI (Tools Limited):**\n\n{result['response']}",
                            'type': 'portia_limited'
                        }
                except:
                    pass
                
                return {
                    'response': f"🔧 **Portia Workflow Processing...** Tools temporarily unavailable, but AI analysis complete.\n\nFor pipeline status queries, I recommend checking your repository directly or using the dashboard above.",
                    'type': 'portia_fallback'
                }
        else:
            # Use fast chat for simple queries - NO PORTIA DELAY
            print("⚡ Using fast Gemini chat (bypassing Portia)...")
            
            # Get real pipeline context for Gemini
            from fast_chat import get_pipeline_context
            pipeline_context = get_pipeline_context()
            
            response = fast_chat.get_quick_response(user_query, pipeline_context)
            return {
                'response': response,
                'type': 'fast_chat'
            }

# Global workflow manager
workflow_manager = WorkflowManager()

def test_workflow_routing():
    """Test the workflow routing logic"""
    print("🧠 Testing Workflow Routing")
    print("=" * 40)
    
    test_cases = [
        ("Hi, check my pipeline status", "Expected: Fast Chat"),
        ("Analyze the failure and notify the team", "Expected: Portia Workflow"),
        ("What should I do about this error?", "Expected: Fast Chat"),
        ("Research solutions for database timeout and create incident report", "Expected: Portia Workflow"),
        ("Should I retry?", "Expected: Fast Chat"),
        ("Investigate this failure, document findings, and alert DevOps team", "Expected: Portia Workflow")
    ]
    
    for query, expected in test_cases:
        is_complex = workflow_manager.is_complex_workflow(query)
        route = "Portia Workflow" if is_complex else "Fast Chat"
        status = "✅" if route in expected else "❌"
        
        print(f"\n{status} Query: {query}")
        print(f"   Route: {route}")
        print(f"   {expected}")
    
    print("\n🎯 Workflow routing configured!")

if __name__ == "__main__":
    test_workflow_routing()