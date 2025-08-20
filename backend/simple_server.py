from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Mock pipeline data
PIPELINES = {
    "frontend-deploy": {
        "id": "frontend-deploy",
        "name": "Frontend Deployment",
        "status": "success",
        "stage": "deployment",
        "last_run": "2024-01-15T10:30:00Z",
        "duration": "5m 23s",
        "commit": "abc123f",
        "branch": "main"
    },
    "backend-api": {
        "id": "backend-api", 
        "name": "Backend API",
        "status": "failed",
        "stage": "testing",
        "last_run": "2024-01-15T11:15:00Z",
        "duration": "3m 45s",
        "commit": "def456g",
        "branch": "develop",
        "error": "Test timeout after 300s - Database connection failed"
    },
    "database-migration": {
        "id": "database-migration",
        "name": "Database Migration", 
        "status": "running",
        "stage": "migration",
        "last_run": "2024-01-15T11:45:00Z",
        "progress": 80,
        "commit": "ghi789h",
        "branch": "main"
    }
}

class APIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == "/":
            self.send_json({
                "message": "DevOps Pipeline API", 
                "version": "1.0.0",
                "endpoints": ["/health", "/pipelines"]
            })
        elif path == "/health":
            self.send_json({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "pipelines_count": len(PIPELINES)
            })
        elif path == "/pipelines":
            self.send_json(list(PIPELINES.values()))
        elif path.startswith("/pipelines/") and path.endswith("/logs"):
            pipeline_id = path.split("/")[2]
            if pipeline_id in PIPELINES:
                pipeline = PIPELINES[pipeline_id]
                if pipeline["status"] == "failed":
                    logs = [
                        "2024-01-15T11:15:00Z [INFO] Starting pipeline execution",
                        "2024-01-15T11:15:30Z [INFO] Build stage completed successfully", 
                        "2024-01-15T11:16:00Z [INFO] Starting test stage",
                        "2024-01-15T11:17:00Z [WARN] Database connection slow",
                        "2024-01-15T11:18:45Z [ERROR] Test timeout after 300s",
                        "2024-01-15T11:18:45Z [ERROR] Database connection failed",
                        "2024-01-15T11:18:45Z [ERROR] Pipeline failed at testing stage"
                    ]
                else:
                    logs = [
                        "2024-01-15T10:30:00Z [INFO] Starting pipeline execution",
                        "2024-01-15T10:32:00Z [INFO] Build stage completed successfully",
                        "2024-01-15T10:33:00Z [INFO] Test stage completed successfully", 
                        "2024-01-15T10:35:23Z [INFO] Deployment completed successfully"
                    ]
                self.send_json({"pipeline_id": pipeline_id, "logs": logs})
            else:
                self.send_error(404, "Pipeline not found")
        elif path.startswith("/pipelines/"):
            pipeline_id = path.split("/")[2]
            if pipeline_id in PIPELINES:
                self.send_json(PIPELINES[pipeline_id])
            else:
                self.send_error(404, "Pipeline not found")
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        if self.path == "/pipelines/action":
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    pipeline_id = data.get('pipeline_id')
                    action = data.get('action')
                    
                    if pipeline_id not in PIPELINES:
                        self.send_error(404, "Pipeline not found")
                        return
                    
                    pipeline = PIPELINES[pipeline_id]
                    timestamp = datetime.now().isoformat()
                    
                    if action == "retry":
                        pipeline["status"] = "running"
                        pipeline["stage"] = "testing"
                        pipeline["last_run"] = timestamp + "Z"
                        pipeline.pop("error", None)
                        message = f"Retry initiated for {pipeline['name']}"
                    elif action == "rollback":
                        pipeline["status"] = "success"
                        pipeline["stage"] = "deployment"
                        pipeline["commit"] = "previous-stable-commit"
                        pipeline["last_run"] = timestamp + "Z"
                        pipeline.pop("error", None)
                        message = f"Rollback completed for {pipeline['name']}"
                    elif action == "escalate":
                        message = f"Issue escalated to DevOps team for {pipeline['name']}"
                    else:
                        self.send_error(400, "Invalid action")
                        return
                    
                    response = {
                        "success": True,
                        "message": message,
                        "pipeline_id": pipeline_id,
                        "action": action,
                        "timestamp": timestamp
                    }
                    self.send_json(response)
                except json.JSONDecodeError:
                    self.send_error(400, "Invalid JSON")
            else:
                self.send_error(400, "No data provided")
        else:
            self.send_error(404, "Not found")
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {format % args}")

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8000), APIHandler)
    print("🚀 DevOps Pipeline API running on http://localhost:8000")
    print("📚 Endpoints: /health, /pipelines, /pipelines/{id}, /pipelines/action")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped")
        server.server_close()