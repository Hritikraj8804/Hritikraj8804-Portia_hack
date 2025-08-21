"""
Portia SDK Integration for DevOps Assistant
Run this locally to create and execute Portia plans
"""
from dotenv import load_dotenv
from portia import Portia, Config
from portia.plan import PlanBuilder
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

class DevOpsRecommendation(BaseModel):
    pipeline_name: str = Field(description="Name of the pipeline")
    status: str = Field(description="Current status")
    recommended_action: str = Field(description="Recommended action: retry, rollback, or escalate")
    reasoning: str = Field(description="Why this action is recommended")
    urgency: str = Field(description="Urgency level: low, medium, high, critical")

class PortiaDevOpsAssistant:
    def __init__(self):
        # Configure Portia with your API keys
        self.config = Config.from_default(
            llm_provider="google", 
            default_model="google/gemini-1.5-flash"
        )
        self.portia = Portia(config=self.config)
    
    def create_devops_analysis_plan(self, user_query):
        """Create a simple plan for DevOps pipeline analysis"""
        
        plan = PlanBuilder(
            f"DevOps Analysis: {user_query}"
        ).step(
            task="You are a DevOps AI Assistant helping newbie engineers. Analyze this query about CI/CD pipelines and provide beginner-friendly explanations and actionable recommendations.",
            tool_id="llm_tool",
            output="$devops_analysis"
        ).build()
        
        return plan
    
    def analyze_pipeline_issue(self, user_query: str):
        """Main method to analyze pipeline issues using Portia"""
        
        # Use simple run method instead of complex plan
        enhanced_query = f"""
        You are a DevOps AI Assistant helping newbie engineers.
        
        User Query: {user_query}
        
        Context: We have CI/CD pipelines that can fail. Help analyze the issue and recommend:
        - retry (for temporary issues like network timeouts)
        - rollback (for code-related problems)
        - escalate (for infrastructure issues)
        
        Provide beginner-friendly explanations without technical jargon.
        """
        
        plan_run = self.portia.run(enhanced_query)
        return plan_run.outputs.final_output
    
    def get_clarification(self, context: str):
        """Get clarification questions for user"""
        
        query = f"""
        Based on this pipeline issue context: {context}
        
        Ask appropriate clarification questions for a DevOps beginner. Focus on:
        1) How critical/urgent is this?
        2) Is it blocking other work?
        3) What action do they prefer?
        
        Provide clear options and explain each one in simple terms.
        """
        
        plan_run = self.portia.run(query)
        return plan_run.outputs.final_output
    
    def explain_for_beginner(self, technical_issue: str, recommended_action: str):
        """Convert technical information to beginner-friendly explanation"""
        
        explanation_plan = (
            PlanBuilderV2("Beginner-Friendly Explanation")
            .input(name="technical_issue", description="Technical description of the issue")
            .input(name="recommended_action", description="Recommended action to take")
            .llm_step(
                task="Convert this technical pipeline issue into beginner-friendly language. Explain: 1) What happened in simple terms, 2) Why it might have happened, 3) What the recommended action will do, 4) Why this solution makes sense. Use analogies and avoid jargon. Be encouraging.",
                inputs=[Input("technical_issue"), Input("recommended_action")],
                name="create_explanation"
            )
            .final_output()
            .build()
        )
        
        plan_run = self.portia.run_plan(
            explanation_plan,
            plan_run_inputs=[
                {"name": "technical_issue", "value": technical_issue},
                {"name": "recommended_action", "value": recommended_action}
            ]
        )
        
        return plan_run.outputs.final_output

# Global instance for use in frontend
devops_assistant = PortiaDevOpsAssistant()

# Test functions
def test_portia_integration():
    """Test the Portia integration"""
    
    print("🤖 Testing Portia DevOps Assistant")
    print("=" * 50)
    
    try:
        # Test pipeline analysis
        result = devops_assistant.analyze_pipeline_issue(
            "My backend deployment pipeline failed and I don't know what to do"
        )
        print(f"Analysis Result: {result}")
        
        # Test clarification
        clarification = devops_assistant.get_clarification(
            "Backend API pipeline failed at testing stage with database timeout"
        )
        print(f"Clarification: {clarification}")
        
        # Test beginner explanation
        explanation = devops_assistant.explain_for_beginner(
            "Database connection timeout after 300 seconds",
            "Retry the pipeline"
        )
        print(f"Beginner Explanation: {explanation}")
        
        print("\n✅ Portia integration working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your API keys are set in .env file")

if __name__ == "__main__":
    test_portia_integration()