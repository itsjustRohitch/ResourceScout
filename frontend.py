import streamlit as st

def render_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Space Grotesk', sans-serif;
            color: #1f1f1f; 
        }
        
        .stApp { background-color: #f7d1ba; } /* Slightly lighter background */
        
        /* --- SIDEBAR --- */
        [data-testid="stSidebar"] {
            background-color: #f7d1ba;
            border-right: 2px solid #000;
        }

        /* LABEL CARDS (The White Boxes for Headers) */
        .sidebar-card {
            background-color: #FFFFFF;
            border: 2px solid #000;
            box-shadow: 4px 4px 0px #000;
            padding: 10px;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 5px; /* Tiny gap before input */
            display: inline-block;
            width: 100%;
            color: black;
            text-shadow: 2px 2px 0px #FFD54F;
        }
        .sidebar-card span { border-bottom: 3px solid #FFD54F; }

        /* INPUTS (Dark Mode Style to match Screenshot) */
        [data-testid="stSidebar"] .stTextInput input, 
        [data-testid="stSidebar"] .stFileUploader {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border: 2px solid #000 !important;
            border-radius: 8px !important;
        }
        
        /* HEADER TITLES */
        .hero-title {
            font-size: 4rem;
            font-weight: 800;
            text-align: center;
            margin-top: 40px;
            color: #000;
            text-shadow: 3px 3px 0px #FFD54F;
        }
        .hero-subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 30px;
        }
        
        /* MAIN ACTION BUTTONS (Yellow Brutalist) */
        .action-btn-container {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        .stButton button {
            background-color: #FFD54F !important;
            color: #000 !important;
            border: 2px solid #000 !important;
            box-shadow: 4px 4px 0px #000 !important;
            font-weight: 600 !important;
            border-radius: 0px !important; /* Sharp edges like screenshot */
            transition: all 0.1s;
        }
        .stButton button:hover {
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0px #000 !important;
        }
        .stButton button:active {
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px #000 !important;
        }

        /* SEARCH BAR (Main) */
        .stTextInput input {
            border: 2px solid #000 !important;
            padding: 15px !important;
            background-color: #222 !important; /* Dark input */
            color: white !important;
            border-radius: 10px !important;
        }

        /* CHAT MESSAGES - FIXED */
        [data-testid="stChatMessage"] {
            background-color: #ffffff !important;
            border: 2px solid #000 !important;
            box-shadow: 4px 4px 0px #ddd !important;
        }
        
        /* Force all text inside chat messages to be black */
        [data-testid="stChatMessage"] p, 
        [data-testid="stChatMessage"] div,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] li {
            color: #000000 !important;
        }
    </style>
    """, unsafe_allow_html=True)