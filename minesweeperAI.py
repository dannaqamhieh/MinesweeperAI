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
        self.game_over_state = False
        self.make_board()
        self.set_numbers()
        self.hide_board()
    #    self.debug_board()

    def make_board(self):
        tmp = []
        for i in range(0, self.row_count + 1):
            del tmp[:]
            for j in range(0, self.col_count + 1):
                tmp.append(Tile("l", i, j, 1.5))

            self.board.append(tmp[:])

        change_count = 0
        while change_count < self.total_bomb_count:
            rando_x = randint(2, (self.row_count))
            rando_y = randint(2, (self.row_count))
            if self.board[rando_x][rando_y].value != 'B':
                self.board[rando_x][rando_y].value = 'B'
                change_count += 1

    def print_board(self):
        flagged_tile_count = 0
        print("[0]", end=" ")
        for i in range(1, self.col_count + 1):
            print("[" + str(i) + "]", end=" ")
        print()
        for i in range(1, self.row_count + 1):
            print("[" + str(i) + "]", end="  ")
            for j in range(1, self.col_count + 1):
                if self.board[i][j].value == "F":
                    flagged_tile_count += 1
                if self.board[i][j].is_revealed:
                    if self.board[i][j].value == 'B':
                        print('\u2588', end="   ")
                    elif self.board[i][j].value != 0:
                        print(self.board[i][j].value, end="   ")
    
                else:
                    print('.', end="   " )
            print()
        print(
            "Flagged bombs to total bombs:",
            str(flagged_tile_count) + "/" + str(self.total_bomb_count) + "\n",
        )

    def hide_board(self):
        for i in range(1, self.row_count+1):
            for j in range(1, self.col_count+1):
                self.board[i][j].is_revealed = False
        

    def find_8neighbors(self, i, j):
        """returns a list of all tiles which neighbor tile (i,j)"""
        ret = []
        for iii in range(-1, 2):
            for jjj in range(-1, 2):
                valid_tile = True
                """catch weird cases"""
                if i+iii < 1 or i+iii > self.row_count:
                    valid_tile = False
                if j+jjj < 1 or j+jjj > self.col_count:
                    valid_tile = False
                """exclude center tile"""
                if valid_tile:
                    ret.append([i+iii,j+jjj])
        try:
            ret.remove([i,j])
        except:
            return ret

        return ret

    def find_4neighbors(self, i, j):
        """returns a list of the four tiles which directly neighbor tile (i,j)"""
        ret = []
        for iii in range(-1, 2):
            for jjj in range(-1, 2):
                valid_tile = True
                """catch weird cases"""
                if i+iii < 1 or i+iii > self.row_count:
                    valid_tile = False
                if j+jjj < 1 or j+jjj > self.col_count:
                    valid_tile = False
                """exclude center tile"""
                if valid_tile:
                    if iii == 0 or jjj == 0: ret.append([i+iii,j+jjj])
        ret.remove([i,j])
        return ret


    def set_numbers(self):
        """loop over every tile in the board
           find surrounding tiles
           count number of bombs,
           set indicator from . to # of bombs"""
        for i in range(1, self.row_count+1):
            for j in range(1, self.col_count+1):
                #check if not bomb
                num_bombs = 0
                if self.board[i][j].value != 'B':
                    neighbors = self.find_8neighbors(i,j)
                    for el in neighbors:
                        if self.board[el[0]][el[1]].value == 'B':
                            num_bombs += 1
                    if num_bombs != 0:
                        self.board[i][j].change_tile_value(num_bombs)
                    else:
                        self.board[i][j].change_tile_value('0')

    def debug_board(self):
        for i in range(1, self.row_count+1):
            for j in range(1, self.row_count+1):
                self.reveal(i,j)
                self.board[i][j].is_revealed=False

    """
    GET Functions.
    Provides access of data from board.
    """

    def reveal(self, x, y):

        self.board[x][y].is_revealed = True 
        neighbors = self.find_4neighbors(x,y)
        for el in neighbors:
            tile = self.board[el[0]][el[1]]
            if tile.value != '0' and not tile.is_revealed:
                tile.is_revealed = True
            elif tile.value == '0' and not tile.is_revealed:
                self.reveal(el[0],el[1])


    def guess(self, x, y):
        if x < 1 or x > 8:
            return False
        elif y < 1 or y > 8:
            return False
        if self.board[x][y].value != 'B':
            self.reveal(int(x),int(y))
            self.print_board()
            return True
        else:
            print("bomb")
            return False


class Tile:

    def __init__(self, value, x_location, y_location, prob):
        self.value = value
        self.x_location = x_location
        self.y_location = y_location
        self.prob = prob
        self.is_revealed = True 

    def change_tile_value(self, new):
        self.value = new
        return self.value

    def reveal(self):
        self.is_revealed = True


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
