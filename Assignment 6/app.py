import streamlit as st
import os
import json
import re
from dotenv import load_dotenv

# LangChain Imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

# Load environment variables from .env if present
load_dotenv()

# ==========================================
# 1. STREAMLIT CONFIG & CUSTOM STYLING
# ==========================================
st.set_page_config(
    page_title="AI Academic Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium dark theme styling with custom cards and glowing accents
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%);
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Headers */
    .app-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #38bdf8, #818cf8, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        margin-top: -1rem;
    }
    
    .app-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Cards & Containers */
    .dashboard-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(129, 140, 248, 0.15);
        border-radius: 16px;
        padding: 1.8rem;
        backdrop-filter: blur(12px);
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
    }

    .card-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        padding-bottom: 0.5rem;
    }

    /* Output Styling */
    .response-container {
        background: rgba(30, 41, 59, 0.5);
        border-left: 4px solid #818cf8;
        border-radius: 4px 8px 8px 4px;
        padding: 1.2rem;
        margin-top: 1rem;
        color: #f1f5f9;
        line-height: 1.6;
    }

    .quiz-container {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(52, 211, 153, 0.25);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .quiz-question {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.8rem;
    }

    /* Status Blocks */
    .success-alert {
        background-color: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }

    .error-alert {
        background-color: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #f87171;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
# We store outputs in session state so they persist when Streamlit reruns
state_variables = {
    "explanation": None,
    "answer": None,
    "summary": None,
    "quiz_raw": None,
    "quiz_data": None,
    "quiz_answers": {},
    "quiz_submitted": False,
    "practice": None,
    "active_tab": 0
}

for var, default in state_variables.items():
    if var not in st.session_state:
        st.session_state[var] = default


# ==========================================
# 3. LLM INITIALIZATION AND CHAINS
# ==========================================

def get_llm():
    """
    Initialize the LangChain LLM client based on sidebar configurations.
    Handles credential retrieval and validates keys.
    """
    # Fetch configurations from user settings or environment variables
    provider = st.session_state.get("llm_provider", "groq").lower()
    
    # Prioritize user input API key, then fall back to environment variable
    if provider == "groq":
        api_key = st.session_state.get("groq_api_key", "").strip()
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY", "").strip()
        model_name = st.session_state.get("groq_model", "llama-3.3-70b-specdec")
    else:
        api_key = st.session_state.get("openai_api_key", "").strip()
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY", "").strip()
        model_name = st.session_state.get("openai_model", "gpt-4o-mini")

    # Raise error if API key is missing
    if not api_key:
        raise ValueError(f"Missing API Key for {provider.capitalize()}. Please configure it in the sidebar or check your environment.")

    temperature = st.session_state.get("temperature", 0.5)

    try:
        if provider == "groq":
            return ChatGroq(
                api_key=api_key,
                model_name=model_name,
                temperature=temperature
            )
        else:
            return ChatOpenAI(
                api_key=api_key,
                model_name=model_name,
                temperature=temperature
            )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM client: {str(e)}")


def run_tutor_chain(prompt_template: ChatPromptTemplate, inputs: dict) -> str:
    """
    Helper function to run LangChain prompt template + LLM + Output Parser.
    Includes global error handling for API failures.
    """
    try:
        llm = get_llm()
        chain = prompt_template | llm | StrOutputParser()
        return chain.invoke(inputs)
    except ValueError as ve:
        st.error(f"🔑 Authentication Error: {str(ve)}")
        return ""
    except Exception as e:
        st.error(f"⚠️ API or Connection Error: {str(e)}")
        return ""


# ==========================================
# 4. PROMPT TEMPLATES & HELPER FUNCTIONS
# ==========================================

# A: Concept Explanation Chain
explain_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a world-class academic tutor. Your task is to explain the topic provided by the student in simple, clear, and engaging language.
Tailor your explanation depth to the student's level: {level}.

Structure your response using these markdown headers:
1. **Core Concept**: A concise explanation in simple terms.
2. **Real-World Analogy**: Use a relatable comparison or metaphor to make the concept stick.
3. **Key Components**: A bulleted breakdown of the 3-4 most important elements.
4. **Did You Know?**: An interesting, lesser-known educational fact about the topic.

Ensure explanations are accurate and age-appropriate."""),
    ("human", "Please explain the concept of: {topic}")
])

# B: Question Answering Chain
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful academic tutor. Answer the student's question clearly, thoroughly, and step-by-step.
Tailor your explanation to the target student level: {level}.
If a general context topic is provided, align your answer with that context.
Provide definitions for technical terms used. Use formatting (bolding, lists, code blocks, or simple math formatting) to make the text readable."""),
    ("human", "Context Topic (optional): {topic}\n\nQuestion: {question}")
])

