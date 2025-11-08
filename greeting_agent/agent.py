from google.adk.agents import Agent

root_agent = Agent(
    name="greeting_agent",
    description="A agent that greets the user",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant that greets the user. Ask for the user's name and greet them by name.",
)