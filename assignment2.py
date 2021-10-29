# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import argparse
import numpy
import random
import math


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

                # If by some chance the place has already been picked (unlikely to happen)
                while self.current_state[x][y] == 'B':
                    x = random.randint(0, self.n - 1)
                    y = random.randint(0, self.n - 1)

                self.current_state[x][y] = 'B'

        # self.current_state[0][0] = 'B'
        # self.draw_board()
        # self.e2()
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
                    previous_char = col[j]
                    counter = 1
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
        for i in range(0, self.n):
            counter = 1
            previous_char = '.'
            for j in range(0, self.n):
                row = self.current_state[j][i]
                if row == '.' or row == 'B':
                    previous_char = row
                    counter = 1
                    continue
                elif row == 'X':
                    if previous_char == 'X':
                        counter += 1
                        if counter == self.s:
                            return row
                    else:
                        previous_char = row
                        counter = 1
                elif row == 'O':
                    if previous_char == 'O':
                        counter += 1
                        if counter == self.s:
                            return row
                    else:
                        previous_char = row
                        counter = 1
        # Main diagonal win
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
                        if j + x > self.n or i + x > self.n:
                            counter = 1
                            break
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
        for i in range(0, self.n):
            for j in range(0, self.n):
                pos = self.current_state[j][i]
                counter = 1
                if pos == '.' or pos == 'B':
                    continue
                for x in range(1, self.s):
                    try:
                        if j - x < 0 or i + x > self.n:
                            counter = 1
                            break
                        if self.current_state[j - x][i + x] == pos:
                            counter = counter + 1
                        else:
                            counter = 1
                            break
                    except IndexError:
                        counter = 1
                if counter == self.s:
                    return pos

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

    def minimax(self, depth, time_left, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        start_time = time.time()
        if time_left < 0.1:
            if max:
                return self.e2('O')
            else:
                return self.e2('X')

        value = math.inf
        if max:
            value = -math.inf
        x = None
        y = None

        result = self.is_end()

        if result == 'X':
            return -self.n * self.n, x, y
        elif result == 'O':
            return self.n * self.n + 1, x, y

        if depth == 0:
            if max:
                return self.e1('O')
            else:
                return self.e1('X')

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        end_time = time.time()
                        new_time_left = time_left - (end_time - start_time)
                        (v, _, _) = self.minimax(depth - 1, new_time_left, max=False)
                        if v > value or value == math.inf:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        end_time = time.time()
                        new_time_left = time_left - (end_time - start_time)
                        (v, _, _) = self.minimax(depth - 1, new_time_left,max=True)
                        if v < value or value == -math.inf:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, depth, time_left,alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:

        start_time = time.time()
        if time_left < 0.1:
            if max:
                return self.e2('O')
            else:
                return self.e2('X')

        value = math.inf
        if max:
            value = -math.inf
        x = None
        y = None

        result = self.is_end()
        if result == 'X':
            return -self.n * self.n, x, y
        elif result == 'O':
            return self.n * self.n + 1, x, y

        if depth == 0:
            if max:
                return self.e2('O')
            else:
                return self.e2('X')

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        end_time = time.time()
                        new_time_left = time_left - (end_time - start_time)
                        (v, _, _) = self.alphabeta(depth - 1, new_time_left, alpha, beta, max=False)
                        if v > value or value == math.inf:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        end_time = time.time()
                        new_time_left = time_left - (end_time - start_time)
                        (v, _, _) = self.alphabeta(depth - 1, new_time_left, alpha, beta, max=True)
                        if v < value or value == -math.inf:
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

    def e1(self, cell):

        visited = [[False for j in range(self.n)] for i in range(self.n)]

        count = 0
        x = 0
        for i in range(self.n):
            for j in range(self.n):
                if visited[i][j] == False and self.current_state[i][j] == cell:
                    self.DFS(i, j, visited, x)
                    count += 1

        test = numpy.array(visited).sum()
        return test, None, None
        # return count

    def e2(self, cell):

        score = 0
        for i in range(self.n):
            for j in range(self.n):
                # print("------------")
                if self.n - j < self.s:
                    continue
                temp = 0
                for x in range(self.s):
                    # print(str(j+x) + "," + str(i))
                    if self.current_state[j + x][i] == '.':
                        continue
                    elif self.current_state[j + x][i] == 'B':
                        score -= 1
                    elif self.current_state[j + x][i] == cell:
                        temp += 1
                        score += 2
                    else:
                        temp -= 1
                        score -= 2
                if temp == 2 and cell == 'X':
                    score = -1000
                    return score, None, None
                elif temp == -2 and cell == 'O':
                    score = 1000
                    return score, None, None

        for i in range(self.n):
            for j in range(self.n):
                # print("----------")
                if self.n - i < self.s:
                    continue
                temp = 0
                for x in range(self.s):
                    # print(str(j) + "," + str(i+x))
                    # print(self.current_state[j][x+i])
                    if self.current_state[j][x + i] == '.':
                        continue
                    elif self.current_state[j][x + i] == 'B':
                        score -= 1
                    elif self.current_state[j][x + i] == cell:
                        temp += 1
                        score += 2
                    else:
                        temp -= 1
                        score -= 2
                if temp == 2 and cell == 'X':
                    score = -1000
                    return score, None, None
                elif temp == -2 and cell == 'O':
                    score = 1000
                    return score, None, None

        for i in range(self.n):
            for j in range(self.n):
                # print("-----------")
                if self.n - i < self.s or self.n - j < self.s:
                    continue
                temp = 0
                for x in range(self.s):
                    # print(str(j+x) + "," + str(i+x))
                    # print(self.current_state[j+x][i+x])
                    if self.current_state[j + x][i + x] == '.':
                        continue
                    elif self.current_state[j + x][i + x] == 'B':
                        score -= 1
                    elif self.current_state[j + x][i + x] == cell:
                        temp += 1
                        score += 2
                    else:
                        temp -= 1
                        score -= 2
                if temp == 2 and cell == 'X':
                    score = -1000
                    return score, None, None
                elif temp == -2 and cell == 'O':
                    score = 1000
                    return score, None, None

        for i in range(self.n - 1, 0, -1):
            for j in range(self.n):
                # print("---------")
                if self.n - i > self.s or self.n - j < self.s:
                    continue
                temp = 0
                for x in range(self.s):
                    # print(str(i-x) + "," + str(j+x))
                    # print(self.current_state[i-x][j+x])
                    if self.current_state[i - x][j + x] == '.':
                        continue
                    elif self.current_state[i - x][j + x] == 'B':
                        score -= 1
                    elif self.current_state[i - x][j + x] == cell:
                        temp += 1
                        score += 2
                    else:
                        temp -= 1
                        score -= 2
                if temp == 2 and cell == 'X':
                    score = -1000
                    return score, None, None
                elif temp == -2 and cell == 'O':
                    score = 1000
                    return score, None, None

        return score, None, None

    def isSafe(self, i, j, visited, cell):
        return (0 <= i < self.n and
                0 <= j < self.n and
                not visited[i][j] and self.current_state[i][j] == cell)

    def DFS(self, i, j, visited, count):

        rowNbr = [-1, -1, -1, 0, 0, 1, 1, 1]
        colNbr = [-1, 0, 1, -1, 1, -1, 0, 1]

        visited[i][j] = True

        for k in range(8):
            if self.isSafe(i + rowNbr[k], j + colNbr[k], visited, self.current_state[i][j]):
                count += 1
                self.DFS(i + rowNbr[k], j + colNbr[k], visited, count)

        if count == 0:
            visited[i][j] = False

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
                    (_, x, y) = self.minimax(self.d1, self.t, max=False)
                else:
                    (_, x, y) = self.minimax(self.d2, self.t, max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(self.d1, self.t, max=False)
                else:
                    (m, x, y) = self.alphabeta(self.d2, self.t, max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
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
        p2 = Game.HUMAN
    elif args.p2.lower() == "ai":
        p2 = Game.AI
    else:
        print("p2 must be human or ai")
        flag = False

    if args.coordinate:
        if len(args.coordinate) != args.b:
            print("Number of coordinates must be the same as b")
            flag = False

    if flag:
        g = Game(args.n, args.b, args.coordinate, args.s, args.d1, args.d2, args.t, a, p1, p2,
                 recommend=True)
        # g.draw_board()
        # g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)

        if a:
            g.play(algo=Game.ALPHABETA, player_x=p1, player_o=p2)
        else:
            g.play(algo=Game.MINIMAX, player_x=p1, player_o=p2)


if __name__ == "__main__":
    main()
