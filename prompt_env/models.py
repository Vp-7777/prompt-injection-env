from pydantic import BaseModel

class Observation(BaseModel):
    user_input: str
    task_type: str
    step: int = 0

class Action(BaseModel):
    action_type: str  # ALLOW / BLOCK / SANITIZE

class Reward(BaseModel):
    score: float
    reason: str