# AI Academic Tutor 🎓

A complete, submission-ready AI-powered tutoring application designed to help students master academic concepts, answer specific homework questions, summarize notes, generate interactive practice quizzes, and suggest study exercises.

Built using **Streamlit**, **LangChain**, and **Groq LLM / OpenAI**.

---

## Project Overview

The AI Academic Tutor is an intelligent study assistant tailored to the Education sector. It bridges the gap between passive reading and active recall. By using advanced LLMs (Groq's Llama 3 or OpenAI's GPT-4o-mini), the app acts as a 24/7 personal tutor that can explain complex ideas simply, answer challenging educational questions, summarize long passages into digestible sections, and evaluate learning through interactive multiple-choice quizzes and critical-thinking exercises.

---

## Features

1. **Concept Explainer 🔍**: Explains academic concepts in clear, simple language customized to a specific educational grade tier (from Elementary School up to PhD levels), complete with real-world analogies.
2. **Q&A Homework Helper 💬**: Provides step-by-step, thorough answers to specific questions within a target topic.
3. **Notes Summarizer 📰**: Transforms long-form educational notes, articles, or chapters into structured summaries consisting of key takeaways, main thesis summary, and terminology glossaries.
4. **Interactive Quiz Generator (MCQs) ✍️**: Dynamically constructs multiple-choice questions based on the topic or provided notes. Questions are rendered as interactive web forms where students select answers, submit for grading, and review detailed diagnostic explanations.
5. **Practice Exercises Generator ✏️**: Creates open-ended practice questions that encourage deep thinking, including self-assessment study guides for each question.
6. **Dual LLM Provider Support**: Fully supports both **Groq LLM** (preferred, fast inference) and **OpenAI** (robust fallback) with customizable parameters (temperature, model choice, grade tier).

---

## Technologies Used

- **Streamlit**: For the clean, responsive, and modern user interface.
- **LangChain**: To construct prompt templates, chain executions, and manage LLM integration.
- **Groq API**: For ultra-fast execution of open-weight models (e.g., Llama 3).
- **OpenAI API**: For GPT models support.
- **Python-dotenv**: For environment variable management.

---

## Project Structure

```
Assignment 6/
├── app.py                  # Main Streamlit application file (UI and backend logic)
├── requirements.txt        # Project dependencies and version locks
├── README.md               # User manual and project documentation
├── reflection.md           # Project design rationale, learnings, and reflection
├── .env.example            # Configuration template for environment variables
└── .gitignore              # Ignored files configuration
```

---

## Installation

### 1. Prerequisites
Make sure you have Python 3.9+ installed on your machine.

### 2. Clone/Copy Project
Navigate to the `Assignment 6` folder in your terminal:
```bash
cd "Assignment 6"
```

### 3. Create a Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables

1. Copy the `.env.example` file to create your own configuration file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and enter your API keys:
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEY=your_groq_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

*Note: You can also override or enter your API keys directly in the sidebar of the running Streamlit application.*

---

## Running the Application

To launch the AI Tutor, run the following command in your terminal:
```bash
streamlit run app.py
```

The application will start, and a link will print in your terminal (typically `http://localhost:8501`) which opens automatically in your web browser.

---