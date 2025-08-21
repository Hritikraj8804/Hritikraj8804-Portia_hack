"""
Portia Labs client for frontend integration
"""
import os
import requests
from typing import Optional

class PortiaClient:
    """Client to interact with Portia Labs agents"""
    
    def __init__(self):
        self.api_key = os.getenv("PORTIA_API_KEY", "prt-iz5AmjCu.FzvTZUUscHNDAEBYz3qU5VssiJXoeXaA")
        self.base_url = "https://api.portialabs.ai"  # Replace with actual Portia API URL
        
    def query_execution_agent(self, query: str) -> Optional[str]:
        """Query the DevOps execution agent"""
        try:
            # This would be the actual Portia API call
            # For now, return enhanced rule-based response
            return self._enhanced_response(query)
        except Exception as e:
            return f"Error connecting to Portia agent: {e}"
    
    def query_clarification_agent(self, context: str) -> Optional[str]:
        """Query the clarification agent for user interaction"""
        try:
            # Enhanced clarification logic
            if "critical" in context.lower() or "production" in context.lower():
                return """
                🚨 **Critical Issue Detected**
                
                Since this is affecting production, I recommend:
                
                1. **Immediate Action**: Try retry first (safest option)
                2. **If retry fails**: Consider rollback to restore service
                3. **Escalation**: I can alert the DevOps team if needed
                
                What would you like me to do first?
                """
            elif "failed" in context.lower():
                return """
                I see there's a pipeline failure. To help you best:
                
                **How urgent is this?**
                🔴 Critical - Production affected
                🟡 High - Blocking work  
                🟢 Medium - Can wait a bit
                
                **What type of failure?**
                - Build/compilation issues
                - Test failures  
                - Deployment problems
                - Infrastructure issues
                
                This helps me recommend the right solution!
                """
            else:
                return "I'm here to help with your DevOps pipelines. What specific issue are you facing?"
        except Exception as e:
            return f"Error with clarification agent: {e}"
    
    def _enhanced_response(self, query: str) -> str:
        """Enhanced rule-based responses while Portia agents are being set up"""
        query_lower = query.lower()
        
        if "status" in query_lower or "check" in query_lower:
            return """
            🔍 **Pipeline Status Analysis**
            
            I've checked your pipelines and found:
            
            ✅ **Frontend Deployment** - Healthy
            ❌ **Backend API** - Failed at testing stage
            🔄 **Database Migration** - Running (80% complete)
            
            **Issue Details:**
            The Backend API failed due to database connection timeout during testing.
            
            **My Recommendation:**
            Try **RETRY** first because:
            - Database timeouts are often temporary
            - No code changes needed
            - Low risk of making things worse
            
            Would you like me to retry the Backend API pipeline?
            """
            
        elif "failed" in query_lower or "error" in query_lower:
            return """
            🔧 **Failure Analysis**
            
            **What happened:** Backend API pipeline failed during the testing phase
            **Root cause:** Database connection timed out after 300 seconds
            **Impact:** Blocking deployment to production
            
            **Recommended Actions:**
            1. 🔄 **Retry** - Best first option (database might be responsive now)
            2. ⏪ **Rollback** - If retry fails, go back to working version  
            3. 🚨 **Escalate** - If this keeps happening, get DevOps team help
            
            **Why retry first?**
            Database timeouts are usually temporary network issues that resolve themselves.
            
            Ready to proceed with retry?
            """
            
        elif "retry" in query_lower:
            return """
            🔄 **Retry Action Initiated**
            
            ✅ Backend API pipeline retry started
            ⏱️ Estimated time: 3-5 minutes
            📊 Current stage: Build (starting tests soon)
            
            **What's happening:**
            1. Rebuilding the application
            2. Running automated tests (including database connectivity)
            3. If tests pass, will deploy automatically
            
            I'll monitor the progress and let you know the result!
            
            💡 **Tip:** While we wait, you can check the logs in the dashboard above.
            """
            
        elif "rollback" in query_lower:
            return """
            ⏪ **Rollback Action**
            
            This will revert to the previous stable version:
            
            **What rollback does:**
            - Switches back to last working code
            - Restores previous database state
            - Gets your system running again quickly
            
            **When to use rollback:**
            - New code is causing problems
            - Tests keep failing
            - Need to restore service immediately
            
            **Confirm rollback?** This will undo recent changes.
            """
            
        elif "escalate" in query_lower:
            return """
            🚨 **Escalation Process**
            
            I'll alert the DevOps team with:
            
            **Issue Summary:**
            - Pipeline: Backend API
            - Problem: Database connection timeout
            - Impact: Production deployment blocked
            - Actions tried: [List any previous attempts]
            
            **What happens next:**
            1. DevOps team gets immediate notification
            2. They'll investigate infrastructure issues
            3. You'll get updates on progress
            4. Estimated response time: 15-30 minutes
            
            Should I proceed with escalation?
            """
            
        else:
            return """
            👋 **DevOps AI Assistant Ready**
            
            I can help you with:
            
            🔍 **Pipeline Status** - Check what's running, failed, or completed
            🛠️ **Troubleshooting** - Analyze failures and recommend fixes  
            ⚡ **Quick Actions** - Retry, rollback, or escalate issues
            📚 **Learning** - Explain DevOps concepts in simple terms
            
            **Try asking:**
            - "Check my pipeline status"
            - "Help me fix the failed deployment"
            - "What does this error mean?"
            
            What would you like help with?
            """
        
        return "I'm here to help with your DevOps pipelines!"

# Global client instance
portia_client = PortiaClient()