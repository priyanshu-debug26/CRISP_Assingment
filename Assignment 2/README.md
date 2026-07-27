# AI Java Code Mentor ☕

AI Java Code Mentor is a modern, clean, and interactive Streamlit web application that serves as a personal AI assistant for Java developers. Powered by Large Language Models on the ultra-fast Groq API, it offers step-by-step code explanations, bug identification, performance optimization suggestions, and comment/Javadoc generation.

---

## 🚀 Features

- **Explain Code:** Breaks down Java code step-by-step, explaining structures, logic, and core OOP/programming concepts.
- **Find Bugs:** Performs syntax, logic, and semantic checks, pointing out issues, explaining them, and displaying corrected code.
- **Optimize Code:** Suggests enhancements for time complexity, space complexity, and modern Java syntax (like streams and pattern matching).
- **Generate Comments:** Injects clean, industry-standard Javadoc headers and inline comments into the code without altering logic.
- **Modern User Interface:** Centered, minimal, and fully styled UI with sidebars, warning states, loading animations, and syntax-highlighted code outputs.
- **Graceful Error Handling:** Full handling for connection errors, API authentication issues, and empty code inputs.

---

## 📁 Project Structure

```text
Assingment 2/
├── app.py              # Main Streamlit web application code
├── llm.py              # Handles Groq API connection and API responses
├── prompts.py          # Stores System and User prompts for analysis tasks
├── .env                # Stores your private Groq API key (excluded from git)
├── requirements.txt    # Lists all required Python dependencies
└── README.md           # Instructions and documentation
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Navigate to the project directory
```bash
cd "Assingment 2"
```

### 3. Create and activate a Virtual Environment (Recommended)
**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure your Groq API Key
1. Open the `.env` file in the root of the project.
2. Locate the line: `GROQ_API_KEY=your_groq_api_key_here`
3. Replace `your_groq_api_key_here` with your actual Groq API key (starts with `gsk_...`). 
   *Note: If you do not have an API key, generate one at [console.groq.com](https://console.groq.com/) for free.*

---

## 🖥️ Running the Application

Once your virtual environment is active and your API key is added, launch the Streamlit app:

```bash
streamlit run app.py
```

This will automatically open your default browser to `http://localhost:8501`. If it doesn't open automatically, command-click or copy-paste that link.

---

## Screenshots

<img width="1920" height="983" alt="image" src="https://github.com/user-attachments/assets/efa109f9-918e-4689-9f5e-5fe454962d52" />
<img width="1920" height="977" alt="image" src="https://github.com/user-attachments/assets/151979fe-97cf-407e-8715-11f1615703b2" />
<img width="1920" height="980" alt="image" src="https://github.com/user-attachments/assets/abb58560-dfaf-40ac-b180-0e5474f499ed" />

---

## 🧠 Technologies Used
- **Streamlit**: For the interactive web application interface.
- **Groq API**: For lightning-fast LLM inference using LPU accelerators.
- **python-dotenv**: To load environment variables securely.
