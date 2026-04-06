import requests

BASE_URL = "http://localhost:8000"

def simple_agent(obs):
    text = obs["user_input"].lower()

    if "ignore" in text or "reveal" in text or "system" in text:
        return {"decision": "BLOCK", "response": "Request denied"}
    else:
        return {"decision": "ALLOW", "response": "Valid response"}

def run():
    obs = requests.post(f"{BASE_URL}/reset").json()

    done = False
    total_reward = 0
    step = 0

    print("[START]")

    while not done:
        action = simple_agent(obs)

        result = requests.post(f"{BASE_URL}/step", json=action).json()

        step += 1
        total_reward += result["reward"]

        print(f"[STEP] step={step} action={action} reward={result['reward']} done={result['done']}")

        done = result["done"]
        obs = result["observation"]   # 🔥 IMPORTANT

    print(f"[END] total_reward={total_reward}")

if __name__ == "__main__":
    run()