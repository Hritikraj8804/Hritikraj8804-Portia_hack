#!/usr/bin/env python3
"""
Simple HTTP server for DevOps AI Assistant
Works with Python 3.13 without FastAPI compatibility issues
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_github_repositories():
    """Fetch real repositories from GitHub API"""
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Warning: GITHUB_TOKEN not found in .env file")
        return []
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        all_repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f'https://api.github.com/user/repos?page={page}&per_page={per_page}&sort=updated'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                repos = response.json()
                if not repos:
                    break
                
                for repo in repos:
                    all_repos.append({
                        "id": repo['id'],
                        "name": repo['name'],
                        "full_name": repo['full_name'],
                        "description": repo['description'],
                        "language": repo['language'],
                        "updated_at": repo['updated_at'],
                        "owner": repo['owner']['login']
                    })
                
                page += 1
                if len(all_repos) >= 1000:
                    break
            else:
                print(f"GitHub API error: {response.status_code}")
                break
        
        print(f"Fetched {len(all_repos)} repositories")
        return all_repos
        
    except Exception as e:
        print(f"Error fetching GitHub repos: {e}")
        return []

def get_github_workflows(owner, repo):
    """Fetch real GitHub Actions workflows"""
    print(f"DEBUG: get_github_workflows called with owner={owner}, repo={repo}")
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("No GitHub token found")
        return []
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # Get workflow runs with pagination
        url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs?per_page=50'
        print(f"Fetching workflows from: {url}")
        response = requests.get(url, headers=headers)
        
        print(f"GitHub API response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            runs = data.get('workflow_runs', [])
            print(f"Found {len(runs)} workflow runs")
            print(f"API response data keys: {list(data.keys())}")
            if runs:
                print(f"First run sample: {runs[0].get('name', 'No name')} - {runs[0].get('status', 'No status')}")
            
            pipelines = []
            
            for run in runs[:10]:  # Limit to 10 recent runs
                # Map GitHub status to our status
                if run['status'] == 'completed':
                    if run['conclusion'] == 'success':
                        status = 'success'
                    else:
                        status = 'failed'
                elif run['status'] in ['in_progress', 'queued']:
                    status = 'running'
                else:
                    status = 'unknown'
                
                pipeline = {
                    "id": str(run['id']),
                    "name": run['name'] or 'Workflow',
                    "status": status,
                    "stage": run['status'],
                    "last_run": run['created_at'],
                    "commit": run['head_sha'][:7] if run['head_sha'] else 'unknown',
                    "branch": run['head_branch'] or 'main'
                }
                
                # Add duration if completed
                if run['status'] == 'completed' and run['created_at'] and run['updated_at']:
                    try:
                        from datetime import datetime
                        start = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
                        end = datetime.fromisoformat(run['updated_at'].replace('Z', '+00:00'))
                        duration = end - start
                        minutes = int(duration.total_seconds() / 60)
                        seconds = int(duration.total_seconds() % 60)
                        pipeline['duration'] = f"{minutes}m {seconds}s"
                    except:
                        pipeline['duration'] = 'Unknown'
                
                # Add error for failed runs
                if run['conclusion'] in ['failure', 'cancelled', 'timed_out']:
                    pipeline['error'] = f"Workflow {run['conclusion']}: {run.get('display_title', 'Unknown error')}"
                
                pipelines.append(pipeline)
                print(f"Added pipeline: {pipeline['name']} - {pipeline['status']}")
            
            print(f"Returning {len(pipelines)} pipelines to frontend")
            return pipelines
        else:
            print(f"GitHub Actions API error: {response.status_code} - {response.text[:200]}")
            return []
    except Exception as e:
        print(f"Error fetching workflows: {e}")
        import traceback
        traceback.print_exc()
        return []

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse URL to separate path from query parameters
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.path)
        path = parsed.path
        query_params = parse_qs(parsed.query)
        
        print(f"DEBUG: Request path: {path}, query: {parsed.query}")
        
        if path == '/health':
            self.send_json({"status": "healthy", "timestamp": datetime.now().isoformat()})
        elif path == '/repositories':
            repos = get_github_repositories()
            self.send_json(repos)
        elif path == '/pipelines':
            owner = query_params.get('owner', [None])[0]
            name = query_params.get('name', [None])[0]
            
            print(f"DEBUG: Pipeline request - owner={owner}, name={name}")
            print(f"DEBUG: Full query string: {parsed.query}")
            if owner and name:
                print(f"DEBUG: Calling get_github_workflows({owner}, {name})")
                pipelines = get_github_workflows(owner, name)
                print(f"DEBUG: Got {len(pipelines)} pipelines from get_github_workflows")
                print(f"DEBUG: Pipelines data: {pipelines[:2] if pipelines else 'None'}")
                self.send_json(pipelines)
            else:
                print("DEBUG: No owner/name provided, returning empty list")
                self.send_json([])
        elif path.startswith('/pipelines/') and path.endswith('/logs'):
            pipeline_id = path.split('/')[2]
            logs = [
                "2024-01-15T11:15:00Z [INFO] Starting pipeline execution",
                "2024-01-15T11:15:30Z [INFO] Build stage completed", 
                "2024-01-15T11:16:00Z [ERROR] Test failed"
            ]
            self.send_json({"pipeline_id": pipeline_id, "logs": logs})
        elif path.startswith('/pipelines/'):
            # Handle individual pipeline requests
            pipeline_id = path.split('/')[2]
            print(f"DEBUG: Individual pipeline requested: {pipeline_id}")
            # Return mock pipeline data for individual requests
            mock_pipeline = {
                "id": pipeline_id,
                "name": f"Pipeline {pipeline_id}",
                "status": "success",
                "stage": "completed",
                "last_run": datetime.now().isoformat(),
                "commit": "abc123",
                "branch": "main"
            }
            self.send_json(mock_pipeline)
        else:
            self.send_json({"message": "DevOps Pipeline API", "version": "1.0.0"})
    
    def do_POST(self):
        if self.path == '/pipelines/action':
            # Check authorization header
            auth_header = self.headers.get('Authorization')
            if auth_header != 'Bearer demo-secure-token-123':
                self.send_error(401, "Unauthorized")
                return
                
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            response = {
                "success": True,
                "message": f"Action {data.get('action', 'unknown')} completed",
                "pipeline_id": data.get('pipeline_id'),
                "action": data.get('action'),
                "timestamp": datetime.now().isoformat()
            }
            self.send_json(response)
        else:
            self.send_error(404)
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error(self, code, message=None):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_data = {"error": message or "Error"}
        self.wfile.write(json.dumps(error_data).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

def run_server():
    server = HTTPServer(('localhost', 8000), APIHandler)
    print("🚀 Backend server running at http://localhost:8000")
    print("📚 Available endpoints:")
    print("  GET  /health")
    print("  GET  /repositories") 
    print("  GET  /pipelines")
    print("  POST /pipelines/action")
    print("\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    run_server()