import streamlit as st
import os
from dotenv import load_dotenv

# Local imports
from pdf_reader import extract_text_from_pdf
from analyzer import analyze_resume

# Load environment variables
load_dotenv()

# ==========================================
# 1. PAGE SETUP & THEME INJECTION
# ==========================================
st.set_page_config(
    page_title="AI Resume Analyzer & ATS Coach",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark-mode premium layout with neon borders and polished score circles
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 60%, #1e1b4b 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* App Title Layout */
    .app-title {
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #38bdf8, #818cf8, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -1rem;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.15rem;
        margin-bottom: 2.5rem;
    }

    /* Cards & Scores */
    .score-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(129, 140, 248, 0.25);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
    }
    .score-circle {
        position: relative;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(15, 23, 42, 0.9) 0%, rgba(9, 13, 22, 0.95) 100%);
        border: 4px solid #818cf8;
        box-shadow: 0 0 15px rgba(129, 140, 248, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    .score-value {
        font-size: 3.2rem;
        font-weight: 800;
        color: #38bdf8;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }
    .score-label {
        font-size: 1.1rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Accent Pill Tags */
    .tag-pill {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.25rem;
        font-weight: 500;
    }
    .tag-pill-soft {
        display: inline-block;
        background: rgba(52, 211, 153, 0.15);
        border: 1px solid rgba(52, 211, 153, 0.3);
        color: #34d399;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.25rem;
        font-weight: 500;
    }
    .tag-pill-role {
        display: inline-block;
        background: rgba(129, 140, 248, 0.15);
        border: 1px solid rgba(129, 140, 248, 0.3);
        color: #818cf8;
        padding: 0.4rem 1rem;
        border-radius: 8px;
        font-size: 0.95rem;
        margin: 0.3rem;
        font-weight: 500;
    }

    /* Lists styling inside expanders */
    .list-item {
        line-height: 1.6;
        margin-bottom: 0.6rem;
        padding-left: 0.5rem;
        border-left: 3px solid #818cf8;
    }
    .list-item-warning {
        line-height: 1.6;
        margin-bottom: 0.6rem;
        padding-left: 0.5rem;
        border-left: 3px solid #f87171;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None
if "current_file_hash" not in st.session_state:
    st.session_state.current_file_hash = None


# ==========================================
# 3. SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Analyzer Configuration")
    
    # Provider selection
    llm_provider = st.selectbox(
        "LLM Provider",
        options=["Groq", "OpenAI"],
        index=0,
        key="llm_provider"
    )
    
    # Dynamic API Credential forms
    if llm_provider == "Groq":
        st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Enter your Groq API Key. If left blank, it will load GROQ_API_KEY from environment variables.",
            key="groq_api_key"
        )
        st.selectbox(
            "Model Selection",
            options=["llama-3.3-70b-specdec", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            index=0,
            key="groq_model"
        )
    else:
        st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Enter your OpenAI API Key. If left blank, it will load OPENAI_API_KEY from environment variables.",
            key="openai_api_key"
        )
        st.selectbox(
            "Model Selection",
            options=["gpt-4o-mini", "gpt-4o"],
            index=0,
            key="openai_model"
        )
        
    st.markdown("---")
    st.markdown("### 🎯 Analysis Preferences")
    
    st.slider(
        "Strictness (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
        help="Lower values yield highly factual recruiting analytics; higher values are more creative with role suggestions.",
        key="temperature"
    )
    
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.85rem; color: #94a3b8; text-align: center;">
            AI Resume Analyzer v1.0.0<br>
            Capstone Project Submission
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# 4. MAIN USER INTERFACE
# ==========================================
st.markdown('<h1 class="app-title">Capstone AI Resume Analyzer 💼</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Upload your PDF resume to receive a comprehensive recruiter review, skill audit, and ATS compliance diagnostic.</p>', unsafe_allow_html=True)

# Grid Layout: Left Column for file uploading and execution triggers; Right Column for instructions
col_input, col_info = st.columns([3, 2], gap="large")

with col_input:
    st.markdown("### 📂 Upload Document")
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF format only)",
        type=["pdf"],
        help="Drag and drop your resume in PDF format. Text-based PDFs produce optimal results."
    )
    
    btn_analyze = st.button("Analyze Resume 🚀", type="primary", use_container_width=True)

with col_info:
    st.markdown("### ℹ️ How it works")
    st.markdown("""
    1. **Text Extraction**: The tool reads content page-by-page from your PDF safely.
    2. **Recruiter Audit**: A technical recruiter agent evaluates your qualifications, format structure, and metrics impact.
    3. **ATS Check**: The system tests keyword alignment and flags common parsing traps.
    4. **Reports Generation**: Detailed score card, strength listings, keyword deficits, and career path pathways are created.
    """)


# ==========================================
# 5. BUSINESS LOGIC & EXECUTION FLOW
# ==========================================
if btn_analyze:
    if uploaded_file is None:
        st.warning("⚠️ Please upload a PDF resume file before clicking the 'Analyze Resume' button.")
    else:
        # Reset analysis if a new file is uploaded
        file_hash = f"{uploaded_file.name}_{uploaded_file.size}"
        
        # 1. API Credentials resolution
        provider = llm_provider.lower()
        if provider == "groq":
            api_key = st.session_state.groq_api_key.strip() if st.session_state.get("groq_api_key") else os.getenv("GROQ_API_KEY", "").strip()
            model_name = st.session_state.groq_model
        else:
            api_key = st.session_state.openai_api_key.strip() if st.session_state.get("openai_api_key") else os.getenv("OPENAI_API_KEY", "").strip()
            model_name = st.session_state.openai_model

        if not api_key:
            st.error(f"🔑 Credentials Error: No API key provided for {llm_provider}. Please specify it in the sidebar settings or .env file.")
        else:
            # 2. Start execution
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Page 1: Read PDF
                status_text.text("Extracting resume text from PDF...")
                progress_bar.progress(20)
                
                resume_text = extract_text_from_pdf(uploaded_file)
                
                # Page 2: Connect to LLM
                status_text.text("Connecting to recruiting agent and running analysis...")
                progress_bar.progress(50)
                
                analysis_results = analyze_resume(
                    resume_text=resume_text,
                    provider=provider,
                    api_key=api_key,
                    model_name=model_name,
                    temperature=st.session_state.temperature
                )
                
                # Page 3: Wrap up
                status_text.text("Structuring analysis reports...")
                progress_bar.progress(90)
                
                st.session_state.resume_analysis = analysis_results
                st.session_state.current_file_hash = file_hash
                
                progress_bar.progress(100)
                status_text.text("Analysis complete!")
                
                # Clear progress bars after completion
                progress_bar.empty()
                status_text.empty()
                st.success("🎉 Your resume analysis has been generated! View the results below.")
                
            except Exception as ex:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Analysis Failed: {str(ex)}")


# ==========================================
# 6. RESULTS SECTION DISPLAY
# ==========================================
if st.session_state.resume_analysis:
    analysis = st.session_state.resume_analysis
    
    st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.1); margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # 6.1 Score & Dashboard Summary
    score = analysis.get("score", 70)
    
    # Visual color mapping based on score performance
    if score >= 80:
        score_color = "#34d399"  # Emerald Green
    elif score >= 60:
        score_color = "#38bdf8"  # Teal Blue
    else:
        score_color = "#f87171"  # Coral Red
        
    col_score_card, col_score_gauge = st.columns([1, 2], gap="large")
    
    with col_score_card:
        st.markdown(f"""
        <div class="score-container">
            <div class="score-circle" style="border-color: {score_color}; box-shadow: 0 0 15px {score_color}60;">
                <div class="score-value" style="color: {score_color};">{score}</div>
            </div>
            <div class="score-label">Resume Health Score</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_score_gauge:
        st.markdown("### 📊 Overall Evaluation Summary")
        if score >= 80:
            st.markdown("""
            **Status: Excellent Profile Match**  
            Your resume is structurally solid, highlights strong keywords, and emphasizes impact with professional outcomes. You are in a great position to apply for competitive job listings.
            """)
        elif score >= 60:
            st.markdown("""
            **Status: Good (Needs Minor Optimization)**  
            Your resume displays adequate skill sets and outlines career history correctly, but lacks quantitative metrics and has minor ATS keyword deficits. Implementing the suggestions below will help improve outcomes.
            """)
        else:
            st.markdown("""
            **Status: Critical Review Required**  
            Your resume has formatting gaps, weak structural clarity, or major keyword misalignment. Recruiters and automated ATS parsers might struggle to index your qualifications. We highly recommend rewriting sections using the guidelines below.
            """)
            
        # Draw a visual progress bar
        st.progress(score / 100)

    # 6.2 Expandable Sections for Detailed Feedback
    st.markdown("### 🔍 Detailed Feedback Reports")
    
    # A: Strengths
    with st.expander("💪 Core Strengths", expanded=True):
        strengths = analysis.get("strengths", [])
        if strengths:
            for s in strengths:
                st.markdown(f'<div class="list-item">{s}</div>', unsafe_allow_html=True)
        else:
            st.info("No particular strengths highlighted.")
            
    # B: Weaknesses
    with st.expander("⚠️ Critical Weaknesses", expanded=True):
        weaknesses = analysis.get("weaknesses", [])
        if weaknesses:
            for w in weaknesses:
                st.markdown(f'<div class="list-item-warning">{w}</div>', unsafe_allow_html=True)
        else:
            st.info("No major weaknesses flagged.")

    # C: Skills Detected (Side-by-Side Columns inside expander)
    with st.expander("🛠️ Skills Detected", expanded=True):
        col_tech, col_soft = st.columns(2)
        with col_tech:
            st.markdown("#### Technical Skills")
            tech_skills = analysis.get("tech_skills", [])
            if tech_skills:
                for skill in tech_skills:
                    st.markdown(f'<span class="tag-pill">{skill}</span>', unsafe_allow_html=True)
            else:
                st.info("No technical skills explicitly identified.")
        with col_soft:
            st.markdown("#### Soft Skills & Methodologies")
            soft_skills = analysis.get("soft_skills", [])
            if soft_skills:
                for skill in soft_skills:
                    st.markdown(f'<span class="tag-pill-soft">{skill}</span>', unsafe_allow_html=True)
            else:
                st.info("No soft skills explicitly identified.")

    # D: ATS Analysis & Keyword Gaps
    with st.expander("🤖 ATS Compatibility & Keyword Gaps", expanded=False):
        col_ats, col_kw = st.columns([3, 2])
        with col_ats:
            st.markdown("#### ATS Parser Alignment")
            ats_feedback = analysis.get("ats_feedback", [])
            if ats_feedback:
                for feedback in ats_feedback:
                    st.markdown(f'<div class="list-item">{feedback}</div>', unsafe_allow_html=True)
            else:
                st.info("ATS parser formatting appears correct.")
        with col_kw:
            st.markdown("#### Missing Key terms")
            missing_kw = analysis.get("missing_keywords", [])
            if missing_kw:
                st.write("Adding these keywords can help match automated job descriptions:")
                for kw in missing_kw:
                    st.markdown(f'<span class="tag-pill-soft" style="background: rgba(248, 113, 113, 0.15); border: 1px solid rgba(248, 113, 113, 0.3); color: #f87171;">{kw}</span>', unsafe_allow_html=True)
            else:
                st.info("No missing keywords identified.")

    # E: Recommended Job Roles
    with st.expander("💼 Recommended Job Roles", expanded=False):
        roles = analysis.get("job_roles", [])
        if roles:
            st.write("Based on experience patterns, you match closely with these professional titles:")
            for r in roles:
                st.markdown(f'<span class="tag-pill-role">{r}</span>', unsafe_allow_html=True)
        else:
            st.info("No specific job roles identified.")

    # F: Actionable Improvement Suggestions
    with st.expander("📈 Actionable Suggestions for Improvement", expanded=False):
        improvements = analysis.get("improvements", [])
        if improvements:
            for idx, imp in enumerate(improvements):
                st.markdown(f'**{idx+1}.** {imp}')
        else:
            st.info("No improvement points recommended.")
            
    # Reset Button
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    if st.button("Clear Report & Start New Analysis"):
        st.session_state.resume_analysis = None
        st.session_state.current_file_hash = None
        st.rerun()
