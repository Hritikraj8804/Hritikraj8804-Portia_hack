"""
Fix Portia integration to work properly
"""
from dotenv import load_dotenv
from portia import Portia, Config
from portia.open_source_tools.registry import example_tool_registry

load_dotenv()

def test_basic_portia():
    """Test basic Portia functionality"""
    
    print("🔧 Testing Basic Portia Integration")
    print("=" * 50)
    
    try:
        # Use basic configuration
        config = Config.from_default(llm_provider="google")
        portia = Portia(config=config, tools=example_tool_registry)
        
        # Simple query that should work
        simple_query = "Add 1 + 1"
        
        print(f"Testing query: {simple_query}")
        result = portia.run(simple_query)
        
        print(f"✅ Success! Result: {result.outputs.final_output}")
        print(f"📋 Plan ID: {result.plan_id}")
        print(f"🆔 Run ID: {result.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_devops_query():
    """Test DevOps-specific query"""
    
    print("\n🤖 Testing DevOps Query")
    print("=" * 30)
    
    try:
        config = Config.from_default(llm_provider="google")
        portia = Portia(config=config, tools=example_tool_registry)
        
        devops_query = """
        I'm a DevOps engineer and my CI/CD pipeline failed. 
        The error is 'database connection timeout after 300 seconds'.
        Should I retry, rollback, or escalate? 
        Explain in beginner-friendly terms.
        """
        
        print("Executing DevOps query...")
        result = portia.run(devops_query)
        
        print(f"✅ DevOps Response: {result.outputs.final_output}")
        print(f"📋 Plan stored in Portia Cloud with ID: {result.plan_id}")
        
        return result
        
    except Exception as e:
        print(f"❌ DevOps Query Error: {e}")
        return None

if __name__ == "__main__":
    # Test basic functionality first
    basic_works = test_basic_portia()
    
    if basic_works:
        # Test DevOps query
        devops_result = test_devops_query()
        
        if devops_result:
            print("\n🎉 SUCCESS! Portia integration working!")
            print("✅ Plans should now appear in Portia dashboard")
            print("🌐 Check: app.portialabs.ai")
        else:
            print("\n⚠️ Basic Portia works, but DevOps query failed")
    else:
        print("\n❌ Basic Portia integration failed")
        print("Check your API keys in .env file")