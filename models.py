from pydantic import BaseModel

class Observation(BaseModel):
    user_input: str
    task_type: str

class Action(BaseModel):
    decision: str  # ALLOW | BLOCK | SANITIZE
    response: str