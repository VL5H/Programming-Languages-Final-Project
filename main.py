import asyncio
from game import Game

async def main():
    print("Welcome to NBA 1K!")

    mode = input("Select Game mode:\n1. vs Computer\n2. vs Friend\nEnter 1 or 2: ")
    vs_friend = mode.strip() == '2'
    game = Game(vs_friend)
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())
