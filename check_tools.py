"""
Check what tools are available in Portia
"""
import os
from dotenv import load_dotenv
from portia import Portia, Config
from portia.open_source_tools.registry import example_tool_registry

load_dotenv()

def check_available_tools():
    """Check what tools Portia has access to"""
    
    print("🛠️ Checking Available Portia Tools")
    print("=" * 40)
    
    try:
        # Initialize Portia
        config = Config.from_default(llm_provider="google")
        portia = Portia(config=config, tools=example_tool_registry)
        
        # Simple query to see what tools are available
        test_query = """
        What tools do you have access to? List all available tools you can use.
        """
        
        print("🚀 Checking available tools...")
        result = portia.run(test_query)
        
        if hasattr(result.outputs.final_output, 'value'):
            response = str(result.outputs.final_output.value)
        else:
            response = str(result.outputs.final_output)
        
        print(f"\n📋 Plan ID: {result.plan_id}")
        print(f"🛠️ Available Tools: {response}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("💡 Portia configuration issue")

if __name__ == "__main__":
    check_available_tools()