import logging
from models import WorkflowState, Task
from agents.plan_agent import call_gemini_api, call_gemma_api, parse_tasks
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env
load_dotenv(dotenv_path=Path(r"C:\Users\gugul\Downloads\AI-Agent\.env"), override=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def reflection_agent(state: WorkflowState) -> WorkflowState:
    logger.info("Reflecting on tasks...")
    
    for task in state.tasks.copy():
        if task.status == "completed" and task.retries < 1 and ("Error" in task.result or "No Wikipedia page found" in task.result):
            logger.info(f"Evaluating task {task.id}: {task.description}")
            prompt = f"""
            Task: {task.description}. Result: {task.result}.
            Should we:
            1. Retry as-is (if temporary error)?
            2. Split into subtasks (if too complex)?
            3. Give up (if impossible)?
            Respond with "RETRY", "SPLIT: <subtask1>, <subtask2>", or "ABORT".
            """
            response = call_gemini_api(prompt)
            if "Error" in response:
                response = call_gemma_api(prompt)
            
            if "SPLIT:" in response:
                logger.info(f"Splitting task {task.id} into subtasks")
                subtasks = parse_tasks(response.split("SPLIT:")[1])
                for i, subtask in enumerate(subtasks, start=len(state.tasks)+1):
                    subtask.id = i
                    state.tasks.append(subtask)
                state.tasks.remove(task)
            elif "RETRY" in response and task.retries < 1:
                logger.info(f"Retrying task {task.id}")
                task.status = "pending"
                task.retries += 1
            elif "ABORT" in response:
                logger.info(f"Aborting task {task.id}")
                task.status = "failed"
        
        elif task.status == "failed" and task.retries < 1:
            logger.info(f"Retrying failed task {task.id}")
            task.status = "pending"
            task.retries += 1
    
    # Generate final output for any tasks
    if state.tasks:
        state.final_output = "\n".join(
            f"Task {t.id}: {t.result if t.result else 'No result yet'}"
            for t in state.tasks
        )
        logger.info("Generated final output")
    
    return state