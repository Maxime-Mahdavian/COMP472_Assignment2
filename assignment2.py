# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import argparse
import numpy
import random


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, n, b, coordinate, s, d1, d2, t, a, p1, p2, recommend=True):
        self.recommend = recommend
        self.n = n
        self.b = b
        self.coordinate = coordinate
        self.s = s
        self.d1 = d1
        self.d2 = d2
        self.t = t
        self.a = a
        self.p1 = p1
        self.p2 = p2
        self.initialize_game()

    def initialize_game(self):

        self.current_state = [['.' for i in range(self.n)] for j in range(self.n)]
        # self.current_state = numpy.full((self.n,self.n), '.')
        if self.coordinate:
            for num in self.coordinate:
                x = int(num[0])
                y = int(num[1])
                if self.is_valid(x, y):
                    self.current_state[x][y] = 'B'
                else:
                    print("Some coordinates are invalid, only the valid ones were put on the board")
                    break
        else:
            for i in range(0, self.b):
                x = random.randint(0, self.n - 1)
                y = random.randint(0, self.n - 1)

                while self.current_state[x][y] == 'B':
                    x = random.randint(0, self.n - 1)
                    y = random.randint(0, self.n - 1)

                self.current_state[x][y] = 'B'

        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        print()
        for y in range(0, self.n):
            print(F'|', end="")
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end="")
                print(F'|', end="")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px > self.n - 1 or py < 0 or py > self.n - 1:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):

        previous_char = '.'
        counter = 1
        # Vertical win
        for i in range(0, self.n):
            col = self.current_state[:][i]
            counter = 1
            previous_char = '.'
            for j in range(0, self.n):
                if col[j] == '.' or col[j] == 'B':
                    continue
                elif col[j] == 'X':
                    if previous_char == 'X':
                        counter = counter + 1
                        if counter == self.s:
                            return col[j]
                    else:
                        previous_char = col[j]
                        counter = 1
                elif col[j] == 'O':
                    if previous_char == 'O':
                        counter = counter + 1
                        if counter == self.s:
                            return col[j]
                    else:
                        previous_char = col[j]
                        counter = 1
        # Horizontal win
        previous_char = '.'
        counter = 1
        for i in range(0, self.n):
            for j in range(0, self.n):
                row = self.current_state[j][i]
                counter = 1
                previous_char = '.'
                if row == '.' or row == 'B':
                    continue
                elif row == 'X':
                    if previous_char == 'X':
                        counter = counter + 1
                        if counter == self.s:
                            return row
                    else:
                        previous_char = row
                        counter = 1
                elif row == 'O':
                    if previous_char == 'O':
                        counter = counter + 1
                        if counter == self.s:
                            return row
                    else:
                        previous_char = row
                        counter = 1

        # Main diagonal win
        # if (self.current_state[0][0] != '.' and
        #         self.current_state[0][0] == self.current_state[1][1] and
        #         self.current_state[0][0] == self.current_state[2][2]):
        #     return self.current_state[0][0]
        counter = 1
        previous_char = '.'
        for i in range(0, self.n):
            for j in range(0, self.n):
                counter = 1
                previous_char = '.'
                pos = self.current_state[j][i]
                counter = 1
                if pos == '.' or pos == 'B':
                    counter = 1
                    continue
                for x in range(1, self.s):
                    try:
                        if self.current_state[j + x][i + x] == pos:
                            counter = counter + 1
                        else:
                            break
                    except IndexError:
                        pass
                if counter == self.s:
                    return pos
                else:
                    counter = 1

        # # Second diagonal win
        # if (self.current_state[0][2] != '.' and
        #         self.current_state[0][2] == self.current_state[1][1] and
        #         self.current_state[0][2] == self.current_state[2][0]):
        #     return self.current_state[0][2]
        counter = 1
        previous_char = '.'
        for i in range(0, self.n):
            for j in range(0, self.n):
                counter = 1
                previous_char = '.'
                pos = self.current_state[j][i]
                counter = 1
                if pos == '.' or pos == 'B':
                    counter = 1
                    continue
                for x in range(1, self.s):
                    try:
                        if self.current_state[j - x][i + x] == pos:
                            counter = counter + 1
                        else:
                            break
                    except IndexError:
                        pass
                if counter == self.s:
                    return pos
                else:
                    counter = 1

        # Is whole board full?
        for i in range(0, self.n):
            for j in range(0, self.n):
                # There's an empty field, we continue the game
                if self.current_state[i][j] == '.':
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    def minimax(self, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(max=False)
                else:
                    (_, x, y) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    # print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()


def main():
    parser = argparse.ArgumentParser("test")
    parser.add_argument("n", help="Size of the board", type=int)
    parser.add_argument("b", help="Number of blocks", type=int)
    parser.add_argument("s", help="The winning line-up size", type=int)
    parser.add_argument("d1", help="Maximum depth of the adversarial search for player 1", type=int)
    parser.add_argument("d2", help="Maximum depth of the adversarial search for player 2", type=int)
    parser.add_argument("t", help="Maximum allowed time (in seconds) for your program to return a move", type=int)
    parser.add_argument("a", help="True for alphabeta and False for minimax", type=str)
    parser.add_argument("p1", help="Human for playable player, AI for computer", type=str)
    parser.add_argument("p2", help="Human for playable player, AI for computer", type=str)
    parser.add_argument("coordinate", help="Coordinates of the block, first digit is X coordinate and second digit is "
                                           "the Y coordinate", nargs='*')
    args = parser.parse_args()

    # Here we check for the validity of the command line arguments (it's easier to do it that way)
    flag = True
    a = True
    p1 = None
    p2 = None

    if args.n < 3 or args.n > 10:
        print("n must be between 3 and 10")
        flag = False
    if args.b < 0 or args.b > 2 * args.n:
        print("b must be between 0 and 2*n")
        flag = False
    if args.s < 3 or args.s > args.n:
        print("s must be between 3 and n")
        flag = False

    if args.a.lower() == "true":
        a = True
    elif args.a.lower() == "false":
        a = False
    else:
        print("a must be true or false")
        flag = False

    if args.p1.lower() == "human":
        p1 = Game.HUMAN
    elif args.p1.lower() == "ai":
        p1 = Game.AI
    else:
        print("p1 must be human or ai")
        flag = False

    if args.p2.lower() == "human":
        p1 = Game.HUMAN
    elif args.p2.lower() == "ai":
        p1 = Game.AI
    else:
        print("p2 must be human or ai")
        flag = False

    if args.coordinate:
        if len(args.coordinate) != args.b:
            print("Number of coordinates must be the same as b")
            flag = False

    if flag:
        g = Game(args.n, args.b, args.coordinate, args.s, args.d1, args.d2, args.t, args.a, args.p1, args.p2,
                 recommend=False)
        # g.draw_board()
        g.play(algo=Game.ALPHABETA, player_x=Game.HUMAN, player_o=Game.HUMAN)
        # g.play(algo=Game.MINIMAX,player_x=Game.HUMAN,player_o=Game.HUMAN)


if __name__ == "__main__":
    main()
