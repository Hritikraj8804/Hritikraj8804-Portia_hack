import streamlit as st
import requests
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="DevOps AI Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
API_BASE_URL = "http://localhost:8000"
API_TOKEN = "Bearer demo-secure-token-123"

# Custom CSS
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
}
.success { border-left-color: #2ca02c; }
.failed { border-left-color: #d62728; }
.running { border-left-color: #ff7f0e; }
</style>
""", unsafe_allow_html=True)

def get_pipelines():
    """Fetch pipeline data from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/pipelines")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_pipeline_logs(pipeline_id):
    """Fetch logs for specific pipeline"""
    try:
        response = requests.get(f"{API_BASE_URL}/pipelines/{pipeline_id}/logs")
        if response.status_code == 200:
            return response.json()["logs"]
        return []
    except:
        return []

def execute_action(pipeline_id, action, reason=""):
    """Execute pipeline action"""
    try:
        headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}
        data = {"pipeline_id": pipeline_id, "action": action, "reason": reason}
        response = requests.post(f"{API_BASE_URL}/pipelines/action", json=data, headers=headers)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def main():
    st.title("🚀 DevOps AI Assistant")
    st.markdown("*Intelligent CI/CD Pipeline Management & Troubleshooting*")
    
    # Sidebar
    st.sidebar.title("🎛️ Control Panel")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=True)
    
    if auto_refresh:
        # Auto-refresh every 30 seconds
        placeholder = st.empty()
        time.sleep(0.1)  # Small delay to prevent immediate refresh
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()
    
    # Fetch pipeline data
    pipelines = get_pipelines()
    
    if not pipelines:
        st.error("❌ Unable to connect to pipeline API. Make sure the backend is running.")
        st.code("python backend/main.py")
        return
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    # Status counts
    success_count = len([p for p in pipelines if p["status"] == "success"])
    failed_count = len([p for p in pipelines if p["status"] == "failed"])
    running_count = len([p for p in pipelines if p["status"] == "running"])
    total_count = len(pipelines)
    
    with col1:
        st.metric("Total Pipelines", total_count)
    with col2:
        st.metric("✅ Successful", success_count)
    with col3:
        st.metric("❌ Failed", failed_count)
    with col4:
        st.metric("🔄 Running", running_count)
    
    # Pipeline status visualization
    st.subheader("📊 Pipeline Status Overview")
    
    # Simple status display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Success", success_count, delta=None)
    with col2:
        st.metric("❌ Failed", failed_count, delta=None)
    with col3:
        st.metric("🔄 Running", running_count, delta=None)
    
    # Pipeline details
    st.subheader("🔍 Pipeline Details")
    
    for pipeline in pipelines:
        status_emoji = {"success": "✅", "failed": "❌", "running": "🔄"}
        emoji = status_emoji.get(pipeline["status"], "❓")
        
        with st.expander(f"{emoji} {pipeline['name']} - {pipeline['status'].upper()}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**ID:** {pipeline['id']}")
                st.write(f"**Stage:** {pipeline['stage']}")
                st.write(f"**Branch:** {pipeline['branch']}")
                st.write(f"**Commit:** {pipeline['commit']}")
                
            with col2:
                st.write(f"**Last Run:** {pipeline['last_run']}")
                if pipeline.get('duration'):
                    st.write(f"**Duration:** {pipeline['duration']}")
                if pipeline.get('progress'):
                    st.progress(pipeline['progress'] / 100)
                    st.write(f"**Progress:** {pipeline['progress']}%")
            
            # Show error if failed
            if pipeline["status"] == "failed" and pipeline.get("error"):
                st.error(f"**Error:** {pipeline['error']}")
            
            # Action buttons for failed pipelines
            if pipeline["status"] == "failed":
                st.write("**🛠️ Available Actions:**")
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if st.button(f"🔄 Retry", key=f"retry_{pipeline['id']}"):
                        result = execute_action(pipeline['id'], 'retry', 'Manual retry from dashboard')
                        if result:
                            st.success(f"✅ {result['message']}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Failed to execute retry")
                
                with action_col2:
                    if st.button(f"⏪ Rollback", key=f"rollback_{pipeline['id']}"):
                        result = execute_action(pipeline['id'], 'rollback', 'Manual rollback from dashboard')
                        if result:
                            st.success(f"✅ {result['message']}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Failed to execute rollback")
                
                with action_col3:
                    if st.button(f"🚨 Escalate", key=f"escalate_{pipeline['id']}"):
                        result = execute_action(pipeline['id'], 'escalate', 'Manual escalation from dashboard')
                        if result:
                            st.success(f"✅ {result['message']}")
                        else:
                            st.error("❌ Failed to escalate")
            
            # Show logs
            if st.button(f"📋 View Logs", key=f"logs_{pipeline['id']}"):
                logs = get_pipeline_logs(pipeline['id'])
                if logs:
                    st.code('\n'.join(logs), language='log')
                else:
                    st.warning("No logs available")
    
    # AI Assistant Chat Interface
    st.subheader("🤖 AI Assistant")
    st.markdown("*Ask me about your pipelines, and I'll help you troubleshoot!*")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your DevOps AI Assistant. I can help you check pipeline status, troubleshoot failures, and recommend actions. What would you like to know?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your pipelines..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response (simplified for demo)
        with st.chat_message("assistant"):
            response = generate_ai_response(prompt, pipelines)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def generate_ai_response(prompt, pipelines):
    """Generate AI response based on prompt and pipeline data"""
    prompt_lower = prompt.lower()
    
    # Simple rule-based responses for demo
    if "status" in prompt_lower or "check" in prompt_lower:
        failed_pipelines = [p for p in pipelines if p["status"] == "failed"]
        if failed_pipelines:
            response = f"I found {len(failed_pipelines)} failed pipeline(s):\n\n"
            for p in failed_pipelines:
                response += f"❌ **{p['name']}**: Failed at {p['stage']} stage\n"
                if p.get('error'):
                    response += f"   Error: {p['error']}\n"
                response += f"   **Recommendation**: Try retry first, then consider rollback if issue persists.\n\n"
        else:
            response = "✅ All pipelines are healthy! No failed pipelines detected."
    
    elif "failed" in prompt_lower or "error" in prompt_lower:
        failed_pipelines = [p for p in pipelines if p["status"] == "failed"]
        if failed_pipelines:
            p = failed_pipelines[0]  # Focus on first failed pipeline
            response = f"The **{p['name']}** pipeline failed at the **{p['stage']}** stage.\n\n"
            if p.get('error'):
                response += f"**Error**: {p['error']}\n\n"
            response += "**My recommendations**:\n"
            response += "1. 🔄 **Retry**: If this looks like a temporary issue\n"
            response += "2. ⏪ **Rollback**: If there are code-related problems\n"
            response += "3. 🚨 **Escalate**: If you need DevOps team assistance\n\n"
            response += "Would you like me to execute any of these actions?"
        else:
            response = "I don't see any failed pipelines currently. All systems appear to be running normally."
    
    elif "retry" in prompt_lower:
        response = "I can help you retry failed pipelines. Use the retry buttons above, or let me know which specific pipeline you'd like to retry."
    
    elif "rollback" in prompt_lower:
        response = "Rollback will revert to the previous stable version. This is recommended when:\n- New code changes are causing issues\n- Tests are failing due to recent commits\n- You need to quickly restore service\n\nWhich pipeline would you like to rollback?"
    
    elif "escalate" in prompt_lower:
        response = "Escalation will notify the DevOps team. This is recommended when:\n- Infrastructure issues are suspected\n- Multiple retries have failed\n- You need expert assistance\n\nI can escalate any pipeline issue for you."
    
    else:
        response = "I can help you with:\n- 📊 Checking pipeline status\n- 🔍 Analyzing failures and errors\n- 🛠️ Recommending actions (retry/rollback/escalate)\n- 📋 Viewing detailed logs\n\nWhat specific help do you need with your pipelines?"
    
    return response

if __name__ == "__main__":
    main()