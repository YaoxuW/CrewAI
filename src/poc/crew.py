from crewai import Agent, Crew, Task, Process

class Poc:
    def crew(self) -> Crew:
        return Crew(
            agents=[],
            tasks=[],
            process=Process.sequential,
            verbose=True
		)