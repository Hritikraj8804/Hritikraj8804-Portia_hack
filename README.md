# DevOps AI Assistant - Hackathon MVP

A streamlined DevOps assistant for CI/CD pipeline management and troubleshooting, built for hackathon demonstration.

## 🎯 Project Overview

This hackathon MVP provides:
- **Real-time Pipeline Monitoring** - View status of all CI/CD pipelines
- **Intelligent Actions** - Retry, rollback, and escalate failed pipelines
- **Repository Selection** - Choose which repository to monitor
- **Simple AI Chat** - Basic troubleshooting assistance
- **Comprehensive Logging** - Full error tracking and analysis

## 🏗️ Architecture

### Simplified Stack
- **Backend**: Python HTTP server with real GitHub data
- **Frontend**: Streamlit dashboard
- **Logging**: Centralized logging system
- **Testing**: Automated test suite

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Setup & Run
```bash
# 1. Clone and navigate
cd portia

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Run tests (recommended)
python test_app.py

# 5. Start both services (one-click)
quick-start.bat

# OR manually:
# Terminal 1: python backend/simple_backend.py
# Terminal 2: streamlit run frontend/app.py
```

### Access
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure
```
portia/
├── backend/
│   └── simple_backend.py   # HTTP server with real GitHub data
├── frontend/
│   └── app.py              # Streamlit dashboard
├── logs/                   # Application logs (auto-created)
├── test_app.py            # Comprehensive test suite
├── logger.py              # Centralized logging system
├── quick-start.bat        # One-click startup script
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

## 🧪 Testing

Run the test suite before starting:
```bash
python test_app.py
```

Tests verify:
- ✅ Backend API endpoints
- ✅ Frontend dependencies
- ✅ Environment configuration
- ✅ Pipeline actions
- ✅ Error handling

## 📊 Features

### Dashboard
- **Repository Selection** - Choose from available repositories
- **Pipeline Status** - Real-time status of all pipelines
- **Health Metrics** - Success/failure counts and health score
- **Quick Actions** - Bulk retry, export reports, deploy

### Pipeline Management
- **Individual Actions** - Retry, rollback, escalate per pipeline
- **Detailed Logs** - View execution logs for troubleshooting
- **Status Filtering** - Filter by success/failed/running
- **Progress Tracking** - Real-time progress for running pipelines

### AI Assistant
- **Status Queries** - Ask about system health
- **Quick Commands** - Simple troubleshooting assistance
- **Help System** - Available commands and guidance

## 🔧 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /repositories` - Available repositories
- `GET /pipelines` - All pipeline statuses
- `GET /pipelines/{id}` - Specific pipeline
- `POST /pipelines/action` - Execute actions (retry/rollback/escalate)
- `GET /pipelines/{id}/logs` - Pipeline logs

## 📝 Logging

All activities are logged to `logs/` directory:
- **app.log** - General application logs
- **api.log** - Backend API logs  
- **frontend.log** - Frontend interaction logs

Log files rotate automatically (10MB max, 5 backups).

## 🎨 Demo Flow

1. **Start Application** - Run backend and frontend
2. **Select Repository** - Choose from available repos
3. **View Dashboard** - See pipeline status and metrics
4. **Handle Failures** - Use retry/rollback actions
5. **Check Logs** - View detailed execution logs
6. **AI Assistance** - Ask status questions

## 🔒 Security

- API token authentication
- Input validation
- Error handling
- Secure credential storage

## 🚀 Deployment

For hackathon demo:
1. Ensure all tests pass
2. Start both backend and frontend
3. Demo repository selection
4. Show pipeline actions
5. Demonstrate AI assistant

## 📄 License

MIT License - Built for hackathon demonstration.

---

**Hackathon Ready** ✅ - Simplified, tested, and optimized for demo presentation.