"""
DevOps Clarification Agent - Handles user interactions and context gathering
"""
from dotenv import load_dotenv
from portia import Portia, Config
from portia.builder import PlanBuilderV2, StepOutput, Input
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

# Data models
class ClarificationResponse(BaseModel):
    question: str = Field(description="Question to ask the user")
    options: List[str] = Field(description="Available options for the user")
    reasoning: str = Field(description="Why this clarification is needed")

class UserContext(BaseModel):
    severity: str = Field(description="Issue severity: low, medium, high, critical")
    blocking_status: bool = Field(description="Whether issue is blocking other work")
    preferred_action: str = Field(description="User's preferred action")
    timeline: str = Field(description="When the issue needs to be resolved")

class ClarificationAgent:
    def __init__(self):
        self.config = Config.from_default(
            llm_provider="google", 
            default_model="google/gemini-1.5-flash"
        )
        self.portia = Portia(config=self.config)
    
    def create_clarification_plan(self):
        """Create a plan for gathering user clarifications"""
        
        plan = (
            PlanBuilderV2("DevOps Issue Clarification")
            .input(
                name="pipeline_issue",
                description="Description of the pipeline issue that needs clarification"
            )
            .input(
                name="user_experience_level", 
                description="User's DevOps experience level",
                default_value="beginner"
            )
            .llm_step(
                task="Based on the pipeline issue, generate appropriate clarification questions for a user with the specified experience level. Focus on severity, impact, and preferred resolution approach.",
                inputs=[Input("pipeline_issue"), Input("user_experience_level")],
                output_schema=ClarificationResponse,
                name="generate_clarification"
            )
            .final_output(
                output_schema=ClarificationResponse
            )
            .build()
        )
        
        return plan
    
    def get_clarification_questions(self, pipeline_issue: str, user_level: str = "beginner"):
        """Generate clarification questions based on the pipeline issue"""
        
        plan = self.create_clarification_plan()
        
        plan_run = self.portia.run_plan(
            plan,
            plan_run_inputs=[
                {"name": "pipeline_issue", "value": pipeline_issue},
                {"name": "user_experience_level", "value": user_level}
            ]
        )
        
        return plan_run.outputs.final_output
    
    def process_user_responses(self, responses: dict):
        """Process user responses and build context"""
        
        processing_plan = (
            PlanBuilderV2("Process User Context")
            .input(name="user_responses", description="User's responses to clarification questions")
            .llm_step(
                task="Analyze user responses and extract key context including severity, blocking status, preferred action, and timeline requirements",
                inputs=[Input("user_responses")],
                output_schema=UserContext,
                name="extract_context"
            )
            .final_output(
                output_schema=UserContext
            )
            .build()
        )
        
        plan_run = self.portia.run_plan(
            processing_plan,
            plan_run_inputs=[{"name": "user_responses", "value": str(responses)}]
        )
        
        return plan_run.outputs.final_output
    
    def generate_beginner_friendly_explanation(self, technical_issue: str, recommended_action: str):
        """Generate beginner-friendly explanations for technical issues"""
        
        explanation_plan = (
            PlanBuilderV2("Generate Beginner Explanation")
            .input(name="technical_issue", description="Technical description of the issue")
            .input(name="recommended_action", description="Recommended technical action")
            .llm_step(
                task="Convert technical pipeline issue and recommended action into beginner-friendly language. Explain what happened, why it happened, and what the recommended action will do. Avoid jargon and use analogies where helpful.",
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

# Predefined clarification templates for common scenarios
CLARIFICATION_TEMPLATES = {
    "severity_assessment": {
        "question": "How critical is this pipeline failure?",
        "options": [
            "🔴 Critical - Production is down or blocked",
            "🟡 High - Blocking important work or releases", 
            "🟢 Medium - Important but not immediately blocking",
            "⚪ Low - Can be addressed later"
        ],
        "follow_up": "This helps me prioritize the response and choose the right action."
    },
    
    "action_preference": {
        "question": "What would you like to do about this failed pipeline?",
        "options": [
            "🔄 Retry - Try running the pipeline again",
            "⏪ Rollback - Go back to the previous working version",
            "🚨 Escalate - Get help from the DevOps team",
            "🤔 Not sure - Help me decide"
        ],
        "follow_up": "I can explain what each option does if you're unsure."
    },
    
    "timeline_urgency": {
        "question": "When does this need to be resolved?",
        "options": [
            "⚡ Immediately - Right now",
            "🕐 Within 1 hour - Soon but not critical",
            "📅 Today - By end of business day",
            "📆 This week - No immediate rush"
        ],
        "follow_up": "This helps me recommend the most appropriate action."
    }
}

# Example usage
if __name__ == "__main__":
    agent = ClarificationAgent()
    
    print("🤖 DevOps Clarification Agent - User Interaction")
    print("=" * 50)
    
    # Example pipeline issue
    issue = "Backend API pipeline failed at testing stage with database connection timeout"
    
    # Get clarification questions
    clarification = agent.get_clarification_questions(issue, "beginner")
    print(f"Clarification: {clarification}")
    
    # Example user responses
    user_responses = {
        "severity": "high - blocking production release",
        "timeline": "needs to be fixed within 1 hour",
        "preference": "not sure what to do, need recommendation"
    }
    
    # Process responses
    context = agent.process_user_responses(user_responses)
    print(f"User Context: {context}")
    
    # Generate beginner explanation
    explanation = agent.generate_beginner_friendly_explanation(
        issue, 
        "retry the pipeline after checking database connectivity"
    )
    print(f"Beginner Explanation: {explanation}")