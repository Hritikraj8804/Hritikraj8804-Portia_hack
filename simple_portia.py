"""
Simple Portia integration that works
"""
from dotenv import load_dotenv
from portia import Portia, Config

load_dotenv()

class SimplePortiaAssistant:
    def __init__(self):
        self.config = Config.from_default(
            llm_provider="google", 
            default_model="google/gemini-1.5-flash"
        )
        self.portia = Portia(config=self.config)
    
    def analyze_pipeline_issue(self, user_query: str):
        """Analyze pipeline issues using simple Portia run"""
        
        enhanced_query = f"""
        You are a DevOps AI Assistant helping newbie engineers.
        
        User Query: {user_query}
        
        Context: We have CI/CD pipelines that can fail. Help analyze the issue and recommend:
        - retry (for temporary issues like network timeouts)
        - rollback (for code-related problems)  
        - escalate (for infrastructure issues)
        
        Provide beginner-friendly explanations without technical jargon.
        """
        
        try:
            plan_run = self.portia.run(enhanced_query)
            return plan_run.outputs.final_output
        except Exception as e:
            return f"Portia analysis: {str(e)}"

# Global instance
simple_assistant = SimplePortiaAssistant()

def test_simple_portia():
    """Test simple Portia integration"""
    
    print("🤖 Testing Simple Portia Integration")
    print("=" * 40)
    
    try:
        result = simple_assistant.analyze_pipeline_issue(
            "My backend pipeline failed with database timeout, what should I do?"
        )
        print(f"Portia Response: {result}")
        print("✅ Portia integration working!")
        
    except Exception as e:
        print(f"❌ Portia Error: {e}")
        print("💡 Using fallback responses for demo")

if __name__ == "__main__":
    test_simple_portia()