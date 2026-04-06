from fastapi import FastAPI
from models import Action
from env import PromptInjectionEnv

app = FastAPI()   # ✅ THIS LINE IS VERY IMPORTANT

env = PromptInjectionEnv()

@app.post("/reset")
def reset(task: str = "easy"):
    return env.reset(task)

@app.post("/step")
def step(action: Action):
    return env.step(action)

@app.get("/state")
def state():
    return env.get_state()