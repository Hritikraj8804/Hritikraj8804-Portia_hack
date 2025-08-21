# Portia Integration Guide

## Current Implementation
The project uses Portia SDK with `working_portia.py` for real AI responses.

## Test Integration
```bash
python working_portia.py
```

## Check Dashboard
View your plans at: https://app.portialabs.ai/dashboard/plan-runs

### 1. DevOps Execution Agent
- **File**: `portia-agents/devops-execution-agent.py`
- **Purpose**: Main pipeline analysis and recommendations
- **Description**: "DevOps pipeline analyzer that checks status and recommends actions"

### 2. DevOps Clarification Agent  
- **File**: `portia-agents/devops-clarification-agent.py`
- **Purpose**: User interaction and beginner-friendly explanations
- **Description**: "User interaction handler for DevOps troubleshooting"

### 3. DevOps Integration Agent
- **File**: `portia-agents/devops-integration-agent.py` 
- **Purpose**: API communication and data retrieval
- **Description**: "API integration manager for pipeline operations"

## Step 3: Configure Environment Variables
In Portia Labs dashboard, set these environment variables:

```
GOOGLE_API_KEY=your-google-api-key
API_BASE_URL=http://localhost:8000
API_AUTH_TOKEN=your-API_AUTH_TOKEN
```

## Step 4: Test Agents
1. Run a test query: "Check my pipeline status and help with any issues"
2. Verify agents can communicate with your local API
3. Test clarification flow with follow-up questions

## Step 5: Integration with Frontend
Once agents are working in Portia Labs:
1. Update frontend chat to call Portia agents
2. Replace rule-based responses with AI agent responses
3. Test end-to-end workflow

## Troubleshooting
- **Agent upload fails**: Check file format and syntax
- **API connection issues**: Ensure local server is running
- **Authentication errors**: Verify API keys are correct
- **No responses**: Check agent logs in Portia dashboard

## Success Criteria
✅ All 3 agents uploaded successfully  
✅ Agents can access local API at localhost:8000  
✅ Test queries return intelligent responses  
✅ Clarification flow works properly  
✅ Frontend integration complete