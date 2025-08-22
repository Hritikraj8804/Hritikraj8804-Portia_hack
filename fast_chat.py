"""
Fast Hugging Face chat for instant responses
"""
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class FastGeminiChat:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def get_quick_response(self, user_query, pipeline_context=None):
        """Get fast response from Google Gemini with pipeline context"""
        
        try:
            if self.google_api_key:
                print(f"⚡ Using Gemini API for: {user_query[:50]}...")
                
                # Add real pipeline context if available
                context_info = ""
                if pipeline_context:
                    failed_pipelines = [p for p in pipeline_context if p.get('status') == 'failed']
                    running_pipelines = [p for p in pipeline_context if p.get('status') == 'running']
                    success_pipelines = [p for p in pipeline_context if p.get('status') == 'success']
                    
                    context_info = f"""
                    
                Current Pipeline Status:
                - ✅ {len(success_pipelines)} successful pipelines
                - ❌ {len(failed_pipelines)} failed pipelines
                - 🔄 {len(running_pipelines)} running pipelines
                
                Failed Pipelines Details:
                {chr(10).join([f"- {p['name']}: {p.get('error', 'Unknown error')}" for p in failed_pipelines[:2]])}
                """
                
                # DevOps-focused prompt with real context
                gemini_prompt = f"""
                You are a DevOps AI Assistant. Provide a helpful, concise response (under 150 words) to this question:
                
                {user_query}
                {context_info}
                
                Context: CI/CD pipelines, troubleshooting, deployment issues.
                Style: Friendly, actionable, beginner-friendly.
                Use the real pipeline data above to give specific advice.
                """
                
                response = self.model.generate_content(gemini_prompt)
                
                if response.text:
                    return f"⚡ **Fast AI:** {response.text.strip()}"
                
                print("Gemini API failed, using fallback")
            else:
                print("No Google API key, using fallback")
            
            # Fallback to smart rule-based responses
            return self._smart_fallback(user_query)
            
        except Exception as e:
            print(f"Gemini error: {e}")
            return self._smart_fallback(user_query)
    
    def _smart_fallback(self, query):
        """Intelligent fallback responses"""
        query_lower = query.lower()
        
        if "status" in query_lower or "check" in query_lower:
            return """🔍 **Pipeline Status Check**

I can see your pipeline dashboard above. Here's what I notice:
- Look for ❌ failed pipelines first
- 🔄 Running pipelines are in progress
- ✅ Successful ones are healthy

**Quick Actions:** Click the action buttons on failed pipelines, or ask me "analyze the failure" for detailed help."""

        elif "failed" in query_lower or "error" in query_lower or "help" in query_lower:
            return """🛠️ **DevOps Troubleshooting**

For pipeline failures, I recommend this approach:

1️⃣ **RETRY** first (fixes 70% of issues)
   - Good for: timeouts, network issues, temporary glitches

2️⃣ **ROLLBACK** if retry fails
   - Good for: code problems, test failures

3️⃣ **ESCALATE** for persistent issues
   - Good for: infrastructure problems, complex errors

**Want detailed analysis?** Ask me to "analyze this failure" and I'll use advanced AI tools."""

        elif "retry" in query_lower:
            return """🔄 **Retry Strategy**

Retry is usually the best first action because:
- ✅ **85% success rate** for common failures
- ⚡ **Quick resolution** (3-5 minutes)
- 🔒 **Safe operation** (no code changes)

**When to retry:**
- Database timeouts
- Network connectivity issues
- Temporary service unavailability
- Build environment glitches

Use the retry button above or ask me to trigger it!"""

        elif "rollback" in query_lower:
            return """⏪ **Rollback Decision**

Rollback when:
- 🐛 New code is causing issues
- 🧪 Tests consistently fail
- 🚨 Need immediate service restoration

**What rollback does:**
- Reverts to last stable version
- Restores working functionality
- Minimal downtime (~2 minutes)

**Risk:** Loses recent changes (can be reapplied later)"""

        elif "escalate" in query_lower:
            return """🚨 **Escalation Process**

Escalate when:
- Multiple retries failed
- Infrastructure issues suspected
- Complex errors beyond standard fixes

**What happens:**
- DevOps team gets immediate alert
- Full diagnostic report generated
- Expert analysis and resolution
- Estimated response: 15-30 minutes

Ready to escalate? I can trigger the process."""

        elif any(word in query_lower for word in ["hi", "hello", "hey", "start"]):
            return """👋 **Hello! DevOps AI Assistant Ready**

I'm here to help with your CI/CD pipelines! I can:

⚡ **Quick Help:**
- Check pipeline status
- Explain errors in simple terms
- Recommend immediate actions

🔧 **Advanced Analysis:**
- Deep failure investigation
- Multi-tool workflow automation
- Team notifications and documentation

**Try asking:** "Check my pipelines" or "Help with the failure" 🚀"""

        else:
            return """🤖 **DevOps AI Assistant**

I can help you with:
- 📊 Pipeline status and health checks
- 🔍 Error analysis and troubleshooting
- 🛠️ Action recommendations (retry/rollback/escalate)
- 📚 DevOps best practices and explanations

**For complex analysis,** I can use advanced AI tools to research solutions and coordinate with your team.

What specific DevOps challenge can I help you solve? 💪"""

# Global instance
fast_chat = FastGeminiChat()

def get_pipeline_context():
    """Get current pipeline status for context"""
    try:
        import requests
        response = requests.get("http://localhost:8000/pipelines", timeout=2)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def test_fast_chat():
    """Test the fast chat system"""
    print("⚡ Testing Fast Gemini Chat System")
    print("=" * 40)
    
    test_queries = [
        "Hi there!",
        "Check my pipeline status", 
        "My deployment failed, help me",
        "Should I retry or rollback?"
    ]
    
    for query in test_queries:
        print(f"\n🔸 Query: {query}")
        response = fast_chat.get_quick_response(query)
        print(f"⚡ Response: {response[:100]}...")
    
    print("\n✅ Fast chat system ready!")

if __name__ == "__main__":
    test_fast_chat()