"""
Demo-ready DevOps Assistant with enhanced AI responses
"""

def get_smart_response(user_query, pipelines):
    """Enhanced AI-like responses for demo"""
    
    query = user_query.lower()
    
    if "status" in query or "check" in query:
        failed = [p for p in pipelines if p["status"] == "failed"]
        if failed:
            return f"""
🔍 **Pipeline Status Analysis**

I've analyzed your pipelines and found:
✅ **{len([p for p in pipelines if p['status'] == 'success'])} Successful**
❌ **{len(failed)} Failed** 
🔄 **{len([p for p in pipelines if p['status'] == 'running'])} Running**

**Critical Issue:** {failed[0]['name']} failed at {failed[0]['stage']} stage
**Error:** {failed[0].get('error', 'Unknown error')}

**My AI Recommendation:** RETRY first because database timeouts are usually temporary network issues that resolve themselves.

Would you like me to retry the failed pipeline?
"""
        else:
            return "✅ **All Systems Healthy!** No failed pipelines detected. Your DevOps setup is running smoothly!"
    
    elif "failed" in query or "error" in query or "help" in query:
        return """
🛠️ **DevOps Troubleshooting Assistant**

I see you're having pipeline issues. Here's my intelligent analysis:

**Most Common Causes:**
1. 🌐 **Network Issues** (60% of cases) → Retry works
2. 🧪 **Test Failures** (25% of cases) → Check code changes  
3. 🏗️ **Build Problems** (15% of cases) → Review dependencies

**My Smart Recommendation:**
Start with **RETRY** because:
- It's the safest option (won't break anything)
- Fixes 60% of pipeline failures automatically
- Takes only 3-5 minutes to complete

**If retry fails twice:** Consider rollback or escalation.

Ready to proceed with retry?
"""
    
    elif "retry" in query:
        return """
🔄 **Retry Action Initiated**

✅ **Backend API pipeline retry started**
⏱️ **Estimated completion:** 3-5 minutes
📊 **Current progress:** Build stage (25% complete)

**What's happening now:**
1. ✅ Code compilation - Complete
2. 🔄 Running tests - In progress
3. ⏳ Database connectivity check - Pending
4. ⏳ Deployment - Waiting

**AI Monitoring:** I'm watching the progress and will alert you if any issues arise.

💡 **Pro Tip:** While we wait, you can check detailed logs in the dashboard above.
"""
    
    elif "rollback" in query:
        return """
⏪ **Rollback Analysis**

**What rollback does:**
- Reverts to last known good version (commit: abc123f)
- Restores previous database state
- Gets your system running in ~2 minutes

**When I recommend rollback:**
- New code changes are causing repeated failures
- Tests consistently fail after recent commits
- You need to restore service immediately

**Risk Assessment:** Low risk - this is a safe operation that restores stability.

**Confirm rollback?** This will undo recent changes but restore service.
"""
    
    elif "escalate" in query:
        return """
🚨 **Escalation Protocol**

**I'll notify the DevOps team with:**

📋 **Incident Summary:**
- Pipeline: Backend API
- Issue: Database connection timeout  
- Impact: Production deployment blocked
- Attempts: [Previous actions tried]
- Urgency: High (based on your input)

**What happens next:**
1. ⚡ Immediate Slack/email notification to on-call engineer
2. 📞 Phone alert if no response in 10 minutes
3. 📊 Full diagnostic report generated
4. 🔍 Infrastructure health check initiated

**Expected Response Time:** 15-30 minutes

Should I proceed with escalation to the DevOps team?
"""
    
    else:
        return """
👋 **DevOps AI Assistant Ready**

I'm your intelligent DevOps companion! I can help with:

🔍 **Smart Analysis** - I analyze pipeline failures and recommend the best actions
🛠️ **Automated Actions** - Execute retries, rollbacks, and escalations  
📚 **Learning Mode** - Explain DevOps concepts in simple terms
🚨 **Proactive Monitoring** - Alert you to potential issues before they become problems

**Popular Commands:**
- "Check my pipeline status"
- "My deployment failed, help me fix it"
- "Should I retry or rollback?"
- "Explain this error in simple terms"

**AI Confidence:** 95% - I'm trained on thousands of DevOps scenarios!

What can I help you troubleshoot today?
"""

# Test the enhanced responses
if __name__ == "__main__":
    print("🤖 Testing Enhanced AI Responses")
    print("=" * 50)
    
    # Mock pipeline data
    mock_pipelines = [
        {"name": "Frontend", "status": "success", "stage": "deployment"},
        {"name": "Backend API", "status": "failed", "stage": "testing", "error": "Database timeout after 300s"},
        {"name": "Database Migration", "status": "running", "stage": "migration"}
    ]
    
    # Test queries
    test_queries = [
        "Check my pipeline status",
        "My deployment failed, help me",
        "Should I retry the backend?",
        "What is escalation?"
    ]
    
    for query in test_queries:
        print(f"\n🔸 Query: {query}")
        response = get_smart_response(query, mock_pipelines)
        print(f"🤖 Response: {response[:100]}...")
    
    print("\n✅ Enhanced AI responses ready for demo!")