# 🔑 API Keys Setup Guide

This guide will help you obtain all the necessary API keys to run the DevOps AI Assistant.

## 🎯 Required API Keys

### 1. Google API Key (Required)
**Used for:** Portia AI's language model backend

**How to get it:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Generative AI API**
4. Go to **APIs & Services** → **Credentials**
5. Click **Create Credentials** → **API Key**
6. Copy your API key

**Add to .env:**
```env
GOOGLE_API_KEY=AIzaSy...your_key_here
```

### 2. Portia API Key (Required)
**Used for:** AI agent management and orchestration

**How to get it:**
1. Visit [Portia Labs](https://portialabs.ai)
2. Sign up for an account
3. Navigate to your dashboard
4. Generate an API key
5. Copy the key (starts with `prt-`)

**Add to .env:**
```env
PORTIA_API_KEY=prt-...your_key_here
```

### 3. GitHub Token (Required)
**Used for:** Accessing repository and pipeline data

**How to get it:**
1. Go to [GitHub Settings](https://github.com/settings/tokens)
2. Click **Generate new token** → **Generate new token (classic)**
3. Give it a descriptive name (e.g., "DevOps AI Assistant")
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `read:org` (Read org and team membership)
5. Click **Generate token**
6. Copy the token immediately (you won't see it again!)

**Add to .env:**
```env
GITHUB_TOKEN=ghp_...your_token_here
```

## 🚀 Optional API Keys (Enhanced Features)

### 4. Tavily API Key (Optional)
**Used for:** Enhanced web search capabilities in AI responses

**How to get it:**
1. Visit [Tavily](https://tavily.com)
2. Sign up for an account
3. Get your API key from the dashboard
4. Copy the key

**Add to .env:**
```env
TAVILY_API_KEY=tvly-...your_key_here
```

### 5. Hugging Face Token (Optional)
**Used for:** Additional AI model capabilities

**How to get it:**
1. Go to [Hugging Face](https://huggingface.co)
2. Create an account and log in
3. Go to **Settings** → **Access Tokens**
4. Create a new token with **Read** permissions
5. Copy the token

**Add to .env:**
```env
HF_TOKEN=hf_...your_token_here
```

## 🔒 Security Best Practices

### Keep Your Keys Safe
- ✅ Never commit `.env` file to version control
- ✅ Use different keys for development and production
- ✅ Regularly rotate your API keys
- ✅ Set appropriate permissions/scopes

### GitHub Token Permissions
For security, only grant minimum required permissions:
- **Public repos only?** Use `public_repo` scope instead of `repo`
- **Read-only access?** Consider using fine-grained tokens

### Rate Limits
Be aware of API rate limits:
- **GitHub:** 5,000 requests/hour for authenticated requests
- **Google:** Varies by service and billing plan
- **Portia:** Check your plan limits

## 🆘 Troubleshooting

### Common Issues

**"Invalid API key" errors:**
- Double-check the key is copied correctly
- Ensure no extra spaces or characters
- Verify the key hasn't expired

**GitHub "403 Forbidden" errors:**
- Check token permissions/scopes
- Verify token hasn't expired
- Ensure you have access to the repositories

**Portia timeout errors:**
- Check your Portia account status
- Verify API key is active
- Try again later (service might be busy)

### Testing Your Keys
Run the test script to verify all keys work:
```bash
python test_app.py
```

## 📚 Next Steps

Once you have your API keys set up:
1. [Return to Getting Started Guide](GETTING_STARTED.md#step-4-test-your-setup)
2. [Learn how to use the application](USER_GUIDE.md)

---

**Need help?** Check our [Troubleshooting Guide](TROUBLESHOOTING.md) or open an issue on GitHub.