"""
DevOps Execution Agent - Primary orchestrator for pipeline operations
"""
from dotenv import load_dotenv
from portia import Portia, Config
from portia.builder import PlanBuilderV2, StepOutput, Input
from pydantic import BaseModel, Field
from typing import List, Optional
import httpx

load_dotenv()

# Data models
class PipelineStatus(BaseModel):
    id: str
    name: str
    status: str
    stage: str
    error: Optional[str] = None

class DevOpsRecommendation(BaseModel):
    pipeline_id: str = Field(description="ID of the pipeline with issues")
    current_status: str = Field(description="Current status of the pipeline")
    recommended_action: str = Field(description="Recommended action: retry, rollback, or escalate")
    reasoning: str = Field(description="Detailed reasoning for the recommendation")
    urgency_level: str = Field(description="Urgency: low, medium, high, critical")

class ExecutionAgent:
    def __init__(self):
        self.config = Config.from_default(
            llm_provider="google", 
            default_model="google/gemini-1.5-flash"
        )
        self.portia = Portia(config=self.config)
    
    def create_pipeline_analysis_plan(self):
        """Create a plan for analyzing pipeline status and providing recommendations"""
        
        plan = (
            PlanBuilderV2("DevOps Pipeline Analysis and Recommendation")
            .input(
                name="api_endpoint",
                description="API endpoint to check pipeline status",
                default_value="http://localhost:8000/pipelines"
            )
            .llm_step(
                task="Fetch and analyze pipeline status from the API endpoint. Identify any failed pipelines and their error details.",
                inputs=[Input("api_endpoint")],
                name="analyze_pipelines"
            )
            .if_(
                condition="Any pipelines have failed status",
                args={"pipeline_data": StepOutput("analyze_pipelines")}
            )
            .llm_step(
                task="For failed pipelines, analyze the error messages and recommend appropriate actions (retry for temporary issues, rollback for code problems, escalate for infrastructure issues). Consider urgency based on pipeline importance.",
                inputs=[StepOutput("analyze_pipelines")],
                output_schema=DevOpsRecommendation,
                name="generate_recommendation"
            )
            .else_()
            .function_step(
                function=lambda: {"message": "All pipelines are healthy - no action needed"},
                name="all_healthy"
            )
            .endif()
            .final_output(
                output_schema=DevOpsRecommendation
            )
            .build()
        )
        
        return plan
    
    def analyze_pipeline_status(self, api_endpoint="http://localhost:8000/pipelines"):
        """Main method to analyze pipeline status and provide recommendations"""
        
        plan = self.create_pipeline_analysis_plan()
        
        # Execute the plan
        plan_run = self.portia.run_plan(
            plan, 
            plan_run_inputs=[{"name": "api_endpoint", "value": api_endpoint}]
        )
        
        return plan_run.outputs.final_output
    
    def execute_pipeline_action(self, pipeline_id: str, action: str, reason: str = ""):
        """Execute a pipeline action (retry, rollback, escalate)"""
        
        action_plan = (
            PlanBuilderV2("Execute Pipeline Action")
            .input(name="pipeline_id", description="Pipeline ID to act on")
            .input(name="action", description="Action to execute")
            .input(name="reason", description="Reason for action")
            .llm_step(
                task="Execute the specified action on the pipeline and confirm the result",
                inputs=[Input("pipeline_id"), Input("action"), Input("reason")],
                name="execute_action"
            )
            .final_output()
            .build()
        )
        
        plan_run = self.portia.run_plan(
            action_plan,
            plan_run_inputs=[
                {"name": "pipeline_id", "value": pipeline_id},
                {"name": "action", "value": action},
                {"name": "reason", "value": reason}
            ]
        )
        
        return plan_run.outputs.final_output

# Example usage
if __name__ == "__main__":
    agent = ExecutionAgent()
    
    print("🚀 DevOps Execution Agent - Pipeline Analysis")
    print("=" * 50)
    
    # Analyze current pipeline status
    result = agent.analyze_pipeline_status()
    print(f"Analysis Result: {result}")
    
    # Example action execution
    if hasattr(result, 'pipeline_id') and hasattr(result, 'recommended_action'):
        print(f"\nExecuting recommended action: {result.recommended_action}")
        action_result = agent.execute_pipeline_action(
            result.pipeline_id, 
            result.recommended_action,
            "Automated action based on AI recommendation"
        )
        print(f"Action Result: {action_result}")