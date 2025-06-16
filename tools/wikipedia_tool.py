import wikipedia
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def wikipedia_search(query: str) -> str:
    try:
        wiki = wikipedia.Wikipedia('en')
        page = wiki.page(query)
        if page.exists():
            return page.summary[:500]  # Limit to 500 chars
        return f"No Wikipedia page found for '{query}'."
    except Exception as e:
        logger.error(f"Wikipedia search error: {str(e)}")
        return f"Error searching Wikipedia: {str(e)}"