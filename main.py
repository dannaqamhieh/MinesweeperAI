# Import modules
from minesweeperAI import MinesweeperAI
import random
from random import randint

row_count = 8
col_count = 8
total_bomb_count = 10
games_played = 10
seed = randint(0,100)
total_wins = 0

for i in range(games_played):
    game = MinesweeperAI(
        row_count,
        col_count,
        total_bomb_count,
        bomb_locations=[],
        board=[],
        move_count=0
        )
    result = game.AI_game()
    total_wins += result
    del game

print("\n-------------------- Trial Over --------------------\n")
print("Total games played:", games_played)
print("Percent won:", 100*(total_wins/games_played), "%")
print("\n----------------------------------------------------\n")
