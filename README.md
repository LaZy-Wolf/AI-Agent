AI Agent Workflow
This repository implements an AI agent workflow using LangGraph, Streamlit, and multiple APIs (Gemini, Gemma, Tavily) to process user queries dynamically. The workflow breaks queries into tasks, executes them using tools (web search, Wikipedia, YouTube, math, browser), and reflects on results to improve outcomes.
Features

Dynamic Task Generation: Uses Gemini/Gemma APIs to break queries into tasks.
Tool Integration: Supports web search (Tavily), Wikipedia, YouTube, math calculations, and browser actions.
Reflection Mechanism: Retries or splits failed tasks for robustness.
Streamlit Interface: User-friendly web app to input queries and view results.
Supported Queries:
"Plan a trip"
"Play Chemical song by Post Malone on YouTube"
"Calculate the area of a circle with radius 5"
"Open Insta"
"Search for recent news on AI"
Arbitrary queries (e.g., "Latest advancements in quantum computing")



Architecture

Plan Agent: Uses Gemini/Gemma to generate tasks from user queries.
Tool Agent: Executes tasks using tools (web search, Wikipedia, etc.).
Reflection Agent: Evaluates failed tasks, retries, or splits them.
Streamlit UI: Displays tasks, results, and final output.

Setup Instructions
Prerequisites

Python 3.10+
Git
API Keys:
Gemini API (for task generation)
Gemma API (fallback task generation)
Tavily API (for web search)



Local Setup

Clone the Repository:
git clone https://github.com/LaZy-Wolf/AI-Agent.git
cd AI-Agent


Create Virtual Environment:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Set Environment Variables:

Copy .env.example to .env:cp .env.example .env


Edit .env with your API keys:GEMINI_API_KEY=your_gemini_key
GEMMA_API_KEY=your_gemma_key
TAVILY_API_KEY=your_tavily_key




Run Streamlit App:
streamlit run app.py


Open http://localhost:8501 in your browser.
Enter queries (e.g., "Plan a trip") and view results.



Hosted Solution

Access the live app at: Streamlit App URL (replace with actual URL after deployment).
Enter queries and view results directly in the browser.
Note: The hosted app uses API keys configured in Streamlit Cloud’s “Secrets”.

Project Structure
AI-Agent/
├── app.py              # Streamlit app
├── workflow.py         # LangGraph workflow definition
├── models.py           # Pydantic models (WorkflowState, Task)
├── agents/
│   ├── plan_agent.py   # Task generation using Gemini/Gemma
│   ├── tool_agent.py   # Task execution with tools
│   ├── reflection_agent.py  # Task reflection and retry
├── tools/
│   ├── web_search.py   # Tavily web search
│   ├── wikipedia_tool.py  # Wikipedia search
│   ├── youtube_tool.py  # YouTube search
│   ├── math_tool.py    # Math calculations
│   ├── browser_tool.py # Browser actions (e.g., open URLs)
├── .env.example        # Example environment variables
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore file
├── .streamlit/
│   ├── config.toml     # Streamlit configuration

Running Tests

Run unit tests with pytest:pytest



Video Explanation

A 5-10 minute video walkthrough is available here (replace with Google Drive link).
Covers: Approach, architecture, code, and live demo.

Troubleshooting

API Errors: Ensure API keys in .env are valid.
ModuleNotFoundError: Verify all dependencies are installed (pip install -r requirements.txt).
Streamlit Issues: Check terminal logs and ensure Python 3.10+ is used.

License
MIT License. See LICENSE for details.
