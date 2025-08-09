import random

class Player:
    def __init__(self, name="Unknown"):
        self.name = name
        self.shots_taken = 0
        self.shots_made = 0
        self.passes_attempted = 0
        self.passes_made = 0

    def pass_ball(self):
        self.passes_attempted += 1
        success_chance = (self.passes_made / self.passes_attempted) * 100 if self.passes_attempted > 0 else 0
        roll = random.randint(1, 100)
        if roll > success_chance:
            self.passes_made += 1
            return True
        return False

    def take_shot(self, shot_value):
        self.shots_taken += 1
        max_roll = {1: 70, 2: 100, 3: 125}.get(shot_value, 125)
        roll = random.randint(1, max_roll)
        success_chance = (self.shots_made / self.shots_taken) * 100 if self.shots_taken > 0 else 0
        if roll > success_chance:
            self.shots_made += 1
            return shot_value
        return 0
