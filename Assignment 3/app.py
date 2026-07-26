import streamlit as st
import os
import shutil
import tempfile
from dotenv import load_dotenv

# Import LangChain utilities
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# App Page Configuration
st.set_page_config(
    page_title="RAG PDF Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Premium CSS Injection
st.markdown("""
<style>
    /* Gradient Background and Theme Settings */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
        color: #f8fafc;
    }
    
    /* Elegant Title and Header styling */
    .app-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: fadeIn 1.5s ease-in-out;
    }
    .app-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Card Styles */
    .status-card {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Custom Chat Bubble Styles */
    .user-bubble {
        background-color: rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.4);
        border-radius: 12px 12px 0 12px;
        padding: 10px 15px;
        margin: 8px 0;
        color: #e2e8f0;
        display: inline-block;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .assistant-bubble {
        background-color: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.4);
        border-radius: 12px 12px 12px 0;
        padding: 10px 15px;
        margin: 8px 0;
        color: #e2e8f0;
        display: inline-block;
        max-width: 80%;
        float: left;
        clear: both;
    }
    
    /* Animation Keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Define directories
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".chromadb")

def clear_vector_store():
    """Helper function to clean up the existing Chroma database files."""
    if os.path.exists(DB_DIR):
        try:
            shutil.rmtree(DB_DIR)
        except Exception as e:
            st.sidebar.error(f"Error clearing database files: {e}")

# Initialize Session States
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_filename" not in st.session_state:
    st.session_state.processed_filename = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None

# Sidebar Title & Configuration
st.sidebar.markdown("<h2 style='color:#38bdf8; font-weight:700;'>⚙️ Configuration</h2>", unsafe_allow_html=True)

# LLM Provider Selection
provider = st.sidebar.selectbox(
    "Select LLM Provider:",
    ["Groq", "OpenAI"],
    index=0,
    help="Select the AI service you want to use for model processing and response generation."
)

# API Key input depending on selection
api_key = ""
if provider == "Groq":
    env_key = os.getenv("GROQ_API_KEY", "")
    api_key = st.sidebar.text_input("Groq API Key:", value=env_key, type="password", help="Enter your Groq API Key.")
else:
    env_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.sidebar.text_input("OpenAI API Key:", value=env_key, type="password", help="Enter your OpenAI API Key.")

# Upload PDF
st.sidebar.markdown("<hr style='border: 1px solid rgba(148, 163, 184, 0.1);'>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='color:#818cf8; font-weight:600;'>📁 Upload Document</h3>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a PDF file:", type=["pdf"])

# Clear DB Button
if st.sidebar.button("🧹 Clear Chat & Index", use_container_width=True):
    clear_vector_store()
    st.session_state.chat_history = []
    st.session_state.processed_filename = None
    st.session_state.retriever = None
    st.sidebar.success("Chat history and Vector Database index cleared!")
    st.rerun()

# ----------------- Document Processing & RAG Pipeline Setup -----------------

if uploaded_file is not None:
    # Check if this file has already been successfully processed
    if st.session_state.processed_filename != uploaded_file.name:
        with st.sidebar.status("🔄 Processing PDF... Please wait.", expanded=True) as status_box:
            try:
                # 1. Verification: Make sure API Key is provided
                if not api_key:
                    st.error(f"Missing API key for {provider}. Please enter it in the sidebar or check your .env configuration.")
                    status_box.update(label="❌ Failed: Missing API Key", state="error")
                    st.stop()
                
                # 2. Save Uploaded File to Temp Location for PyPDFLoader
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                # 3. Read and extract text from PDF
                status_box.write("📖 Reading and extracting text from PDF...")
                loader = PyPDFLoader(tmp_path)
                documents = loader.load()
                
                # Clean up temporary file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

                # Verification: Check if PDF is empty
                if not documents or not any(doc.page_content.strip() for doc in documents):
                    st.error("The uploaded PDF appears to be empty or has no readable text extraction. Please try another PDF.")
                    status_box.update(label="❌ Failed: Empty PDF", state="error")
                    st.stop()

                # 4. Split text into chunks
                status_box.write("✂️ Splitting text into chunks...")
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_splitter.split_documents(documents)
                status_box.write(f"Generated {len(chunks)} chunks.")

                # 5. Generate embeddings and setup ChromaDB
                status_box.write("🧠 Generating embeddings and indexing chunks...")
                
                # Clear previous database files
                clear_vector_store()
                
                # Initialize Embeddings
                if provider == "OpenAI":
                    from langchain_openai import OpenAIEmbeddings
                    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
                else:
                    # Using lightweight sentence-transformers for Groq since Groq lacks native embeddings endpoint
                    from langchain_huggingface import HuggingFaceEmbeddings
                    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

                # Store embeddings in ChromaDB
                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    persist_directory=DB_DIR
                )
                
                # Setup Retriever
                st.session_state.retriever = vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 4}
                )
                
                # Update Session State
                st.session_state.processed_filename = uploaded_file.name
                status_box.update(label="✅ PDF Processed Successfully!", state="complete")
                st.sidebar.success(f"Loaded: {uploaded_file.name}")
                st.session_state.chat_history = []  # Reset chat history for the new PDF
                st.rerun()

            except Exception as e:
                st.error(f"An error occurred while processing the PDF: {e}")
                status_box.update(label="❌ Failed with error", state="error")
                st.stop()

# ----------------- UI Content Area -----------------

# Header
st.markdown("<h1 class='app-title'>🤖 RAG PDF Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Upload a PDF in the sidebar, ask questions, and get precise context-backed answers.</p>", unsafe_allow_html=True)

# Main Application Flow UI
if st.session_state.retriever is None:
    # Dashboard Info when no PDF is loaded
    st.markdown("""
    <div class='status-card'>
        <h3>👋 Welcome to the RAG PDF Chatbot!</h3>
        <p>To start interacting with your documents, please complete the following steps in the sidebar:</p>
        <ol>
            <li>Select your preferred <b>LLM Provider</b> (Groq or OpenAI).</li>
            <li>Ensure the corresponding <b>API Key</b> is supplied (either loaded from <code>.env</code> or typed in).</li>
            <li>Upload any <b>PDF file</b>.</li>
        </ol>
        <p><i>Note: Choosing Groq uses the ultra-fast local <b>all-MiniLM-L6-v2</b> HuggingFace model for generating embeddings, completely free of charge!</i></p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Layout for active PDF Chatting
    st.markdown(f"**Current Indexed Document:** `{st.session_state.processed_filename}`")
    
    # Display Chat Messages
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # User Input
    if user_query := st.chat_input("Ask a question about the document..."):
        # Append User message to history
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        # 1. Verify API Key
        if not api_key:
            error_msg = f"API key for {provider} is missing. Please provide it in the sidebar."
            st.error(error_msg)
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            st.stop()

        # 2. Initialize LLM Model
        try:
            if provider == "OpenAI":
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0,
                    api_key=api_key
                )
            else:
                from langchain_groq import ChatGroq
                llm = ChatGroq(
                    model="llama-3.1-8b-instant",
                    temperature=0,
                    groq_api_key=api_key
                )
        except Exception as e:
            error_msg = f"Failed to initialize the LLM model: {e}"
            st.error(error_msg)
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            st.stop()

        # 3. Create RAG QA Chain
        # Define Prompt Template
        template = """You are an advanced AI assistant designed to answer questions using ONLY the provided context from a PDF document.

Context:
{context}

Question: {question}

Instructions:
1. Formulate your answer based ONLY on the provided Context.
2. If the answer cannot be found in the Context, state clearly: "I cannot find the answer to this question in the provided PDF document."
3. Do not make up answers or use external knowledge outside the Context.
4. Keep the answer clear, professional, and structured.

Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)

        # Build chain using LangChain Expression Language (LCEL)
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": st.session_state.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # Generate LLM answer with loading spinner
        with st.spinner("🔍 Analyzing document context and generating response..."):
            try:
                response = rag_chain.invoke(user_query)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.chat_message("assistant").write(response)
            except Exception as e:
                error_msg = f"Failed to generate response: {e}"
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
