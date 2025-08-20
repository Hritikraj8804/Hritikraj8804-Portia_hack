from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="DevOps Pipeline API", version="1.0.0")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "https://*.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Models
class PipelineStatus(BaseModel):
    id: str
    name: str
    status: str
    stage: str
    last_run: str
    duration: Optional[str] = None
    progress: Optional[int] = None
    commit: str
    branch: str
    error: Optional[str] = None

class ActionRequest(BaseModel):
    pipeline_id: str
    action: str  # retry, rollback, escalate
    reason: Optional[str] = None

class ActionResponse(BaseModel):
    success: bool
    message: str
    pipeline_id: str
    action: str
    timestamp: str

# Simple auth check
def verify_token(authorization: Optional[str] = Header(None)):
    if authorization != "Bearer demo-secure-token-123":
        raise HTTPException(status_code=401, detail="Invalid token")
    return authorization

@app.get("/")
def root():
    return {
        "message": "DevOps Pipeline API", 
        "version": "1.0.0",
        "endpoints": ["/health", "/pipelines", "/pipelines/{id}", "/pipelines/action"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "pipelines_count": len(PIPELINES)
    }

@app.get("/pipelines", response_model=List[PipelineStatus])
def get_all_pipelines():
    return list(PIPELINES.values())

@app.get("/pipelines/{pipeline_id}", response_model=PipelineStatus)
def get_pipeline(pipeline_id: str):
    if pipeline_id not in PIPELINES:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return PIPELINES[pipeline_id]

@app.post("/pipelines/action", response_model=ActionResponse)
def execute_action(request: ActionRequest, token: str = Depends(verify_token)):
    if request.pipeline_id not in PIPELINES:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    pipeline = PIPELINES[request.pipeline_id]
    timestamp = datetime.now().isoformat()
    
    if request.action == "retry":
        pipeline["status"] = "running"
        pipeline["stage"] = "testing"
        pipeline["last_run"] = timestamp + "Z"
        pipeline.pop("error", None)
        message = f"Retry initiated for {pipeline['name']}"
        
    elif request.action == "rollback":
        pipeline["status"] = "success"
        pipeline["stage"] = "deployment"
        pipeline["commit"] = "previous-stable-commit"
        pipeline["last_run"] = timestamp + "Z"
        pipeline.pop("error", None)
        message = f"Rollback completed for {pipeline['name']}"
        
    elif request.action == "escalate":
        message = f"Issue escalated to DevOps team for {pipeline['name']}"
        
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use: retry, rollback, escalate")
    
    return ActionResponse(
        success=True,
        message=message,
        pipeline_id=request.pipeline_id,
        action=request.action,
        timestamp=timestamp
    )

@app.get("/pipelines/{pipeline_id}/logs")
def get_pipeline_logs(pipeline_id: str):
    if pipeline_id not in PIPELINES:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
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
    elif pipeline["status"] == "running":
        logs = [
            "2024-01-15T11:45:00Z [INFO] Starting pipeline execution",
            "2024-01-15T11:46:00Z [INFO] Build stage completed successfully",
            "2024-01-15T11:47:00Z [INFO] Migration stage in progress...",
            "2024-01-15T11:48:00Z [INFO] 80% complete - applying schema changes"
        ]
    else:
        logs = [
            "2024-01-15T10:30:00Z [INFO] Starting pipeline execution",
            "2024-01-15T10:32:00Z [INFO] Build stage completed successfully",
            "2024-01-15T10:33:00Z [INFO] Test stage completed successfully", 
            "2024-01-15T10:35:23Z [INFO] Deployment completed successfully"
        ]
    
    return {"pipeline_id": pipeline_id, "logs": logs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)