import requests
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool  # <-- Add this missing import line!
from pydantic import BaseModel, Field

# Define an explicit schema for the tool inputs so the LLM knows EXACTLY how to pass arguments
class WeatherInput(BaseModel):
    location: str = Field(description="The city name to fetch the weather forecast for, e.g., 'Goa', 'Delhi'")

@tool(args_schema=WeatherInput)
def get_weather_forecast(location: str) -> str:
    """
    Fetches a real-time weather forecast for a specific city using the Open-Meteo API.
    """
    # Coordinates map for database cities
    coordinates = {
        "delhi": {"lat": 28.6139, "lon": 77.2090},
        "mumbai": {"lat": 19.0760, "lon": 72.8777},
        "goa": {"lat": 15.2993, "lon": 74.1240},
        "bangalore": {"lat": 12.9716, "lon": 77.5946},
        "chennai": {"lat": 13.0827, "lon": 80.2707},
        "hyderabad": {"lat": 17.3850, "lon": 78.4867},
        "kolkata": {"lat": 22.5726, "lon": 88.3639},
        "jaipur": {"lat": 26.9124, "lon": 75.7873}
    }
    
    city_clean = str(location).strip().lower()
    if city_clean not in coordinates:
        return f"Weather data not found for city: {location}. Available cities: Delhi, Mumbai, Goa, Bangalore, Chennai, Hyderabad, Kolkata, Jaipur."
        
    coords = coordinates[city_clean]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            
            forecast_lines = [f"Weather Forecast for {location.title()}:"]
            for i in range(len(daily.get("time", []))):
                date = daily["time"][i]
                max_temp = daily["temperature_2m_max"][i]
                min_temp = daily["temperature_2m_min"][i]
                forecast_lines.append(f"• {date}: Max Temp: {max_temp}°C, Min Temp: {min_temp}°C")
                
            return "\n".join(forecast_lines[:3]) # Return first 3 days cleanly
        else:
            return f"Could not fetch weather data from API (Status Code: {response.status_code})."
    except Exception as e:
        return f"Error connecting to weather service: {str(e)}"