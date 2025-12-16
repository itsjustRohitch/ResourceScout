# ResourceScout

**Theme:** Hyper-Personalized Learning  
**Hackathon:** GenAI Frontiers: App Development using the Gemini API

ResourceScout is an autonomous academic research assistant that transforms static course materials (PDFs, images, handouts) into interactive learning experiences. It leverages the multimodal capabilities of **Google Gemini 2.5 Flash** to "see" documents, understand context, and autonomously curate high-quality study resources from across the web.

---

## ⚠️ Mandatory API Disclaimer
**This project requires a valid Google Gemini API Key to function.** User API keys are used strictly for the current session to authenticate requests with Google's Generative AI services. Keys are **never stored**, logged, or saved to any persistent database.

---

## 🌟 Key Features

* **👁️ Multimodal Document Intelligence:** * Uses **Gemini 2.5 Flash** to perform OCR on handwritten notes and analyze complex PDF diagrams.
    * Understand context from visual inputs (charts, graphs) as well as text.

* **🧠 "Two-Brain" Architecture:**
    * **Architect Brain (JSON Mode):** Handles structured logic, intent classification, and generates precise search queries.
    * **Writer Brain (Creative Mode):** Generates human-like summaries, quizzes, and explanations.

* **🕵️ Autonomous Research Agent:**
    * Automatically detects the hardest concepts in your document.
    * Performs real-time, region-locked (US-EN) web searches to find verified academic articles.
    * Fetches relevant YouTube video tutorials automatically.

* **🛡️ Fail-Safe Resiliency:** * Features a robust fallback system that generates direct deep-links to reputable sources (Khan Academy, Google Scholar) if external search APIs experience downtime or rate limits.

* **🎨 Brutalist Dark Mode UI:** * A high-contrast, focus-driven interface built with Streamlit custom CSS.

---

## 🛠️ Tech Stack

* **Core Engine:** Google Gemini 2.5 Flash (`google-generativeai`)
* **Frontend:** Streamlit
* **Search Tools:** `duckduckgo-search` (Web), `Youtube-python` (Video)
* **Processing:** `Pillow` (Image Processing), `PyPDF2` (Document Parsing)

---

## 📂 Repository Structure

A quick guide to the codebase architecture:

```text
ResourceScout/
├── main.py              # 🖥️ The Entry Point: Handles the Streamlit UI, State Management, and Layout.
├── service.py           # ⚙️ The Controller: Connects the UI to the Core logic; handles caching and error recovery.
├── core/                # 🧠 The Core Engine (Backend Logic)
│   ├── llm.py           #    - Gemini Handler: Manages the "Two-Brain" (JSON vs Text) logic and Retry loops.
│   ├── retrieval.py     #    - Search Engine: Handles DuckDuckGo (Web) and YouTube searching with strict region filtering.
│   └── files.py         #    - I/O Layer: Processes PDF parsing and Image OCR using Gemini Vision.
├── requirements.txt     # 📦 Dependencies: List of required Python libraries.
└── .gitignore           # 🛡️ Safety: Prevents uploading venv, secrets, and cache files.

---

## 🚀 How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/resourcescout.git](https://github.com/yourusername/resourcescout.git)
    cd resourcescout
    ```

2.  **Set Up Environment**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App**
    ```bash
    streamlit run main.py
    ```

5.  **Authenticate:** Enter your Gemini API Key in the sidebar to activate the agent.

---

## 💡 Usage Examples

1.  **Syllabus Extraction:** Upload a course handout and click **"Summarize Docs"**. The agent will extract the core syllabus and find resources for the most complex topic.
2.  **Exam Prep:** Upload a photo of a math problem and ask: *"Give me 5 similar numerical problems to practice."*
3.  **Concept Deep-Dive:** Ask any question, and the agent will return a text explanation + a video tutorial + an academic article.

---

## 🏆 Project Status

Submitted for the **GenAI Frontiers Hackathon 2025**.
* **Model Used:** Gemini 2.5 Flash
* **Agent Type:** Multi-step Retrieval Augmented Generation (RAG)
