"""
Simple Portia test without tools
"""
import os
from dotenv import load_dotenv
from portia import Portia, Config

load_dotenv()

def simple_portia_test():
    """Test basic Portia functionality"""
    
    print("Testing Basic Portia Functionality")
    print("=" * 40)
    
    try:
        # Simple config without tools
        config = Config.from_default(llm_provider="google")
        portia = Portia(config=config)
        
        # Very simple query
        query = "What is DevOps? Give a brief answer."
        
        print("Sending simple query to Portia...")
        result = portia.run(query)
        
        if hasattr(result.outputs.final_output, 'value'):
            response = str(result.outputs.final_output.value)
        else:
            response = str(result.outputs.final_output)
        
        print(f"\nPlan ID: {result.plan_id}")
        print(f"Response: {response}")
        print("\nBasic Portia functionality working!")
        
    except Exception as e:
        print(f"\nBasic Portia Error: {str(e)}")
        print("Check your PORTIA_API_KEY and Google API key")

if __name__ == "__main__":
    simple_portia_test()