# C: Summarization Chain
summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert educational summarizer. Your task is to extract core knowledge from text inputs and summarize them clearly for student learning.

Structure your response using these markdown headers:
1. **TL;DR**: A one-sentence summary of the main idea.
2. **Key Takeaways**: Bullet points containing the critical concepts and arguments.
3. **Important Terminology**: Short glossary defining key terms or names found in the text.
4. **Concept Summary**: A cohesive, well-written synthesis paragraph summarizing the entire text.

Format the summary clearly."""),
    ("human", "Please summarize this educational text:\n\n{text}")
])

# D: Quiz Generation Chain
quiz_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a teacher designing a quiz to test student comprehension.
Your task is to generate a list of {num_questions} multiple-choice questions (MCQs) based on the provided material.
Each question must have exactly 4 choices, one correct answer, and a clear explanation of why it is correct.

You MUST format the output as a valid JSON array of objects. Do not include markdown code block syntax (like ```json) in your final response. Return ONLY the raw JSON string.

JSON Schema structure:
[
  {{
    "question": "The question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0,
    "explanation": "Explanation why Option A is correct."
  }}
]

Base the quiz on the following material:
Topic/Context: {topic}
Source Material (if any): {text}"""),
    ("human", "Generate a quiz with {num_questions} multiple-choice questions.")
])

# E: Practice Questions Chain
practice_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an academic coach. Suggest open-ended practice questions to help a student self-assess their understanding of a topic or text.
Generate exactly {num_questions} questions that promote critical thinking, synthesis, or application of knowledge rather than rote recall.

For each question, provide:
1. The question.
2. A **"Study Guide Check"**: Bullet points explaining what core ideas a successful answer should mention, serving as a rubric for self-grading.

