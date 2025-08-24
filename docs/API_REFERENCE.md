# 🔌 API Reference

Complete reference for the DevOps AI Assistant backend API.

## 🌐 Base URL
```
http://localhost:8000
```

## 🔐 Authentication
Most endpoints require authentication using a bearer token:
```http
Authorization: Bearer demo-secure-token-123
```

## 📋 Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API information | ❌ |
| GET | `/health` | Health check | ❌ |
| GET | `/repositories` | List repositories | ❌ |
| GET | `/pipelines` | List pipelines | ❌ |
| GET | `/pipelines/{id}` | Get specific pipeline | ❌ |
| GET | `/pipelines/{id}/logs` | Get pipeline logs | ❌ |
| POST | `/pipelines/action` | Execute pipeline action | ✅ |

## 📖 Detailed Endpoint Documentation

### GET `/`
Get basic API information.

**Response:**
```json
{
  "message": "DevOps AI Assistant API",
  "version": "1.0.0",
  "status": "running"
}
```

### GET `/health`
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET `/repositories`
Get list of available GitHub repositories.

**Response:**
```json
[
  {
    "id": 123456789,
    "name": "my-awesome-project",
    "full_name": "username/my-awesome-project",
    "description": "An awesome project description",
    "language": "Python",
    "updated_at": "2024-01-15T10:30:00Z",
    "owner": "username"
  }
]
```

### GET `/pipelines`
Get list of pipelines, optionally filtered by repository.

**Query Parameters:**
- `owner` (optional) - Repository owner
- `name` (optional) - Repository name

**Example:**
```http
GET /pipelines?owner=username&name=my-project
```

**Response:**
```json
[
  {
    "id": "run_123456789",
    "name": "CI/CD Pipeline",
    "status": "success",
    "stage": "production",
    "branch": "main",
    "commit": "abc123def456",
    "last_run": "2024-01-15T10:30:00Z",
    "duration": "5m 23s",
    "progress": 100,
    "error": null
  },
  {
    "id": "run_987654321",
    "name": "Test Pipeline",
    "status": "failed",
    "stage": "testing",
    "branch": "feature/new-feature",
    "commit": "def456abc123",
    "last_run": "2024-01-15T09:15:00Z",
    "duration": "2m 45s",
    "progress": 75,
    "error": "Test suite failed: 3 tests failing"
  }
]
```

### GET `/pipelines/{id}`
Get details for a specific pipeline.

**Path Parameters:**
- `id` - Pipeline ID

**Response:**
```json
{
  "id": "run_123456789",
  "name": "CI/CD Pipeline",
  "status": "success",
  "stage": "production",
  "branch": "main",
  "commit": "abc123def456",
  "last_run": "2024-01-15T10:30:00Z",
  "duration": "5m 23s",
  "progress": 100,
  "error": null,
  "repository": {
    "name": "my-project",
    "owner": "username"
  }
}
```

### GET `/pipelines/{id}/logs`
Get execution logs for a specific pipeline.

**Path Parameters:**
- `id` - Pipeline ID

**Response:**
```json
{
  "pipeline_id": "run_123456789",
  "logs": [
    "[INFO] Workflow: CI/CD Pipeline",
    "[INFO] Status: completed - success",
    "[INFO] Started: 2024-01-15T10:25:00Z",
    "[INFO] Branch: main",
    "",
    "[JOB] Build and Test",
    "[INFO] Status: completed - success",
    "[INFO] Started: 2024-01-15T10:25:30Z",
    "[INFO] Completed: 2024-01-15T10:28:15Z",
    "  [STEP] Checkout code: success",
    "    Started: 2024-01-15T10:25:30Z",
    "    Completed: 2024-01-15T10:25:45Z",
    "  [STEP] Setup Python: success",
    "    Started: 2024-01-15T10:25:45Z",
    "    Completed: 2024-01-15T10:26:00Z",
    "  [STEP] Install dependencies: success",
    "    Started: 2024-01-15T10:26:00Z",
    "    Completed: 2024-01-15T10:27:30Z",
    "  [STEP] Run tests: success",
    "    Started: 2024-01-15T10:27:30Z",
    "    Completed: 2024-01-15T10:28:15Z"
  ]
}
```

