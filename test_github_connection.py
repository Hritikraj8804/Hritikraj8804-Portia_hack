"""
Test GitHub tool connection through Portia
"""
import os
from dotenv import load_dotenv
from portia import Portia, Config
from portia.open_source_tools.registry import example_tool_registry

load_dotenv()

def test_github_connection():
    """Test if Portia can connect to GitHub"""
    
    print("🔧 Testing GitHub Tool Connection")
    print("=" * 40)
    
    try:
        # Initialize Portia
        config = Config.from_default(llm_provider="google")
        portia = Portia(config=config, tools=example_tool_registry)
        
        # Simple GitHub test query
        test_query = """
        Use the GitHub tool to check if you can access the repository Hritikraj8804/devops-python-app.
        Just confirm if the repository exists and if you can see any basic information about it.
        """
        
        print("🚀 Sending test query to Portia...")
        result = portia.run(test_query)
        
        if hasattr(result.outputs.final_output, 'value'):
            response = str(result.outputs.final_output.value)
        else:
            response = str(result.outputs.final_output)
        
        print(f"\n📋 Plan ID: {result.plan_id}")
        print(f"🤖 Response: {response}")
        
        # Check if GitHub tool was used successfully
        if "cannot" in response.lower() or "do not have access" in response.lower():
            print("\n❌ GitHub tool connection FAILED")
            print("💡 Check Portia dashboard tool configuration")
        else:
            print("\n✅ GitHub tool connection SUCCESS")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("💡 Check API keys and Portia configuration")

if __name__ == "__main__":
    test_github_connection()