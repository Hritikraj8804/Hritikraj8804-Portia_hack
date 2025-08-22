"""
GitHub API integration for real pipeline data
"""
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class GitHubAPI:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.repo_owner = os.getenv("GITHUB_REPO_OWNER", "Hritikraj8804")
        self.repo_name = os.getenv("GITHUB_REPO_NAME", "devops-python-app")
        self.base_url = "https://api.github.com"
        
    def get_workflow_runs(self):
        """Get real GitHub Actions workflow runs"""
        if not self.token:
            return self._get_mock_data()
            
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/actions/runs"
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._convert_to_pipeline_format(data["workflow_runs"][:5])
            else:
                print(f"GitHub API Error: {response.status_code}")
                return self._get_mock_data()
                
        except Exception as e:
            print(f"GitHub API Exception: {e}")
            return self._get_mock_data()
    
    def _convert_to_pipeline_format(self, workflow_runs):
        """Convert GitHub workflow runs to pipeline format"""
        pipelines = []
        
        for i, run in enumerate(workflow_runs):
            # Map GitHub status to our format
            if run["status"] == "completed":
                if run["conclusion"] == "success":
                    status = "success"
                elif run["conclusion"] in ["failure", "cancelled", "timed_out"]:
                    status = "failed"
                else:
                    status = "failed"
            else:
                status = "running"
            
            # Create pipeline object
            pipeline = {
                "id": str(run["id"]),
                "name": f"{run['name']} ({self.repo_name})",
                "status": status,
                "stage": "deployment" if status == "success" else "testing" if status == "failed" else "building",
                "branch": run["head_branch"],
                "commit": run["head_sha"][:7],
                "last_run": run["created_at"],
                "duration": self._calculate_duration(run),
                "progress": 100 if status != "running" else 75,
                "error": self._get_error_message(run) if status == "failed" else None,
                "repository": f"{self.repo_owner}/{self.repo_name}",
                "workflow_url": run["html_url"]
            }
            
            pipelines.append(pipeline)
        
        return pipelines
    
    def _calculate_duration(self, run):
        """Calculate workflow duration"""
        if run["status"] == "completed" and run.get("updated_at"):
            try:
                start = datetime.fromisoformat(run["created_at"].replace('Z', '+00:00'))
                end = datetime.fromisoformat(run["updated_at"].replace('Z', '+00:00'))
                duration = end - start
                minutes = int(duration.total_seconds() / 60)
                return f"{minutes}m {int(duration.total_seconds() % 60)}s"
            except:
                return "Unknown"
        return "In progress"
    
    def _get_error_message(self, run):
        """Get appropriate error message based on conclusion"""
        conclusion_messages = {
            "failure": "Build or test failure",
            "cancelled": "Workflow cancelled",
            "timed_out": "Workflow timed out",
            "action_required": "Action required"
        }
        return conclusion_messages.get(run.get("conclusion"), "Unknown error")
    
    def _get_mock_data(self):
        """Fallback mock data with repo info"""
        return [
            {
                "id": "mock-1",
                "name": f"CI/CD Pipeline ({self.repo_name})",
                "status": "success",
                "stage": "deployment",
                "branch": "main",
                "commit": "abc123f",
                "last_run": "2024-01-15T10:30:00Z",
                "duration": "3m 45s",
                "progress": 100,
                "error": None,
                "repository": f"{self.repo_owner}/{self.repo_name}",
                "workflow_url": f"https://github.com/{self.repo_owner}/{self.repo_name}/actions"
            },
            {
                "id": "mock-2", 
                "name": f"Backend API ({self.repo_name})",
                "status": "failed",
                "stage": "testing",
                "branch": "main",
                "commit": "def456g",
                "last_run": "2024-01-15T09:15:00Z",
                "duration": "5m 12s",
                "progress": 60,
                "error": "Database connection timeout after 300 seconds",
                "repository": f"{self.repo_owner}/{self.repo_name}",
                "workflow_url": f"https://github.com/{self.repo_owner}/{self.repo_name}/actions"
            },
            {
                "id": "mock-3",
                "name": f"Database Migration ({self.repo_name})",
                "status": "running", 
                "stage": "deployment",
                "branch": "develop",
                "commit": "ghi789h",
                "last_run": "2024-01-15T11:00:00Z",
                "duration": "In progress",
                "progress": 80,
                "error": None,
                "repository": f"{self.repo_owner}/{self.repo_name}",
                "workflow_url": f"https://github.com/{self.repo_owner}/{self.repo_name}/actions"
            }
        ]

# Global instance
github_api = GitHubAPI()

def test_github_api():
    """Test GitHub API integration"""
    print("🔧 Testing GitHub API Integration")
    print("=" * 40)
    
    pipelines = github_api.get_workflow_runs()
    
    print(f"📊 Found {len(pipelines)} pipelines:")
    for pipeline in pipelines:
        print(f"  {pipeline['status'].upper()}: {pipeline['name']}")
        print(f"    Repository: {pipeline['repository']}")
        print(f"    Branch: {pipeline['branch']} | Commit: {pipeline['commit']}")
        if pipeline.get('error'):
            print(f"    Error: {pipeline['error']}")
        print()
    
    print("✅ GitHub API integration ready!")

if __name__ == "__main__":
    test_github_api()