Base the questions on:
Topic/Context: {topic}
Source Material (if any): {text}"""),
    ("human", "Generate {num_questions} open-ended practice questions.")
])


# ==========================================
# 5. STREAMLIT SIDEBAR (SETTINGS)
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Tutor Settings")
    
    # LLM Provider selection
    llm_provider = st.selectbox(
        "LLM Provider",
        options=["Groq", "OpenAI"],
        index=0,
        key="llm_provider"
    )
    
    # Dynamic API Key inputs
    if llm_provider == "Groq":
        st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Enter your Groq API Key. If left blank, we will look for GROQ_API_KEY in environment variables.",
            key="groq_api_key"
        )
        st.selectbox(
            "Model",
            options=["llama-3.3-70b-specdec", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            index=0,
            key="groq_model"
        )
    else:
        st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Enter your OpenAI API Key. If left blank, we will look for OPENAI_API_KEY in environment variables.",
            key="openai_api_key"
        )
        st.selectbox(
            "Model",
            options=["gpt-4o-mini", "gpt-4o"],
            index=0,
            key="openai_model"
        )

    st.markdown("---")
    st.markdown("### 🎯 Educational Preferences")
    
    # Target explanation level
    level = st.selectbox(
        "Tutor Target Grade",
        options=["Elementary School (Age 5-10)", "Middle School (Age 11-14)", "High School (Age 15-18)", "College / Undergraduate", "PhD / Specialist"],
        index=3,
        key="target_level"
    )
    
    # Temperature (creativity control)
    st.slider(
        "Explanation Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.1,
        help="Lower values are more factual and consistent; higher values are more creative and expressive.",
        key="temperature"
    )
    
    # Number of questions slider for Quizzes
    st.slider(
        "Number of Questions",
        min_value=3,
        max_value=10,
        value=5,
        step=1,
        key="num_questions"
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.85rem; color: #94a3b8; text-align: center;">
            AI Academic Tutor v1.0.0<br>
            Powered by LangChain & Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# 6. MAIN APPLICATION LAYOUT
# ==========================================
st.markdown('<h1 class="app-title">Academic AI Tutor 🎓</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Your personalized learning environment for explaining concepts, summarizing text, and testing knowledge.</p>', unsafe_allow_html=True)

# Grid Layout for Input controls
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="card-header">
        📚 Concept Explorer & Q&A
    </div>
    """, unsafe_allow_html=True)
    
    topic_input = st.text_input(
        "Concept or Topic",
        placeholder="e.g., Photosynthesis, Theory of Relativity, Supply & Demand",
        help="Input a broad concept you want to learn or ask questions about."
    )
    
    question_input = st.text_input(
        "Ask a Question",
        placeholder="e.g., What is the role of stomata?, How does time dilation happen?",
        help="Ask a specific question related to your study topic."
    )
    
    st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
    
    btn_explain, btn_answer = st.columns(2)
    with btn_explain:
        explain_clicked = st.button("Explain Concept 🔍", use_container_width=True)
    with btn_answer:
        answer_clicked = st.button("Answer Question 💬", use_container_width=True)

with col2:
    st.markdown("""
    <div class="card-header">
        📝 Reading Notes & Study Material
    </div>
    """, unsafe_allow_html=True)
    
    text_input = st.text_area(
        "Study Text / Book Chapters / Notes",
        placeholder="Paste paragraphs, article text, or class notes here (minimum 20 characters recommended)...",
        height=175,
        help="Insert reading content here to summarize, generate study quizzes, or extract practice questions."
    )
    
    st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
    
    btn_summarize, btn_quiz, btn_practice = st.columns(3)
    with btn_summarize:
        summarize_clicked = st.button("Summarize Text 📰", use_container_width=True)
    with btn_quiz:
        quiz_clicked = st.button("Generate Quiz 📝", use_container_width=True)
    with btn_practice:
        practice_clicked = st.button("Practice Qs ✏️", use_container_width=True)


# ==========================================
# 7. BUSINESS LOGIC & STATE HANDLING
# ==========================================

# Handler: Explain Concept
if explain_clicked:
    if not topic_input.strip():
        st.warning("⚠️ Please provide a topic or concept in the 'Concept or Topic' field to explain.")
    else:
        with st.spinner("🧠 Preparing tutor explanation..."):
            res = run_tutor_chain(
                explain_prompt,
                {"topic": topic_input.strip(), "level": level}
            )
            if res:
                st.session_state.explanation = res
                st.session_state.active_tab = 0 # Redirect focus

# Handler: Answer Question
if answer_clicked:
    if not question_input.strip():
        st.warning("⚠️ Please enter a specific question in the 'Ask a Question' field.")
    else:
        with st.spinner("🤖 Answering question..."):
            res = run_tutor_chain(
                answer_prompt,
                {
                    "topic": topic_input.strip() if topic_input.strip() else "General",
                    "question": question_input.strip(),
                    "level": level
                }
            )
            if res:
                st.session_state.answer = res
                st.session_state.active_tab = 1

