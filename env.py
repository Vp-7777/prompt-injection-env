from dataset import get_sample
from reward import compute_reward

class PromptInjectionEnv:

    def __init__(self):
        self.state = None
        self.current = None

    def reset(self, task="easy"):
        self.current = get_sample(task)

        if self.current["type"] == "single":
            self.state = {
                "user_input": self.current["input"],
                "task_type": task
            }

        else:  # multi-step
            self.current["step"] = 0
            msg, _ = self.current["conversation"][0]

            self.state = {
                "user_input": msg,
                "task_type": task,
                "step": 0
            }

        return self.state

    def step(self, action):

        # SINGLE STEP
        if self.current["type"] == "single":
            reward = compute_reward(action, self.current["is_attack"])
            done = True

            return {
                "observation": self.state,
                "reward": reward,
                "done": done,
                "info": {}
            }

        # MULTI STEP (HARD TASK)
        else:
            step_idx = self.current["step"]
            _, is_attack = self.current["conversation"][step_idx]

            reward = compute_reward(action, is_attack)

            step_idx += 1
            self.current["step"] = step_idx

            if step_idx >= len(self.current["conversation"]):
                done = True
            else:
                next_msg, _ = self.current["conversation"][step_idx]
                self.state["user_input"] = next_msg
                self.state["step"] = step_idx
                done = False

            return {
                "observation": self.state,
                "reward": reward,
                "done": done,
                "info": {}
            }

    def get_state(self):
        return self.state   # ✅ FIXED