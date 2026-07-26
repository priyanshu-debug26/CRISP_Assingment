# Reflection Report - Assignment 5: Tool Integration

## 1. What Was Built
I implemented a **Weather API Tool Integration** within a Streamlit dashboard. The application provides two interfaces: a direct city weather lookup widget displaying real-time metrics (Temperature, Condition, Humidity, and Wind Speed) in styled cards, and an interactive chat interface powered by a LangChain Agent. The agent decides when to invoke the custom weather API tool, receives raw JSON payloads, parses them, and responds to natural-language user questions (e.g. *"Should I bring a jacket in London?"* or *"Compare the weather in Tokyo and Sydney"*).

---

## 2. Technical Concepts Explained

### How API Integration Works
API (Application Programming Interface) integration is the process of connecting an application to external software components to exchange data. In this project:
1. The user inputs a city name.
2. The application uses the `requests` library to send an HTTP GET request to the Open-Meteo Geocoding API, which matches the city name to latitude and longitude coordinates.
3. It takes these coordinates and makes a second HTTP GET request to the Open-Meteo Forecast API.
4. The API returns a JSON payload containing weather variables.
5. The application parses the JSON response, translates numeric weather codes into human-readable conditions, and formats them for either the Streamlit UI or the LangChain agent.

---

## 3. Challenges Faced
* **WMO Weather Code Parsing**: Open-Meteo returns integer weather codes (e.g. 0, 3, 51) rather than plain-text descriptions. I resolved this by mapping WMO weather codes to user-friendly descriptions and emojis (e.g., `0: "Clear sky ☀️"`) to make the interface clear.
* **Geocoding City Names**: Weather APIs usually require exact coordinates (lat/lon) or special city IDs. Using the Open-Meteo Geocoding API resolved this, allowing users to type standard names (like "New York") and converting them to coordinates dynamically.
* **API Availability**: OpenWeatherMap API requires email signups and key approval cycles. To eliminate key issues for reviewers, I integrated Open-Meteo, which is free and does not require keys, ensuring 100% immediate runnability.

---

## 4. What Was Learned
* **API Requests & Parsing**: Deepened understanding of handling HTTP status codes, query quoting, and handling exceptions (like `ConnectionError` or `Timeout`) gracefully in Python.
* **Structuring LLM Tools**: Learned how to define tool inputs and descriptions clearly. The LLM relies on the tool description docstring to understand what parameters to supply, so naming it descriptively is crucial.

---

## 5. Future Improvements
* **Interactive Maps**: Integrate `folium` or `deck.gl` to display the geocoded city coordinates on an interactive 3D map.
* **Air Quality Index (AQI)**: Integrate Open-Meteo's Air Quality API to retrieve metrics like PM2.5, PM10, and ozone concentrations.
* **Multi-Day Forecasting**: Provide 7-day weather trend charts using Streamlit line charts (`st.line_chart`) to visualize temperature fluctuations over time.
