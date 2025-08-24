# 🚀 Getting Started with DevOps AI Assistant

Welcome to the DevOps AI Assistant! This guide will help you set up and run the project in just a few minutes.

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.11+** installed on your system
- **Git** for cloning the repository
- A **GitHub account** (for accessing repository data)
- **API keys** (we'll help you get these)

## 🔧 Step-by-Step Setup

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd portia
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up API Keys
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` file in your text editor and add your API keys:
   ```env
   # Required API Keys
   GOOGLE_API_KEY=your_google_api_key_here
   PORTIA_API_KEY=your_portia_api_key_here
   GITHUB_TOKEN=your_github_token_here
   
   # Optional (for enhanced features)
   TAVILY_API_KEY=your_tavily_api_key_here
   HF_TOKEN=your_huggingface_token_here
   ```

   **Need help getting API keys?** → [API Keys Setup Guide](API_KEYS.md)

### Step 4: Test Your Setup
```bash
python test_app.py
```
If all tests pass ✅, you're ready to go!

### Step 5: Start the Application

**Option A: One-Click Start (Windows)**
```bash
quick-start.bat
```

**Option B: Manual Start**
```bash
# Terminal 1 - Start Backend
python backend/simple_backend.py

# Terminal 2 - Start Frontend
streamlit run frontend/app.py
```

### Step 6: Access the Application
- **Frontend Dashboard**: http://localhost:8501
- **Backend API**: http://localhost:8000

## 🎯 First Steps

1. **Select a Repository** - Choose from available GitHub repositories
2. **View Pipeline Status** - See real-time CI/CD pipeline information
3. **Chat with Portia AI** - Ask questions about your DevOps setup
4. **Explore Logs** - View detailed pipeline execution logs

## 📚 Next Steps

- [Understanding the Interface](USER_GUIDE.md) - Learn how to use all features
- [API Documentation](API_REFERENCE.md) - Explore backend endpoints
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [Contributing](CONTRIBUTING.md) - Help improve the project

## 🆘 Need Help?

- Check our [Troubleshooting Guide](TROUBLESHOOTING.md)
- Review [Frequently Asked Questions](FAQ.md)
- Open an issue on GitHub

---

**Ready to explore DevOps with AI?** 🚀 [Start using the application →](USER_GUIDE.md)