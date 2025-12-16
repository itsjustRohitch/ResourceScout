"""
Service Layer: Integration & Caching.
"""

import streamlit as st
import urllib.parse
from core import files, retrieval, llm

# ==========================================
# 1. CONSTANTS & CONFIGURATION
# ==========================================

CMD_SUMMARIZE = "Summarize the uploaded documents."
CMD_QUIZ = "Generate a quiz based on the context."

# ==========================================
# 2. CACHING WRAPPERS
# ==========================================

@st.cache_data(ttl=3600, show_spinner=False)
def cached_video_search(query: str):
    return retrieval.search_youtube(query)

@st.cache_data(ttl=3600, show_spinner=False)
def cached_web_search(query: str, category: str):
    return retrieval.search_web(query, category)

@st.cache_resource
def get_llm_handler(api_key: str):
    return llm.GeminiHandler(api_key)

# ==========================================
# 3. BUSINESS LOGIC
# ==========================================

def handle_request(query: str, context: str, api_key: str) -> llm.ResourceResult:
    """
    The central brain. 
    Includes a Universal Fallback to handle complex generation requests.
    """
    handler = get_llm_handler(api_key)
    
    # --- HELPER: Fail-Safe Link Generator ---
    def ensure_links(topic, current_links):
        """If no links found, generate direct search links so the UI is never empty."""
        if not current_links:
            safe_topic = urllib.parse.quote(topic)
            return [
                {
                    "title": f"📖 Learn '{topic}' on Khan Academy", 
                    "link": f"https://www.khanacademy.org/search?page_search_query={safe_topic}"
                },
                {
                    "title": f"🎓 Academic Papers: {topic}", 
                    "link": f"https://scholar.google.com/scholar?q={safe_topic}"
                }
            ]
        return current_links

    # --- ROUTE 1: SUMMARIES (Syllabus Mode) ---
    if query == CMD_SUMMARIZE:
        prompt = f"""
        Analyze the document and extract the Technical Syllabus.
        Ignore admin details. Focus on core modules.
        
        Format:
        1. List 3-5 key technical modules.
        2. Briefly explain sub-topics.
        
        CRITICAL: On the very last line, output the search tag like this:
        SEARCH_QUERY: <Insert the hardest technical topic here>
        
        Document Context:
        {context[:20000]}
        """
        
        full_response = handler.generate_text(prompt)
        clean_response = full_response.replace("**SEARCH_QUERY:**", "SEARCH_QUERY:")
        
        # Default fallback
        search_topic = "Computer Science Core"
        summary_text = full_response

        if "SEARCH_QUERY:" in clean_response:
            parts = clean_response.split("SEARCH_QUERY:")
            summary_text = parts[0].strip()
            search_topic = parts[1].strip()

        # FORCE BOTH:
        videos = cached_video_search(search_topic)
        raw_articles = cached_web_search(search_topic, "cs")
        articles = ensure_links(search_topic, raw_articles)
            
        return llm.ResourceResult(
            explanation=summary_text, 
            category="Syllabus",
            videos=videos,
            articles=articles
        )
        
    # --- ROUTE 2: QUIZ ---
    elif query == CMD_QUIZ:
        text = handler.generate_text(f"Create a 3-question quiz based on:\n{context[:5000]}")
        return llm.ResourceResult(explanation=text, category="Quiz")

    # --- ROUTE 3: INTELLIGENT RESEARCH ---
    data = handler.analyze_query(query, context)
    
    # --- ROUTE 4: UNIVERSAL FALLBACK (The Fix for "Failed to Analyze") ---
    # If the JSON model fails (returns None), we switch to the Text model.
    if not data:
        print("⚠️ JSON Analysis failed. Switching to Direct Text Generation.")
        fallback_text = handler.generate_text(f"Context: {context[:10000]}\n\nUser Request: {query}")
        
        # We still want resources, so we use the raw user query
        videos = cached_video_search(query)
        raw_articles = cached_web_search(query, "general")
        articles = ensure_links(query, raw_articles)
        
        return llm.ResourceResult(
            explanation=fallback_text,
            category="general",
            videos=videos,
            articles=articles
        )

    # --- ROUTE 5: STANDARD SUCCESS FLOW ---
    # Chat Bypass
    if data.get("category") == "chat":
        return llm.ResourceResult(
            explanation=data.get("explanation", "Hello!"),
            category="chat"
        )

    # Force Video Search
    yt_query = data.get("youtube_query")
    if not yt_query: yt_query = query 
    videos = cached_video_search(yt_query)
    
    # Force Web Search (+ Fail-Safe)
    web_query = data.get("web_query")
    if not web_query: web_query = query
    
    raw_articles = cached_web_search(web_query, data.get("category", "general"))
    articles = ensure_links(web_query, raw_articles)

    return llm.ResourceResult(
        explanation=data.get("explanation", ""),
        category=data.get("category", "general"),
        book=data.get("book"),
        videos=videos,
        articles=articles
    )

def process_file(file, api_key):
    return files.parse_file(file, api_key)