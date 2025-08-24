import streamlit as st
import requests
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

load_dotenv()

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

def get_portia_response(prompt, selected_repo, pipelines):
    """Get response using actual Portia SDK"""
    try:
        # Force local mode to avoid cloud API timeouts
        os.environ['PORTIA_LOCAL_MODE'] = 'true'
        os.environ['PORTIA_DISABLE_CLOUD'] = 'true'
        
        # Import Portia SDK
        from portia import Portia, Config
        
        # Build simple DevOps query
        devops_query = f"""
I'm monitoring a DevOps system with the following status:
- Repository: {selected_repo.get('name', 'Unknown')}
- Total Pipelines: {len(pipelines)}
- Failed: {len([p for p in pipelines if p.get('status') == 'failed'])}
- Successful: {len([p for p in pipelines if p.get('status') == 'success'])}

User asks: {prompt}

Provide a brief, helpful DevOps response."""
        
        # Create Portia config for local operation
        config = Config(
            llm_provider="google",
            enable_tools=True,              # Enable tools including Tavily
            enable_introspection=False,
            enable_remote_tools=False,      # Keep remote MCP disabled
            use_local_mode=True,            # Force local mode to avoid cloud API timeouts
            timeout=30                      # Shorter timeout for local operation
        )
        portia = Portia(config=config)
        
        # Run simple query
        result = portia.run(devops_query)
        
        # Extract response
        if hasattr(result.outputs, 'final_output'):
            if hasattr(result.outputs.final_output, 'value'):
                response = str(result.outputs.final_output.value)
            else:
                response = str(result.outputs.final_output)
        else:
            response = "Portia processed your request successfully."
        
        return f"🤖 **Portia AI** (Agent Manager)\n\n{response}"
        
    except ImportError:
        print("Portia SDK not available")
        return get_portia_fallback_response(prompt, selected_repo, pipelines)
    except Exception as e:
        print(f"Portia SDK error: {e}")
        return get_portia_fallback_response(prompt, selected_repo, pipelines)

def get_portia_fallback_response(prompt, selected_repo, pipelines):
    """Portia-style intelligent fallback when API is unavailable"""
    prompt_lower = prompt.lower()
    failed_count = len([p for p in pipelines if p.get('status') == 'failed'])
    success_count = len([p for p in pipelines if p.get('status') == 'success'])
    
    # Add Portia branding to responses
    portia_prefix = "🤖 **Portia AI** (Local Mode)\n\n"
    
    if any(word in prompt_lower for word in ['status', 'health']):
        return f"""{portia_prefix}📊 **System Analysis for {selected_repo.get('name', 'Repository')}**

{'🚨 **CRITICAL**: Multiple failures detected!' if failed_count > 2 else '⚠️ **WARNING**: Issues found!' if failed_count > 0 else '✅ **HEALTHY**: All systems operational!'}

**Pipeline Summary:**
• Total: {len(pipelines)} pipelines
• ✅ Success: {success_count}
• ❌ Failed: {failed_count}
• 🔄 Running: {len([p for p in pipelines if p.get('status') == 'running'])}

*Note: Using local Portia intelligence while API reconnects.*"""
    
    elif any(word in prompt_lower for word in ['failed', 'error']):
        if failed_count == 0:
            return f"{portia_prefix}🎉 Excellent! No failed pipelines detected. Your DevOps pipeline is running smoothly!"
        
        failed_pipelines = [p for p in pipelines if p.get('status') == 'failed'][:3]
        return f"""{portia_prefix}🔍 **Failure Analysis**

**{failed_count} pipeline(s) need attention:**

{chr(10).join([f"• **{p.get('name', 'Unknown')}**: {p.get('error', 'Unknown error')}" for p in failed_pipelines])}

**💡 Portia Recommendations:**
• Check logs for detailed error information
• Use retry buttons for transient failures
• Consider rollback if issues persist"""
    
    else:
        return f"""{portia_prefix}I'm Portia, your DevOps AI Assistant. I'm analyzing your pipeline data locally while attempting to connect to Portia services.

**Current Status for {selected_repo.get('name', 'Repository')}:**
• {len(pipelines)} total pipelines
• {success_count} successful, {failed_count} failed

**💬 Try asking:** "What's the status?" or "Show failed pipelines"

*Attempting to reconnect to Portia API...*"""

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
    
    # Check if repository is selected
    if 'selected_repo' in st.session_state:
        show_pipelines()
    else:
        show_repositories()

def show_repositories():
    
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
        
        # Show instruction
        st.info("👆 Click on any repository card above to start monitoring its pipelines")
    else:
        st.warning("⚠️ No repositories found. Make sure the backend is running.")

def show_pipelines():
    selected_repo = st.session_state.get('selected_repo')
    if not selected_repo:
        return
    
    # Show selected repository info with back button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(f"✅ Monitoring: **{selected_repo.get('full_name', selected_repo['name'])}** ({selected_repo.get('language', 'Unknown')})")
    with col2:
        if st.button("← Back to Repos"):
            del st.session_state.selected_repo
            st.rerun()
    
    # Fetch pipelines for selected repo
    with st.spinner(f'🔄 Loading pipelines for {selected_repo.get("full_name", selected_repo["name"])}...'):
        print(f"FRONTEND DEBUG: Fetching pipelines for owner={selected_repo.get('owner')}, name={selected_repo.get('name')}")
        pipelines = get_pipelines(selected_repo.get('owner'), selected_repo.get('name'))
        print(f"FRONTEND DEBUG: Received {len(pipelines)} pipelines from API")
    
    if not pipelines:
        st.warning(f"⚠️ No pipeline data found for {selected_repo.get('full_name', selected_repo['name'])}")
        st.info(f"Debug: API call was made to /pipelines?owner={selected_repo.get('owner')}&name={selected_repo.get('name')}")
        return
    
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
    

    # Pipeline Details
    st.markdown("### 🔍 Pipeline Details")
    
    for pipeline in pipelines:
        if not isinstance(pipeline, dict):
            continue
        status_emoji = {"success": "✅", "failed": "❌", "running": "🔄"}
        emoji = status_emoji.get(pipeline.get("status"), "❓")
        
        with st.expander(f"{emoji} {pipeline['name']}", expanded=False):
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
            {"role": "assistant", "content": f"👋 Hi! I'm Portia, your DevOps AI Assistant. I can see you're monitoring **{selected_repo.get('full_name', 'your repository')}** with {len(pipelines)} pipelines. How can I help you today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about pipelines..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        with st.spinner("🤖 Portia is thinking... (this may take a moment)"):
            response = get_portia_response(prompt, selected_repo, pipelines)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to display the new messages
        st.rerun()

if __name__ == "__main__":
    main()