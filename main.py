# Import modules
from minesweeperAI import MinesweeperAI
import random
from random import randint

row_count = 16
col_count = 32
total_bomb_count = 50 
seed = randint(0,100)

game = MinesweeperAI(
        row_count,
        col_count,
        total_bomb_count,
        bomb_locations=[],
        board=[],
        move_count=0
        )

game.print_board()
game.guess(1,1)
