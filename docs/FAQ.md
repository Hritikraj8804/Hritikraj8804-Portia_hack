# ❓ Frequently Asked Questions

Common questions about the DevOps AI Assistant.

## 🚀 General Questions

### What is the DevOps AI Assistant?
The DevOps AI Assistant is an intelligent tool that helps you monitor and manage CI/CD pipelines using AI. It connects to your GitHub repositories, displays real-time pipeline status, and provides AI-powered assistance through Portia for troubleshooting and optimization.

### What makes this different from other DevOps tools?
- **AI-Powered Insights** - Uses Portia AI for intelligent analysis
- **Real GitHub Integration** - Works with actual repository data
- **Context-Aware Chat** - AI understands your specific pipeline status
- **Easy Setup** - Simple installation and configuration
- **Open Source** - Free to use and modify

### Do I need to pay for anything?
The application itself is free and open source. However, you'll need API keys for:
- **Google API** - Free tier available, paid for heavy usage
- **Portia AI** - Check their pricing plans
- **GitHub** - Free for public repos, paid for private repos
- **Tavily** (optional) - Enhanced search capabilities

## 🔧 Setup and Installation

### What are the system requirements?
- **Python 3.11 or higher**
- **Windows, macOS, or Linux**
- **Internet connection** (for API calls)
- **4GB RAM minimum** (8GB recommended)
- **GitHub account** with repository access

### How long does setup take?
Typically 10-15 minutes:
- 2-3 minutes: Install dependencies
- 5-10 minutes: Get API keys
- 2-3 minutes: Configure and test

### Can I run this on macOS/Linux?
Yes! The application is cross-platform. Use these commands instead:
```bash
# Instead of quick-start.bat
python backend/simple_backend.py &
streamlit run frontend/app.py

# Instead of restart_backend.bat
pkill -f "simple_backend.py"
python backend/simple_backend.py &
```

### Do I need Docker?
No, Docker is not required. The application runs directly with Python and pip.

## 🔑 API Keys and Security

### Are my API keys safe?
Yes, when used properly:
- Keys are stored locally in `.env` file
- Never committed to version control
- Used only for legitimate API calls
- You control access and permissions

### Can I use this with private repositories?
Yes, if your GitHub token has appropriate permissions:
- Use `repo` scope for full private repo access
- Or `public_repo` scope for public repos only

### What if I don't have a Portia API key?
The application will work with fallback responses:
- Chat still functions with local intelligence
- Responses are context-aware but not AI-enhanced
- You can add Portia key later for full features

### How often should I rotate API keys?
**Recommended schedule:**
- **GitHub tokens** - Every 6 months
- **Google API keys** - Annually
- **Portia keys** - As per their recommendations
- **Immediately** if compromised

## 🔍 Features and Usage

### Which repositories can I monitor?
Any GitHub repository you have access to:
- **Public repositories** - With basic GitHub token
- **Private repositories** - With appropriate token permissions
- **Organization repos** - If you're a member

### How real-time is the data?
- **Pipeline status** - Updates every 30 seconds
- **Manual refresh** - Instant updates available
- **GitHub API limits** - May affect refresh frequency

### Can I monitor multiple repositories?
Yes, but one at a time in the current interface:
- Switch between repositories easily
- Chat history resets for each repository
- Each repo has independent monitoring

### What pipeline information is shown?
- **Status** - Success, failed, running
- **Metadata** - Branch, commit, timestamps
- **Logs** - Detailed execution information
- **Errors** - Failure reasons and debugging info

## 🤖 AI Assistant (Portia)

### What can I ask the AI assistant?
**Pipeline Questions:**
- "What's the current status?"
- "Why did the build fail?"
- "How many pipelines are running?"

**DevOps Advice:**
- "How to improve build performance?"
- "Best practices for CI/CD?"
- "Security recommendations?"

**Troubleshooting:**
- "How to fix this error?"
- "What's causing the failures?"
- "Debugging steps for [issue]?"

### How smart is the AI?
The AI is context-aware and can:
- Understand your specific repository and pipeline status
- Search the web for additional DevOps information
- Provide actionable recommendations
- Learn from conversation context

### Why do responses sometimes take long?
- **Portia processing** - AI agent management takes time
- **Web searches** - Tavily searches for additional context
- **Complex queries** - Detailed analysis requires more processing
- **API limits** - Rate limiting may cause delays

### Can I use it offline?
Partially:
- **Repository data** - Cached locally after first load
- **AI chat** - Requires internet for Portia API
- **Fallback mode** - Local responses when API unavailable

## 🔧 Technical Questions

### What technologies are used?
**Frontend:**
- Streamlit for web interface
- Python for data processing

**Backend:**
- Python HTTP server
- GitHub API integration
- Real-time data fetching

**AI:**
- Portia for agent management
- Google Gemini for language processing
- Tavily for web search

### Can I customize the interface?
Yes, the code is open source:
- Modify Streamlit components
- Add new features
- Change styling and layout
- Contribute improvements back

### How do I add new features?
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test thoroughly
5. Submit a pull request

### Is there an API I can use?
Yes! The backend provides REST API endpoints:
- `GET /repositories` - List repositories
- `GET /pipelines` - Get pipeline data
- `GET /pipelines/{id}/logs` - Get logs
- See [API Reference](API_REFERENCE.md) for details

## 🐛 Common Issues

### "No repositories found" - What's wrong?
Usually a GitHub token issue:
1. Check token is in `.env` file
2. Verify token has correct permissions
3. Test token with: `curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user`

### Chat responses are generic - Why?
Possible causes:
- Portia API key missing or invalid
- Network connectivity issues
- API rate limits reached
- Using fallback mode (still functional)

### Application is slow - How to improve?
**Performance tips:**
- Use status filters to reduce data load
- Refresh manually instead of auto-refresh
- Check internet connection speed
- Close other resource-intensive applications

### Can I run multiple instances?
Yes, but use different ports:
```bash
# Instance 1 (default)
python backend/simple_backend.py  # Port 8000
streamlit run frontend/app.py     # Port 8501

# Instance 2
python backend/simple_backend.py --port 8002
streamlit run frontend/app.py --server.port 8503
```

## 📊 Data and Privacy

### What data is collected?
The application only accesses:
- **GitHub repository metadata** (names, descriptions, languages)
- **Pipeline status and logs** (from GitHub Actions)
- **Your chat messages** (sent to Portia AI)

### Is my data stored anywhere?
- **Locally** - Temporary caching for performance
- **API providers** - Standard API usage logs
- **No permanent storage** - Data not saved long-term

### Can I use this in production?
The current version is designed for:
- **Development environments**
- **Personal projects**
- **Small team monitoring**

For production use, consider:
- Enhanced security measures
- Proper authentication
- Rate limiting and monitoring
- Data backup strategies

## 🆘 Getting More Help

### Where can I find more documentation?
- [Getting Started Guide](GETTING_STARTED.md)
- [User Guide](USER_GUIDE.md)
- [API Reference](API_REFERENCE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

### How do I report bugs?
1. Check [existing issues](https://github.com/your-repo/issues)
2. Create new issue with:
   - Clear description
   - Steps to reproduce
   - Error messages
   - System information

### Can I contribute to the project?
Absolutely! See our [Contributing Guide](CONTRIBUTING.md) for:
- Code contribution guidelines
- Development setup
- Pull request process
- Community guidelines

### Is there a community?
- **GitHub Discussions** - Ask questions and share ideas
- **Issues** - Report bugs and request features
- **Pull Requests** - Contribute code improvements

---

**Have a question not answered here?** Open an issue on GitHub or check our other documentation!