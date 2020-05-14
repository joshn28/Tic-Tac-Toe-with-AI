import random

positions = {(1, 1): (2, 0), (1, 2): (1, 0), (1, 3): (0, 0), (2, 1): (2, 1), (2, 2): (1, 1),
             (2, 3): (0, 1), (3, 1): (2, 2), (3, 2): (1, 2), (3, 3): (0, 2)}

valid_inputs = ["start", "user", "easy", "medium", "hard"]
commands = ""

def empty_cell(string):
    if string == '_':
        return ' '
    return string

class TicTacToe:
    """Tic-Tac-Toe Game
    """

    def __init__(self):
        self.lines = [[" ", " ", " "],
                     [" ", " ", " "],
                     [" ", " ", " "]]

    def __str__(self):
        """Displays the Tic-Tac-Toe board
        """

        return f"""
        ---------
        | {self.lines[0][0]} {self.lines[0][1]} {self.lines[0][2]} |
        | {self.lines[1][0]} {self.lines[1][1]} {self.lines[1][2]} |
        | {self.lines[2][0]} {self.lines[2][1]} {self.lines[2][2]} |
        ---------
        """

    def cell_full(self, coordinate):
        """Checks if the cell with the given coordinates is full"""
        global positions
        p = positions[coordinate]
        if self.lines[p[0]][p[1]] != " ":
            return True
        return False

    def winner(self, symbol):
        """Checks if 'X' or 'O' has won"""
        bools = []
        for lst in self.lines:
            temp = []
            for sign in lst:
                if sign == symbol:
                    temp.append(True)
                else:
                    temp.append(False)
            bools.append(temp)
        for boolean in bools:
            if all(boolean):
                return True
        if self.lines[0][0] == symbol and self.lines[1][1] == symbol and \
                self.lines[2][2] == symbol:
            return True
        elif self.lines[2][0] == symbol and self.lines[1][1] == symbol and \
                self.lines[0][2] == symbol:
            return True
        else:
            for i in range(3):
                lst = []
                for j in range(3):
                    lst.append(self.lines[j][i] == symbol)
                if all(lst):
                    return True
        return False

    def game_status(self):
        """Displays the game status"""
        if self.winner("X"):
            return "X wins"
        elif self.winner("O"):
            return "O wins"
        elif all([symbol != ' ' for lst in self.lines for symbol in lst]):
            return "Draw"
        elif any([symbol == ' ' for lst in self.lines for symbol in lst]):
            return 'Game not finished'

    def bot_random(self, string, mode):
        """Makes a bot make a move based on <mode>"""
        print(f'Making move level "{mode}"'  )

        if mode == "hard":
            best_score = -100
            availSpots = self.available_spots()
            for i in range(len(availSpots)):
                self.lines[availSpots[i][0]][availSpots[i][1]] = string
                score = self.minimax(True, string)
                self.lines[availSpots[i][0]][availSpots[i][1]] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (availSpots[i][0], availSpots[i][1])
            self.lines[best_move[0]][best_move[1]] = string
            return
        elif mode == "medium":
            # Checks if any of the rows have 2 of <string>
            for i in range(len(self.lines)):
                if self.lines[i].count(' ') == 1 and \
                self.lines.count(string) == 2:
                    self.lines[i][self.lines[i].index(' ')] = string
                    return
                elif self.lines[i].count(' ') == 1:
                    self.lines[i][self.lines[i].index(' ')] = string
                    return
            # Checks if any of the columns has 2 of <string>
            for i in range(len(self.lines)):
                num_strings = 0
                empty = []
                for pos in range(len(self.lines)):
                    if self.lines[pos][i] == ' ':
                        empty.append((pos, i))
                    elif self.lines[pos][i] == string:
                        num_strings += 1
                if num_strings == 2 and len(empty) == 1:
                    self.lines[empty[0][0]][empty[0][1]] = string
                    return
        # Make the bot do a random move
        while True:
            com = random.choice(list(positions.keys()))
            if not self.cell_full(com):
                pos = positions[com]
                self.lines[pos[0]][pos[1]] = string
                break


    def human(self, string):
        """Allows a user to make a move"""
        while True:
            try:
                user = input("Enter the coordinates: ")
                coordinates = (int(user[0]), int(user[2]))
                if coordinates[0] > 3 or coordinates[0] < 1:
                    print("Coordinates should be from 1 to 3!")
                elif coordinates[1] > 3 or coordinates[1] < 1:
                    print("Coordinates should be from 1 to 3!")
                elif self.cell_full(coordinates):
                    print("This cell is occupied! Choose another one!")
                else:
                    pos = positions[coordinates]
                    self.lines[pos[0]][pos[1]] = string
                    break
            except:
                print("You should enter numbers!")


    def available_spots(self):
        """Finds the available positions on the board"""
        spots = []
        for x in range(len(self.lines)):
            for y in range(len(self.lines)):
                if self.lines[x][y] == ' ':
                    spots.append((x, y))
        return spots

    def minimax(self, ai, string):
        """The minimax algorithm to make the bot pick the most optimial
        optimal position
        """
        availSpots = self.available_spots()
        if string == 'X':
            opponent = 'O'
        else:
            opponent = 'X'
        if self.winner(string):
            return 10
        elif self.winner(opponent):
            return -10
        elif len(availSpots) == 0:
            return 0

        if ai:
            best_score = -100
            for i in range(len(availSpots)):
                self.lines[availSpots[i][0]][availSpots[i][1]] = string
                score = self.minimax(False, opponent)
                self.lines[availSpots[i][0]][availSpots[i][1]] = ' '
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = 100
            for i in range(len(availSpots)):
                self.lines[availSpots[i][0]][availSpots[i][1]] = string
                score = self.minimax(True, opponent)
                self.lines[availSpots[i][0]][availSpots[i][1]] = ' '
                best_score = min(best_score, score)
            return best_score


def main_loop():
    # Function to play the game
    game = TicTacToe()
    print(game)
    while True:
        if commands[1] not in valid_inputs[2:] and commands[2] not in valid_inputs[2:]:
            game.human('X')
            print(game)
            if game.game_status() != 'Game not finished':
                print(game.game_status())
                break
            game.human('O')
            print(game)
        elif commands[1] == "user":
            game.human('X')
            print(game)
            if game.game_status() != 'Game not finished':
                print(game.game_status())
                break
            game.bot_random('O', commands[2])
            print(game)
        elif "user" not in commands[1:]:
            game.bot_random('X', commands[1])
            print(game)
            if game.game_status() != 'Game not finished':
                print(game.game_status())
                break
            game.bot_random('O', commands[2])
            print(game)
        else:
            game.bot_random('X', commands[1])
            print(game)
            if game.game_status() != 'Game not finished':
                print(game.game_status())
                break
            game.human('O')
            print(game)
        if game.game_status() != 'Game not finished':
            print(game.game_status())
            break

# Command menu to play
while True:
    commands = input("Input command: ").split()
    if commands[0] == "exit":
        break
    elif len(commands) < 3 or commands[0] != "start" or \
    not all([command in valid_inputs for command in commands]):
        print("Bad parameters!")
    else:
        main_loop()
