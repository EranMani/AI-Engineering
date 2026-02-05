from pydantic_ai import Agent, RunContext

# We define the agent once. This acts as our "Service" definition.
# We are using a 'fake' model for now so we don't need an API key yet.
agent = Agent(
    'test',  # This replaces 'gpt-4o' for testing
    deps_type=str, # <--- Pay attention here
    system_prompt="You are a helpful assistant. Use the user's name in your response."
)

@agent.system_prompt
def add_user_name(ctx: RunContext[str]) -> str:
    # This function runs AUTOMATICALY every time the agent is called.
    return f"The user's name is {ctx.deps}."

# Simulating running it with a specific user context
# We pass 'Eran' as the dependency
result = agent.run_sync("Hello, who am I?", deps="Eran")

print(result.data)
# Output (simulated): "Hello! You are Eran."