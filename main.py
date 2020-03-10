# Import modules
from minesweeperAI import MinesweeperAI
import random
from random import randint
import sys

row_count = 10
col_count = 10
total_bomb_count = 35
games_played = 1000
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
