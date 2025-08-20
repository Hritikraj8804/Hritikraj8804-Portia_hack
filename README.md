# DevOps Onboarding & Troubleshooting AI Assistant

A comprehensive AI assistant built on Portia Labs platform to help newbie DevOps engineers with CI/CD pipeline management, troubleshooting, and intelligent decision-making.

## 🎯 Project Overview

This hackathon project creates an interactive DevOps assistant that:
- Checks CI/CD pipeline status in real-time
- Provides intelligent troubleshooting guidance
- Suggests appropriate actions (retry, rollback, escalate)
- Uses Portia's multi-agent system for structured workflows
- Includes a Streamlit frontend for visualization

## 🏗️ Architecture

### Multi-Agent System
- **Execution Agent**: Orchestrates pipeline operations and decision-making
- **Clarification Agent**: Handles user interactions and context gathering
- **Integration Agent**: Manages secure API communications with CI/CD systems
- **Logging Agent**: Tracks all interactions and maintains audit trails
- **Notification Agent**: Sends alerts and manages escalations

### Technology Stack
- **Backend**: FastAPI with Python 3.11
- **Frontend**: Streamlit for visualization and interaction
- **AI Platform**: Portia Labs multi-agent system
- **Deployment**: Heroku + Portia Cloud

## 📋 4-Day Development Plan (2 hours/day)

### Day 1: Foundation & Backend (2 hours)
**Milestone**: Core infrastructure ready
- Set up FastAPI backend with mock CI/CD data (45 min)
- Create basic endpoints for pipeline status, actions (45 min)
- Design multi-agent workflow architecture (30 min)

**Deliverables**:
- Working FastAPI server with mock data
- API documentation
- Multi-agent interaction diagram

### Day 2: Portia Integration (2 hours)
**Milestone**: AI agents configured and working
- Create Portia agent configurations (60 min)
- Implement clarification scripts and user flows (45 min)
- Test basic agent interactions (15 min)

**Deliverables**:
- Portia agent plan files
- Clarification dialogue samples
- Basic workflow testing

### Day 3: Frontend & Enhancement (2 hours)
**Milestone**: Complete user interface
- Build Streamlit frontend with pipeline visualization (60 min)
- Integrate frontend with Portia agents (45 min)
- Add authentication and security (15 min)

**Deliverables**:
- Interactive Streamlit dashboard
- Secure API integration
- End-to-end workflow testing

### Day 4: Deployment & Polish (2 hours)
**Milestone**: Production-ready MVP
- Deploy backend to Heroku (30 min)
- Deploy Portia agents to cloud (30 min)
- Deploy Streamlit frontend (30 min)
- Final testing and demo preparation (30 min)

**Deliverables**:
- Deployed application
- Complete documentation
- Demo-ready system

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Portia Labs account
- OpenAI or Google API key

### Setup
```bash
# 1. Clone and setup
git clone <repo>
cd portia

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Add your API keys to .env

# 4. Start backend
python backend/main.py

# 5. Start frontend (new terminal)
streamlit run frontend/app.py

# 6. Upload agents to Portia Labs
# Upload files from portia-agents/ to your Portia dashboard
```

### Usage Flow
1. **Access Dashboard**: Open Streamlit app at http://localhost:8501
2. **Check Pipelines**: View real-time pipeline status
3. **Get Assistance**: Chat with AI assistant for troubleshooting
4. **Take Actions**: Execute recommended actions (retry/rollback/escalate)
5. **Monitor Results**: Track outcomes and logs

## 🤖 Multi-Agent Workflow

### Typical Conversation Flow
```
User: "Check my deployment pipeline status"
↓
Execution Agent → Integration Agent: Fetch pipeline data
↓
Integration Agent: Calls API, returns status with failures
↓
Execution Agent → Clarification Agent: Pipeline failed, need user input
↓
Clarification Agent → User: "Pipeline failed at testing. Is this blocking production?"
↓
User: "Yes, it's critical"
↓
Clarification Agent → Execution Agent: High priority, blocking issue
↓
Execution Agent: Evaluates options (retry/rollback/escalate)
↓
Clarification Agent → User: "I recommend retry first, then escalate if it fails again"
↓
User: "Proceed with retry"
↓
Execution Agent → Integration Agent: Execute retry
↓
Logging Agent: Records all interactions
↓
Notification Agent: Confirms action and monitors progress
```

## 📁 Project Structure
```
portia/
├── backend/              # FastAPI backend
│   ├── main.py          # API server
│   ├── models.py        # Data models
│   └── requirements.txt # Backend dependencies
├── frontend/            # Streamlit frontend
│   ├── app.py          # Main dashboard
│   ├── components/     # UI components
│   └── utils.py        # Helper functions
├── portia-agents/       # Portia agent configurations
│   ├── execution-agent.py
│   ├── clarification-agent.py
│   ├── integration-agent.py
│   ├── logging-agent.py
│   └── notification-agent.py
├── deployment/          # Deployment configurations
├── docs/               # Documentation
├── .env.example        # Environment template
└── requirements.txt    # Main dependencies
```

## 🔧 API Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /pipelines` - All pipeline statuses
- `GET /pipelines/{id}` - Specific pipeline
- `POST /pipelines/action` - Execute actions
- `GET /pipelines/{id}/logs` - Pipeline logs

## 🎨 Frontend Features
- **Dashboard**: Real-time pipeline status visualization
- **Chat Interface**: Interactive AI assistant
- **Action Panel**: Execute pipeline actions
- **Logs Viewer**: Detailed pipeline logs
- **History**: Track all interactions and decisions

## 🚀 Deployment

### Backend (Heroku)
```bash
heroku create devops-assistant-api
heroku config:set PORTIA_API_KEY="your-key"
git subtree push --prefix backend heroku main
```

### Frontend (Streamlit Cloud)
1. Connect GitHub repo to Streamlit Cloud
2. Set environment variables
3. Deploy automatically

### Portia Agents
1. Upload agent files to Portia Labs dashboard
2. Configure environment variables
3. Test agent interactions

## 🔒 Security Features
- API key authentication
- Input validation
- Rate limiting
- Secure credential storage
- Audit logging

## 📊 Monitoring & Analytics
- Pipeline status tracking
- User interaction analytics
- Agent performance metrics
- Error rate monitoring
- Escalation effectiveness

## 🎯 Demo Script
1. Show pipeline dashboard with mixed statuses
2. Demonstrate AI assistant troubleshooting
3. Execute retry action through chat
4. Show escalation workflow
5. Display comprehensive logging

## 🤝 Contributing
This is a hackathon project. Focus on MVP functionality and clear documentation for judges and users.

## 📄 License
MIT License - Built for hackathon demonstration.