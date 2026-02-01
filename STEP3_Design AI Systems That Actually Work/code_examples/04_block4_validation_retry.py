from dataclasses import field
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

MAX_RETRIES = 3
retry_count = 0

messages = [
    {"role": "system", "content": "You are a helpful assistant that can help with cooking recipes."},
    {"role": "user", "content": "How do I make a chicken recipe?"}
]

class Ingredient(BaseModel):
    name: str = Field(description="the name of the ingredient")
    quantity: str = Field(description="the quantity of the ingredient, e.g: 2 cups")

class Recipe(BaseModel):
    name: str = Field(description="the name of the recipe")
    prep_time: int = Field(description="the preparation time in minutes")
    ingredients: list[Ingredient] = Field(description="the list of ingredients")

    @field_validator("name")
    @classmethod
    def check_title(cls, v):
        if "Chicken" in v:
            raise ValueError("No Chicken recipes allowed! I hate chicken!")
        return v

while retry_count < MAX_RETRIES:
    try:
        print(f"Attempt {retry_count + 1}...")
        completion = client.beta.chat.completions.parse(
            model="gpt-5-nano",
            messages=messages,
            response_format=Recipe
        )

        message = completion.choices[0].message
        if message.refusal:
            print(f"Safety Refusal: {message.refusal.reason}")
            break # stop trying if its a safety issue

        recipe = message.parsed
        print(f"Recipe Name: {recipe.name}")
        print(f"Ingredients to be used are: {[f"{ingredient.name} - {ingredient.quantity}" for ingredient in recipe.ingredients]}")
        break # exit the loop

    except Exception as e:
        print(f"Validation Error: {e}")
        retry_count += 1

        # Feed the error message back to the model
        # NOTE: we need to tell the model exactly why it failed so it can fix it
        messages.append({"role": "user", "content": f"Your previous response failed validation. Error: {e}. Please try again."})

if retry_count == MAX_RETRIES:
    print("Max retries reached. Failed to get a valid recipe.")
