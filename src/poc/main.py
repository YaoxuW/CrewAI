import sys
import warnings

from datetime import datetime
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from .models import AgentCreateRequest, TaskCreateRequest
from .crew import Poc
from crewai import Agent, Crew, Task, Process

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

load_dotenv()

app = FastAPI()

global_crew = Poc().crew()


@app.get("/")
def read_root():
    return {"message": "CrewAi + FastAPI Example"}


@app.post("/agents")
def create_agent(request: AgentCreateRequest):
    new_agent = Agent(
        role=request.role,
        goal=request.goal,
        backstory=request.backstory,
        verbose=request.verbose,
        # Tools
    )

    global_crew.agents.append(new_agent)
    return {"message": f"Agent '{request.role}' created and added to the crew."}


@app.get("/agents")
def list_agents():
    agents_info = []
    for agent in global_crew.agents:
        agents_info.append(
            {
                "role": agent.role,
                "goal": agent.goal,
                "backstory": agent.backstory,
                "verbose": agent.verbose,
            }
        )
    return {"agents": agents_info}


@app.post("/tasks")
def create_task(request: TaskCreateRequest):
    target_agent = None
    for agent in global_crew.agents:
        if agent.role == request.agent_role:
            target_agent = agent
            break

    if not target_agent:
        raise HTTPException(
            status_code=404, detail="Could not find an agent with that role."
        )

    new_task = Task(
        description=request.description,
        expected_output=request.expected_output or "",
        agent=target_agent,
    )

    global_crew.tasks.append(new_task)
    return {"message": f"Task created for agent '{target_agent.role}'."}


@app.get("/tasks")
def list_tasks():
    tasks_info = []
    for task in global_crew.tasks:
        tasks_info.append(
            {
                "description": task.description,
                "expected_output": task.expected_output,
                "assigned_agent": task.agent.role if task.agent else None,
            }
        )
    return {"tasks": tasks_info}


@app.post("/crew/run")
def run():
    try:
        crew_output = global_crew.kickoff()
        print(f"Raw Output: {crew_output.raw}")
        return {"message": "Crew run completed", "raw_output": crew_output.raw}
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
