"""
External Retrieval Module.

This module is responsible for fetching real-time data from the internet.
Key Features:
1. Trusted Source Filtering: Biases web searches towards academic/reputable domains.
2. STRICT English Filtering: Blocks foreign language results.
"""

from youtube_search import YoutubeSearch
from duckduckgo_search import DDGS
from typing import List, Dict
import re

# ==========================================
# 1. DOMAIN ALLOWLISTS
# ==========================================
TRUSTED_SITES = {
    "cs": [
        "geeksforgeeks.org", "w3schools.com", "freecodecamp.org", 
        "stackoverflow.com", "realpython.com", "medium.com", "tutorialspoint.com"
    ],
    "math": [
        "khanacademy.org", "wolfram.com", "brilliant.org", 
        "libretexts.org", "tutorial.math.lamar.edu"
    ],
    "physics": [
        "physicsclassroom.com", "hyperphysics.phy-astr.gsu.edu", 
        "britannica.com", "nasa.gov", "cern.ch"
    ],
    "general": [
        "britannica.com", "bbc.com", "nytimes.com", "investopedia.com"
    ],
    # (You can keep the other categories if you want, or stick to these core ones)
}

# ==========================================
# 2. HELPER: STRICT LANGUAGE FILTER
# ==========================================
def is_english(text):
    """
    Returns True ONLY if the text is composed of standard English characters.
    This aggressively filters out Chinese, Russian, Arabic, etc.
    """
    try:
        # If the text can be encoded to ASCII, it's safe (English/Numbers/Symbols).
        # If it crashes, it contains foreign characters.
        text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

# ==========================================
# 3. SEARCH FUNCTIONS
# ==========================================

def search_youtube(query: str, max_results: int = 2) -> List[Dict]:
    """Raw YouTube search."""
    videos = []
    try:
        results = YoutubeSearch(query, max_results=max_results).to_dict()
        for r in results:
            videos.append({
                "url": f"https://www.youtube.com/watch?v={r['id']}", 
                "title": r['title'], 
                "thumb": r['thumbnails'][0]
            })
    except Exception:
        pass 
    return videos

def search_web(query: str, category: str) -> List[Dict]:
    """
    Performs a web search with STRICT English enforcement.
    """
    trusted_domains = TRUSTED_SITES.get(category.lower(), TRUSTED_SITES["general"])
    
    # Strategy A: Strict Academic Search
    site_string = " OR ".join([f"site:{d}" for d in trusted_domains[:4]])
    smart_query = f"{query} ({site_string})"
    
    links = []
    
    try:
        # Attempt 1: Trusted Sites (forced region: us-en)
        with DDGS() as ddgs:
            results = list(ddgs.text(smart_query, region='us-en', max_results=4))
            
            if results:
                for r in results:
                    # Double Check: Only add if title is English
                    if is_english(r['title']):
                        links.append({"title": r['title'], "link": r['href']})
                
                # If we found valid links, return them
                if links: return links
            
    except Exception as e:
        print(f"⚠️ Trusted search failed: {e}")

    # Strategy B: General Fallback (Strict English)
    if not links:
        print("⚠️ Falling back to general web search (English Only)...")
        try:
            with DDGS() as ddgs:
                # region='us-en' is the key here!
                for r in ddgs.text(query, region='us-en', max_results=5):
                    # Final Filter: discard anything suspicious
                    if is_english(r['title']):
                        links.append({"title": r['title'], "link": r['href']})
                        
        except Exception as e:
            print(f"🚨 General search failed: {e}")
            
    return links