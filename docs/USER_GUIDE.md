# 📖 User Guide - DevOps AI Assistant

Learn how to use all the features of the DevOps AI Assistant effectively.

## 🏠 Dashboard Overview

When you first open the application at http://localhost:8501, you'll see:

### Main Interface Components
- **Header** - Project title and description
- **Repository Selection** - Browse and select GitHub repositories
- **Pipeline Dashboard** - View CI/CD pipeline status
- **AI Chat** - Interact with Portia AI assistant
- **Sidebar Controls** - Filters and refresh options

## 📋 Repository Selection

### Browsing Repositories
1. **Search** - Use the search bar to find specific repositories
2. **Pagination** - Navigate through multiple pages of repositories
3. **Repository Cards** - Each card shows:
   - Repository name and description
   - Programming language
   - Last update date

### Selecting a Repository
- Click the **🚀 Monitor [Repo Name]** button
- The system will load pipeline data for that repository
- Chat history will reset for the new repository context

## 📊 Pipeline Dashboard

Once you select a repository, you'll see:

### Metrics Overview
Four key metrics displayed as cards:
- **📊 Total Pipelines** - Overall pipeline count
- **✅ Successful** - Successfully completed pipelines
- **❌ Failed** - Failed pipelines needing attention
- **🔄 Running** - Currently executing pipelines

### Pipeline Details
Each pipeline is shown as an expandable card:

**Card Header Shows:**
- Status emoji (✅ success, ❌ failed, 🔄 running)
- Pipeline name

**Expanded Details Include:**
- Pipeline ID and stage
- Branch and commit information
- Last run timestamp and duration
- Progress bar (for running pipelines)
- Error messages (for failed pipelines)

### Pipeline Actions
- **📋 View Logs** - See detailed execution logs
- **Expand/Collapse** - Click card headers to show/hide details

## 🤖 AI Assistant (Portia)

### Starting a Conversation
1. Scroll to the **🤖 AI Assistant** section
2. Type your question in the chat input
3. Press Enter or click send

### What You Can Ask
**Pipeline Status Questions:**
- "What's the current status?"
- "How many pipelines failed?"
- "Show me the system health"

**Troubleshooting Help:**
- "Why did the pipeline fail?"
- "How can I fix the build errors?"
- "What are the common DevOps issues?"

**Best Practices:**
- "DevOps recommendations for this project"
- "How to improve pipeline performance?"
- "Security best practices for CI/CD"

### AI Response Features
- **Context-Aware** - Knows your current repository and pipeline status
- **Portia-Powered** - Uses advanced AI agent management
- **Web Search** - Can search for additional DevOps information
- **Actionable Advice** - Provides specific recommendations

## 🎛️ Sidebar Controls

### Refresh Options
- **🔄 Refresh Now** - Manually refresh pipeline data
- **Auto-refresh** - Data refreshes automatically every 30 seconds

### Filters
- **Filter by Status** - Show only specific pipeline states:
  - Success ✅
  - Failed ❌
  - Running 🔄

### System Status
- **Green** - All systems operational
- **Red** - Pipelines need attention (with count)

## 🔍 Advanced Features

### Pipeline Logs
1. Click **📋 View Logs** on any pipeline
2. See detailed execution information:
   - Workflow name and status
   - Job details and conclusions
   - Step-by-step execution
   - Timestamps and duration
   - Error messages and stack traces

### Repository Navigation
- **← Back to Repos** - Return to repository selection
- **Search** - Find repositories quickly
- **Pagination** - Navigate large repository lists

## 💡 Tips for Best Experience

### Effective AI Conversations
1. **Be Specific** - Ask about particular pipelines or errors
2. **Provide Context** - Mention what you're trying to achieve
3. **Follow Up** - Ask clarifying questions for better help

### Monitoring Best Practices
1. **Regular Checks** - Monitor failed pipelines promptly
2. **Use Filters** - Focus on specific pipeline states
3. **Review Logs** - Check detailed logs for troubleshooting

### Performance Tips
1. **Refresh Data** - Use manual refresh for latest information
2. **Filter Results** - Reduce data load with status filters
3. **Clear Chat** - Chat resets automatically when changing repos

## 🚨 Understanding Pipeline States

### Status Indicators
- **✅ Success** - Pipeline completed successfully
- **❌ Failed** - Pipeline encountered errors
- **🔄 Running** - Pipeline currently executing
- **❓ Unknown** - Status couldn't be determined

### Error Information
Failed pipelines show:
- **Error Message** - Brief description of the failure
- **Detailed Logs** - Complete execution trace
- **Timestamp** - When the failure occurred

## 🔄 Workflow Examples

### Daily Monitoring Routine
1. Open the application
2. Select your main project repository
3. Check the metrics dashboard for any failures
4. Expand failed pipelines to see error details
5. Use AI assistant to get troubleshooting advice
6. Review logs for detailed debugging information

### Troubleshooting Failed Pipelines
1. Identify failed pipelines from the dashboard
2. Click to expand the failed pipeline card
3. Read the error message
4. Click **📋 View Logs** for detailed information
5. Ask the AI assistant: "Why did [pipeline name] fail?"
6. Follow the AI's recommendations

### Getting DevOps Advice
1. Select a repository you want to improve
2. Ask the AI assistant questions like:
   - "How can I improve this project's CI/CD?"
   - "What are the best practices for [language] projects?"
   - "How to optimize build times?"

## 📚 Next Steps

- [API Reference](API_REFERENCE.md) - Explore backend endpoints
- [Troubleshooting](TROUBLESHOOTING.md) - Solve common issues
- [Contributing](CONTRIBUTING.md) - Help improve the project

---

**Questions?** Check our [FAQ](FAQ.md) or open an issue on GitHub.