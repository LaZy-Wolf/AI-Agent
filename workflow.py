from langgraph.graph import StateGraph, END
from models import WorkflowState
from agents.plan_agent import plan_agent
from agents.tool_agent import tool_agent
from agents.reflection_agent import reflection_agent
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the graph with explicit state schema
workflow = StateGraph(WorkflowState)

# Nodes
workflow.add_node("plan", plan_agent)
workflow.add_node("execute", tool_agent)
workflow.add_node("reflect", reflection_agent)

# Edges
workflow.set_entry_point("plan")
workflow.add_edge("plan", "execute")
workflow.add_conditional_edges(
    "execute",
    lambda state: "reflect" if any(task.status == "failed" or "Error" in task.result for task in state.tasks) else END,
)
workflow.add_conditional_edges(
    "reflect",
    lambda state: "plan" if any(task.status == "pending" and task.retries < 1 for task in state.tasks) else END,
)

# Compile the graph with state schema
graph = workflow.compile()