from pydantic import BaseModel
from typing import List, Optional

class AgentCreateRequest(BaseModel):
    role: str
    goal: str
    background: Optional[str] = None
    version: bool = True

class TaskCreateRequest(BaseModel):
    description: str
    expected_output: Optional[str] = None
    agent_role: Optional[str] = None