from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: int
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None
    retries: int = 0  # Track retry attempts

class WorkflowState(BaseModel):
    query: str
    tasks: List[Task] = []
    final_output: Optional[str] = None