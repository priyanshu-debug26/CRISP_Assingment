# Assignment 3: RAG PDF Chatbot

An intelligent, context-aware PDF Chatbot built with Python, Streamlit, and LangChain. The application implements a Retrieval-Augmented Generation (RAG) pipeline using ChromaDB as a vector store to allow users to ask questions about uploaded PDF documents and receive accurate, source-backed answers.

---

## 🌟 Features

* **PDF Document Upload**: Interactive sidebar to upload any standard text-based PDF.
* **Smart Text Chunking**: Automatically processes, cleans, and splits the extracted text into chunks with context overlap using LangChain's `RecursiveCharacterTextSplitter`.
* **Flexible Embedding Generation**:
  * **Groq Option**: Free, fast embedding generation using local HuggingFace `all-MiniLM-L6-v2` sentence-transformers (does not consume API limits).
  * **OpenAI Option**: Generates premium embeddings using OpenAI's `text-embedding-ada-002` API.
* **Vector Store Indexing**: Stores document embeddings inside a local ChromaDB instance.
* **Contextual Search**: Retrieves the top $k$ most relevant text blocks from the PDF for each user query.
* **Robust Error Handling**: Gracefully handles scenarios like empty PDFs, missing API keys, or service timeouts.
* **Interactive Web UI**: Elegant, dark-mode Streamlit dashboard with responsive layout and real-time step status feedback.

---

## 🛠️ Technologies Used

* **Python 3.8+**
* **Streamlit**: Web Application Framework.
* **LangChain**: RAG orchestration framework.
* **ChromaDB**: High-performance local vector database.
* **PyPDF**: PDF document parsing.
* **HuggingFace Transformers**: Local embedding models.
* **Groq API / OpenAI API**: Leading Large Language Model providers.

---

## 📂 Project Structure

```text
Assignment 3/
├── .env.example         # Template for configuration keys
├── .gitignore           # Exclusions for cache, venv, and vector database
├── app.py               # Main Streamlit web application code
├── README.md            # Project documentation and guide
├── reflection.md        # Reflection report summarizing implementation
└── requirements.txt     # Python dependencies
```

---

## 🚀 Installation & Setup

Follow these simple steps to set up the project locally:

### 1. Clone the Repository
Ensure you are in the project folder:
```bash
cd "Assignment 3"
```

### 2. Set Up a Virtual Environment
Create and activate a Python virtual environment:
```bash
# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to a new file named `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in your API keys:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
OPENAI_API_KEY=your_actual_openai_api_key_here
```

---

## 🎯 Running the Project

Start the Streamlit application with the following command:
```bash
streamlit run app.py
```
This will open the web interface in your default browser at `http://localhost:8501`.

---

## Screenshot

<img width="1920" height="980" alt="image" src="https://github.com/user-attachments/assets/546fe8c3-02a6-466d-aa81-75d08c6507c2" />
<img width="1920" height="979" alt="image" src="https://github.com/user-attachments/assets/43aab63c-6dab-4713-885a-22ee948b45e9" />

