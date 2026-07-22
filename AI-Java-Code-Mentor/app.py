import streamlit as st
import os
from dotenv import load_dotenv

# Import the backend analyzer function
from llm import get_mentor_response

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Java Code Mentor",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, polished UI styling
st.markdown("""
<style>
    /* Center the title and adjust font weights */
    .main-title {
        text-align: center;
        font-family: 'Outfit', 'Inter', sans-serif;
        color: #FF4B4B;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        font-family: 'Inter', sans-serif;
        color: #555555;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Enhance buttons */
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 2.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(255, 75, 75, 0.2);
    }
    div.stButton > button:first-child:hover {
        background-color: #E04040;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 75, 75, 0.3);
    }
    
    /* Code area styling */
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.95rem;
        border-radius: 8px;
    }
    
    /* Dark mode adjustments for standard background */
    @media (prefers-color-scheme: dark) {
        .subtitle {
            color: #bbbbbb;
        }
    }
</style>
""", unsafe_allow_html=True)

# Centered App Title
st.markdown('<div class="main-title">☕ AI Java Code Mentor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your personal AI companion for writing clean, efficient, and bug-free Java code</div>', unsafe_allow_html=True)

# Default code for the text area
DEFAULT_JAVA_CODE = """// Example Java code (Bubble Sort)
public class BubbleSort {
    void bubbleSort(int arr[]) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // swap temp and arr[i]
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
}
"""

# --- Sidebar Configuration ---
st.sidebar.header("🛠️ Mentor Controls")

# Model Selection Dropdown
available_models = {
    "Llama 3.3 70B (Recommended)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B (Fast & Light)": "llama-3.1-8b-instant",
    "Mixtral 8x7B": "mixtral-8x7b-32768"
}
selected_model_name = st.sidebar.selectbox(
    "Select Groq AI Model",
    options=list(available_models.keys()),
    index=0
)
selected_model_id = available_models[selected_model_name]

# Check API Key Status
api_key = os.getenv("GROQ_API_KEY")
st.sidebar.markdown("---")
st.sidebar.subheader("🔑 API Connection Status")
if api_key and api_key.strip() != "" and api_key != "your_groq_api_key_here":
    st.sidebar.success("Connected to Groq API")
else:
    st.sidebar.warning("API Key Missing in .env")
    st.sidebar.info(
        "To fix: Add your `GROQ_API_KEY=gsk_...` key in the `.env` file in the project folder."
    )

# App Information
st.sidebar.markdown("---")
st.sidebar.subheader("📖 About AI Java Code Mentor")
st.sidebar.markdown(
    """
    This tool is powered by state-of-the-art Large Language Models on **Groq's LPU inference engine** to provide instant feedback on your Java code.
    
    ### Features:
    * **Explain Code:** Understand how complex logic runs step-by-step.
    * **Find Bugs:** Detect code errors, edge cases, and runtime exceptions.
    * **Optimize Code:** Improve execution time and space complexity.
    * **Generate Comments:** Add Javadocs and inline notes following standards.
    """
)

# --- Main Interface ---

# 1. Code Input Area
java_code = st.text_area(
    "Paste your Java code here:",
    value=DEFAULT_JAVA_CODE,
    height=280,
    placeholder="public class Main { ... }"
)

# 2. Mentor Task Dropdown and Analyze Button (Using columns for side-by-side layout)
col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

with col1:
    task_option = st.selectbox(
        "Choose what the Mentor should do:",
        options=["Explain Code", "Find Bugs", "Optimize Code", "Generate Comments"],
        index=0
    )

with col2:
    analyze_button = st.button("Analyze Code", use_container_width=True)

# 3. Execution & Results Display
if analyze_button:
    if not java_code.strip():
        st.warning("⚠️ Please paste some Java code before clicking 'Analyze'.")
    else:
        # Show spinner during the API call
        with st.spinner("⏳ The Mentor is reviewing your code..."):
            response = get_mentor_response(
                task=task_option,
                code=java_code,
                model=selected_model_id
            )
        
        # Display the result
        st.markdown("---")
        st.subheader(f"💡 Mentor Feedback: {task_option}")
        
        # Display response using Streamlit's native Markdown formatting (supports code highlighting, etc.)
        st.markdown(response)
