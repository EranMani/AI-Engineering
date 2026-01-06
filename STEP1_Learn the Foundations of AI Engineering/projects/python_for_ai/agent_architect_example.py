from typing import Dict, Any, Tuple, Set, List


agent_profile: Dict[str, Any] = {
    "name": "Matt",
    "level": 30,
    "is_alive": True
}

start_coords: Tuple[int, int] = (25, 80)

skills: Set[str] = {"Stealth", "Hacking", "Stealth"}

mission_history: [List[str]] = ["Setup complete"]

print(skills)

def create_agent(name: str, level: int, is_alive: bool) -> Dict[str, Any]:
    return {"name": name, "level": level, "is_alive": is_alive}

new_agent = create_agent("Saruman", 99, True)


class Agent:
    def __init__(self, name:str, level:int , is_alive:bool):
        self.name = name
        self.level = level
        self.is_alive = is_alive