# Handler: Summarize
if summarize_clicked:
    if not text_input.strip() or len(text_input.strip()) < 10:
        st.warning("⚠️ Please paste educational text (at least 10 characters) in the 'Reading Notes' text area to summarize.")
    else:
        with st.spinner("📝 Summarizing reading materials..."):
            res = run_tutor_chain(
                summarize_prompt,
                {"text": text_input.strip()}
            )
            if res:
                st.session_state.summary = res
                st.session_state.active_tab = 2

# Handler: Generate Quiz
if quiz_clicked:
    context_topic = topic_input.strip()
    context_text = text_input.strip()
    
    if not context_topic and not context_text:
        st.warning("⚠️ To generate a quiz, please fill out the 'Concept or Topic' field OR paste study notes.")
    else:
        with st.spinner("✍️ Writing multiple-choice questions..."):
            res = run_tutor_chain(
                quiz_prompt,
                {
                    "topic": context_topic if context_topic else "General",
                    "text": context_text if context_text else "Not provided",
                    "num_questions": st.session_state.num_questions
                }
            )
            if res:
                st.session_state.quiz_raw = res
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                
                # Attempt to parse output to JSON list
                # Clean up any potential markdown wrapped codeblock
                cleaned_res = res.strip()
                if cleaned_res.startswith("```"):
                    cleaned_res = re.sub(r"^```(?:json)?\n", "", cleaned_res)
                    cleaned_res = re.sub(r"\n```$", "", cleaned_res)
                
                try:
                    parsed_json = json.loads(cleaned_res)
                    st.session_state.quiz_data = parsed_json
                    st.session_state.active_tab = 3
                except json.JSONDecodeError:
                    st.session_state.quiz_data = None  # Fallback to displaying raw output
                    st.session_state.active_tab = 3
                    st.error("⚠️ Failed to parse the quiz into an interactive format. Displaying raw quiz instead.")

# Handler: Practice Questions
if practice_clicked:
    context_topic = topic_input.strip()
    context_text = text_input.strip()
    
    if not context_topic and not context_text:
        st.warning("⚠️ To suggest practice questions, please fill out the 'Concept or Topic' field OR paste study notes.")
    else:
        with st.spinner("✏️ Formulating practice exercises..."):
            res = run_tutor_chain(
                practice_prompt,
                {
                    "topic": context_topic if context_topic else "General",
                    "text": context_text if context_text else "Not provided",
                    "num_questions": st.session_state.num_questions
                }
            )
            if res:
                st.session_state.practice = res
                st.session_state.active_tab = 4


# ==========================================
# 8. RESPONSE DISPLAY AREA
# ==========================================
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

workspace_modes = [
    "💡 Concept Explanation",
    "❓ Question Answered",
    "📖 Notes Summary",
    "✍️ Practice Quiz (MCQ)",
    "✏️ Study Exercises"
]

# Render workspace toggler using radio buttons styled horizontally
selected_tool = st.radio(
    "Tutor Workspace Tools",
    options=workspace_modes,
    index=int(st.session_state.active_tab),
    horizontal=True,
)

# Sync manual clicks back to session state active_tab
st.session_state.active_tab = workspace_modes.index(selected_tool)

# Add spacing
st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

# Active Workspace view rendering
if selected_tool == "💡 Concept Explanation":
    if st.session_state.explanation:
        st.markdown(f'<div class="response-container">{st.session_state.explanation}</div>', unsafe_allow_html=True)
    else:
        st.info("💡 Enter a topic above and click 'Explain Concept' to generate a lesson guide here.")

elif selected_tool == "❓ Question Answered":
    if st.session_state.answer:
        st.markdown(f'<div class="response-container">{st.session_state.answer}</div>', unsafe_allow_html=True)
    else:
        st.info("❓ Ask an academic question above and click 'Answer Question' to get help here.")

elif selected_tool == "📖 Notes Summary":
    if st.session_state.summary:
        st.markdown(f'<div class="response-container">{st.session_state.summary}</div>', unsafe_allow_html=True)
    else:
        st.info("📖 Paste study notes on the right and click 'Summarize Text' to view a structured digest here.")

