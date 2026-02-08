import pytest
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelMessage, ModelResponse, ToolCallPart

from fact_checker import agent, Verdict, AgentContext

# the mock brain
def mock_brain_function(messages: list[ModelMessage], info) -> ModelResponse:
    if len(messages) == 1:
        return ModelResponse(parts=[
            ToolCallPart(
                tool_name="search_web",
                args={"query": "eiffle tower exists in holland"}
            )
        ])
    else:
        return ModelResponse(parts=[
            ToolCallPart(
                tool_name="final_result",
                args={
                    "claim": "eiffle tower exists in holland",
                    "verdict": Verdict.FALSE,
                    "evidence": "Eiffle tower exists in franch!",
                    "source_url": "https://www.google.com"
                }
            )
        ])

@pytest.mark.asyncio
async def test_search_incremenet_and_verdict():
    ctx = AgentContext()

    with agent.override(model=FunctionModel(function=mock_brain_function)):
        result = await agent.run(
            "eiffle tower exists in holland",
            deps=ctx
        )

    print(f"\n📊 Verdict: {result.output.verdict}")
    print(f"evidence: {result.output.evidence}")
    assert result.output.verdict == Verdict.FALSE

    print(f"🔢 Search Count: {ctx.search_count}")
    assert ctx.search_count == 1