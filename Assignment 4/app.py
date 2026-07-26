import streamlit as st
import os
import datetime
import numexpr
from dotenv import load_dotenv

# LangChain Imports
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

# Load environment variables
load_dotenv()

# App Configuration
st.set_page_config(
    page_title="Agentic AI Chatbot",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Premium CSS Injection
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%);
        color: #f3f4f6;
    }
    .app-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .app-subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }
    .step-card {
        background-color: rgba(31, 41, 55, 0.6);
        border: 1px solid rgba(156, 163, 175, 0.15);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(8px);
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. LLM CONFIGURATION
# ==========================================
def get_llm(provider: str, api_key: str):
    """
    Configure and return the LLM model based on user selection.
    """
    if not api_key:
        raise ValueError(f"API Key for {provider} is required.")
        
    if provider == "Groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            groq_api_key=api_key
        )
    elif provider == "OpenAI":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=api_key
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


# ==========================================
# 2. TOOL DEFINITIONS
# ==========================================

# Wikipedia wrapper setup
wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1000)
wiki_search_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

@tool
def calculate(expression: str) -> str:
    """Useful for evaluating mathematical and arithmetic expressions. 
    Input must be a valid python math string, e.g., '2 * (3 + 5)' or '2**10'."""
    try:
        # Safely evaluate mathematical expressions using numexpr
        result = numexpr.evaluate(expression).item()
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}. Ensure the expression is mathematically valid."

@tool
def get_current_datetime() -> str:
    """Returns the current date and time. No inputs needed."""
    now = datetime.datetime.now()
    return f"Current local date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

@tool
def search_wikipedia(query: str) -> str:
    """Useful for searching Wikipedia for summaries of articles, historical facts, people, places, or general events.
    Input should be a clean, plain text query."""
    try:
        return wiki_search_tool.run(query)
    except Exception as e:
        return f"Error searching Wikipedia: {e}"

# List of tools equipped for the agent
tools = [calculate, get_current_datetime, search_wikipedia]


# ==========================================
# 3. MEMORY & AGENT INITIALIZATION
# ==========================================
def get_agent_executor(llm):
    """
    Initialize the Agent and AgentExecutor with tools and conversational prompt structure.
    """
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an advanced AI Agent equipped with tools for arithmetic, real-time date/time, and general Wikipedia search. "
            "Think step-by-step to plan how to answer the user query. "
            "Use tools ONLY when necessary. If tools are not needed, answer using your core capabilities. "
            "Remember past conversations using the chat history provided."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create Executor with intermediate steps enabled for planning demonstration
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        return_intermediate_steps=True
    )


# ==========================================
# 4. STREAMLIT UI & INTERFACE
# ==========================================

# Sidebar Configuration
st.sidebar.markdown("<h2 style='color:#60a5fa; font-weight:700;'>⚙️ Agent Settings</h2>", unsafe_allow_html=True)

# Provider select box
provider = st.sidebar.selectbox(
    "LLM Provider:",
    ["Groq", "OpenAI"],
    index=0
)

# API Key input
api_key = ""
if provider == "Groq":
    env_key = os.getenv("GROQ_API_KEY", "")
    api_key = st.sidebar.text_input("Groq API Key:", value=env_key, type="password")
else:
    env_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.sidebar.text_input("OpenAI API Key:", value=env_key, type="password")

# Clear Memory button
st.sidebar.markdown("<hr style='border:1px solid rgba(156,163,175,0.15);'>", unsafe_allow_html=True)
if st.sidebar.button("🧹 Clear Conversation Memory", use_container_width=True):
    st.session_state.messages = []
    st.sidebar.success("Chat history cleared!")
    st.rerun()

# Available Tools Dashboard
st.sidebar.markdown("<h3 style='color:#a78bfa;'>🛠️ Equipped Tools</h3>", unsafe_allow_html=True)
st.sidebar.markdown("""
* **Calculator**: Solves complex math with `numexpr`.
* **Current Date & Time**: Real-time datetime reports.
* **Wikipedia**: Search engine for knowledge retrieval.
""")

# Initialize state history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main Title Header
st.markdown("<h1 class='app-title'>🕵️ Agentic AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>A smart AI agent demonstrating real-time Planning, Memory recall, and Tool usage.</p>", unsafe_allow_html=True)

# Show past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "steps" in message:
            with st.expander("🔍 View Thinking Process & Planning"):
                for step in message["steps"]:
                    st.markdown(f"**Action**: `{step['tool']}({step['tool_input']})`")
                    st.markdown(f"**Result**: {step['observation']}")

# User text input
if user_prompt := st.chat_input("Ask a question (e.g., 'What day is it today?' or 'Calculate 2^15' or 'Who is Alan Turing?')"):
    
    # Check for empty prompt
    if not user_prompt.strip():
        st.warning("Please type a valid, non-empty question.")
        st.stop()
        
    # Append User Message to State
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    # 1. Error Handling: Missing API Key
    if not api_key:
        err_msg = f"API Key for {provider} is missing. Please configure it in your `.env` or input it in the sidebar settings."
        st.error(err_msg)
        st.session_state.messages.append({"role": "assistant", "content": err_msg})
        st.stop()

    # 2. Setup LLM & Executor
    try:
        llm = get_llm(provider, api_key)
        agent_executor = get_agent_executor(llm)
    except Exception as e:
        err_msg = f"Failed to initialize LLM / Agent: {e}"
        st.error(err_msg)
        st.session_state.messages.append({"role": "assistant", "content": err_msg})
        st.stop()

    # 3. Format Chat Memory history for LangChain
    chat_history_list = []
    for msg in st.session_state.messages[:-1]: # exclude last user prompt
        if msg["role"] == "user":
            chat_history_list.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            chat_history_list.append(AIMessage(content=msg["content"]))

    # 4. Invoke Agent & Track Planning Steps
    steps_record = []
    response_content = ""

    with st.status("🕵️ Agent planning and executing steps...", expanded=True) as status_box:
        try:
            # Run the agent executor
            result = agent_executor.invoke({
                "input": user_prompt,
                "chat_history": chat_history_list
            })
            
            response_content = result.get("output", "No response generated.")
            
            # Extract and display intermediate thoughts/planning steps
            intermediate_steps = result.get("intermediate_steps", [])
            if intermediate_steps:
                status_box.write("### 🔍 Planning Details:")
                for action, observation in intermediate_steps:
                    step_detail = {
                        "tool": action.tool,
                        "tool_input": action.tool_input,
                        "observation": observation
                    }
                    steps_record.append(step_detail)
                    
                    # Output individual actions visually in the status box
                    status_box.markdown(f"**Tool Call:** Invoked `{action.tool}` with input `{action.tool_input}`")
                    status_box.markdown(f"**Observation:** {observation}")
                    status_box.markdown("---")
            else:
                status_box.write("✨ No tools were required. Answered using internal knowledge.")
                
            status_box.update(label="🤖 Finished Planning & Tool execution!", state="complete")

        except Exception as e:
            response_content = f"Error during agent execution: {e}"
            status_box.update(label="❌ Failed during execution", state="error")
            st.error(response_content)

    # 5. Display Final Response
    st.chat_message("assistant").write(response_content)
    
    # Save Assistant response with steps
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response_content,
        "steps": steps_record
    })
