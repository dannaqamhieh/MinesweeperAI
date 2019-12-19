import random
from random import randint

class MinesweeperAI:

    board = []

    def __init__(self, row_count, col_count, total_bomb_count,
                 seed=randint(0,100), bomb_locations=[], board=[],
                 move_count=0):
        self.row_count = row_count
        self.col_count = col_count
        self.total_bomb_count = total_bomb_count
        self.game_over_state = 0
        self.make_board()
        self.print_board()

    def make_board(self):
        for i in range(self.row_count + 1):
            for j in range(self.col_count + 1):
                self.board.append(Tile("l", i, j, 1.5))
        change_count = 0
        while change_count < self.total_bomb_count:
            rando = randint(2, (self.row_count * self.col_count))
            if self.board[rando].value == "l":
                self.board[rando].change_tile_value("B")
                print(change_count, ")", rando, ":", self.board[rando].value)
                change_count += 1
        print(change_count)

    def print_board(self):
        flagged_tile_count = 0
        print("[0]", end=" ")
        for i in range(1, self.row_count + 1):
            print("[" + str(i) + "]", end=" ")
        print()
        for i in range(1, self.row_count + 1):
            print("[" + str(i) + "]", end="  ")
            for j in range(1, self.col_count + 1):
                tile = self.board[i * j].get_tile_value()
                if tile == "F":
                    flagged_tile_count += 1
                print(tile, end="   ")
            print()
        print(
            "Flagged bombs to total bombs:",
            str(flagged_tile_count) + "/" + str(self.total_bomb_count) + "\n",
        )

    # def change_random_tiles(self, amount, change_to):
    #     change_count = 0
    #     while change_count < amount:
    #         rando = randint(2, (self.row_count * self.col_count))
    #         self.board[rando].change_tile_value(change_to)
    #         print(self.board[rando].value)
    #         change_count += 1

    """
    GET Functions.
    Provides access of data from board.
    """

class Tile:

    def __init__(self, value, x_location, y_location, prob):
        self.value = value
        self.x_location = x_location
        self.y_location = y_location
        self.prob = prob

    def change_tile_value(self, new):
        self.value = new
        return self.value


    """
    GET Functions.
    Provides access of data from board.
    """

    def get_tile_location(self):
        return self.location

    def get_tile_value(self):
        return self.value

    def get_tile_prob(self):
        return self.prob
