"""
Test if GitHub tool is properly enabled in Portia
"""
import os
from dotenv import load_dotenv
from portia import Portia, Config
from portia.open_source_tools.registry import example_tool_registry

load_dotenv()

def test_github_tool_access():
    """Test if Portia can access GitHub tool"""
    
    print("🔧 Testing GitHub Tool Access in Portia")
    print("=" * 50)
    
    try:
        config = Config.from_default(llm_provider="google")
        portia = Portia(config=config, tools=example_tool_registry)
        
        # Simple test query
        query = """
        List all available tools you have access to. 
        Specifically check if you have access to a GitHub tool.
        """
        
        print("🚀 Checking available tools...")
        result = portia.run(query)
        
        if hasattr(result.outputs.final_output, 'value'):
            response = str(result.outputs.final_output.value)
        else:
            response = str(result.outputs.final_output)
        
        print(f"\n📋 Plan ID: {result.plan_id}")
        print(f"🛠️ Available Tools Response:")
        print(response)
        
        # Check if GitHub is mentioned
        if "github" in response.lower():
            print("\n✅ GitHub tool appears to be available!")
        else:
            print("\n❌ GitHub tool not found in available tools")
            print("💡 Please enable GitHub tool in Portia dashboard")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    test_github_tool_access()