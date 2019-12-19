# Import modules
from minesweeperAI import MinesweeperAI
import random
from random import randint

row_count = 8
col_count = 8
total_bomb_count = 10
seed = randint(0,100)

game = MinesweeperAI(
    row_count,
    col_count,
    total_bomb_count,
    bomb_locations=[],
    board=[],
    move_count=0
)

# game.row_count = 8
# game.col_count = 8
# game.total_bomb_count = 10
# game.seed = randint(0,100)
