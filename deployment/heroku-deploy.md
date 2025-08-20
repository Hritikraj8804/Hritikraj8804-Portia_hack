# Heroku Deployment Guide

## Prerequisites
- Heroku CLI installed
- Git repository initialized
- Heroku account

## Backend Deployment

### 1. Create Heroku App
```bash
heroku create devops-assistant-api
```

### 2. Set Environment Variables
```bash
heroku config:set GOOGLE_API_KEY="your-google-api-key"
heroku config:set PORTIA_API_KEY="your-portia-api-key"
heroku config:set API_AUTH_TOKEN="your-secure-token"
```

### 3. Deploy Backend
```bash
# Copy Procfile to root
cp deployment/Procfile .

# Deploy
git add .
git commit -m "Deploy backend to Heroku"
git push heroku main
```

### 4. Verify Deployment
```bash
heroku open
# Should show API documentation
```

## Frontend Deployment (Streamlit Cloud)

### 1. Push to GitHub
```bash
git push origin main
```

### 2. Connect to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Connect your GitHub repository
3. Set main file: `frontend/app.py`
4. Add environment variables:
   - `API_BASE_URL`: Your Heroku app URL
   - `API_TOKEN`: Your auth token

### 3. Deploy
Streamlit Cloud will automatically deploy when you push to GitHub.

## Environment Variables for Production

### Backend (Heroku)
```
GOOGLE_API_KEY=your-google-api-key
PORTIA_API_KEY=your-portia-api-key
API_AUTH_TOKEN=secure-random-token
```

### Frontend (Streamlit Cloud)
```
API_BASE_URL=https://your-heroku-app.herokuapp.com
API_TOKEN=Bearer secure-random-token
```

## Monitoring and Logs

### Heroku Logs
```bash
heroku logs --tail
```

### Health Check
```bash
curl https://your-heroku-app.herokuapp.com/health
```

## Scaling
```bash
# Scale up
heroku ps:scale web=2

# Scale down
heroku ps:scale web=1
```