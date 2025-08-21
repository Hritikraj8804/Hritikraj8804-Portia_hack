"""
Working Portia integration for DevOps Assistant
"""
from dotenv import load_dotenv
from portia import Portia, Config
from portia.open_source_tools.registry import example_tool_registry

load_dotenv()

class WorkingPortiaAssistant:
    def __init__(self):
        # Use working configuration
        self.config = Config.from_default(llm_provider="google")
        self.portia = Portia(config=self.config, tools=example_tool_registry)
    
    def analyze_devops_issue(self, user_query):
        """Analyze DevOps issues using working Portia setup"""
        
        # Simple query that works with available tools
        enhanced_query = f"""
        You are a DevOps AI Assistant. Answer this question about CI/CD pipelines: {user_query}
        
        Provide recommendations from these options:
        - RETRY: For temporary issues like timeouts or network problems
        - ROLLBACK: For code-related problems or test failures  
        - ESCALATE: For infrastructure or persistent issues
        
        Give a clear, beginner-friendly explanation with your reasoning.
        """
        
        try:
            # Use Portia to generate and execute plan
            plan_run = self.portia.run(enhanced_query)
            
            # Handle different output types
            if hasattr(plan_run.outputs.final_output, 'value'):
                response_text = str(plan_run.outputs.final_output.value)
            else:
                response_text = str(plan_run.outputs.final_output)
            
            return {
                'response': response_text,
                'plan_id': plan_run.plan_id,
                'run_id': plan_run.id,
                'success': True
            }
            
        except Exception as e:
            # Return a helpful DevOps response as fallback
            if "database timeout" in user_query.lower():
                fallback = "**RETRY** - Database timeouts are usually temporary. Try running the pipeline again as the database connection should be restored."
            elif "failed" in user_query.lower():
                fallback = "**RETRY** first for temporary issues, then **ROLLBACK** if it's a code problem, or **ESCALATE** for infrastructure issues."
            else:
                fallback = "I recommend checking your pipeline logs first, then try **RETRY** for temporary issues."
            
            return {
                'response': fallback,
                'success': False,
                'error': str(e)
            }

# Global instance for frontend
working_assistant = WorkingPortiaAssistant()

def test_working_portia():
    """Test the working Portia assistant"""
    
    print("🚀 Testing Working Portia DevOps Assistant")
    print("=" * 50)
    
    test_queries = [
        "My backend pipeline failed with database timeout, what should I do?",
        "Should I retry or rollback a failed deployment?",
        "Check pipeline status and recommend actions"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: {query}")
        result = working_assistant.analyze_devops_issue(query)
        
        if result['success']:
            print(f"✅ Success!")
            print(f"📋 Plan ID: {result['plan_id']}")
            print(f"🤖 Response: {result['response'][:100]}...")
        else:
            print(f"❌ Failed: {result['response']}")
    
    print("\n🎯 Check Portia dashboard at app.portialabs.ai for your plans!")

if __name__ == "__main__":
    test_working_portia()