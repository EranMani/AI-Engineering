Architecture Decision Record: PydanticAI vs. Vanilla OpenAIDate: 2026-02-09Status: DecidedContext: We need to build reliable, type-safe AI agents. We evaluated two approaches: using the raw OpenAI SDK ("Vanilla") versus using the PydanticAI framework.1. Executive SummaryVerdict: Adopt PydanticAI.While Vanilla OpenAI is sufficient for simple, one-off scripts, it becomes unmanageable for complex agents involving tools, memory, and structured data. PydanticAI reduces boilerplate by ~60%, enforces type safety at runtime, and eliminates common classes of errors (like JSON parsing failures).2. The "Lines of Code" (LOC) MetricEstimates based on equivalent functionality.FeatureVanilla OpenAI (LOC)PydanticAI (LOC)ReductionSimple Chat10 lines5 lines50%Structured Output25 lines10 lines60%Tool Definition20 lines (JSON Schema)3 lines (Decorator)85%Tool Execution15 lines (Manual Parse)0 lines (Auto)100%Dependency InjectionHigh CouplingZero CouplingN/A3. Side-by-Side Code ComparisonA. Tools (The Biggest Winner)Vanilla (The "JSON Hell"):Python# 1. Define the function
def get_weather(city): ...

# 2. Manually write the schema (prone to typos)
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

# 3. Call the model
response = client.chat.completions.create(..., tools=tools)

# 4. Manually parse and execute
if response.choices[0].message.tool_calls:
    args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    get_weather(args["city"])
PydanticAI (The "Pythonic Way"):Python# 1. Define and Register in one step
@agent.tool
def get_weather(ctx: RunContext, city: str):
    """Get the weather for a city."""
    return f"Weather in {city} is sunny."

# 2. Run (Auto-execution included)
result = agent.run_sync("Weather in Tokyo?")
B. Structured OutputVanilla:Pythonclass Movie(BaseModel):
    title: str

# Must manually pass response_format AND parse the object path
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[...],
    response_format=Movie
)
data = response.choices[0].message.parsed
PydanticAI:Pythonagent = Agent(..., result_type=Movie)
# Result is already validated and parsed
result = agent.run_sync("Movie info")
data = result.data
4. Safety & Reliability AnalysisThe "JSON Decode" RiskVanilla: You must manually run json.loads(). If the LLM returns invalid JSON (e.g., missing a quote), your app crashes unless you wrap it in try/except blocks.PydanticAI: Handles retry logic internally. If the JSON is broken, it automatically asks the LLM to fix it (Self-Correction) without crashing the app.The "Coupling" Risk (Dependency Injection)Vanilla: You must pass user objects (user_id, db_conn) as arguments to every single function in your chain. Refactoring is painful.PydanticAI: Uses RunContext to inject dependencies only where they are needed. Your business logic remains clean and decoupled from your infrastructure code.5. ConclusionWe are moving forward with PydanticAI for the following reasons:Velocity: We write less code to achieve the same result.Reliability: The framework handles the "messy" parts of LLMs (parsing, retries, history).Maintainability: Type hints and decorators are standard Python practices; JSON schemas are not.