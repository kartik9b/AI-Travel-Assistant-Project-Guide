import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import your custom tools from the tools folder
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.places_tool import discover_places
from tools.weather_tool import get_weather_forecast

def initialize_travel_agent(api_key: str):
    """
    Initializes and configures the LangChain agent with custom data retrieval tools.
    """
    # Group the tools into a list for the agent
    tools = [search_flights, search_hotels, discover_places, get_weather_forecast]
    
    # Initialize the OpenAI model (using gpt-4-turbo for reliable reasoning)
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3, openai_api_key=api_key)
    
    # Define system instructions to force a logical workflow
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert AI Travel Planner. Your mission is to construct optimized, budget-tracked, structured itineraries.
        
        CRITICAL EXECUTION PROTOCOL:
        1. Query `search_flights` to find transit options between cities. Highlight the cheapest/best fit.
        2. Query `Google Hotels` to locate accommodation options in the destination city.
        3. Query `get_weather_forecast` to provide weather expectations for the trip.
        4. Query `discover_places` to distribute points of interest cleanly across days.
        5. Provide a transparent total cost summary (Flights + Hotels calculated by days + estimated meals/local transport).
        
        Always present your final itinerary cleanly using structured markdown layout sections."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Construct the OpenAI Tools Agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Return the executor with verbose=True so you can watch its "thought process" in the terminal
    return AgentExecutor(agent=agent, tools=tools, verbose=True)