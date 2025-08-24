import streamlit as st
import requests
from datetime import datetime, timedelta
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

# Simplified CSS
st.markdown("""
<style>
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-left: 4px solid #667eea;
    margin: 0.5rem 0;
}

.success-card { border-left-color: #28a745; background: #f8fff9; }
.failed-card { border-left-color: #dc3545; background: #fff8f8; }
.running-card { border-left-color: #ffc107; background: #fffdf7; }

.repo-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #e1e5e9;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    cursor: pointer;
}

.repo-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-color: #667eea;
}

.language-tag {
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.2rem 0.5rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_repositories():
    """Fetch repositories with caching"""
    try:
        response = requests.get(f"{API_BASE_URL}/repositories", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching repositories: {e}")
        return []

@st.cache_data(ttl=30)
def get_pipelines(repo_owner=None, repo_name=None):
    """Fetch pipelines with caching"""
    try:
        url = f"{API_BASE_URL}/pipelines"
        if repo_owner and repo_name:
            url += f"?owner={repo_owner}&name={repo_name}"
        
        print(f"FRONTEND DEBUG: Making API call to: {url}")
        response = requests.get(url, timeout=5)
        print(f"FRONTEND DEBUG: API response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"FRONTEND DEBUG: API response data type: {type(data)}")
            print(f"FRONTEND DEBUG: API response length: {len(data) if isinstance(data, list) else 'Not a list'}")
            if isinstance(data, list) and len(data) > 0:
                print(f"FRONTEND DEBUG: First pipeline sample: {data[0]}")
            return data
        else:
            print(f"FRONTEND DEBUG: API error response: {response.text}")
        return []
    except Exception as e:
        print(f"Error fetching pipelines: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_pipeline_logs(pipeline_id):
    """Fetch pipeline logs"""
    try:
        response = requests.get(f"{API_BASE_URL}/pipelines/{pipeline_id}/logs", timeout=5)
        if response.status_code == 200:
            return response.json()["logs"]
        return []
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

def execute_action(pipeline_id, action, reason=""):
    """Execute pipeline action"""
    try:
        headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}
        data = {"pipeline_id": pipeline_id, "action": action, "reason": reason}
        
        response = requests.post(f"{API_BASE_URL}/pipelines/action", json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error executing action: {e}")
        return None

def main():
    print("Starting DevOps AI Assistant frontend")
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 DevOps AI Assistant</h1>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">Intelligent CI/CD Pipeline Management</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">Hackathon MVP • Real-time Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch repositories
    repositories = get_repositories()
    
    if repositories:
        st.subheader("📋 Select Repository to Monitor")
        
        # Search bar
        search_term = st.text_input("🔍 Search repositories...", placeholder="Type repository name")
        
        # Filter repositories based on search
        if search_term:
            filtered_repos = [repo for repo in repositories if search_term.lower() in repo['name'].lower()]
        else:
            filtered_repos = repositories
        
        # Pagination
        repos_per_page = 9
        total_pages = (len(filtered_repos) + repos_per_page - 1) // repos_per_page
        
        # Initialize current page
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        if total_pages > 1:
            # Compact pagination on right side
            col1, col2 = st.columns([3, 1])
            with col2:
                # Single line pagination
                pagination_html = f"""
                <div style="text-align: right; margin: 0.5rem 0;">
                    <span style="color: #666; font-size: 0.9rem;">Page {st.session_state.current_page} of {total_pages}</span>
                </div>
                """
                st.markdown(pagination_html, unsafe_allow_html=True)
                
                # Navigation buttons in one row
                nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
                with nav_col1:
                    if st.button("←", disabled=st.session_state.current_page <= 1, key="prev_btn"):
                        st.session_state.current_page -= 1
                        st.rerun()
                with nav_col2:
                    if st.button("1", disabled=st.session_state.current_page == 1, key="first_btn"):
                        st.session_state.current_page = 1
                        st.rerun()
                with nav_col3:
                    if st.button(str(total_pages), disabled=st.session_state.current_page == total_pages, key="last_btn"):
                        st.session_state.current_page = total_pages
                        st.rerun()
                with nav_col4:
                    if st.button("→", disabled=st.session_state.current_page >= total_pages, key="next_btn"):
                        st.session_state.current_page += 1
                        st.rerun()
        
        page = st.session_state.current_page
        
        # Calculate start and end indices
        start_idx = (page - 1) * repos_per_page
        end_idx = start_idx + repos_per_page
        page_repos = filtered_repos[start_idx:end_idx]
        
        # Reset to page 1 if search changes the results
        if len(filtered_repos) > 0 and start_idx >= len(filtered_repos):
            st.session_state.current_page = 1
            st.rerun()
        
        # Show results info on left
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"📊 Showing {len(page_repos)} of {len(filtered_repos)} repositories")
        
        # Display repositories as cards
        cols_per_row = 3
        for i in range(0, len(page_repos), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, col in enumerate(cols):
                repo_index = i + j
                if repo_index < len(page_repos):
                    repo = page_repos[repo_index]
                    
                    with col:
                        # Repository card
                        description = (repo.get('description') or 'No description')
                        if len(description) > 60:
                            description = description[:60] + '...'
                        
                        card_html = f"""
                        <div class="repo-card">
                            <h4 style="margin: 0 0 0.5rem 0; color: #333;">📋 {repo['name']}</h4>
                            <p style="margin: 0 0 0.5rem 0; color: #666; font-size: 0.9rem; min-height: 2.5rem;">{description}</p>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                                <span class="language-tag">{repo.get('language', 'Unknown')}</span>
                                <span style="color: #999; font-size: 0.8rem;">Updated: {repo.get('updated_at', 'Unknown')[:10] if repo.get('updated_at') else 'Unknown'}</span>
                            </div>
                        </div>
                        """
                        
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Monitor button
                        if st.button(f"🚀 Monitor {repo['name']}", key=f"repo_{start_idx + repo_index}"):
                            st.session_state.selected_repo = repo
                            st.rerun()
        
        # Show instruction if no repo selected
        if 'selected_repo' not in st.session_state:
            st.info("👆 Click on any repository card above to start monitoring its pipelines")
            return
    else:
        st.warning("⚠️ No repositories found. Make sure the backend is running.")
        return
    
    # Get selected repository
    selected_repo = st.session_state.get('selected_repo')
    if not selected_repo:
        return
    
    # Fetch pipelines for selected repo
    with st.spinner(f'🔄 Loading pipelines for {selected_repo.get("full_name", selected_repo["name"])}...'):
        print(f"FRONTEND DEBUG: Fetching pipelines for owner={selected_repo.get('owner')}, name={selected_repo.get('name')}")
        pipelines = get_pipelines(selected_repo.get('owner'), selected_repo.get('name'))
        print(f"FRONTEND DEBUG: Received {len(pipelines)} pipelines from API")
    
    if not pipelines:
        st.warning(f"⚠️ No pipeline data found for {selected_repo.get('full_name', selected_repo['name'])}")
        st.info(f"Debug: API call was made to /pipelines?owner={selected_repo.get('owner')}&name={selected_repo.get('name')}")
        return
    
    # Show selected repository info with back button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(f"✅ Monitoring: **{selected_repo.get('full_name', selected_repo['name'])}** ({selected_repo.get('language', 'Unknown')})")
    with col2:
        if st.button("← Back to Repos"):
            del st.session_state.selected_repo
            st.rerun()
    
    # Sidebar controls
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 8px; color: white; text-align: center; margin-bottom: 1rem;">
        <h3 style="margin: 0;">🎛️ Control Panel</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh
    st.sidebar.subheader("🔄 Refresh")
    if st.sidebar.button("🔄 Refresh Now"):
        st.cache_data.clear()
        st.rerun()
    
    # Pipeline filters
    st.sidebar.subheader("🔍 Filters")
    status_filter = st.sidebar.multiselect(
        "Filter by status",
        ["success", "failed", "running"],
        default=["success", "failed", "running"]
    )
    
    # Apply status filter
    if status_filter and pipelines:
        pipelines = [p for p in pipelines if isinstance(p, dict) and p.get('status') in status_filter]
    
    # System status
    failed_count = len([p for p in pipelines if p.get('status') == 'failed'])
    if failed_count > 0:
        st.sidebar.error(f"🚨 {failed_count} pipeline(s) need attention!")
    else:
        st.sidebar.success("✅ All systems operational")
    
    # Metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    success_count = len([p for p in pipelines if isinstance(p, dict) and p.get("status") == "success"])
    failed_count = len([p for p in pipelines if isinstance(p, dict) and p.get("status") == "failed"])
    running_count = len([p for p in pipelines if isinstance(p, dict) and p.get("status") == "running"])
    total_count = len(pipelines)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #667eea;">📊 {total_count}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Total Pipelines</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card success-card">
            <h3 style="margin: 0; color: #28a745;">✅ {success_count}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Successful</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card failed-card">
            <h3 style="margin: 0; color: #dc3545;">❌ {failed_count}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Failed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card running-card">
            <h3 style="margin: 0; color: #ffc107;">🔄 {running_count}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Running</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🔄 Retry All Failed"):
            failed_pipelines = [p for p in pipelines if p.get('status') == 'failed']
            if failed_pipelines:
                for pipeline in failed_pipelines:
                    execute_action(pipeline['id'], 'retry', 'Bulk retry from quick actions')
                st.success(f"✅ Initiated retry for {len(failed_pipelines)} pipeline(s)")
                time.sleep(1)
                st.rerun()
            else:
                st.info("📊 No failed pipelines to retry")
    
    with action_col2:
        if st.button("📋 Export Report"):
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'repository': selected_repo.get('full_name', 'Unknown'),
                'total_pipelines': total_count,
                'success_count': success_count,
                'failed_count': failed_count,
                'running_count': running_count
            }
            st.download_button(
                label="📎 Download JSON Report",
                data=str(report_data),
                file_name=f"pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with action_col3:
        if st.button("🚀 Deploy Latest"):
            success_pipelines = [p for p in pipelines if p.get('status') == 'success']
            if success_pipelines:
                st.success("🚀 Deployment initiated!")
            else:
                st.warning("⚠️ No successful builds available")
    
    # Pipeline Details
    st.markdown("### 🔍 Pipeline Details")
    
    for pipeline in pipelines:
        if not isinstance(pipeline, dict):
            continue
        status_emoji = {"success": "✅", "failed": "❌", "running": "🔄"}
        emoji = status_emoji.get(pipeline.get("status"), "❓")
        
        with st.expander(f"{emoji} {pipeline['name']}", expanded=pipeline['status'] == 'failed'):
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
                st.markdown("#### 🛠️ Quick Actions")
                
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if st.button("🔄 Retry", key=f"retry_{pipeline['id']}"):
                        with st.spinner('Retrying pipeline...'):
                            result = execute_action(pipeline['id'], 'retry', 'Manual retry')
                            if result:
                                st.success(f"✅ {result['message']}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Failed to execute retry")
                
                with action_col2:
                    if st.button("⏪ Rollback", key=f"rollback_{pipeline['id']}"):
                        with st.spinner('Rolling back...'):
                            result = execute_action(pipeline['id'], 'rollback', 'Manual rollback')
                            if result:
                                st.success(f"✅ {result['message']}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Failed to execute rollback")
                
                with action_col3:
                    if st.button("🚨 Escalate", key=f"escalate_{pipeline['id']}"):
                        result = execute_action(pipeline['id'], 'escalate', 'Manual escalation')
                        if result:
                            st.success(f"✅ {result['message']}")
                        else:
                            st.error("❌ Failed to escalate")
            
            # Logs section
            if st.button(f"📋 View Logs", key=f"logs_{pipeline['id']}"):
                with st.spinner('Loading logs...'):
                    logs = get_pipeline_logs(pipeline['id'])
                    if logs:
                        st.markdown("**Pipeline Logs:**")
                        st.code('\n'.join(logs), language='log')
                    else:
                        st.warning("⚠️ No logs available")
    
    # Simple AI Assistant
    st.markdown("### 🤖 AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hi! I'm your DevOps AI Assistant. I can help you with pipeline status, troubleshooting, and recommendations. What would you like to know?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about pipelines..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Simple responses for common queries
            if prompt.lower() in ['status', 'health']:
                response = f"""📊 **System Status Report**

✅ **Healthy:** {success_count} pipelines
❌ **Failed:** {failed_count} pipelines  
🔄 **Running:** {running_count} pipelines

{'🚨 **Action Required:** Failed pipelines need attention!' if failed_count > 0 else '✅ **All Systems Operational**'}"""
            elif 'retry' in prompt.lower():
                response = "🔄 **Retry Command Detected**\n\nTo retry a pipeline, use the action buttons in the pipeline details above."
            elif 'help' in prompt.lower():
                response = """🤖 **Available Commands:**

• `status` - Get system status report
• `retry` - Information about retrying pipelines  
• `help` - Show this help message

You can also use the action buttons in the pipeline details for direct actions."""
            else:
                response = "I'm your DevOps AI Assistant. I can help with pipeline status and troubleshooting. Try asking about 'status' or 'help' for available commands."
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()