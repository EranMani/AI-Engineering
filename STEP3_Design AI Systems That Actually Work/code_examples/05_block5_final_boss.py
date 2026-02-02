from typing import Union, Literal
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI
from enum import Enum
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

MAX_RETRIES = 3
CURRENT_RETRY = 0
CONFIDENCE_THRESHOLD = 0.6

class Commands(str, Enum):
    NAVIGATION = "Navigation"
    LIFE_SUPPORT = "Life Support"
    SECURITY = "Security"
    DANGEROUS = "Dangerous"
    UNKNOWN = "Unknown"

class Segments(str, Enum):
    BRIDGE = "bridge"
    CARGO = "cargo"

class DangerLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Dangerous(BaseModel):
    command: Literal["Dangerous"] = Field(description="The type of command")
    danger_level: DangerLevel = Field(description="The danger level of the command")
    reason: str = Field(description="The reason for the dangerous command")
    confidence: float = Field(description="The confidence score for the command")

class Unknown(BaseModel):
    command: Literal["Unknown"] = Field(description="The type of command")
    reason: str = Field(description="The reason for the unknown command")
    confidence: float = Field(description="The confidence score for the command")

class Navigation(BaseModel):
    command: Literal["Navigation"] = Field(description="The type of command")
    destination: str = Field(description="The destination to navigate to")
    warp_speed: float = Field(description="The speed to navigate at")
    confidence: float = Field(description="The confidence score for the command")

    @field_validator("warp_speed")
    @classmethod
    def validate_warp_speed(cls, v):
        if v > 9.9:
            raise ValueError("Warp speed cannot exceed 9.9")
        
        return v

class LifeSupport(BaseModel):
    command: Literal["Life Support"] = Field(description="The type of command")
    segment: Segments = Field(description="The segment to navigate to")
    status: bool = Field(description="The status of the life support")
    confidence: float = Field(description="The confidence score for the command")

class Security(BaseModel):
    command: Literal["Security"] = Field(description="The type of command")
    level: str = Field(description="The level of security")
    auth_code: str = Field(description="The authentication code")
    confidence: float = Field(description="The confidence score for the command")

class Command(BaseModel):
    command: Union[Navigation, LifeSupport, Security] = Field(description="The command to execute")

def call_ai(messages: dict, response_format: BaseModel) -> Command:
    completion = client.beta.chat.completions.parse(
        model="gpt-5-nano",
        messages=messages,
        response_format=response_format
    )

    return completion.choices[0].message.parsed

def add_new_message(messages: dict, role: str, content: str) -> dict:
    messages.append({
        "role": role, "content": content
    })

    return messages

def process_command(command: Command, result):
    if command == "Navigation":
        engage_engine(result.command.warp_speed)
    elif command == "Life Support":
        print(f"Life Support command: {result.command.segment} at status {result.command.status}")
    elif command == "Security":
        print(f"Security command: {result.command.level} at auth code {result.command.auth_code}")

def fallback_command(message: str):
    if "self destruct" in message.lower():
        return Dangerous(command=Commands.DANGEROUS, danger_level=DangerLevel.HIGH, reason="Self destruct command detected", confidence=1.0)

    return Unknown(reason="Unknown command detected", confidence=1.0)

def engage_engine(speed: float):
    print(f"Engaging engine at warp speed {speed}")
    print("🌟 STARSHIP ACCELERATING... (Whoosh!)")

messages = [
    {"role": "system", "content": "You are a helpful assistant that can help with navigation, life support, and security commands."},
    {"role": "user", "content": "I need to navigate to the bridge at warp speed 12."}
]

while CURRENT_RETRY < MAX_RETRIES:
    try:
        result = call_ai(messages, Command)
        if result.command.confidence < CONFIDENCE_THRESHOLD:
            fallback_result = fallback_command(messages[-1]["content"])
            if fallback_result.command == Commands.DANGEROUS:
                print(f"Dangerous command: {fallback_result.danger_level} detected. Reason: {fallback_result.reason}")
            elif fallback_result.command == Commands.UNKNOWN:
                print(f"Unknown command: {fallback_result.reason}")
            break

        process_command(result.command.command, result)
        break

    except Exception as e:
        print(f"Error: {e}")
        CURRENT_RETRY += 1

        add_new_message(messages, "user", f"Your previous response failed validation. Error: {e}. Please try again.")

if CURRENT_RETRY == MAX_RETRIES:
    print("System error! Maximum retries reached.")



