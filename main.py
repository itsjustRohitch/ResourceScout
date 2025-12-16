"""
ResourceScout Application Entry Point.

This module serves as the frontend orchestrator for the Streamlit application.
It handles:
1. Session State management.
2. UI Layout (Sidebar vs Main Area).
3. Event handling (Button clicks, Chat input).
4. Interfacing with the business logic layer (service.py).

Dependencies:
- streamlit: UI framework.
- service: The bridge to core logic (caching & API handling).
- frontend: Pure UI styling resources.
"""

import streamlit as st
import random
import frontend
import service 

# ==========================================
# 1. APP CONFIGURATION & STATE
# ==========================================

st.set_page_config(
    page_title="ResourceScout", 
    page_icon="⚡", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize Session State variables if they don't exist
if "messages" not in st.session_state: 
    st.session_state.messages = []

if "context_cache" not in st.session_state: 
    st.session_state.context_cache = ""

if "file_list" not in st.session_state: 
    st.session_state.file_list = []

frontend.render_css()

# ==========================================
# 2. MAIN APPLICATION LOOP
# ==========================================

def main():
    """
    Main execution loop for the Streamlit app.
    Renders the sidebar first, then conditionally renders the 
    Landing Page or the Chat Interface based on chat history.
    """
    
    # --- SIDEBAR: Configuration & Knowledge Base ---
    with st.sidebar:
        # 1. Credentials
        st.markdown('<div class="sidebar-card"><span>🔑 API ACCESS</span></div>', unsafe_allow_html=True)
        api_key = st.text_input("Gemini API Key", type="password", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. File Upload
        st.markdown('<div class="sidebar-card"><span>📂 KNOWLEDGE BASE</span></div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Context", type=["pdf", "pptx", "png", "jpg"], label_visibility="collapsed")
        
        # Process file only if it's new (prevents re-indexing on every interaction)
        if uploaded_file and uploaded_file.name not in st.session_state.file_list:
            with st.spinner("Indexing..."):
                text = service.process_file(uploaded_file, api_key)
                if not text.startswith("Error"):
                    st.session_state.context_cache += f"\n\n--- {uploaded_file.name} ---\n{text}"
                    st.session_state.file_list.append(uploaded_file.name)
        
        # 3. Reset Controls
        st.markdown("---")
        if st.button("🗑️ Clear Memory", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # --- MAIN UI: Router Logic ---
    
    # CASE A: No messages yet -> Show Landing Page
    if not st.session_state.messages:
        st.markdown('<div class="hero-title">ResourceScout</div>', unsafe_allow_html=True)
        
        col1, = st.columns([1])
        with col1:
            # Primary Search Bar
            q = st.text_input("Search", placeholder="Ask anything...", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Action Dashboard (Quick Buttons)
            b1, b2, b3 = st.columns(3)
            with b1: 
                if st.button("📝 Summarize Docs", use_container_width=True): q = service.CMD_SUMMARIZE
            with b2: 
                if st.button("🧪 Generate Quiz", use_container_width=True): q = service.CMD_QUIZ
            with b3: 
                if st.button("🚀 Random Topic", use_container_width=True): 
                    q = f"Explain {random.choice(['Quantum Computing', 'Roman History', 'Neuroscience'])}"

            # Handle Submission
            if q and api_key:
                st.session_state.messages.append({"role": "user", "content": q})
                st.rerun()
            elif q and not api_key:
                st.error("Please enter API Key")

    # CASE B: Chat History exists -> Show Conversation
    else:
        # Render History
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
                # If message contains rich resource data, render multimedia
                if "data" in msg:
                    res = msg["data"]
                    
                    # Render YouTube Grid
                    if res.videos:
                        cols = st.columns(len(res.videos))
                        for idx, v in enumerate(res.videos):
                            with cols[idx]: st.video(v["url"]); st.caption(v["title"])
                    
                    # Render Article Links
                    with st.expander(f"📚 Sources"):
                        if res.articles:
                            for a in res.articles: 
                                st.markdown(f"- [{a['title']}]({a['link']})")
                        else:
                            st.caption("No sources found (or search failed).")

        # Handle Follow-up Input
        if query := st.chat_input("Next question..."):
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()

    # --- WORKER: Process New User Message ---
    # This block triggers the Service Layer when the last message is from the user
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Call the Service Layer (cached internally)
                result = service.handle_request(
                    st.session_state.messages[-1]["content"], 
                    st.session_state.context_cache, 
                    api_key
                )
                
                # Render Response
                st.markdown(result.explanation)
                
                # Save to History (including the 'data' object for persistence)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": result.explanation, 
                    "data": result
                })
                st.rerun()

if __name__ == "__main__":
    main()