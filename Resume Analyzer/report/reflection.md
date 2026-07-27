# Capstone Reflection Report: AI Resume Analyzer

## 1. Objective
The objective of this capstone project is to develop a professional-grade, deployment-ready **AI Resume Analyzer**. The application serves job seekers by providing immediate recruiter-level feedback, assessing ATS compatibility, scanning for key skills, and suggesting targeted enhancements. It helps candidates identify structural and content weaknesses, align keyword density to automated scanners, and identify suitable job targets based on experience history.

---

## 2. Project Summary
The application is structured into a modular Python project:
- **`app.py`**: Streamlit-based web dashboard styled with CSS. Implements progress loaders, API keys form inputs, and accordion-style breakdown results.
- **`analyzer.py`**: A LangChain-powered orchestration layer that invokes Chat LLMs (Groq Llama 3 or OpenAI GPT-4o-mini), enforces standard JSON outputs, and cleans output wrappers.
- **`pdf_reader.py`**: Text extraction layer using `PyPDF2` that checks formatting safety and returns clean string content while handling structural errors.
- **`prompts.py`**: Holds recruiter persona templates instructing the LLM to analyze objectively and format using a valid JSON schema.
- **`report/reflection.md`**: This reflection report.
- **`README.md`**: Complete architectural layout, deployment guidelines, and environment configuration options.

---

## 3. Technologies Used
- **Streamlit**: For quick formulation of a responsive UI. Custom CSS is injected to transform default styles into a polished dark workspace theme.
- **LangChain Core**: Utilized to declare prompts (`ChatPromptTemplate`) and map them dynamically to LLMs (`ChatGroq` / `ChatOpenAI`) and output parsers (`StrOutputParser`).
- **Groq LLM API**: Selected as the primary LLM client to query `llama-3.3-70b-specdec` for ultra-low latency analyses.
- **OpenAI API**: Provided as a fallback option, querying `gpt-4o-mini` for highly reliable structural formatting.
- **PyPDF2**: Utilized to read page streams and extract text efficiently.
- **Python-dotenv**: Used to parse `.env` keys.

---

## 4. Challenges Faced & Solutions
1. **Unstructured Output Formatting**: Generative LLMs often output markdown text with introductory greetings, which causes JSON parsing errors.
   - *Solution*: I designed the prompt to explicitly require JSON format without conversational fluff. In `analyzer.py`, regex stripping checks are run to isolate the JSON content from markdown block tags (` ```json ... ``` `) before running `json.loads`.
2. **Defensive Value Fallbacks**: If the LLM misses returning a key (e.g. `ats_feedback`) in its JSON, default json loaders can crash the Streamlit widgets.
   - *Solution*: A post-processing key-validation loop checks the parsed dictionary against required keys and populates missing fields with default lists/values, avoiding rendering failures.
3. **Empty or Scanned PDF Handling**: Uploading image-based (scanned) resumes yields zero characters during text extraction.
   - *Solution*: Written strict verification inside `pdf_reader.py` that raises a custom `ValueError` if the character length is zero, advising the user to upload a text-readable PDF.

---

## 5. Learning Outcomes
- **Modular Design Principles**: Keeping PDF reading, prompt schemas, LLM wrappers, and UI states separate keeps the code maintainable.
- **Defensive Error Handling**: Catching specific exceptions (`PdfReadError`, `JSONDecodeError`) at the component boundaries allows displaying targeted, friendly warning banners to the user.
- **Streamlit State Management**: Storing the analysis dictionary inside `st.session_state` ensures that reports are preserved on UI updates (like sliding strictness or switching accordion expanders).

---

## 6. Future Improvements
- **Interactive Resume Editor**: Side-by-side view where the user can edit their resume text and see their health score update dynamically.
- **Job Description Matcher (Role RAG)**: Allow the user to paste a specific job description, run a vector similarity comparison, and output a custom "Match Score" with missing qualifications.
- **PDF Layout Analyzer**: Integrate libraries like `pdfplumber` or OCR models to verify column structures, check font readability, and analyze visual design layout issues.
