import pytest
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelMessage, ModelResponse, ToolCallPart

from credit_agent import agent, UserFinancialProfile, RiskProfile, Decision, mock_db

def mock_brain_function(messages: list[ModelMessage], info) -> ModelResponse:
    if messages:
        last_msg = messages[-1]
        print(last_msg)
        print(f"\n📨 MESSAGE RECEIVED BY BRAIN (Type: {type(last_msg).__name__}):")

    if len(messages) == 1:
        return ModelResponse(parts=[
            ToolCallPart(
                tool_name="get_monthly_spending",
                args={"user_id": 1}
            )
        ])
    else:
        return ModelResponse(parts=[
            ToolCallPart(
                tool_name="final_result",
                args={
                    "decision": Decision.REJECTED,
                    "reasoning": "The user risk profile is high.",
                    "new_limit": 5000.0,
                    "avg_monthly_spend": 1000.0
                }
            )
        ])

@pytest.mark.asyncio
async def test_agent_reject_high_risk_profile():
    with agent.override(model=FunctionModel(mock_brain_function)):
        try:
            result = await agent.run(
                user_prompt="Increase the credit limit for user 1 to $10,000",
                deps=UserFinancialProfile(user_id=1, annual_income=100000, current_limit=2000, risk_profile=RiskProfile.HIGH, db_connection=mock_db)
            )

            print(f"\n📊 SUCCESS! Result: {result}")
            assert result.output.decision == Decision.REJECTED
            assert result.output.reasoning == "Policy Violation: High Risk Profile."

        except Exception as e:
            print(f"\n Crash Detected!!")
            print(f"Error type: {type(e)}")
            print(f"Error message: {e}")

            raise e # fail the test

        tool_names = [
            part.tool_name 
            for msg in result.new_messages() 
            if msg.parts 
            for part in msg.parts 
            if part.part_kind == 'tool-call'
        ]
        print(f"\nTools called: {tool_names}")
        assert "get_monthly_spending" in tool_names