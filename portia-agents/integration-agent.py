"""
DevOps Integration Agent - Handles secure API communications with CI/CD systems
"""
from dotenv import load_dotenv
from portia import Portia, Config
from portia.tool import Tool, ToolRunContext
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import httpx
import os

load_dotenv()

# Custom tools for pipeline integration
class PipelineStatusSchema(BaseModel):
    api_url: str = Field(default="http://localhost:8000/pipelines", description="Pipeline API endpoint")

class PipelineActionSchema(BaseModel):
    pipeline_id: str = Field(..., description="ID of the pipeline")
    action: str = Field(..., description="Action: retry, rollback, or escalate")
    reason: Optional[str] = Field(None, description="Reason for the action")

class PipelineStatusTool(Tool[str]):
    """Tool to fetch pipeline status from CI/CD API"""
    
    id: str = "pipeline_status_tool"
    name: str = "Pipeline Status Tool"
    description: str = "Fetch current status of all CI/CD pipelines from the API"
    args_schema: type[BaseModel] = PipelineStatusSchema
    output_schema: tuple[str, str] = ("str", "JSON string containing pipeline status data")
    
    def run(self, context: ToolRunContext, api_url: str = "http://localhost:8000/pipelines") -> str:
        """Fetch pipeline status from API"""
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(api_url)
                response.raise_for_status()
                return response.text
        except httpx.RequestError as e:
            return f"Error connecting to pipeline API: {str(e)}"
        except httpx.HTTPStatusError as e:
            return f"Pipeline API error {e.response.status_code}: {e.response.text}"

class PipelineActionTool(Tool[str]):
    """Tool to execute actions on pipelines"""
    
    id: str = "pipeline_action_tool"
    name: str = "Pipeline Action Tool"
    description: str = "Execute actions (retry, rollback, escalate) on CI/CD pipelines"
    args_schema: type[BaseModel] = PipelineActionSchema
    output_schema: tuple[str, str] = ("str", "Result of the pipeline action")
    
    def run(self, context: ToolRunContext, pipeline_id: str, action: str, reason: Optional[str] = None) -> str:
        """Execute pipeline action"""
        if action not in ["retry", "rollback", "escalate"]:
            return f"Invalid action: {action}. Must be retry, rollback, or escalate"
        
        api_url = "http://localhost:8000/pipelines/action"
        auth_token = os.getenv("API_AUTH_TOKEN", "Bearer demo-secure-token-123")
        
        payload = {
            "pipeline_id": pipeline_id,
            "action": action,
            "reason": reason or f"Automated {action} via AI assistant"
        }
        
        headers = {
            "Authorization": auth_token,
            "Content-Type": "application/json"
        }
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(api_url, json=payload, headers=headers)
                response.raise_for_status()
                return response.text
        except httpx.RequestError as e:
            return f"Error executing pipeline action: {str(e)}"
        except httpx.HTTPStatusError as e:
            return f"Pipeline action failed {e.response.status_code}: {e.response.text}"

class PipelineLogsTool(Tool[str]):
    """Tool to fetch pipeline logs"""
    
    id: str = "pipeline_logs_tool"
    name: str = "Pipeline Logs Tool"
    description: str = "Fetch detailed logs from a specific pipeline"
    args_schema: type[BaseModel] = BaseModel
    output_schema: tuple[str, str] = ("str", "Pipeline logs as text")
    
    def run(self, context: ToolRunContext, pipeline_id: str) -> str:
        """Fetch pipeline logs"""
        api_url = f"http://localhost:8000/pipelines/{pipeline_id}/logs"
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(api_url)
                response.raise_for_status()
                return response.text
        except httpx.RequestError as e:
            return f"Error fetching pipeline logs: {str(e)}"
        except httpx.HTTPStatusError as e:
            return f"Failed to get logs {e.response.status_code}: {e.response.text}"

class IntegrationAgent:
    """Integration agent for secure API communications"""
    
    def __init__(self):
        self.config = Config.from_default(
            llm_provider="google", 
            default_model="google/gemini-1.5-flash"
        )
        
        # Create tool instances
        self.tools = [
            PipelineStatusTool(),
            PipelineActionTool(),
            PipelineLogsTool()
        ]
        
        self.portia = Portia(config=self.config, tools=self.tools)
    
    def get_pipeline_status(self, api_url: str = "http://localhost:8000/pipelines"):
        """Get pipeline status using AI agent with tools"""
        
        query = f"Check the status of all pipelines at {api_url} and provide a summary of any issues found"
        
        plan_run = self.portia.run(query)
        return plan_run.outputs.final_output
    
    def execute_pipeline_action(self, pipeline_id: str, action: str, reason: str = ""):
        """Execute pipeline action using AI agent with tools"""
        
        query = f"Execute {action} action on pipeline {pipeline_id} with reason: {reason}"
        
        plan_run = self.portia.run(query)
        return plan_run.outputs.final_output
    
    def analyze_pipeline_logs(self, pipeline_id: str):
        """Analyze pipeline logs using AI agent"""
        
        query = f"Get and analyze the logs for pipeline {pipeline_id}. Identify any errors or issues and suggest potential solutions."
        
        plan_run = self.portia.run(query)
        return plan_run.outputs.final_output
    
    def comprehensive_pipeline_analysis(self):
        """Perform comprehensive analysis of all pipelines"""
        
        query = """
        Perform a comprehensive analysis of all pipelines:
        1. Check the status of all pipelines
        2. For any failed pipelines, get their logs
        3. Analyze the errors and recommend appropriate actions
        4. Prioritize issues by severity and impact
        """
        
        plan_run = self.portia.run(query)
        return plan_run.outputs.final_output

# Security and authentication helpers
class APISecurityManager:
    """Manages secure API communications"""
    
    @staticmethod
    def get_auth_headers():
        """Get authentication headers for API calls"""
        token = os.getenv("API_AUTH_TOKEN", "Bearer demo-secure-token-123")
        return {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "DevOps-AI-Assistant/1.0"
        }
    
    @staticmethod
    def validate_api_response(response: httpx.Response) -> bool:
        """Validate API response for security"""
        # Check for common security headers
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options", 
            "X-XSS-Protection"
        ]
        
        # Log missing security headers (in production, use proper logging)
        missing_headers = [h for h in security_headers if h not in response.headers]
        if missing_headers:
            print(f"Warning: Missing security headers: {missing_headers}")
        
        return response.status_code < 400
    
    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize input data for API calls"""
        # Remove potentially dangerous characters
        dangerous_chars = ["<", ">", "&", "\"", "'", ";"]
        
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                for char in dangerous_chars:
                    value = value.replace(char, "")
            sanitized[key] = value
        
        return sanitized

# Example usage
if __name__ == "__main__":
    agent = IntegrationAgent()
    
    print("🔗 DevOps Integration Agent - API Communication")
    print("=" * 50)
    
    # Test pipeline status
    print("1. Checking pipeline status...")
    status = agent.get_pipeline_status()
    print(f"Status: {status}")
    
    print("\n2. Performing comprehensive analysis...")
    analysis = agent.comprehensive_pipeline_analysis()
    print(f"Analysis: {analysis}")
    
    # Test individual tools
    print("\n3. Testing individual tools...")
    status_tool = PipelineStatusTool()
    context = ToolRunContext()
    
    result = status_tool.run(context)
    print(f"Direct tool result: {result[:200]}...")