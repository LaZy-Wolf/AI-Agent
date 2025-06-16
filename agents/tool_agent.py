from models import WorkflowState, Task
from tools.web_search import web_search
from tools.wikipedia_tool import wikipedia_search
from tools.youtube_tool import youtube_search
from tools.math_tool import calculate
from tools.browser_tool import open_url
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def tool_agent(state: WorkflowState) -> WorkflowState:
    web_search_tasks = 0
    max_web_searches = 2  # Limit to 2 Tavily calls
    for task in state.tasks:
        if task.status == "pending":
            task.status = "in_progress"
            query = task.description.lower()
            logger.info(f"Executing task {task.id}: {task.description}")
            try:
                if "youtube" in query or "play" in query:
                    task.result = youtube_search(task.description)
                elif "attraction" in query or "information" in query:
                    task.result = wikipedia_search(task.description)
                elif "calculate" in query or "compute" in query:
                    task.result = calculate(task.description)
                elif "open" in query and ("website" in query or "insta" in query):
                    task.result = open_url(task.description)
                else:
                    if web_search_tasks < max_web_searches and ("flights" in query or "hotels" in query or "budget" in query or "bookings" in query):
                        task.result = web_search(task.description)
                        web_search_tasks += 1
                    else:
                        task.result = "Task skipped to avoid rate limits."
                task.status = "completed" if task.result and "Error" not in task.result else "failed"
            except Exception as e:
                task.result = f"Error executing task: {str(e)}"
                task.status = "failed"
    return state