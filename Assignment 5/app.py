import streamlit as st
import os
import requests
from dotenv import load_dotenv

# LangChain Imports
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

# Load environment variables
load_dotenv()

# App Configuration
st.set_page_config(
    page_title="Weather Tool Assistant",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling Injection
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #1e293b 100%);
        color: #f8fafc;
    }
    .app-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #38bdf8, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .app-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# WMO weather code descriptions
WMO_CODES = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
    45: "Fog 🌫️", 48: "Depositing rime fog 🌫️",
    51: "Light drizzle 🌧️", 53: "Moderate drizzle 🌧️", 55: "Dense drizzle 🌧️",
    56: "Light freezing drizzle 🌧️", 57: "Dense freezing drizzle 🌧️",
    61: "Slight rain 🌦️", 63: "Moderate rain 🌧️", 65: "Heavy rain 🌧️",
    66: "Light freezing rain 🌧️", 67: "Heavy freezing rain 🌧️",
    71: "Slight snow fall ❄️", 73: "Moderate snow fall ❄️", 75: "Heavy snow fall ❄️",
    77: "Snow grains ❄️",
    80: "Slight rain showers 🌦️", 81: "Moderate rain showers 🌦️", 82: "Violent rain showers 🌧️",
    85: "Slight snow showers ❄️", 86: "Heavy snow showers ❄️",
    95: "Thunderstorm ⛈️", 96: "Thunderstorm with slight hail ⛈️", 99: "Thunderstorm with heavy hail ⛈️"
}


# ==========================================
# 1. API HELPER FUNCTIONS
# ==========================================

def geocode_city(city_name: str):
    """
    Geocode city name to coordinates using Open-Meteo Geocoding API.
    """
    if not city_name or not city_name.strip():
        raise ValueError("City name cannot be empty.")
        
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={requests.utils.quote(city_name)}&count=1&language=en&format=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "name": result["name"],
                "country": result.get("country", ""),
                "admin1": result.get("admin1", "")
            }
        return None
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Internet connection error. Please verify your connection.")
    except Exception as e:
        raise RuntimeError(f"Error connecting to geocoding service: {e}")


def fetch_weather(latitude: float, longitude: float):
    """
    Fetch weather details for coordinates using Open-Meteo Forecast API.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "current" in data:
            current = data["current"]
            weather_code = current.get("weather_code", 0)
            condition = WMO_CODES.get(weather_code, "Unknown Condition 🌤️")
            return {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "condition": condition,
                "wind_speed": current.get("wind_speed_10m"),
                "temp_unit": data.get("current_units", {}).get("temperature_2m", "°C"),
                "humidity_unit": data.get("current_units", {}).get("relative_humidity_2m", "%"),
                "wind_unit": data.get("current_units", {}).get("wind_speed_10m", "km/h")
            }
        return None
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Internet connection error. Please verify your connection.")
    except Exception as e:
        raise RuntimeError(f"Error fetching weather details: {e}")


# ==========================================
# 2. LANGCHAIN WEATHER TOOL
# ==========================================

@tool
def get_weather(city: str) -> str:
    """Useful for fetching current weather metrics (temperature, conditions, humidity, wind speed) for a given city name.
    Do NOT call this tool with generic terms like 'here', 'today', 'now', or 'my location' as the city parameter. It must be a specific city name."""
    if not city or not city.strip() or city.strip().lower() in ["here", "today", "now", "my location", "current"]:
        return "Error: Please specify a concrete city name (e.g., 'London' or 'Tokyo') to check the weather."
    try:
        geo = geocode_city(city)
        if not geo:
            return f"Error: Could not locate city '{city}'. Please check the spelling."
        
        weather = fetch_weather(geo["latitude"], geo["longitude"])
        if not weather:
            return f"Error: Could not retrieve weather details for '{geo['name']}'."
        
        location = f"{geo['name']}, {geo['country']}"
        if geo['admin1']:
            location = f"{geo['name']}, {geo['admin1']}, {geo['country']}"
            
        summary = (
            f"Weather details for {location}:\n"
            f"- Temperature: {weather['temperature']}{weather['temp_unit']}\n"
            f"- Condition: {weather['condition']}\n"
            f"- Humidity: {weather['humidity']}{weather['humidity_unit']}\n"
            f"- Wind Speed: {weather['wind_speed']}{weather['wind_unit']}"
        )
        return summary
    except Exception as e:
        return f"Error fetching weather: {e}"

tools = [get_weather]


# ==========================================
# 3. LLM CONFIGURATION
# ==========================================

def get_llm(provider: str, api_key: str):
    """
    Configure and return the LLM model based on user settings.
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


def get_agent_executor(llm):
    """
    Initialize the conversational Weather Agent.
    """
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful Weather Assistant. You have access to a weather tool that fetches "
            "temperature, condition, humidity, and wind speed for a specific city name.\n"
            "CRITICAL: The weather tool requires a specific city name to function. If the user's query "
            "does not mention a city (e.g. 'will it rain today?'), do NOT call the tool or try to guess a city. "
            "Instead, politely ask the user which city they are asking about.\n"
            "Once a city is specified, use the tool and translate these observations into helpful advice (e.g., whether to bring an umbrella or wear a coat).\n"
            "If the user asks an unrelated question, politely redirect them to weather-related topics."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True
    )


# ==========================================
# 4. STREAMLIT UI & INTERFACE
# ==========================================