elif selected_tool == "✍️ Practice Quiz (MCQ)":
    if st.session_state.quiz_data:
        st.markdown("### ✍️ Interactive Reading Comprehension Quiz")
        st.write("Select the correct answer for each question and submit at the bottom.")
        
        # Render each question as a card
        for idx, q_item in enumerate(st.session_state.quiz_data):
            try:
                question_text = q_item.get("question", f"Question {idx+1}")
                options = q_item.get("options", [])
                correct_idx = q_item.get("correct_index", 0)
                explanation = q_item.get("explanation", "")
                
                st.markdown(f"""
                <div class="quiz-container">
                    <div class="quiz-question">Q{idx+1}: {question_text}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Option selection
                selected = st.radio(
                    f"Choose one option for Question {idx+1}:",
                    options=options,
                    index=None,
                    key=f"q_radio_{idx}",
                    label_visibility="collapsed"
                )
                
                if selected is not None:
                    selected_idx = options.index(selected)
                    st.session_state.quiz_answers[idx] = selected_idx
                
                # Show results after submit
                if st.session_state.quiz_submitted:
                    user_ans = st.session_state.quiz_answers.get(idx)
                    if user_ans == correct_idx:
                        st.markdown(f'<div class="success-alert">✅ Correct! {explanation}</div>', unsafe_allow_html=True)
                    else:
                        selected_lbl = options[user_ans] if user_ans is not None else "Unanswered"
                        correct_lbl = options[correct_idx]
                        st.markdown(f'<div class="error-alert">❌ Incorrect. You selected: "{selected_lbl}".<br>Correct Answer: <b>{correct_lbl}</b>.<br><br><i>Reason: {explanation}</i></div>', unsafe_allow_html=True)
                        
                st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            except Exception as item_err:
                st.error(f"Error rendering question {idx+1}: {str(item_err)}")
                
        # Submit Quiz Action
        if not st.session_state.quiz_submitted:
            if st.button("Submit Answers", type="primary"):
                # Check if all questions are answered
                unanswered = len(st.session_state.quiz_data) - len(st.session_state.quiz_answers)
                if unanswered > 0:
                    st.warning(f"⚠️ You left {unanswered} question(s) blank. Please select an option for all questions before submitting.")
                else:
                    st.session_state.quiz_submitted = True
                    st.rerun()
        else:
            # Show score summary
            score = sum(1 for i, q in enumerate(st.session_state.quiz_data) if st.session_state.quiz_answers.get(i) == q.get("correct_index"))
            total = len(st.session_state.quiz_data)
            percentage = int((score / total) * 100)
            
            st.markdown(f"""
            <div class="dashboard-card" style="text-align: center; border-color: rgba(52, 211, 153, 0.4);">
                <h3 style="color: #34d399; margin: 0;">Quiz Results</h3>
                <div style="font-size: 3rem; font-weight: 800; color: #34d399; margin: 1rem 0;">
                    {score} / {total}
                </div>
                <p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 1.5rem;">
                    You scored <b>{percentage}%</b>! Check above to read detailed explanations for each question.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Reset / Retry Quiz"):
                st.session_state.quiz_submitted = False
                st.session_state.quiz_answers = {}
                st.rerun()

    elif st.session_state.quiz_raw:
        # Fallback raw presentation
        st.markdown(f'<div class="response-container">{st.session_state.quiz_raw}</div>', unsafe_allow_html=True)
    else:
        st.info("📝 Enter a topic or paste study notes, then click 'Generate Quiz' to take an interactive MCQ quiz here.")

elif selected_tool == "✏️ Study Exercises":
    if st.session_state.practice:
        st.markdown(f'<div class="response-container">{st.session_state.practice}</div>', unsafe_allow_html=True)
    else:
        st.info("✏️ Provide a topic or paste study text, then click 'Practice Qs' to get open-ended critical thinking questions here.")

