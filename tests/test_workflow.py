import pytest
from models import WorkflowState
from workflow import graph

def test_workflow():
    initial_state = WorkflowState(query="Calculate the area of a circle with radius 5")
    result = graph.invoke(initial_state)
    assert any("78.54" in task.result for task in result.tasks if task.result), "Math calculation failed"