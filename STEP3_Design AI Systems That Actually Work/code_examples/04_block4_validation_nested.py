from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant that can help with cooking recipes."},
    {"role": "user", "content": "Give me a recipe for chocolate cake."}
]

class Ingredient(BaseModel):
    name: str = Field(description="the name of the ingredient")
    quantity: str = Field(description="the quantity of the ingredient, e.g: 2 cups")

class Recipe(BaseModel):
    title: str = Field(description="the title of the recipe")
    prep_time: int = Field(description="the preparation time in minutes")
    ingredients: list[Ingredient] = Field(description="the list of ingredients")

completion = client.beta.chat.completions.parse(
    model="gpt-5-nano",
    messages=messages,
    response_format=Recipe
)

recipe = completion.choices[0].message.parsed
print(f"Recipe Title: {recipe.title}")
print(f"Ingredients to be used are: {[f"{ingredient.name} - {ingredient.quantity}" for ingredient in recipe.ingredients]}")