from crewai import Agent, Crew, Task, Process


class Poc:
    def default_agent(self) -> Agent:
        """A single, generic agent with minimal specialization."""
        return Agent(
            role="Generic Agent",
            goal="Handle tasks of a broad scope",
            backstory="A general-purpose agent with minimal specialization",
            verbose=True,
        )

    def default_task(self) -> Task:
        """A default, generic task assigned to the default agent."""
        return Task(
            description="Perform a general demonstration of agent capabilities.",
            expected_output="A brief summary of the agent's process or findings",
            agent=self.default_agent(),
        )

    def crew(self) -> Crew:
        """
        Creates a Crew with one default agent and one default task.
        This satisfies the requirement that Crew has at least one agent and one task.
        """
        return Crew(
            agents=[self.default_agent()],
            tasks=[self.default_task()],
            process=Process.sequential,
            verbose=True,
        )
