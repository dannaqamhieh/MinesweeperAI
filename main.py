# Import modules
from minesweeperAI import MinesweeperAI
import random
from random import randint

row_count = 16
col_count = 16
total_bomb_count = 40
seed = randint(0,100)

game = MinesweeperAI(
        row_count,
        col_count,
        total_bomb_count,
        bomb_locations=[],
        board=[],
        move_count=0
        )

game.AI_game()
