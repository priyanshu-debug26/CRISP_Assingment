# Reflection Report - Assignment 4: Agentic AI

## 1. What Was Built
I built an autonomous **Agentic AI Chatbot** using Streamlit and LangChain. The system enables natural language interactions where the AI does not just generate static text, but actively interacts with its environment using a suite of equipped tools (Calculator, Local Datetime, and Wikipedia Search). The application features stateful conversational memory and visualizes the agent's step-by-step reasoning process (thoughts, actions, and observations) directly inside the Streamlit user interface, allowing users to watch the agent plan and execute tasks.

---

## 2. Core Concepts Explained

### What are Tools?
In Agentic AI, **Tools** are interfaces or capabilities equipped to an LLM that allow it to interact with external systems, run code, read files, or query databases. Large Language Models are generally restricted to their training data and struggle with exact mathematical calculations or real-time data. Tools extend their reach—allowing the agent to search the web (Wikipedia tool), execute calculations (Calculator tool), or read the system clock (Date & Time tool).

### What is Memory?
**Memory** is the mechanism by which an AI agent stores and retrieves context across multi-turn interactions. Without memory, every LLM query is completely independent and stateless (the agent forgets who you are or what you asked previously). Conversational Memory compiles past messages and feeds them back into the LLM context, enabling coherent follow-up questions and long-term context retention.

### What is Planning?
**Planning** is the cognitive ability of an agent to break down a user's complex goal into sub-tasks, select appropriate tools, analyze observations, and iteratively refine its approach before outputting a final answer. Instead of responding immediately, the agent enters a Reason-and-Act (ReAct) or Tool-Calling loop:
1. **Thought**: Formulates a plan based on the user prompt.
2. **Action**: Invokes a tool with specific parameters.
3. **Observation**: Evaluates the output returned by the tool.
4. **Conclusion**: Determines if more steps are needed, or outputs the final response.

---

## 3. Challenges Faced
* **Streamlit Stateful Variables**: Streamlit reruns the entire python script whenever a user interacts with the UI, which ordinarily wipes local python memory. Bridging this by converting the `st.session_state` chat log list dynamically into LangChain `HumanMessage` and `AIMessage` objects on every run ensured stable and persistent agent memory.
* **Math Evaluation Security**: Standard Python `eval()` poses severe security hazards (such as shell injections). I solved this by implementing `numexpr` to safely evaluate mathematical equations without exposing the local filesystem or environment to arbitrary code execution.
* **Model Decommissioning**: Standard model endpoints can change. During testing, older models were identified as decommissioned. I updated the codebase to use Groq's active `llama-3.1-8b-instant` model to guarantee stability.

---

## 4. Future Improvements
* **Structured Multi-Agent Systems**: Split tasks among specialized sub-agents (e.g., a dedicated math sub-agent and a separate researcher agent) that communicate with each other using frameworks like LangGraph.
* **Web Search Engine Integration**: Upgrade Wikipedia searches to a general search engine (like Tavily or DuckDuckGo Search API) to fetch active current events and news.
* **Persistent Disk Memory**: Store historical messages in a database (like PostgreSQL or Redis) instead of Streamlit's in-memory session state, allowing users to resume chats days later.
