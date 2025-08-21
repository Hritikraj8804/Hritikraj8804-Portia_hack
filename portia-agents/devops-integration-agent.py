"""
DevOps Integration Agent for Portia Labs Cloud
Upload this file to your Portia Labs dashboard
"""
from dotenv import load_dotenv
from portia import Portia, Config
import os

load_dotenv()

# Configure Portia for cloud execution
config = Config.from_default(
    llm_provider="google", 
    default_model="google/gemini-1.5-flash"
)

portia = Portia(config=config)

# API integration queries
INTEGRATION_QUERIES = {
    "check_status": """
    Connect to the DevOps pipeline API and check the current status of all pipelines.
    
    API Endpoint: http://localhost:8000/pipelines
    
    Tasks:
    1. Fetch the pipeline data
    2. Identify any failed pipelines
    3. Extract error messages and failure details
    4. Summarize the overall health status
    5. Highlight any urgent issues that need attention
    
    Provide a clear summary of what you found.
    """,
    
    "execute_action": """
    Execute a pipeline action through the API.
    
    API Endpoint: http://localhost:8000/pipelines/action
    Method: POST
    
    Required data:
    - pipeline_id: The ID of the pipeline to act on
    - action: retry, rollback, or escalate
    - reason: Why this action is being taken
    
    After executing:
    1. Confirm the action was successful
    2. Explain what happens next
    3. Provide expected timeline
    4. Mention how to monitor progress
    """,
    
    "get_logs": """
    Retrieve and analyze pipeline logs to understand failures.
    
    API Endpoint: http://localhost:8000/pipelines/{pipeline_id}/logs
    
    Tasks:
    1. Fetch the logs for the specified pipeline
    2. Identify error patterns and root causes
    3. Look for common issues (timeouts, connection failures, test failures)
    4. Suggest potential solutions based on the error patterns
    5. Determine if this is a temporary or persistent issue
    
    Provide analysis in beginner-friendly terms.
    """
}

def check_pipeline_status():
    """Check status of all pipelines"""
    
    query = INTEGRATION_QUERIES["check_status"]
    
    # Generate plan for status check
    plan = portia.plan(query)
    
    # Execute the plan
    plan_run = portia.run_plan(plan)
    
    return plan_run.outputs.final_output

def execute_pipeline_action(pipeline_id, action, reason="AI-recommended action"):
    """Execute action on a specific pipeline"""
    
    query = f"""
    {INTEGRATION_QUERIES["execute_action"]}
    
    Specific Action Details:
    - Pipeline ID: {pipeline_id}
    - Action: {action}
    - Reason: {reason}
    
    Execute this action and provide confirmation.
    """
    
    plan = portia.plan(query)
    plan_run = portia.run_plan(plan)
    
    return plan_run.outputs.final_output

def analyze_pipeline_logs(pipeline_id):
    """Get and analyze logs for a specific pipeline"""
    
    query = f"""
    {INTEGRATION_QUERIES["get_logs"]}
    
    Pipeline ID to analyze: {pipeline_id}
    
    Focus on identifying the root cause and providing actionable insights.
    """
    
    plan = portia.plan(query)
    plan_run = portia.run_plan(plan)
    
    return plan_run.outputs.final_output

def comprehensive_analysis():
    """Perform complete pipeline analysis"""
    
    query = """
    Perform a comprehensive DevOps pipeline analysis:
    
    1. Check status of all pipelines at http://localhost:8000/pipelines
    2. For any failed pipelines, get their logs
    3. Analyze errors and determine root causes
    4. Recommend appropriate actions (retry/rollback/escalate)
    5. Prioritize issues by severity and business impact
    6. Provide a summary with next steps
    
    Present findings in a clear, actionable format for a DevOps beginner.
    """
    
    plan = portia.plan(query)
    plan_run = portia.run_plan(plan)
    
    return plan_run.outputs.final_output

# Example usage for testing
if __name__ == "__main__":
    print("🔗 DevOps Integration Agent - API Communication")
    print("=" * 50)
    
    try:
        # Test comprehensive analysis
        result = comprehensive_analysis()
        print(f"Analysis Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your API is running at http://localhost:8000")