# Sidebar Configurations
st.sidebar.markdown("<h2 style='color:#38bdf8; font-weight:700;'>⚙️ API Settings</h2>", unsafe_allow_html=True)
provider = st.sidebar.selectbox("LLM Provider:", ["Groq", "OpenAI"], index=0)

api_key = ""
if provider == "Groq":
    env_key = os.getenv("GROQ_API_KEY", "")
    api_key = st.sidebar.text_input("Groq API Key:", value=env_key, type="password")
else:
    env_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.sidebar.text_input("OpenAI API Key:", value=env_key, type="password")

st.sidebar.markdown("<hr style='border:1px solid rgba(148,163,184,0.15);'>", unsafe_allow_html=True)
if st.sidebar.button("🧹 Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.sidebar.success("Chat history cleared!")
    st.rerun()

# Initialize Chat Memory state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main Title Header
st.markdown("<h1 class='app-title'>🌤️ Weather Tool Integration</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Integrate real-time APIs to answer weather questions naturally using LangChain Agents.</p>", unsafe_allow_html=True)

# Main Page Layout: Search Card at top, Chat assistant below
st.markdown("### 🔍 City Weather Lookup")
search_col1, search_col2 = st.columns([4, 1])

with search_col1:
    city_input = st.text_input("Enter city name:", placeholder="e.g. London, Paris, Tokyo, New York", label_visibility="collapsed")

with search_col2:
    search_clicked = st.button("Get Weather", use_container_width=True)

# Process Direct City Lookup
if search_clicked or (city_input and not st.session_state.messages):
    if not city_input.strip():
        st.warning("Please enter a valid city name.")
    else:
        with st.spinner("Fetching coordinates and weather details..."):
            try:
                # 1. Geocode
                geo = geocode_city(city_input)
                if not geo:
                    st.error(f"Could not find coordinates for city: '{city_input}'. Please check spelling.")
                else:
                    # 2. Fetch Weather
                    weather = fetch_weather(geo["latitude"], geo["longitude"])
                    if not weather:
                        st.error(f"Could not retrieve weather data for '{geo['name']}'.")
                    else:
                        # 3. Display Metrics
                        location = f"{geo['name']}, {geo['country']}"
                        if geo['admin1']:
                            location = f"{geo['name']}, {geo['admin1']}, {geo['country']}"
                        
                        st.markdown(f"#### 📍 Weather in {location}:")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-label'>🌡️ Temp</div>
                                <div class='metric-value'>{weather['temperature']}{weather['temp_unit']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-label'>🌤️ Condition</div>
                                <div class='metric-value' style='font-size: 1.2rem; margin-top:0.8rem;'>{weather['condition']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col3:
                            st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-label'>💧 Humidity</div>
                                <div class='metric-value'>{weather['humidity']}{weather['humidity_unit']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col4:
                            st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-label'>💨 Wind</div>
                                <div class='metric-value'>{weather['wind_speed']}{weather['wind_unit']}</div>
                            </div>
                            """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"API Error: {e}")

st.markdown("<hr style='border:1px solid rgba(148,163,184,0.15); margin: 2rem 0;'>", unsafe_allow_html=True)
st.markdown("### 💬 Ask Weather Questions to the Agent")

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Chat Input
if user_prompt := st.chat_input("Ask a question (e.g. 'Should I wear a coat in Berlin today?' or 'Is it raining in Sydney?')"):
    
    if not user_prompt.strip():
        st.warning("Please type a valid question.")
        st.stop()
        
    # Append user prompt
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    # 1. Error Handling: Missing Key
    if not api_key:
        err_msg = f"API Key for {provider} is missing. Please set it in the sidebar or config."
        st.error(err_msg)
        st.session_state.messages.append({"role": "assistant", "content": err_msg})
        st.stop()

    # 2. Setup LLM & Executor
    try:
        llm = get_llm(provider, api_key)
        agent_executor = get_agent_executor(llm)
    except Exception as e:
        err_msg = f"Error starting LLM/Agent: {e}"
        st.error(err_msg)
        st.session_state.messages.append({"role": "assistant", "content": err_msg})
        st.stop()

    # 3. Format Chat Memory history for LangChain
    chat_history_list = []
    for msg in st.session_state.messages[:-1]:
        if msg["role"] == "user":
            chat_history_list.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            chat_history_list.append(AIMessage(content=msg["content"]))

    # 4. Invoke Agent Weather Tool
    with st.status("🔍 Consulting weather API...", expanded=True) as status_box:
        try:
            result = agent_executor.invoke({
                "input": user_prompt,
                "chat_history": chat_history_list
            })
            
            response_content = result.get("output", "No response generated.")
            
            # Write agent planning actions
            intermediate_steps = result.get("intermediate_steps", [])
            if intermediate_steps:
                for action, obs in intermediate_steps:
                    status_box.markdown(f"**Action:** Querying weather API with input `{action.tool_input}`")
                    status_box.markdown(f"**API Response:**\n`{obs}`")
            else:
                status_box.write("Answered using internal knowledge (no API query required).")
                
            status_box.update(label="🤖 Answer compiled!", state="complete")
        except Exception as e:
            response_content = f"Failed to get weather details: {e}"
            status_box.update(label="❌ API Connection Failed", state="error")
            st.error(response_content)

    # 5. Display response
    st.chat_message("assistant").write(response_content)
    st.session_state.messages.append({"role": "assistant", "content": response_content})
