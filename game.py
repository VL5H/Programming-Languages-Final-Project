import asyncio
import random
from player import Player

class Game:
    def __init__(self, vs_friend=False):
        self.team = [Player(name) for name in ["Lebron", "Kyrie", "Durant", "Curry", "Booker"]]
        self.player_with_ball = random.randint(0, 4)
        self.your_score = 0
        self.friend_score = 0
        self.computer_score = 0
        self.possessions_left = 10
        self.vs_friend = vs_friend

    async def display_player_stats(self):
        p = self.team[self.player_with_ball]
        print(f"\nPlayer {p.name} has the ball.")
        print(f"Shots Taken: {p.shots_taken}, Shots Made: {p.shots_made}")
        print(f"Passes Attempted: {p.passes_attempted}, Passes Made: {p.passes_made}")

    async def display_team_stats(self):
        for i, p in enumerate(self.team):
            print(f"\nPlayer {i}: {p.name}")
            print(f"Shots Taken: {p.shots_taken}, Shots Made: {p.shots_made}")
            print(f"Passes Attempted: {p.passes_attempted}, Passes Made: {p.passes_made}")

    async def display_team_roster(self):
        print("\n=== Your Team Roster ===")
        for i, player in enumerate(self.team):
            print(f"  [{i}] {player.name}")
        print("============================")

    def reset_possession(self):
        self.player_with_ball = random.randint(0, 4)

    async def get_action(self):
        print("\nChoose an action:")
        print("s = Shoot, p = Pass, t = Team Stats, c = Current Score")
        return input("Your action: ").strip().lower()

    async def player_turn(self):
        self.reset_possession()
        await self.display_player_stats()
        while True:
            action = await self.get_action()

            if action == 's':
                shot_value = int(input("Enter shot value (2 or 3): "))
                score = self.team[self.player_with_ball].take_shot(shot_value)
                if score > 0:
                    print(f"Shot success! You scored {score} points.")
                    self.your_score += score
                    break
                else:
                    print("Shot failed!")
                    if random.choice([True, False]):
                        print("Turnover!")
                        await (self.friend_turn() if self.vs_friend else self.computer_turn())
                        return
                    else:
                        print("You retain possession.")
            elif action == 'p':
                target = int(input("Pass to teammate (0-4): "))
                if self.team[self.player_with_ball].pass_ball():
                    print("Pass successful.")
                    self.player_with_ball = target
                else:
                    print("Pass failed!")
                    if random.choice([True, False]):
                        print("Interception!")
                        await (self.friend_turn() if self.vs_friend else self.computer_turn())
                        return
                    else:
                        print("You retain possession.")
            elif action == 't':
                await self.display_team_stats()
            elif action == 'c':
                print(f"Your Score: {self.your_score}")
                print(f"{'Friend' if self.vs_friend else 'Computer'} Score: {self.friend_score if self.vs_friend else self.computer_score}")
                print(f"Possessions left: {self.possessions_left}")
            else:
                print("Invalid action.")
        self.possessions_left -= 1
        await (self.friend_turn() if self.vs_friend else self.computer_turn())

    async def computer_turn(self):
        print("\n--- Computer's Turn ---")
        for _ in range(3):  # allow up to 3 shots after rebounds
            if random.randint(1, 100) >= 40:
                pts = random.randint(2, 3)
                self.computer_score += pts
                print(f"Computer scored {pts} points!")
                break
            else:
                print("Your team intercepted the ball!")
                break

        self.possessions_left -= 1

    async def friend_turn(self):
        self.reset_possession()
        print("\n--- Player 2's Turn ---")
        self.player_with_ball = random.randint(0, 4)
        await self.display_player_stats()
        action = await self.get_action()
        if action == 's':
            shot_value = int(input("Player 2: Shot value (1-3): "))
            score = self.team[self.player_with_ball].take_shot(shot_value)
            if score > 0:
                print(f"Player 2 scored {score} points!")
                self.friend_score += score
            else:
                print("Player 2 missed!")
        elif action == 'p':
            target = int(input("Player 2: Pass to (0-4): "))
            if self.team[self.player_with_ball].pass_ball():
                self.player_with_ball = target
                await self.friend_turn()
                return
            else:
                print("Pass failed.")
        elif action == 't':
            await self.display_team_stats()
            await self.friend_turn()
            return
        elif action == 'c':
            print(f"You: {self.your_score}, Player 2: {self.friend_score}")
            print(f"Possessions left: {self.possessions_left}")
            await self.friend_turn()
            return
        else:
            print("Invalid input.")
        self.possessions_left -= 1

    async def display_final_results(self):
        print("\n=== FINAL RESULTS ===")
        await self.display_team_stats()
        print(f"\nYour Score: {self.your_score}")
        if self.vs_friend:
            print(f"Player 2 Score: {self.friend_score}")
            if self.your_score > self.friend_score:
                print("You Win!")
            elif self.friend_score > self.your_score:
                print("Player 2 Wins!")
            else:
                print("It's a Tie!")
        else:
            print(f"Computer Score: {self.computer_score}")
            if self.your_score > self.computer_score:
                print("You Win!")
            elif self.computer_score > self.your_score:
                print("Computer Wins!")
            else:
                print("It's a Tie!")

    async def run(self):
        await self.display_team_roster()
        while self.possessions_left > 0:
            print("\n=== New Possession ===")
            await self.player_turn()
        print("\nGAME OVER!")
        await self.display_final_results()
