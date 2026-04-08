from dataset import get_sample
from reward import compute_reward
from models import Observation, Action, Reward
from grader import Grader


class PromptInjectionEnv:

    def __init__(self):
        self._state = None
        self.current = None
        self.grader = None

    def reset(self, task="easy"):
        self.grader = Grader()
        self.current = get_sample(task)

        if self.current["type"] == "single":
            self._state = Observation(
                user_input=self.current["input"],
                task_type=task,
                step=0
            )
        else:
            self.current["step"] = 0
            msg, _ = self.current["conversation"][0]

            self._state = Observation(
                user_input=msg,
                task_type=task,
                step=0
            )

        return self._state

    def step(self, action: Action):

        # =========================
        # VALIDATE ACTION
        # =========================
        if action.action_type not in ["ALLOW", "BLOCK", "SANITIZE"]:
            return {
                "observation": self._state,
                "reward": Reward(score=-1.0, reason="Invalid action"),
                "done": True,
                "info": {"error": "Invalid action"}
            }

        # =========================
        # SINGLE STEP
        # =========================
        if self.current["type"] == "single":

            is_attack = self.current["is_attack"]

            self.grader.evaluate_step(action.action_type, is_attack)

            score, reason = compute_reward(action.action_type, is_attack)

            final_score = self.grader.final_score()

            return {
                "observation": self._state,
                "reward": Reward(score=score, reason=reason),
                "done": True,
                "info": {
                    "final_score": final_score
                }
            }

        # =========================
        # MULTI STEP
        # =========================
        step_idx = self.current["step"]
        _, is_attack = self.current["conversation"][step_idx]

        self.grader.evaluate_step(action.action_type, is_attack)

        score, reason = compute_reward(action.action_type, is_attack)

        # Move to next step
        step_idx += 1
        self.current["step"] = step_idx

        if step_idx >= len(self.current["conversation"]):
            done = True
        else:
            next_msg, _ = self.current["conversation"][step_idx]

            self._state = Observation(
                user_input=next_msg,
                task_type=self._state.task_type,
                step=step_idx
            )
            done = False

        # Final score handling
        if done:
            final_score = self.grader.final_score()
            info = {"final_score": final_score}
        else:
            info = {}

        return {
            "observation": self._state,
            "reward": Reward(score=score, reason=reason),
            "done": done,
            "info": info
        }

    # =========================
    # API SUPPORT
    # =========================
    def get_state(self):
        return self._state

    # =========================
    # OPENENV SPEC (IMPORTANT)
    # =========================
    def state(self):
        return self._state