### POST `/pipelines/action`
Execute an action on a pipeline (retry, rollback, escalate).

**Authentication:** Required

**Request Body:**
```json
{
  "pipeline_id": "run_123456789",
  "action": "retry",
  "reason": "Transient network error resolved"
}
```

**Available Actions:**
- `retry` - Retry a failed pipeline
- `rollback` - Rollback to previous version
- `escalate` - Escalate issue to team

**Response:**
```json
{
  "success": true,
  "message": "Pipeline retry initiated successfully",
  "action_id": "action_789123456",
  "pipeline_id": "run_123456789"
}
```

## 🔍 Pipeline Status Values

| Status | Description |
|--------|-------------|
| `success` | Pipeline completed successfully |
| `failed` | Pipeline failed with errors |
| `running` | Pipeline is currently executing |
| `pending` | Pipeline is queued for execution |
| `cancelled` | Pipeline was cancelled |

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing token |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

## 🚨 Error Responses

All error responses follow this format:
```json
{
  "error": true,
  "message": "Description of the error",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 📝 Usage Examples

### Python Example
```python
import requests

# Get repositories
response = requests.get('http://localhost:8000/repositories')
repos = response.json()

# Get pipelines for a specific repo
response = requests.get(
    'http://localhost:8000/pipelines',
    params={'owner': 'username', 'name': 'my-project'}
)
pipelines = response.json()

# Execute pipeline action
headers = {'Authorization': 'Bearer demo-secure-token-123'}
data = {
    'pipeline_id': 'run_123456789',
    'action': 'retry',
    'reason': 'Manual retry'
}
response = requests.post(
    'http://localhost:8000/pipelines/action',
    json=data,
    headers=headers
)
result = response.json()
```

### JavaScript Example
```javascript
// Get repositories
const repos = await fetch('http://localhost:8000/repositories')
  .then(res => res.json());

// Get pipelines
const pipelines = await fetch(
  'http://localhost:8000/pipelines?owner=username&name=my-project'
).then(res => res.json());

// Execute action
const result = await fetch('http://localhost:8000/pipelines/action', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer demo-secure-token-123',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    pipeline_id: 'run_123456789',
    action: 'retry',
    reason: 'Manual retry'
  })
}).then(res => res.json());
```

### cURL Examples
```bash
# Get repositories
curl http://localhost:8000/repositories

# Get pipelines for specific repo
curl "http://localhost:8000/pipelines?owner=username&name=my-project"

# Get pipeline logs
curl http://localhost:8000/pipelines/run_123456789/logs

# Execute pipeline action
curl -X POST http://localhost:8000/pipelines/action \
  -H "Authorization: Bearer demo-secure-token-123" \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline_id": "run_123456789",
    "action": "retry",
    "reason": "Manual retry"
  }'
```

## 🔧 Rate Limiting

The API implements basic rate limiting:
- **100 requests per minute** per IP address
- **Authenticated requests** have higher limits
- **429 Too Many Requests** returned when limit exceeded

## 📚 Integration Guide

### Frontend Integration
The Streamlit frontend uses these endpoints:
1. `GET /repositories` - Load repository list
2. `GET /pipelines` - Load pipeline data for selected repo
3. `GET /pipelines/{id}/logs` - Display pipeline logs

### Custom Integration
To integrate with your own frontend:
1. Start with `GET /repositories` to list available repos
2. Use `GET /pipelines` with repo filters to get pipeline data
3. Poll the pipelines endpoint for real-time updates
4. Use `GET /pipelines/{id}/logs` for detailed debugging

## 📖 Related Documentation

- [Getting Started](GETTING_STARTED.md) - Setup and installation
- [User Guide](USER_GUIDE.md) - Using the frontend interface
- [Troubleshooting](TROUBLESHOOTING.md) - Common API issues

---

**Need help?** Open an issue on GitHub or check our [FAQ](FAQ.md).