"""
DevOps Execution Agent for Portia Labs Cloud
Upload this file to your Portia Labs dashboard
"""
from dotenv import load_dotenv
from portia import Portia, Config
from pydantic import BaseModel, Field
import os

load_dotenv()

# Configure Portia for cloud execution
config = Config.from_default(
    llm_provider="google", 
    default_model="google/gemini-1.5-flash"
)

portia = Portia(config=config)

# Define the main DevOps analysis query
DEVOPS_QUERY = """
You are a DevOps AI Assistant helping newbie engineers with CI/CD pipeline issues.

Your task:
1. Check pipeline status at http://localhost:8000/pipelines
2. Identify any failed pipelines and analyze their errors
3. Recommend appropriate actions: retry (for temporary issues), rollback (for code issues), or escalate (for infrastructure issues)
4. Provide beginner-friendly explanations without technical jargon
5. Ask clarifying questions about urgency and impact if needed

Context: The user is a beginner DevOps engineer who needs clear, actionable guidance.

Please analyze the current pipeline status and provide recommendations.
"""

def analyze_pipelines():
    """Main function to analyze pipeline status and provide recommendations"""
    
    # Generate plan for pipeline analysis
    plan = portia.plan(DEVOPS_QUERY)
    
    # Execute the plan
    plan_run = portia.run_plan(plan)
    
    return plan_run.outputs.final_output

# Example usage for testing
if __name__ == "__main__":
    print("🔍 DevOps Execution Agent - Pipeline Analysis")
    print("=" * 50)
    
    try:
        result = analyze_pipelines()
        print(f"Analysis Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your API keys are configured in .env file")