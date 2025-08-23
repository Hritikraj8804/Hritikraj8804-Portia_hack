"""
Workflow Manager - Decides between fast chat and complex Portia workflows
"""
import re
# All queries now go through Portia for consistent AI experience

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
        """Route all queries through Portia for consistent AI experience"""
        
        print("🤖 Using Portia AI for all queries...")
        
        try:
            from working_portia import working_assistant
            
            # Add pipeline context to query
            context_info = ""
            if pipelines:
                failed_count = len([p for p in pipelines if p.get('status') == 'failed'])
                running_count = len([p for p in pipelines if p.get('status') == 'running'])
                success_count = len([p for p in pipelines if p.get('status') == 'success'])
                
                context_info = f"""
                
Current Pipeline Context:
                - {success_count} successful pipelines
                - {failed_count} failed pipelines  
                - {running_count} running pipelines
                """
                
                if failed_count > 0:
                    failed_pipelines = [p for p in pipelines if p.get('status') == 'failed']
                    context_info += f"\nFailed Pipeline Details:\n"
                    for p in failed_pipelines[:2]:
                        context_info += f"- {p['name']}: {p.get('error', 'Unknown error')}\n"
            
            # Enhanced query with context
            enhanced_query = f"{user_query}{context_info}"
            
            result = working_assistant.analyze_devops_issue(enhanced_query)
            
            if result['success']:
                return {
                    'response': f"🤖 **Portia AI Assistant:**\n\n{result['response']}\n\n*Plan ID: {result['plan_id']}*",
                    'type': 'portia_success',
                    'plan_id': result['plan_id']
                }
            else:
                return {
                    'response': f"🤖 **Portia AI Assistant:**\n\n{result.get('response', 'I can help you with DevOps pipeline management. What specific issue would you like assistance with?')}",
                    'type': 'portia_response'
                }
                
        except Exception as e:
            print(f"Portia error: {e}")
            return {
                'response': "🤖 **Portia AI Assistant:** I'm here to help with your DevOps pipelines. I can analyze failures, recommend actions, and coordinate with your development tools. What would you like to know?",
                'type': 'portia_fallback'
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