class Grader:

    def __init__(self):
        self.total_steps = 0
        self.correct_steps = 0
        self.partial_steps = 0
        self.false_positives = 0
        self.missed_attacks = 0

    def evaluate_step(self, action, is_attack):
        self.total_steps += 1

        action = str(action).strip().upper()

        # =========================
        # CASE 1: ATTACK INPUT
        # =========================
        if is_attack:

            if action == "BLOCK":
                self.correct_steps += 1

            elif action == "SANITIZE":
                self.partial_steps += 1

            else:
                self.missed_attacks += 1

        # =========================
        # CASE 2: SAFE INPUT
        # =========================
        else:

            if action == "ALLOW":
                self.correct_steps += 1

            elif action == "SANITIZE":
                self.partial_steps += 1

            elif action == "BLOCK":
                self.false_positives += 1

    def final_score(self):

        if self.total_steps == 0:
            return 0.0

        # =========================
        # BASE ACCURACY
        # =========================
        accuracy = self.correct_steps / self.total_steps

        # =========================
        # PARTIAL CREDIT
        # =========================
        partial_bonus = (self.partial_steps / self.total_steps) * 0.5

        # =========================
        # PENALTIES
        # =========================
        penalty = (
            (self.false_positives * 0.1) +
            (self.missed_attacks * 0.2)
        )

        # =========================
        # FINAL SCORE
        # =========================
        score = accuracy + partial_bonus - penalty

        # Clamp between 0 and 1
        score = max(0.0, min(1.0, score))

        return round(score, 2)