# 🔧 Troubleshooting Guide

Common issues and solutions for the DevOps AI Assistant.

## 🚨 Quick Fixes

### Application Won't Start
**Problem:** Error when running `quick-start.bat` or manual start commands

**Solutions:**
1. **Check Python version:**
   ```bash
   python --version  # Should be 3.11+
   ```

2. **Install/update dependencies:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Check if ports are available:**
   ```bash
   # Windows
   netstat -an | findstr :8000
   netstat -an | findstr :8501
   ```

4. **Restart with clean environment:**
   ```bash
   restart_backend.bat
   streamlit run frontend/app.py --server.port 8501
   ```

### "No repositories found" Error
**Problem:** Frontend shows no repositories available

**Solutions:**
1. **Check backend is running:**
   - Visit http://localhost:8000
   - Should show API information

2. **Verify GitHub token:**
   ```bash
   # Test your GitHub token
   curl -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/user
   ```

3. **Check .env file:**
   ```env
   GITHUB_TOKEN=ghp_your_token_here  # Must start with ghp_
   ```

4. **Test API endpoint:**
   ```bash
   curl http://localhost:8000/repositories
   ```

## 🔑 API Key Issues

### Google API Key Problems
**Symptoms:**
- "Invalid API key" errors
- Portia initialization failures

**Solutions:**
1. **Verify key format:**
   ```env
   GOOGLE_API_KEY=AIzaSy...  # Should start with AIzaSy
   ```

2. **Check API is enabled:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable "Generative AI API"
   - Verify billing is set up

3. **Test the key:**
   ```bash
   curl -X POST \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
   ```

### Portia API Key Problems
**Symptoms:**
- "Portia API key not configured"
- Timeout errors during chat

**Solutions:**
1. **Verify key format:**
   ```env
   PORTIA_API_KEY=prt-...  # Should start with prt-
   ```

2. **Check account status:**
   - Visit [Portia Labs](https://portialabs.ai)
   - Verify account is active
   - Check usage limits

3. **Test with fallback:**
   - Chat should work with fallback responses
   - Look for "Portia AI (Local Mode)" messages

### GitHub Token Problems
**Symptoms:**
- "403 Forbidden" errors
- Empty repository lists

**Solutions:**
1. **Check token permissions:**
   - Go to [GitHub Settings](https://github.com/settings/tokens)
   - Verify token has `repo` and `workflow` scopes

2. **Test token access:**
   ```bash
   curl -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/user/repos
   ```

3. **Regenerate if needed:**
   - Create new token with proper scopes
   - Update .env file immediately

## 🌐 Network and Connection Issues

### Backend Connection Errors
**Problem:** Frontend can't connect to backend

**Solutions:**
1. **Check backend is running:**
   ```bash
   # Should show process running on port 8000
   netstat -an | findstr :8000
   ```

2. **Restart backend:**
   ```bash
   # Kill existing process
   taskkill /f /im python.exe
   # Start fresh
   python backend/simple_backend.py
   ```

3. **Check firewall:**
   - Allow Python through Windows Firewall
   - Ensure ports 8000 and 8501 are open

### Portia Timeout Errors
**Problem:** Chat responses timeout or fail

**Solutions:**
1. **Check internet connection:**
   - Portia requires internet access
   - Test with: `ping api.portialabs.ai`

2. **Increase timeout:**
   - Wait longer for responses
   - Portia can take 30-60 seconds

3. **Use fallback mode:**
   - System automatically falls back to local responses
   - Look for "Local Mode" in chat responses

## 📊 Data and Display Issues

### Pipeline Data Not Loading
**Problem:** Selected repository shows no pipeline data

**Solutions:**
1. **Check repository has workflows:**
   - Go to GitHub repository
   - Look for `.github/workflows/` folder
   - Verify Actions are enabled

2. **Test API directly:**
   ```bash
   curl "http://localhost:8000/pipelines?owner=USERNAME&name=REPO"
   ```

3. **Check GitHub API limits:**
   - GitHub allows 5,000 requests/hour
   - Wait if limit exceeded

### Chat History Issues
**Problem:** Chat shows old conversations after changing repos

**Solutions:**
1. **Manual refresh:**
   - Click "← Back to Repos"
   - Select repository again

2. **Clear browser cache:**
   - Refresh page (F5)
   - Clear Streamlit cache

3. **Restart application:**
   - Stop both frontend and backend
   - Start fresh

## 🐛 Common Error Messages

### "ModuleNotFoundError"
**Error:** `ModuleNotFoundError: No module named 'portia'`

**Solution:**
```bash
pip install -r requirements.txt
# Or specifically:
pip install portia-sdk-python[google]
```

### "Pydantic Version Conflict"
**Error:** Pydantic compatibility issues

**Solution:**
```bash
pip install "pydantic>=2.11.5" --force-reinstall
```

### "Port already in use"
**Error:** `OSError: [WinError 10048] Only one usage of each socket address`

**Solution:**
```bash
# Kill processes using the ports
taskkill /f /im python.exe
# Or use different ports
streamlit run frontend/app.py --server.port 8502
```

### "SSL Certificate Error"
**Error:** SSL/TLS certificate verification errors

**Solution:**
```bash
# Temporary fix (not recommended for production)
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## 🔍 Debugging Steps

### Enable Debug Mode
1. **Backend debugging:**
   ```python
   # In simple_backend.py, add:
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Frontend debugging:**
   ```bash
   streamlit run frontend/app.py --logger.level debug
   ```

### Check Log Files
1. **Backend logs:**
   - Look for error messages in terminal
   - Check for API response codes

2. **Frontend logs:**
   - Check browser developer console
   - Look for network request failures

### Test Individual Components
1. **Test backend only:**
   ```bash
   python backend/simple_backend.py
   # Visit http://localhost:8000
   ```

2. **Test API endpoints:**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/repositories
   ```

3. **Test frontend only:**
   ```bash
   streamlit run frontend/app.py
   # Check if UI loads without backend
   ```

## 🆘 Getting Help

### Before Asking for Help
1. **Run the test suite:**
   ```bash
   python test_app.py
   ```

2. **Check all API keys are set:**
   ```bash
   # Windows
   type .env
   ```

3. **Verify system requirements:**
   - Python 3.11+
   - All dependencies installed
   - Internet connection available

### Where to Get Help
1. **Check existing issues:**
   - Search GitHub issues
   - Look for similar problems

2. **Create detailed issue:**
   - Include error messages
   - Provide system information
   - Share relevant logs

3. **Community resources:**
   - Project documentation
   - Stack Overflow
   - Discord/Slack communities

### Information to Include
When reporting issues, include:
- **Operating system** and version
- **Python version** (`python --version`)
- **Error messages** (full stack trace)
- **Steps to reproduce** the problem
- **Expected vs actual behavior**

## 📚 Related Documentation

- [Getting Started](GETTING_STARTED.md) - Initial setup
- [API Keys Setup](API_KEYS.md) - Obtaining API keys
- [User Guide](USER_GUIDE.md) - Using the application
- [FAQ](FAQ.md) - Frequently asked questions

---

**Still having issues?** Open an issue on GitHub with detailed information about your problem.