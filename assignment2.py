# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
import os
import tempfile
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

    def __init__(self, n, b, coordinate, s, d1, d2, t, a, p1, p2, file, recommend=True, scoreboard=False):
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
        self.file = file
        self.heuristic_eval = 0
        self.total_moves = 0
        self.scoreboard = scoreboard
        self.recursion_depth = []
        self.evaluation_depth = []
        self.total_evaluation_depth = []
        self.total_recursion_depth = []
        self.total_evaluation_time = []
        self.total_heuristics_eval = []
        self.eval_by_depth = [0 for i in range(max(self.d1, self.d2) + 1)]
        self.total_eval_by_depth = [0 for i in range(max(self.d1, self.d2) + 1)]
        self.initialize_game()

    def initialize_game(self):

        if self.scoreboard:
            self.file = open("temp.txt", "w")

        self.current_state = [['.' for i in range(self.n)] for j in range(self.n)]
        # self.current_state = numpy.full((self.n,self.n), '.')
        string = "blocs=["
        if self.coordinate:
            for num in self.coordinate:
                x = int(num[0])
                y = int(num[1])
                if self.is_valid(x, y):
                    self.current_state[x][y] = 'B'
                    string += "(" + str(x) + "," + str(y) + "), "
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
                string += "(" + str(x) + "," + str(y) + "), "

        string += ']\n\n'
        string += "Player 1: "
        if self.p1 == 2:
            string += "AI"
        elif self.p1 == 3:
            string += "Human"
        string += " d=" + str(self.d1) + " a=" + str(self.a) + " e1\n"
        string += "Player 2: "
        if self.p2 == 2:
            string += "AI"
        elif self.p2 == 3:
            string += "Human"

        string += " d=" + str(self.d2) + " a=" + str(self.a) + ' e2\n\n'

        self.file.write(string)

        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        print()
        string = "  "
        for z in range(0, self.n):
            string += str(z) + " "

        print(string)
        for y in range(0, self.n):
            print(F'{y}', end="")
            print(F'|', end="")
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end="")
                print(F'|', end="")
            print()
        print()

    def print_board(self):
        string = "\n"
        string += "  "
        for z in range(0, self.n):
            string += str(z) + " "

        string += "\n"
        for y in range(0, self.n):
            string += str(y)
            string += '|'
            for x in range(0, self.n):
                string += self.current_state[x][y]
                string += '|'
            string += '\n'
        string += '\n'

        return string

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
                self.file.write("The winner is X!\n\n")
            elif self.result == 'O':
                print('The winner is O!')
                self.file.write("The winner is O!\n\n")
            elif self.result == '.':
                print("It's a tie!")
                self.file.write("It's a tie!\n\n")
            # self.initialize_game()
            self.file.write("Average evaluation time: " + str(numpy.mean(self.total_evaluation_time)) + "s\n")
            self.file.write("Heuristic evaluations: " + str(sum(self.total_heuristics_eval)) + "\n")
            self.file.write("Evaluation by depth: " + self.print_eval_by_depth(self.total_eval_by_depth) + "\n")
            self.file.write("Average evaluation depth: " + str(numpy.mean(self.total_evaluation_depth)) + "\n")
            self.file.write("Average recursion depth: " + str(numpy.mean(self.total_recursion_depth)) + "\n")
            self.file.write("Total moves: " + str(self.total_moves))
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                self.file.write(F'Player {self.player_turn} under Human control plays: x = {px}, y = {py}\n')
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'

        self.heuristic_eval = 0
        self.recursion_depth.clear()
        self.evaluation_depth.clear()
        for i in range(len(self.eval_by_depth)):
            self.eval_by_depth[i] = 0
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
                self.recursion_depth.append(self.d2 - depth)
                self.evaluation_depth.append(self.d2 - depth)
                return self.e1('O', self.d2 - depth)
            else:
                self.recursion_depth.append(self.d1 - depth)
                self.evaluation_depth.append(self.d1 - depth)
                return self.e2('X', self.d1 - depth)

        value = math.inf
        if max:
            value = -math.inf
        x = None
        y = None

        result = self.is_end()

        if result == 'X':
            self.heuristic_eval += 1
            self.recursion_depth.append(self.d1 - depth)
            return -self.n * self.n, x, y
        elif result == 'O':
            self.heuristic_eval += 1
            self.recursion_depth.append(self.d2 - depth)
            return self.n * self.n + 1, x, y

        if depth == 0:
            if max:
                self.recursion_depth.append(self.d2)
                self.evaluation_depth.append(self.d2)
                return self.e1('O', self.d2)
            else:
                self.recursion_depth.append(self.d1)
                self.evaluation_depth.append(self.d1)
                return self.e2('X', self.d1)

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
                        (v, _, _) = self.minimax(depth - 1, new_time_left, max=True)
                        if v < value or value == -math.inf:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, depth, time_left, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:

        start_time = time.time()
        if time_left < 0.1:
            if max:
                self.recursion_depth.append(self.d2 - depth)
                self.evaluation_depth.append(self.d2 - depth)
                return self.e1('O', self.d2 - depth)
            else:
                self.recursion_depth.append(self.d1 - depth)
                self.evaluation_depth.append(self.d1 - depth)
                return self.e2('X', self.d1 - depth)

        value = math.inf
        if max:
            value = -math.inf
        x = None
        y = None

        result = self.is_end()
        if result == 'X':
            self.heuristic_eval += 1
            self.recursion_depth.append(self.d1 - depth)
            self.evaluation_depth.append(self.d1 - depth)
            self.eval_by_depth[self.d1 - depth] += 1
            self.total_eval_by_depth[self.d1 - depth] += 1
            return -self.n * self.n, x, y
        elif result == 'O':
            self.heuristic_eval += 1
            self.evaluation_depth.append(self.d2 - depth)
            self.recursion_depth.append(self.d2 - depth)
            self.eval_by_depth[self.d2 - depth] += 1
            return self.n * self.n + 1, x, y

        if depth == 0:
            if max:
                self.recursion_depth.append(self.d2)
                self.evaluation_depth.append(self.d2)
                return self.e1('O', self.d2)
            else:
                self.recursion_depth.append(self.d1)
                self.evaluation_depth.append(self.d1)
                return self.e2('X', self.d1)

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

    def e1(self, cell, depth):

        self.heuristic_eval += 1
        self.eval_by_depth[depth] += 1
        self.total_eval_by_depth[depth] += 1
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

    def e2(self, cell, depth):

        self.eval_by_depth[depth] += 1
        self.total_eval_by_depth[depth] += 1
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
                if temp == self.s - 1 and cell == 'X':
                    score = -1000
                    return score, None, None
                elif temp == -(self.s - 1) and cell == 'O':
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
                if temp == self.s - 1 and cell == 'X':
                    score = -1000
                    return score, None, None
                elif temp == -(self.s - 1) and cell == 'O':
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
                if temp == self.s - 1 and cell == 'X':
                    score = -1000
                    return score, None, None
                elif temp == -(self.s - 1) and cell == 'O':
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
                if temp == self.s - 1 and cell == 'X':
                    score = -1000
                    return score, None, None
                elif temp == -(self.s - 1) and cell == 'O':
                    score = 1000
                    return score, None, None

        return score, None, None

    def isSafe(self, i, j, visited, cell):
        return (0 <= i < self.n and
                0 <= j < self.n and
                not visited[i][j] and self.current_state[i][j] == cell)

    def DFS(self, i, j, visited, count):

        self.heuristic_eval += 1
        rowNbr = [-1, -1, -1, 0, 0, 1, 1, 1]
        colNbr = [-1, 0, 1, -1, 1, -1, 0, 1]

        visited[i][j] = True

        for k in range(8):
            if self.isSafe(i + rowNbr[k], j + colNbr[k], visited, self.current_state[i][j]):
                count += 1
                self.DFS(i + rowNbr[k], j + colNbr[k], visited, count)

        if count == 0:
            visited[i][j] = False

    def print_eval_by_depth(self, list):
        string = "{"

        for i in range(len(list)):
            if list[i] == 0:
                continue
            else:
                string += (str(i) + ": " + str(list[i]) + ", ")
        string += "}"
        return string

    def play(self, algo=None, player_x=None, player_o=None):

        move = 1
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN

        self.file.write("Initial board configuration")
        self.file.write(self.print_board())
        while True:
            self.total_moves += 1
            self.draw_board()
            string = "Move: " + str(move) + '\n'
            move += 1
            if self.check_end():
                if self.scoreboard:
                    os.remove("temp.txt")
                return (self.result, numpy.mean(self.total_evaluation_time), sum(self.total_heuristics_eval), self.total_eval_by_depth,
                        numpy.mean(self.total_evaluation_depth), numpy.mean(self.total_recursion_depth), self.total_moves)
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
            self.total_evaluation_time.append(round(end - start, 7))
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                    string += 'Player ' + str(self.player_turn) + ' under AI control plays: x = ' + str(
                        x) + ', y = ' + str(y) + '\n'
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
                string += 'Player ' + str(self.player_turn) + ' under AI control plays: x = ' + str(x) + ', y = ' + str(
                    y) + '\n'

            stats = "Evaluation time: " + str(round(end - start, 7)) + "s\n"
            stats += "Heuristic evaluations: " + str(self.heuristic_eval) + "\n"
            self.total_heuristics_eval.append(self.heuristic_eval)
            stats += "Evaluation by depth: " + self.print_eval_by_depth(self.eval_by_depth) + "\n"
            stats += "Average evaluation depth: " + str(numpy.mean(self.evaluation_depth)) + "\n"
            self.total_evaluation_depth.append(numpy.mean(self.evaluation_depth))
            stats += "Average Recursion depth: " + str(numpy.average(self.recursion_depth))
            self.total_recursion_depth.append(numpy.average(self.recursion_depth))
            stats += "\n\n"
            self.current_state[x][y] = self.player_turn
            string += self.print_board()
            self.file.write(string)
            self.file.write(stats)
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
        filename = "gameTrace-" + str(args.n) + str(args.b) + str(args.s) + str(args.t) + ".txt"
        file = open(filename, "w")
        file.write("n=" + str(args.n) + " b=" + str(args.b) + " s=" + str(args.s) + " t=" + str(args.t) + "\n")
        g = Game(args.n, args.b, args.coordinate, args.s, args.d1, args.d2, args.t, a, p1, p2, file,
                 recommend=True)

        if a:
            g.play(algo=Game.ALPHABETA, player_x=p1, player_o=p2)
        else:
            g.play(algo=Game.MINIMAX, player_x=p1, player_o=p2)

        scoreboard = "scoreboard-" + str(args.n) + str(args.b) + str(args.s) + str(args.t) + ".txt"
        scoreboard_file = open(scoreboard, "w")
        scoreboard_file.write(
            "n=" + str(args.n) + " b=" + str(args.b) + " s=" + str(args.s) + " t=" + str(args.t) + "\n\n")
        scoreboard_file.write("Player 1: d=" + str(args.d1) + " a=" + str(args.a) + "\n")
        scoreboard_file.write("Player 2: d=" + str(args.d1) + " a=" + str(args.a) + "\n\n")
        scoreboard_file.write("10 games\n\n")
        # self.file.write("Average evaluation time: " + str(numpy.mean(self.total_evaluation_time)) + "s\n")
        # self.file.write("Heuristic evaluations: " + str(sum(self.total_heuristics_eval)) + "\n")
        # self.file.write("Evaluation by depth: " + self.print_eval_by_depth(self.total_eval_by_depth) + "\n")
        # self.file.write("Average evaluation depth: " + str(numpy.mean(self.total_evaluation_depth)) + "\n")
        # self.file.write("Average recursion depth: " + str(numpy.mean(self.total_recursion_depth)) + "\n")
        # self.file.write("Total moves: " + str(self.total_moves))

        results = []
        total_eval_time = []
        total_heuristic_eval = []
        total_eval_by_depth = [0 for i in range(max(args.d1, args.d2) + 1)]
        total_evaluation_depth = []
        total_recursion_depth = []
        total_moves = []
        for i in range(10):
            if i % 2 == 0:
                if a:
                    g = Game(args.n, args.b, args.coordinate, args.s, args.d1, args.d2, args.t, a, p1, p2, file,
                             recommend=True, scoreboard=True)
                    result, eval_time, heuristic_eval, eval_by_depth, eval_depth, recursion_depth, moves = \
                        g.play(algo=Game.ALPHABETA, player_x=p1, player_o=p2)
                else:
                    g = Game(args.n, args.b, args.coordinate, args.s, args.d1, args.d2, args.t, a, p1, p2, file,
                             recommend=True, scoreboard=True)
                    result, eval_time, heuristic_eval, eval_by_depth, eval_depth, recursion_depth, moves = \
                        g.play(algo=Game.MINIMAX, player_x=p1, player_o=p2)
            else:
                if a:
                    g = Game(args.n, args.b, args.coordinate, args.s, args.d1, args.d2, args.t, a, p1, p2, file,
                             recommend=True, scoreboard=True)
                    result, eval_time, heuristic_eval, eval_by_depth, eval_depth, recursion_depth, moves = \
                        g.play(algo=Game.ALPHABETA, player_x=p2, player_o=p1)
                else:
                    g = Game(args.n, args.b, args.coordinate, args.s, args.d1, args.d2, args.t, a, p1, p2, file,
                             recommend=True, scoreboard=True)
                    result, eval_time, heuristic_eval, eval_by_depth, eval_depth, recursion_depth, moves = \
                        g.play(algo=Game.MINIMAX, player_x=p2, player_o=p1)

            results.append(result)
            total_eval_time.append(eval_time)
            total_heuristic_eval.append(heuristic_eval)
            total_evaluation_depth.append(eval_depth)
            total_recursion_depth.append(recursion_depth)
            total_moves.append(moves)

            for j in range(len(eval_by_depth)):
                total_eval_by_depth[j] += eval_by_depth[j]

        # print(results.count('O'))
        # print(results.count('X'))
        scoreboard_file.write("Total wins for heuristic e1: " + str(results.count('O')) + " (" + str(results.count('O')/10*100) + "%)\n")
        scoreboard_file.write("Total wins for heuristic e2: " + str(results.count('X')) + " (" + str(results.count('X')/10*100) + "%)\n\n")

        scoreboard_file.write("Average evaluation time: " + str(numpy.mean(total_eval_time)) + "s\n")
        scoreboard_file.write("Total heuristic evaluation: " + str(sum(total_heuristic_eval)) + "\n")
        scoreboard_file.write("Evaluations by depth: " + str(Game.print_eval_by_depth(g,total_eval_by_depth)) + "\n")
        scoreboard_file.write("Average evaluation depth: " + str(numpy.mean(total_evaluation_depth)) + "\n")
        scoreboard_file.write("Average recursion depth: " + str(numpy.mean(total_recursion_depth)) + "\n")
        scoreboard_file.write("Average moves per game: " + str(numpy.mean(total_moves)) + "\n")

        file.close()
        scoreboard_file.close()


if __name__ == "__main__":
    main()
