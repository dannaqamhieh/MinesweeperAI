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

    def AI_game(self):
        print("\n-------------------- MINESWEEPER --------------------\n")
        print("----- GAME START")
        print("----- Board Size:", (self.row_count * self.col_count))
        print("----- Mine Number:", self.total_bomb_count, "\n")
        self.make_board()
        self.print_board()

        while self.game_over_state == False:
            self.hide_board()
            self.reveal(1, 1)
            self.trivial_parse()
            self.print_board()
            self.check_board()
            self.update_probs()
            break

    def get_tile_prob(self, x, y): # return unknown_tiles / remaining mines
        flagged_mines = 0
        known_tiles = 0
        mine_value = int(self.board[x][y].value)
        neighbors = self.find_8neighbors(x, y)
        total_tiles = len(neighbors)
        for el in neighbors:
            neighbor = self.board[el[0]][el[1]]
            if neighbor.is_revealed == True:
                if neighbor.value == "F":
                    flagged_mines += 1
                known_tiles += 1
        unknown_tiles = total_tiles - known_tiles
        mines_remaining = mine_value - flagged_mines
        if mines_remaining > 0:
            prob = mines_remaining / unknown_tiles
            print(prob)
            return prob

    def update_probs(self):
        """" Parse through all known tiles that border at least one unknown
        tile. Calculate the probability for each of the unknown tiles by
        dividing the number of remaining mines for the known tile by the number
        of neighboring unkown tiles. Append this value to the probability list
        of each of the neighboring unknown tiles.
        """

        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[i][j]
                if (tile.is_revealed == True) and tile.value != " " and tile.value != "F":
                    flagged_mines = 0
                    known_tiles = 0
                    mine_value = int(tile.value)
                    neighbors = self.find_8neighbors(i, j)
                    if len(neighbors) > 0:
                        total_tiles = len(neighbors)
                        for el in neighbors:
                            neighbor = self.board[el[0]][el[1]]
                            if neighbor.is_revealed == True:
                                if neighbor.value == "F":
                                    flagged_mines += 1
                                known_tiles += 1
                        unknown_tiles = total_tiles - known_tiles
                        mines_remaining = mine_value - flagged_mines
                    unknowns = self.unknown_neighbors(i, j)
                    if len(unknowns) > 0:
                        prob = mines_remaining / len(unknowns)
                        for el in unknowns:
                            self.board[el.x_location][el.y_location].prob_list.append(prob)
                            print("(", el.x_location, ",", el.y_location, "):", self.board[el.x_location][el.y_location].prob_list)




        # for i in range(1, self.row_count + 1):
        #     for j in range(1, self.col_count + 1):
        #         tile = self.board[i][j]
        #         if tile.is_revealed == False and tile.value != "B":
        #             flagged_mines = 0
        #             known_tiles = 0
        #             mine_value = int(tile.value)
        #             neighbors = self.find_8neighbors(i, j)
        #             if len(neighbors) > 0:
        #                 total_tiles = len(neighbors)
        #                 for el in neighbors:
        #                     neighbor = self.board[el[0]][el[1]]
        #                     if neighbor.is_revealed == True:
        #                         if neighbor.value == "F":
        #                             flagged_mines += 1
        #                         known_tiles += 1
        #                 unknown_tiles = total_tiles - known_tiles
        #                 mines_remaining = mine_value - flagged_mines
        #                 prob = mines_remaining / unknown_tiles
        #                 for el in neighbors:
        #                     neighbor = self.board[el[0]][el[1]]
        #                     neighbor.prob_list.append(prob)
        #                 print(tile.prob_list, tile.x_location)

    def unknown_neighbors(self, i, j):
        neighbors = self.find_8neighbors(i, j)
        unknowns = []
        for el in neighbors:
            neighbor = self.board[el[0]][el[1]]
            if neighbor.is_revealed == False:
                unknowns.append(neighbor)
        try:
            unknowns.remove([i,j])
        except:
            return unknowns
        return unknowns

    def check_board(self):
        """ Parse through entire board and verify that the values and flags
        make sense.
        """
        ERROR = False
        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                if (self.board[i][j].is_revealed == True) and (self.board[i][j].value != "F"):
                    mine_value = int(self.board[i][j].value)
                    flagged_mines = 0
                    neighbors = self.find_8neighbors(i, j)
                    total_tiles = len(neighbors)
                    for el in neighbors:
                        tile = self.board[el[0]][el[1]]
                        if tile.is_revealed == True:
                            if tile.value == "F":
                                flagged_mines += 1
                    if (flagged_mines > mine_value): # check
                        print("ERROR: Contradiction found at", self.board[el[0]][el[1]])
                        ERROR = True
        if ERROR == True:
            print("ERROR: Contradiction found.")
        else:
            print("No contradictions detected.")

    def trivial_parse(self):
        """ Parse through entire board. If a known tile has the same number of
        surrounding flagged tiles as its value, reveal all surrounding tiles.
        If a known tile has the same number of remaining mines as unknown surrounding
        tiles, flag all surrounding tiles. Loop until no changes can be made.
        """
        updated = True
        while updated == True:
            updated = False
            for i in range(1, self.row_count + 1):
                for j in range(1, self.col_count + 1):
                    if (self.board[i][j].is_revealed == True) and (self.board[i][j].value != "F"):
                        mine_value = int(self.board[i][j].value)
                        flagged_mines = 0
                        known_tiles = 0
                        neighbors = self.find_8neighbors(i, j)
                        total_tiles = len(neighbors)
                        for el in neighbors:
                            tile = self.board[el[0]][el[1]]
                            if tile.is_revealed == True:
                                if tile.value == "F":
                                    flagged_mines += 1
                                known_tiles += 1
                        if ((mine_value - flagged_mines) == (total_tiles -  known_tiles)): # flag all unknowns
                            for el in neighbors:
                                tile = self.board[el[0]][el[1]]
                                if tile.is_revealed == False:
                                    updated = True
                                    tile.flag_tile()
                        elif (flagged_mines == mine_value): # reveal all neighbors
                            updated = True
                            for el in neighbors:
                                tile = self.board[el[0]][el[1]]
                                self.auto_reveal(el[0], el[1])

    def make_board(self):
        tmp = []
        for i in range(0, self.row_count + 1):
            del tmp[:]
            for j in range(0, self.col_count + 1):
                tmp.append(Tile("l", i, j, 1.5, True))
            self.board.append(tmp[:])

        change_count = 0
        while change_count < self.total_bomb_count:
            rando_x = randint(1, (self.row_count))
            rando_y = randint(1, (self.col_count))
            first = (rando_x != 1) and (rando_y != 1)
            if (self.board[rando_x][rando_y].value != 'B' and first ):
                    self.board[rando_x][rando_y].value = 'B'
                    change_count += 1
        self.set_numbers()

    def print_board(self):
        flagged_tile_count = 0
        print("[0]", end=" ")
        for i in range(1, self.col_count + 1):
            print("[" + str(i).zfill(2) + "]", end=" ")
        print()
        for i in range(1, self.row_count + 1):
            print("[" + str(i).zfill(2) + "]", end="  ")
            for j in range(1, self.col_count + 1):
                if self.board[i][j].value == "F":
                    flagged_tile_count += 1
                if self.board[i][j].is_revealed:
                    if self.board[i][j].value == 'B':
                        print('\u2588', end="    ")
                    elif self.board[i][j].value != 0:
                        if self.board[i][j].value == "0":
                            print(" ", end="    ")
                        else:
                            print(self.board[i][j].value, end="    ")
                else:
                    print('.', end="    " )
            print()
        print(
            "\nFlagged bombs to total bombs:",
            str(flagged_tile_count) + "/" + str(self.total_bomb_count) + "\n",
        )

    def hide_board(self):
        for i in range(1, self.row_count+1):
            for j in range(1, self.col_count+1):
                self.board[i][j].is_revealed = False

    def reveal_board(self):
        for i in range(1, self.row_count+1):
            for j in range(1, self.col_count+1):
                self.board[i][j].is_revealed = True

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
                        self.board[i][j].value = (num_bombs)
                    else:
                        self.board[i][j].value = ('0')

    def auto_reveal(self, x, y):
        self.board[x][y].is_revealed = True
        if self.board[x][y].value == '0':
            neighbors = self.find_4neighbors(x,y)
            for el in neighbors:
                tile = self.board[el[0]][el[1]]
                if tile.value != '0' and not tile.is_revealed:
                    tile.is_revealed = True
                elif tile.value == '0' and not tile.is_revealed:
                    self.auto_reveal(el[0],el[1])

    def reveal(self, x, y):
        if (x < 1) or (x > self.row_count) or (y < 1) or (y > self.col_count):
            return False
        if self.board[x][y].value != 'B':
            self.auto_reveal(int(x),int(y))
            return True
        else:
            print("bomb")
            return False


class Tile:

    def __init__(self, value, x_location, y_location, prob, is_revealed, prob_list=[]):
        self.value = value
        self.x_location = x_location
        self.y_location = y_location
        self.prob = prob
        self.is_revealed = True
        self.prob_list=[]

    def flag_tile(self):
        self.value = "F"
        self.is_revealed = True

    """
    GET Functions.
    Provides access of data from board.
    """
