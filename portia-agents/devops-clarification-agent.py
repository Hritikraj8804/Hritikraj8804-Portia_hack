"""
DevOps Clarification Agent for Portia Labs Cloud
Upload this file to your Portia Labs dashboard
"""
from dotenv import load_dotenv
from portia import Portia, Config
from pydantic import BaseModel, Field

load_dotenv()

# Configure Portia for cloud execution
config = Config.from_default(
    llm_provider="google", 
    default_model="google/gemini-1.5-flash"
)

portia = Portia(config=config)

# Clarification templates for different scenarios
CLARIFICATION_QUERIES = {
    "severity": """
    A pipeline has failed and I need to understand the severity to recommend the right action.
    
    Ask the user: "How critical is this pipeline failure?"
    
    Provide these options:
    🔴 Critical - Production is down or blocked
    🟡 High - Blocking important work or releases  
    🟢 Medium - Important but not immediately blocking
    ⚪ Low - Can be addressed later
    
    Explain: "This helps me prioritize the response and choose the right action."
    """,
    
    "action_preference": """
    Based on the pipeline failure, I need to understand what the user wants to do.
    
    Ask the user: "What would you like to do about this failed pipeline?"
    
    Provide these options:
    🔄 Retry - Try running the pipeline again (good for temporary issues)
    ⏪ Rollback - Go back to the previous working version (good for code problems)
    🚨 Escalate - Get help from the DevOps team (good for complex issues)
    🤔 Not sure - Help me decide based on the error
    
    Explain each option in simple terms without technical jargon.
    """,
    
    "beginner_explanation": """
    Explain this technical pipeline issue in beginner-friendly terms:
    
    - What happened in simple language
    - Why it might have happened
    - What the recommended action will do
    - Use analogies where helpful
    - Avoid technical jargon
    - Be encouraging and supportive
    
    Remember: The user is new to DevOps and may feel overwhelmed.
    """
}

def get_clarification(scenario, context=""):
    """Generate clarification questions based on scenario"""
    
    query = CLARIFICATION_QUERIES.get(scenario, CLARIFICATION_QUERIES["beginner_explanation"])
    
    if context:
        query += f"\n\nContext: {context}"
    
    # Generate plan for clarification
    plan = portia.plan(query)
    
    # Execute the plan
    plan_run = portia.run_plan(plan)
    
    return plan_run.outputs.final_output

def explain_for_beginner(technical_issue, recommended_action):
    """Convert technical information to beginner-friendly explanation"""
    
    query = f"""
    Convert this technical pipeline issue into beginner-friendly language:
    
    Technical Issue: {technical_issue}
    Recommended Action: {recommended_action}
    
    Provide:
    1. What happened (in simple terms)
    2. Why it happened (possible causes)
    3. What we'll do to fix it
    4. Why this solution makes sense
    
    Use encouraging language and avoid jargon.
    """
    
    plan = portia.plan(query)
    plan_run = portia.run_plan(plan)
    
    return plan_run.outputs.final_output

# Example usage for testing
if __name__ == "__main__":
    print("🤖 DevOps Clarification Agent - User Interaction")
    print("=" * 50)
    
    # Test severity clarification
    severity_question = get_clarification("severity")
    print(f"Severity Question: {severity_question}")
    
    # Test beginner explanation
    explanation = explain_for_beginner(
        "Database connection timeout in testing stage",
        "Retry the pipeline"
    )
    print(f"Beginner Explanation: {explanation}")