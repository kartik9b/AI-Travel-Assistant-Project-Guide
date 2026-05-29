import json
import os
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool  # <-- Add this missing import line!
@tool

def search_flights(source: str = None, destination: str = None, **kwargs) -> str:
    """
    Searches for available flights from a source city to a destination city.
    Accepts source, from_city, destination, or to_city parameters.
    """
    # Fallback in case the LLM passes names like 'from_city' or 'to_city'
    src_city = source or kwargs.get("from_city") or kwargs.get("from")
    dst_city = destination or kwargs.get("to_city") or kwargs.get("to")
    
    if not src_city or not dst_city:
        return "Error: Missing source or destination city parameter."

    file_path = os.path.join("data", "flights.json")
    try:
        with open(file_path, "r") as f:
            flights = json.load(f)
        
        matches = [
            f for f in flights 
            if str(f.get("from", "")).lower() == str(src_city).lower() 
            and str(f.get("to", "")).lower() == str(dst_city).lower()
        ]
        
        if not matches:
            return f"No direct flights found from {src_city} to {dst_city} in our records."
            
        matches = sorted(matches, key=lambda x: x.get("price", 0))
        return json.dumps(matches[:3], indent=2)
    except Exception as e:
        return f"Error reading flight database: {str(e)}"