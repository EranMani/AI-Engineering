from pydantic import BaseModel, Field
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

TASKS_LIMIT = 3

class Task(BaseModel):
    task_id: int = Field(description="The id of the task")
    task_name: str = Field(description="The name of the task")
    task_description: str = Field(description="The description of the task")

class TaskList(BaseModel):
    tasks: list[Task] = Field(description="The list of tasks to perform")

class CodeOutput(BaseModel):
    code: str = Field(description="The code to perform the task")
    explanation: str = Field(description="The explanation of the code")

lead_agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt=f"You are a Tech Lead. Break down the feature request into small, actionable coding tasks. You are limited to {TASKS_LIMIT} tasks.",
    output_type=TaskList
)

coder_agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt="You are a Senior Python Developer. Write the code for the given task.",
    output_type=CodeOutput
)


def main():
    feature_request = "Add a 'Login with Google' feature."

    result = lead_agent.run_sync(user_prompt=feature_request)
    task_list = result.output.tasks
    
    for task in task_list:
        print(task)
        
        code_request = f"Write the code for the task: {task.task_name}. Here is the task description: {task.task_description}."
        result = coder_agent.run_sync(user_prompt=code_request)
        print(f"Coding agent: Here is the code for the task: \n {result.output.code} \n\n Here is the explanation: \n {result.output.explanation}")
        print("--------------------------------")



if __name__ == "__main__":
    main()