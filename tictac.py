# -----------------------------------------------------------------------------
# Name:       tictac
# Purpose:    Implement a game of Tic Tac Toe
#
# Author:
# -----------------------------------------------------------------------------
"""
Play tic tac toe of any board size with computer.

A GUI application that simulates a tic tac toe game, use mouse to play the
game with computer. Player and computer take turn on the same board.
"""
import tkinter
import random


class Game(object):
    """
    Represents a tic tac toe game instance.

    Argument:
    parent (Tkinter.Frame): Root frame for the game to show

    Attributes:
    none

    Class variables:
    BOARD_SIZE (int): Board size
    DIMENSION (int): Board dimension
    GRID_SIZE (int): Size of each grid, computed
    COLOR_PLAYER (string): Grid color for player
    COLOR_COMPUTER (string): Grid color for computer
    """

    # Game setting constants
    BOARD_SIZE = 500  # Board size
    DIMENSION = 3      # Board dimension
    GRID_SIZE = BOARD_SIZE // DIMENSION  # Size of each grid
    COLOR_PLAYER = "green"   # Grid color for player
    COLOR_COMPUTER = "blue"  # Grid color for computer

    @classmethod
    def init_constants(cls):
        cls.VICTORY_HORIZONTAL = list([[(k, line)
                                      for k in range(Game.DIMENSION)]
                                      for line in range(Game.DIMENSION)])
        cls.VICTORY_VERTICAL = list([[(line, k)
                                    for k in range(Game.DIMENSION)]
                                    for line in range(Game.DIMENSION)])
        cls.VICTORY_DIAGONAL = list([[(i, Game.DIMENSION-1-i)
                                    for i in range(Game.DIMENSION-1, -1, -1)],
                                    [(i, i)
                                     for i in range(Game.DIMENSION)]])

    def __init__(self, parent):

        self.init_constants()

        parent.title('Tic Tac Toe')
        self.parent = parent
        # Add your instance variables  if needed here
        self.board = dict()

        top_frame = tkinter.Frame(parent)
        top_frame.pack(side=tkinter.TOP)
        center_frame = tkinter.Frame(top_frame)
        center_frame.pack(side=tkinter.BOTTOM)
        bottom_frame = tkinter.Frame(parent)
        bottom_frame.pack(side=tkinter.BOTTOM)

        # Create a canvas widget
        board_canvas = tkinter.Canvas(center_frame,
                                      width=Game.BOARD_SIZE,
                                      height=Game.BOARD_SIZE)

        # Create the restart button widget
        restart_button = tkinter.Button(top_frame, text="Restart")
        restart_button.bind("<Button-1>", self.restart)
        restart_button.pack()

        # Create a label widget for the win/lose message
        status_line = tkinter.Label(bottom_frame, text="")
        status_line.pack()

        self.status_line = status_line
        self.board_canvas = board_canvas
        self.initialize_game()

    def initialize_game(self):
        """
        Draws separation lines onto board canvas

        Parameters:
        none

        Returns:
        none
        """
        # Draw separation lines
        for i in range(1, Game.DIMENSION):
            # Horizontal lines
            self.board_canvas.create_line(0,
                                          Game.GRID_SIZE * i,
                                          Game.BOARD_SIZE,
                                          Game.GRID_SIZE * i)
            # Vertical lines
            self.board_canvas.create_line(Game.GRID_SIZE * i,
                                          0,
                                          Game.GRID_SIZE * i,
                                          Game.BOARD_SIZE)
        self.board_canvas.bind("<Button-1>", self.play)
        self.board_canvas.pack()

    def restart(self, event):
        """
        This method is invoked when the user clicks on the RESTART button.
        Clears everything in the board canvas and draw new separation lines

        Parameters:
        event: Mouse event from Tkinter

        Returns:
        none
        """
        self.board_canvas.delete("all")  # Erase the canvas
        self.board = dict()  # clear model
        self.update_status_line("")  # clear status line
        self.initialize_game()  # invoke initialize_game

    def play(self, event):
        # This method is invoked when the user clicks on a square.
        # If the square is already taken, do nothing.

        p_column = int(event.x * (Game.DIMENSION/Game.BOARD_SIZE))
        p_row = int(event.y * (Game.DIMENSION/Game.BOARD_SIZE))

        if 0 <= p_column <= 2 and 0 <= p_row <= 2 \
           and (p_column, p_row) not in self.board:
            self.move((p_column, p_row), "P")
            # Player made a move, check if won
            if not self.check_game_ended():
                move = self.gen_random_move()
                self.move(move, "C")
                self.check_game_ended()

    def check_game(self):
        # Check if the game is won or lost
        # Return True or False
        d_winner = self.line_winner(Game.VICTORY_DIAGONAL)
        v_winner = self.line_winner(Game.VICTORY_VERTICAL)
        h_winner = self.line_winner(Game.VICTORY_HORIZONTAL)

        winner = [d_winner, v_winner, h_winner]

        if "P" in winner:
            return True
        elif "C" in winner:
            return False

    def check_game_ended(self):
        # Check if player won and tie
        end = False
        check = self.check_game()
        no_more_moves = self.no_more_moves()

        if no_more_moves and not check:
            self.update_status_line("It's a tie!")
            end = True
        elif check is not None:
            self.board_canvas.unbind("<Button-1>")
            end = True
            if check:
                self.update_status_line("Congrats, you won!")
            elif not check:
                self.update_status_line("You lost!")
        return end

    def move(self, move, player):
        column = move[0]
        row = move[1]

        if 0 <= column <= Game.DIMENSION and 0 <= row <= Game.DIMENSION:
            if (column, row) not in self.board:
                self.board[(column, row)] = player
                self.fill_grid(column, row, player)

    def gen_random_move(self, column=-1, row=-1):
        if column < 0 or row < 0 or (column, row) in self.board:
            return self.gen_random_move(random.randint(0, Game.DIMENSION-1),
                                        random.randint(0, Game.DIMENSION-1))
        else:
            return (column, row)

    def gen_smart_move(self):
        if not self.smart_route_valid():
            self.smart_route = self.gen_smart_route()
        return [x for x in self.smart_route if x not in self.board] \
               if self.smart_route else []

    def gen_smart_route(self):
        c_moves = self.get_all_moves("C")
        if not c_moves:
            c_moves = [self.gen_random_move()]
        impossible = False
        win_h = []
        win_v = []
        win_d = []

        while not (win_h or win_v or win_d) and not impossible:
            for move in c_moves:
                win_h = self.win(Game.VICTORY_HORIZONTAL, move)


    def win(self, victory, move):
        return move in [seq for seq in victory]

    def get_all_moves(self, player):
        return [move for move in self.board if self.board[move] is player]

    def smart_route_valid(self):
        """
        True if self.smart_route in self.board is all "C"s
        """
        return "P" not in self.extract_values(self.smart_route) \
               if self.smart_route else False

    def update_status_line(self, text):
        self.status_line.config(text=text)

    def no_more_moves(self):
        return len(self.board) >= Game.DIMENSION * Game.DIMENSION

    def line_winner(self, line):
        for row in line:
            result = self.extract_values(row)
            return result[0] \
                if len(result) == Game.DIMENSION and \
                all(x == result[0] for x in result) \
                else None

    def extract_values(self, arr):
        return [v for k, v in self.board.items() if k in arr]

    def fill_grid(self, column, row, player):

        print("Filling for", (column, row))

        grid_start = (column * Game.GRID_SIZE, row * Game.GRID_SIZE)
        grid_end = (grid_start[0] + Game.GRID_SIZE,
                    grid_start[1] + Game.GRID_SIZE)

        color = Game.COLOR_PLAYER
        if player is "C":
            color = Game.COLOR_COMPUTER

        self.board_canvas.create_rectangle(grid_start[0],
                                           grid_start[1],
                                           grid_end[0],
                                           grid_end[1],
                                           fill=color)


def main():
    # Instantiate a root window
    root = tkinter.Tk()
    # Instantiate a Game object
    game = Game(root)
    # Enter the main event loop
    root.mainloop()

if __name__ == '__main__':
    main()