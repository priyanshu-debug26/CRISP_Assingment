# Assignment 5: Weather API Tool Integration

A modular AI assistant that integrates with real-time REST API interfaces to fetch, parse, and answer questions about local weather. Built with Python, Streamlit, and LangChain Agents, the application connects to the Open-Meteo REST APIs to get current temperature, conditions, humidity, and wind speeds with zero configuration or keys required.

---

## 🌟 Features

* **Direct Weather Dashboard**: Input a city and fetch immediate weather metrics showing Temperature, Condition, Humidity, and Wind Speed in beautiful visual cards.
* **Conversational AI Agent**: Natural language chat interface. Ask weather questions (e.g. *"Should I pack an umbrella for Rome today?"*) and the agent will dynamically query the Weather API to answer.
* **Keyless REST API Integration**: Leverages Open-Meteo's free geocoding and forecasting API endpoints, running out-of-the-box without requiring API sign-ups.
* **Robust Error Validation**: Catches incorrect city names, missing connection credentials, empty queries, or network timeouts.

---

## 🛠️ Technologies Used

* **Python 3.8+**
* **Streamlit**: Web dashboard framework.
* **LangChain Agents**: Frame for tool execution loops.
* **requests**: Python HTTP library to interact with REST APIs.
* **Groq API / OpenAI API**: Cognitive reasoning engines.

---

## 📂 Project Structure

```text
Assignment 5/
├── .env.example         # Environment keys template
├── .gitignore           # Python caches and local venv rules
├── app.py               # Main modular application containing helpers and UI
├── README.md            # Installation and setup documentation
├── reflection.md        # Technical explanation and learning report
└── requirements.txt     # Python dependencies
```

---

## 🚀 Installation & Setup

### 1. Navigate to Project Folder
```bash
cd "Assignment 5"
```

### 2. Set Up a Virtual Environment
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

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
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

Start the web server:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

