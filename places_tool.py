import json
import os
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool  # <-- Add this missing import line!

@tool
def discover_places(city: str) -> str:
    """
    Retrieves top sightseeing spots, parks, temples, and attractions for a given city with visitor ratings.
    """
    file_path = os.path.join("data", "places.json")
    try:
        with open(file_path, "r") as f:
            places = json.load(f)
            
        matches = [p for p in places if p["city"].lower() == city.lower()]
        
        if not matches:
            return f"No unique tourist landmarks found for {city}."
            
        # Sort by best rating
        matches = sorted(matches, key=lambda x: x["rating"], reverse=True)
        return json.dumps(matches[:6], indent=2)
    except Exception as e:
        return f"Error reading places database: {str(e)}"