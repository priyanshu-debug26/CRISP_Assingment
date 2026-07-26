# Assignment 4: Agentic AI Chatbot

An interactive, multi-tool conversational AI Agent built with Python, Streamlit, and LangChain Agents. The application demonstrates the core concepts of modern **Agentic AI**—combining Large Language Models with **Tools**, dynamic session **Memory**, and explicit step-by-step **Planning** before arriving at responses.

---

## 🌟 Features

* **Natural Language Processing**: Chat with an AI agent naturally.
* **Autonomous Tool Selection**: The agent decides if and when to invoke tools based on the query.
* **Three Built-in Tools**:
  * **Calculator**: Safe mathematical expression evaluation using Python's `numexpr` library.
  * **Current Date & Time**: Real-time access to the local clock.
  * **Wikipedia Search**: Retrieval tool that fetches Wikipedia page summaries.
* **Conversation Memory**: Remembers past conversational context statefully throughout the session.
* **Planning Visualization**: Shows the agent's real-time reasoning loops, including intermediate thoughts, selected tool actions, and raw observations directly in the UI.
* **Robust Error Handling**: Handles missing API keys, empty prompts, invalid math equations, or failed tool calls gracefully.

---

## 🛠️ Technologies Used

* **Python 3.8+**
* **Streamlit**: Web application dashboard.
* **LangChain Agents**: Frame for building autonomous agents.
* **numexpr**: High-performance mathematical compiler.
* **wikipedia**: Knowledge base api.
* **Groq API / OpenAI API**: Underlying intelligence engines.

---

## 📂 Project Structure

```text
Assignment 4/
├── .env.example         # Configuration environment keys template
├── .gitignore           # Python caches and venv exclusions
├── app.py               # Main modular application script
├── README.md            # Project documentation and guide
├── reflection.md        # Technical explanation report
└── requirements.txt     # Python dependencies
```

---

## 🚀 Installation & Setup

### 1. Navigate to Project Directory
```bash
cd "Assignment 4"
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment:
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Configuration
Copy the template `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in your API keys:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
OPENAI_API_KEY=your_actual_openai_api_key_here
```

---

## 🎯 Running the Application

Launch the Streamlit app:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---
