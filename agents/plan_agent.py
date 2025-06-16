import requests
import re
import logging
import os
from models import WorkflowState, Task
from typing import List
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(r"C:\Users\gugul\Downloads\AI-Agent\.env"), override=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
logger.info(f"GEMINI_API_KEY loaded: {GEMINI_API_KEY[:5]}...{GEMINI_API_KEY[-5:] if GEMINI_API_KEY else 'None'}")
logger.info(f"GEMMA_API_KEY loaded: {GEMMA_API_KEY[:5]}...{GEMMA_API_KEY[-5:] if GEMMA_API_KEY else 'None'}")

GEMMA_API_URL = "https://api.aimlapi.com/v1/chat/completions"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def call_gemma_api(prompt: str) -> str:
    if not GEMMA_API_KEY or len(GEMMA_API_KEY) < 10:
        logger.warning("Invalid Gemma API key, skipping")
        return ""
    headers = {
        "Authorization": f"Bearer {GEMMA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "google/gemma-3-4b-it",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that breaks down queries into tasks. Return tasks as a numbered list (e.g., 1. Task description)."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 1000,
    }
    try:
        logger.info("Calling Gemma API")
        response = requests.post(GEMMA_API_URL, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]
        logger.info(f"Gemma API response: {result[:100]}...")
        return result
    except Exception as e:
        logger.error(f"Gemma API error: {str(e)}")
        return ""

def call_gemini_api(prompt: str) -> str:
    if not GEMINI_API_KEY or len(GEMINI_API_KEY) < 10:
        logger.warning("Invalid Gemini API key, skipping")
        return ""
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
    }
    try:
        logger.info("Calling Gemini API")
        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        logger.info(f"Gemini API response: {result[:100]}...")
        return result
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return ""

def parse_tasks(api_response: str) -> List[Task]:
    tasks = []
    seen_descriptions = set()
    lines = api_response.split("\n")
    task_id = 1
    logger.info(f"Parsing API response: {api_response[:200]}...")
    for line in lines:
        line = line.strip()
        if re.match(r"^\d+\.\s*|^-\s*|^[*]\s*|^[0-9]+\)\s*|^[a-z]\.\s*", line) and not line.startswith("**"):
            task_desc = re.sub(r"^\d+\.\s*|^-\s*|^[*]\s*|^[0-9]+\)\s*|^[a-z]\.\s*", "", line).strip()
            if task_desc and task_desc not in seen_descriptions:
                tasks.append(Task(id=task_id, description=task_desc))
                seen_descriptions.add(task_desc)
                task_id += 1
    if not tasks:
        logger.warning("No tasks parsed, trying fallback parsing")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("**") and not line.startswith("#") and line not in seen_descriptions:
                tasks.append(Task(id=task_id, description=line))
                seen_descriptions.add(line)
                task_id += 1
    logger.info(f"Parsed {len(tasks)} tasks")
    return tasks

def plan_agent(state: WorkflowState) -> WorkflowState:
    query = state.query.lower()
    prompt = f"Break down the query '{query}' into a list of specific tasks. Return tasks as a numbered list (e.g., 1. Task description)."
    logger.info(f"Planning for query: {query}")
    
    api_response = call_gemini_api(prompt)
    if api_response:
        tasks = parse_tasks(api_response)
    else:
        if GEMMA_API_KEY and len(GEMMA_API_KEY) >= 10:
            api_response = call_gemma_api(prompt)
            tasks = parse_tasks(api_response) if api_response else []
        else:
            tasks = []
    
    if not tasks:
        logger.warning("Using fallback tasks")
        if "plan a trip" in query:
            tasks = [
                Task(id=1, description="Search for flights to Paris"),
                Task(id=2, description="Find hotels in Paris"),
                Task(id=3, description="List top attractions in Paris"),
            ]
        elif "play chemical song" in query:
            tasks = [Task(id=1, description="Search for Chemical by Post Malone on YouTube")]
        elif "calculate the area of a circle" in query:
            tasks = [Task(id=1, description="Compute circle area with radius 5")]
        elif "open insta" in query or "open instagram" in query:
            tasks = [Task(id=1, description="Open Instagram website")]
        else:
            tasks = [
                Task(id=1, description=f"Search for information on '{query}'"),
                Task(id=2, description=f"Check relevant sources for '{query}'")
            ]
    
    state.tasks = tasks
    logger.info(f"Assigned {len(tasks)} tasks to state")
    return state