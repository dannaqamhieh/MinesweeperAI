import random
from random import randint

class MinesweeperAI:

    wins = 0
    loss = 0
    board = []

    def __init__(self, row_count, col_count, total_bomb_count,
                 seed=randint(0,100), bomb_locations=[], board=[],
                 move_count=0, wins=0, loss=0):
        self.row_count = row_count
        self.col_count = col_count
        self.total_bomb_count = total_bomb_count
        self.game_over_state = False

    def __delete__(self, instance):
        del self.board
        del self.row_count
        del self.col_count
        del self.total_bomb_count
        del self.bomb_locations
        del self.move_count
        del self.game_over_state
        del self.wins
        del self.loss

    def AI_game(self):
        # print("\n-------------------- MINESWEEPER --------------------\n")
        # print("      GAME START")
        # print("      Board Size:", (self.row_count * self.col_count))
        # print("      Mine Number:", self.total_bomb_count)
        # print("      Mine Density:", (self.total_bomb_count/(self.row_count*self.col_count)))
        # print("\n-----------------------------------------------------\n")
        self.game_over_state = False
        self.make_board()
        # self.print_board()
        self.hide_board()
        self.reveal(1, 1)
        self.update_probs()
        self.greedy_prob_method()


        while self.game_over_state == False:
            # self.print_board()
            self.trivial_parse()
            # self.print_board()
            # self.check_board()
            self.update_probs()
            self.greedy_prob_method()
            # self.print_all_probs()
            self.AI_reveal()
            self.update_probs()
            self.greedy_prob_method()
            # self.print_board()
            # self.print_all_prob_lists()
            # self.print_all_probs()
            print(self.game_over_state)

        # self.print_board()
        # self.print_all_probs()
        if self.wins == 1:
            return 1
        else:
            return 0

    def AI_reveal(self):
        """ Parse through every prob value for every tile in the grid. Reveal
        the tile with the lowest probability of having a mine. If there are
        multiple tiles with the same lowest probability, reveal the first.
        """
        lowest = 1.0
        lowest_found = False
        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[int(i)][int(j)]
                if len(tile.prob_list) > 0:
                    if (tile.prob != 0) and (tile.prob <= 1.0):
                        if tile.prob < lowest:
                            lowest = tile.prob
                            lowest_tile = tile
                            lowest_found = True
        # print(lowest)
        # print("Reveal: (", lowest_tile.x_location, ",", lowest_tile.y_location, "):", lowest_tile.prob)
        if lowest_found == True:
            self.auto_reveal(lowest_tile.x_location, lowest_tile.y_location)

    def average_prob_method(self):
        """ Parse through every tile in the grid. Update the prob value
        to be the average of all the values in the prob_list.
        """
        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[int(i)][int(j)]
                list = tile.prob_list
                if len(list) > 0:
                    total = 0
                    for i in list:
                        if i <= 1:
                            total += idea
                    average = total / len(list)
                    tile.prob = average
                else:
                    tile.prob = 1.5

    def greedy_prob_method(self):
        """ Parse through every tile in the grid. Update the prob value
        to be the highest of all the values in the prob_list.
        """
        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[int(i)][int(j)]
                list = tile.prob_list
                if len(list) > 0:
                    highest = 0
                    for k in list:
                        if k > highest and (k <= 1):
                            highest = k
                    tile.prob = highest
                else:
                    tile.prob = 1.5

    def update_probs(self):
        """" Parse through all known tiles that border at least one unknown
        tile. Calculate the probability for each of the unknown tiles by
        dividing the number of remaining mines for the known tile by the number
        of neighboring unkown tiles. Append this value to the probability list
        of each of the neighboring unknown tiles.

        Also parse through all unknown tiles. Calculate the probability for
        each unknown to be total_mines_remaining / total unknowns. Append
        this value to the probability list for each.
        """
        self.clear_prob_lists()
        unknown_num = self.get_num_unknowns()
        total_mines = self.get_num_mines_remaining()
        if total_mines > 0:
            prob_value = total_mines / unknown_num
            for i in range(1, self.row_count + 1):
                for j in range(1, self.col_count + 1):
                    tile = self.board[i][j]
                    if tile.is_revealed == False:
                        tile.prob_list.append(prob_value)

        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[i][j]
                if (tile.is_revealed == True) and tile.value != " " and tile.value != "F" and tile.value != "B":
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
                            # print("(", el.x_location, ",", el.y_location, "):", self.board[el.x_location][el.y_location].prob_list)

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

    def get_num_unknowns(self):
        count = 0
        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[i][j]
                if tile.is_revealed == False:
                    count += 1
        return count

    def get_num_mines_remaining(self):
        count = 0
        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[i][j]
                if tile.value == "F":
                    count += 1
        total_mines_remaining = self.total_bomb_count - count
        return total_mines_remaining

    def clear_prob_lists(self):
        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[i][j]
                tile.prob_list = []

    def print_all_prob_lists(self):
        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[i][j]
                print("(", tile.x_location, ",", tile.y_location, "):", tile.prob_list)

    def print_all_probs(self):
        for i in range(1, self.row_count + 1):
            for j in range(1, self.col_count + 1):
                tile = self.board[i][j]
                print("(", tile.x_location, ",", tile.y_location, "):", tile.prob)

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

    def get_num_flags(self):
        ret = 0
        for i in range(1, self.row_count+1):
            for j in range(1, self.col_count+1):
                if self.board[i][j].value != 'F':
                    ret += 1

        return ret

    def trivial_parse(self):
        """ Parse through entire board. If a known tile has the same number of
        surrounding flagged tiles as its value, reveal all surrounding tiles.
        If a known tile has the same number of remaining mines as unknown surrounding
        tiles, flag all surrounding tiles. Loop until no changes can be made.
        """
        updated = True
        # if self.get_num_flags() == self.total_bomb_count:
        #     updated = False
        #     for i in range(1, self.row_count+1):
        #         for j in range(1, self.col_count+1):
        #             if self.board[i][j].value != 'F' and not self.board[i][j].is_revealed:
        #                 self.reveal(i, j)

        while updated:
            updated = False
            unknowns = 0
            for i in range(1, self.row_count + 1):
                for j in range(1, self.col_count + 1):
                    if (self.board[i][j].is_revealed == True):
                        if self.board[i][j].value != "F":
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
                    else:
                        unknowns += 1
        if unknowns == 0:
                self.win_game()

    def make_board(self):
        tmp = []
        init_prob = self.total_bomb_count/(self.row_count*self.col_count)
        for i in range(0, self.row_count + 1):
            del tmp[:]
            for j in range(0, self.col_count + 1):
                tmp.append(Tile('z', i, j, init_prob, True))
            self.board.append(tmp[:])
            for el in tmp: del el

        change_count = 0
        while change_count < self.total_bomb_count:
            rando_x = randint(1, (self.row_count))
            rando_y = randint(1, (self.col_count))
            first = not (rando_x == 1 and rando_y == 1)
            if (self.board[rando_x][rando_y].value != 'B' and first):
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
        """ Loop over every tile in the board find surrounding tiles count
            number of bombs, set indicator from . to # of bombs
        """
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
        elif self.board[x][y].value == "B":
            self.lose_game()

    def lose_game(self):
        self.loss += 1
        self.game_over_state = True
        print("YOU LOSE.")


    def win_game(self):
        self.wins += 1
        self.game_over_state = True
        print("YOU WIN.")

    def reveal(self, x, y):
        if (x < 1) or (x > self.row_count) or (y < 1) or (y > self.col_count):
            return False
        if self.board[x][y].value != 'B':
            self.auto_reveal(int(x),int(y))
            return True
        else:
            self.lose_game()
            print("bomb")
            return False


class Tile:

    def __init__(self, value, x_location, y_location, prob, is_revealed, prob_list=[]):
        self.value = value
        self.x_location = x_location
        self.y_location = y_location
        self.prob = 0
        self.is_revealed = True
        self.prob_list=[]

    def __delete__(self, instance):
        del self.value
        del self.x_location
        del self.y_location
        del self.prob
        del self.is_revealed
        del self.prob_list
        print('deleted tile')

    def flag_tile(self):
        self.value = "F"
        self.is_revealed = True

    """
    GET Functions.
    Provides access of data from board.
    """
