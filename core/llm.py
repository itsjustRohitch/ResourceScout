"""
LLM Handler Module.

This module encapsulates all interactions with the Google Gemini API.
It implements a "Two-Brain" architecture:
1. JSON Model: For structured data extraction (categorization, query generation).
2. Text Model: For creative writing (summaries, quizzes).

Dependencies:
- google-generativeai: The official SDK for Gemini.
- dataclasses: For structured data passing.
"""

import google.generativeai as genai
import json
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# ==========================================
# 1. DATA STRUCTURES
# ==========================================

@dataclass
class ResourceResult:
    """
    Standardized response object passed between the Engine and UI.
    This ensures that regardless of the action (Research, Quiz, Summary),
    the UI always receives the same shape of data.
    """
    explanation: str
    category: str = "general"
    book: Optional[str] = None
    videos: List[Dict[str, str]] = field(default_factory=list)
    articles: List[Dict[str, str]] = field(default_factory=list)

# ==========================================
# 2. GEMINI WRAPPER
# ==========================================

class GeminiHandler:
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            # Brain 1: The "Architect"
            # Configured to force JSON output. This guarantees parsing reliability.
            self.json_model = genai.GenerativeModel(
                model_name, 
                generation_config={"response_mime_type": "application/json"}
            )
            
            # Brain 2: The "Writer"
            # Standard configuration for free-form text generation.
            self.text_model = genai.GenerativeModel(model_name)

    def _generate_with_retry(self, model, prompt, retries=3):
        """Helper to retry API calls if we hit a rate limit (Quota Error)."""
        for attempt in range(retries):
            try:
                return model.generate_content(prompt)
            except Exception as e:
                # Check if it's a 429 Quota Error
                if "429" in str(e) or "Quota" in str(e):
                    if attempt < retries - 1:
                        wait_time = (attempt + 1) * 5  # Wait 5s, then 10s...
                        print(f"⚠️ Quota hit. Waiting {wait_time}s to retry...")
                        time.sleep(wait_time)
                        continue
                # If it's not a quota error, or we ran out of retries, raise it
                raise e
        return None

    def analyze_query(self, query: str, context: str) -> Optional[Dict]:
        """
        Uses the JSON-enforced model to analyze the user's intent.
        Handles both academic research requests AND casual chat.
        """
        if not self.api_key: return None
        
        prompt = f"""
        Role: ResourceScout, a helpful and encouraging academic research assistant.
        Query: {query}
        Context: {context[:50000]}
        
        Instructions:
        1. If the user input is a greeting (hi, hello), gratitude (thanks), or small talk:
           - Set "category" to "chat".
           - Write a warm, friendly response in "explanation" (e.g., "You're welcome! Happy to help you learn.").
           - Set other fields to null.
           
        2. If the user input is an educational question:
           - Set "category" to "cs", "math", "science", or "general".
           - Generate the research queries as usual.
        
        Return JSON: {{
            "category": "cs|math|science|general|chat",
            "explanation": "Detailed academic summary (approx 200 words) OR friendly chat response.",
            "book": "Standard textbook title (or null if chat).",
            "youtube_query": "Search query for video (or null if chat).",
            "web_query": "Search query for articles (or null if chat)."
        }}
        """
        try:
            # Use the retry helper to ensure reliability
            res = self._generate_with_retry(self.json_model, prompt)
            return json.loads(res.text)
        except Exception as e:
            print(f"🚨 JSON Gen Error: {e}")
            return None

    def generate_text(self, prompt: str) -> str:
        """
        Uses the creative text model for tasks that don't need structure.
        Used for: Summaries, Quizzes, Random Topics.
        """
        if not self.api_key: return "API Key missing."
        try:
            # Use the retry helper
            res = self._generate_with_retry(self.text_model, prompt)
            return res.text
        except Exception as e:
            return f"Generation failed: {str(e)}"