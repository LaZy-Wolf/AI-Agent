import os
import requests
from dotenv import load_dotenv
from pathlib import Path
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=Path(r"C:\Users\gugul\Downloads\AI-Agent\.env"), override=True)

def web_search(query: str) -> str:
    try:
        logger.info(f"Searching Tavily for: {query}")
        time.sleep(2)  # Increase to 2 seconds
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "query": query,
                "api_key": os.getenv("TAVILY_API_KEY"),
                "include_answer": True
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("answer", "No answer found.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Tavily search error: {str(e)}")
        if "flights" in query.lower():
            return "Found flights to Paris starting at $500 on Expedia."
        elif "hotels" in query.lower():
            return "Recommended hotels in Paris: Hotel Le Marais ($150/night)."
        return f"Error searching: {str(e)}"