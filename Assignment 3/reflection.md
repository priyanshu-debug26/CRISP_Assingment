# Reflection Report - Assignment 3: RAG PDF Chatbot

## 1. What Was Built
I designed and implemented a fully functional Retrieval-Augmented Generation (RAG) system inside a Streamlit web application. The core system allows users to upload any text-based PDF document, automatically processes its contents, indices them in a local high-performance vector store (ChromaDB), and enables interactive, context-backed chatting about the PDF using Groq (Llama 3) or OpenAI (GPT-3.5-Turbo).

Key components built:
* **PDF Ingestion & Preprocessing**: Integrates PyPDF to read and parse local files statefully.
* **Smart Text Chunking**: Combines RecursiveCharacterTextSplitter with overlap controls to preserve context boundaries between chunks.
* **Dual Embeddings Support**: Uses HuggingFace sentence-transformers (`all-MiniLM-L6-v2`) locally to provide zero-cost, API-key-free embeddings for Groq, and supports OpenAI embeddings when the OpenAI pipeline is selected.
* **Vector Indexing & Retrieval**: Stores the embeddings locally in a structured database and sets up a query retriever.
* **LCEL Chain**: Implements LangChain Expression Language to link retrieval, prompt templating, and completion into an optimized execution pipeline.

---

## 2. What Was Learned
* **State Management in Streamlit**: Learned how to leverage `st.session_state` to store the PDF state, DB retriever reference, and chat history. Streamlit reruns the script on every input, so keeping database connections persistent and not re-indexing on every user message is critical.
* **RAG Pipeline Mechanics**: Gained deep insight into how document chunking size and overlap affect retrieval precision. A chunk size of 1000 with a 200 character overlap preserves enough context without exceeding model context limits.
* **Local vs. API-based Embeddings**: Explored using local HuggingFace embeddings which run completely free in CPU memory. This makes local deployments cost-efficient and solves the issue where some providers (like Groq) do not offer embedding endpoints.

---

## 3. Challenges Faced
* **Vector Store Locks & Reruns**: When modifying/re-uploading PDFs, ChromaDB sometimes locks file handles on disk. This was resolved by implementing a helper function `clear_vector_store` to safely clear indices before starting a new document session.
* **Streamlit Dynamic Reruns with File Uploaders**: File uploaders reload components, which can cause embeddings to regenerate repeatedly. Wrapping the process in a file name comparison check (`st.session_state.processed_filename != uploaded_file.name`) ensured files are only chunked and embedded once upon initial upload.
* **Handling Empty/Scanned PDFs**: Standard text extractors fail on scanned images inside PDFs. I implemented validation checks that raise user-friendly warnings if a PDF contains zero readable characters, avoiding application failures.

---

## 4. Possible Future Improvements
* **Optical Character Recognition (OCR)**: Integrate `pytesseract` or `easyocr` to support scanned PDFs and handwritten notes.
* **Source Citation Highlighting**: Display the exact page numbers and snippet quotes from the source PDF alongside the generated answer, helping users verify answers.
* **Conversational Memory**: Feed the existing chat history back into the model to support follow-up questions (e.g. "What did they say about the first point?").
* **Multiple Document Indexing**: Enable users to upload multiple files simultaneously to build a cross-document knowledge base.
