from httpx._transports import mock
import pytest
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelMessage, ModelResponse, ToolCallPart
from datetime import datetime

from my_agent import Decision, agent, UserProfile, Decision, LoyaltyTier

"""
NOTE: FunctionModel looks like a model. The Agent talks to it like a model. 
      But inside, it is just a simple Python function you wrote.
      It does exactly what you tell it to do, every single time. No improvising.

NOTE: ModelMessage, When the Agent talks to the model, it sends the entire conversation history.
      This list of events is a list of ModelMessage objects.

NOTE: ModelResponse, This is what the Stunt Double says back to the Agent.
      It can be text: ModelResponse(parts=[TextPart("Hello!")])
      It can be an action: ModelResponse(parts=[ToolCallPart(...)])
"""

def mock_brain_function(messages: list[ModelMessage], info) -> ModelResponse:
    # Logic: Look at how many messages correspond to "turns" in the conversation.

    # 🕵️‍♂️ SPY: Print the last message the Agent sent us
    if messages:
        last_msg = messages[-1]
        print(f"\n📨 MESSAGE RECEIVED BY BRAIN (Type: {type(last_msg).__name__}):")
        
        # If it's a Retry Prompt (Validation Error), it comes as a UserMessage or similar
        # Let's just print the content to be safe
        if hasattr(last_msg, 'parts'):
            for part in last_msg.parts:
                print(f"   -> CONTENT: {part}")

    # TURN 1: if there is only 1 message (user input), ask for the order
    if len(messages) == 1:
        # return the response that tells the agent: call this tool
        return ModelResponse(parts=[
            ToolCallPart(
                tool_name="get_order",
                args={"order_id": "order123"}
            )
        ])

    # TURN 2: if there are more messages, it means the tool ran
    else:
        # pretend we read the tool output and decided to Reject
        # we pass the date of purchase here
        return ModelResponse(parts=[
            ToolCallPart(
                tool_name="final_result",
                args={
                    "decision": "REJECTED",
                    "refund_amount": 0.0,
                    "reasoning": "The order is too old to be refunded.",
                    "date_of_purchase": '2020-01-01'
                }
            )
        ])

@pytest.mark.asyncio
async def test_agent_rejects_old_orders():
    # 1. SETUP: Override the brain
    with agent.override(model=FunctionModel(mock_brain_function)):
        
        print(f"\n🚀 STARTING TEST WITH AGENT FROM: {agent.model}")

        try:
            # 2. RUN: Increase retries to 5 so we don't crash instantly
            #    This allows the agent to try to fix the validation error (though our mock is dumb and won't)
            result = await agent.run(
                user_prompt="I want to refund my order123", 
                deps=UserProfile(id=123, name="John Doe", loyalty_tier=LoyaltyTier.BRONZE)
            )
            
            # 3. ASSERT: Use .data to access the result
            print(f"\n📊 SUCCESS! Result: {result}")
            assert result.output.decision == Decision.REJECTED
            assert result.output.reasoning == "The order is too old to be refunded."

        except Exception as e:
            # 🚨 THIS WILL REVEAL THE HIDDEN ERROR
            print(f"\n💥 CRASH DETECTED!")
            print(f"   Error Type: {type(e)}")
            print(f"   Error Message: {e}")

            # If there is a hidden cause (like a Validation Error), print it
            if hasattr(e, '__cause__') and e.__cause__:
                print(f"   🕵️‍♂️ REAL CAUSE: {e.__cause__}")
            
            raise e # Fail the test

        # 4. VERIFY TOOLS
        tool_names = [
            part.tool_name 
            for msg in result.new_messages() 
            if msg.parts 
            for part in msg.parts 
            if part.part_kind == 'tool-call'
        ]
        print(f"\nTools called: {tool_names}")
        assert "get_order" in tool_names
        

       

