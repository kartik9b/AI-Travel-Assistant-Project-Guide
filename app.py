import streamlit as st
import os

# Import the correct Ollama integration module from LangChain
from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import your custom database tools from the tools folder
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.places_tool import discover_places
from tools.weather_tool import get_weather_forecast

def initialize_local_travel_agent():
    """
    Initializes the local LangChain tool-calling agent using an optimized 
    local Ollama model instance.
    """
    # Group the active local tool parameters together
    tools = [search_flights, search_hotels, discover_places, get_weather_forecast]
    
    # Initialize the Local Ollama Model engine. 
    # Using 'qwen2.5:3b' (or fallback 'qwen2.5:1.5b') with a low temperature to minimize hallucinations.
    llm = ChatOllama(model="qwen2.5:3b", temperature=0.1)
    
    # Cleaned, strict System Reasoning Prompts to keep the local model from outputting JSON objects
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert AI Travel Planner. You have access to specialized tools that fetch REAL flight, hotel, tourist attraction, and weather data.
        
        STRICT OPERATIONAL PROTOCOLS:
        1. If the user wants a trip from Delhi to Goa, you MUST pass source="Delhi" and destination="Goa" to the `search_flights` tool. Do not guess other cities.
        2. Always use `Google Hotels` for the user's selected Destination City only.
        3. Never output raw JSON strings, empty JSON frames, or tool schema brackets (e.g., '{{"name": ...}}') to the final user interface.
        4. Read the text outputs returned by your tools, process the data contextually, and compile a clean, readable, day-by-day Markdown itinerary. Include pricing summaries and clear headings."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Compile the active tool calling pipeline agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


# --- STREAMLIT USER INTERFACE LAYOUT DESIGN ---
st.set_page_config(page_title="Local Agentic AI Travel Planner", page_icon="✈️", layout="wide")

st.title("🗺️ Local Agentic AI Travel Planning Assistant")
st.caption("Internship Capstone Project — Powered by LangChain, Local Ollama, & Open-Meteo API")

# Sidebar Status Control Panel Layout (No API key needed anymore!)
with st.sidebar:
    st.header("🖥️ System Infrastructure")
    st.success("Connected to Local Ollama Instance")
    st.markdown("---")
    st.markdown("### Supported Database Cities:")
    st.info("Delhi, Mumbai, Goa, Bangalore, Chennai, Hyderabad, Kolkata, Jaipur")

# Main Dashboard Application Interactive Input Layout Form
st.subheader("Plan Your Upcoming Journey")
col1, col2, col3 = st.columns(3)

with col1:
    src = st.selectbox("Departure City (Source)", ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Jaipur", "Goa"])
with col2:
    dst = st.selectbox("Destination City", ["Goa", "Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Jaipur"])
with col3:
    duration = st.slider("Trip Duration (Days)", min_value=1, max_value=5, value=3)

preferences = st.text_input("Special Requirements / Preferences (e.g., 'Budget travel under ₹10,000', 'Prefer luxury hotels')", "")

if st.button("🚀 Generate Optimized Travel Plan"):
    if src == dst:
        st.error("Source and Destination inputs cannot match.")
    else:
        with st.spinner("Local AI Agent is reasoning, querying local files, and fetching weather telemetry..."):
            try:
                # Instantiate running framework instance natively
                runner = initialize_local_travel_agent()
                
                # Construct clean deterministic search query
                query = f"Build a structured {duration}-day trip itinerary from {src} to {dst}."
                if preferences:
                    query += f" Take into account these specific traveler preferences: {preferences}"
                
                # Execute pipeline query sequence 
                result = runner.invoke({"input": query})
                
                # Render beautifully formatted Markdown presentation directly on the dashboard page
                st.success("✨ Itinerary Formulated Successfully!")
                st.markdown("---")
                st.markdown(result["output"])
                
            except Exception as e:
                st.error(f"An unexpected runtime exception stopped execution: {str(e)}")