import json
import os
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool  # <-- Add this missing import line!

@tool
def search_hotels(city: str = None, **kwargs) -> str:
    """
    Finds available hotels and accommodations in a specific destination city.
    """
    target_city = city or kwargs.get("destination") or kwargs.get("destination_city") or kwargs.get("location")
    if not target_city:
        return "Error: Missing city parameter for hotel search."

    file_path = os.path.join("data", "hotels.json")
    try:
        with open(file_path, "r") as f:
            hotels = json.load(f)
            
        matches = [h for h in hotels if str(h.get("city", "")).lower() == str(target_city).lower()]
        
        if not matches:
            return f"No accommodations listed for {target_city}."
            
        matches = sorted(matches, key=lambda x: (-x.get("stars", 0), x.get("price_per_night", 0)))
        return json.dumps(matches[:4], indent=2)
    except Exception as e:
        return f"Error reading hotel database: {str(e)}"