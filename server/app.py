from fastapi import FastAPI
from prompt_env.env import PromptInjectionEnv
from models import Action   # ✅ FIXED HERE

app = FastAPI()
env = PromptInjectionEnv()


@app.get("/reset")
def reset(task: str = "easy"):
    return env.reset(task)


@app.post("/step")
def step(action: Action):
    return env.step(action)


@app.get("/state")
def state():
    return env.get_state()


# ✅ REQUIRED MAIN FUNCTION FOR OPENENV
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


# ✅ REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()