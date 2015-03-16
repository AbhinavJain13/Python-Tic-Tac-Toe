# -----------------------------------------------------------------------------
# Name:       tictac
# Purpose:    Implement a game of Tic Tac Toe
#
# Author:
# -----------------------------------------------------------------------------
'''
Enter the module docstring here
'''
import tkinter
import random



class Game(object):
    '''
    Enter the class docstring here
    '''
    BOARD_SIZE = 500
    PADDING = BOARD_SIZE // 3
    # Add your class variables if needed here
    def __init__(self, parent):

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

        # Create the restart button widget
        restart_button = tkinter.Button(top_frame, text="Restart")
        restart_button.pack()

        # Create a canvas widget
        board_canvas = tkinter.Canvas(center_frame, width=Game.BOARD_SIZE,
                                      height=Game.BOARD_SIZE)

        # Horizontal lines
        board_canvas.create_line(0,
                                 Game.PADDING,
                                 Game.BOARD_SIZE,
                                 Game.PADDING)
        board_canvas.create_line(0,
                                 Game.PADDING * 2,
                                 Game.BOARD_SIZE,
                                 Game.PADDING * 2)

        # Vertical lines
        board_canvas.create_line(Game.PADDING,
                                 0,
                                 Game.PADDING,
                                 Game.BOARD_SIZE)
        board_canvas.create_line(Game.PADDING * 2,
                                 0,
                                 Game.PADDING * 2,
                                 Game.BOARD_SIZE)

        # Bind action
        board_canvas.bind("<Button-1>", self.play)
        board_canvas.pack()

        # Create a label widget for the win/lose message
        status_line = tkinter.Label(bottom_frame, text="")
        status_line.pack()

        self.status_line = status_line
        self.board_canvas = board_canvas

        self.initialize_game()

    def initialize_game(self):
        # These are the initializations that need to happen
        # at the beginning and after restarts
        self.board = {}

        pass

    def restart(self):
        # This method is invoked when the user clicks on the RESTART button.
        # Erase the canvas
        # invoke initialize_game
        self.initialize_game()

    def play(self, event):
        # This method is invoked when the user clicks on a square.
        # If the square is already taken, do nothing.

        p_column = int(event.x * (3/Game.BOARD_SIZE))
        p_row = int(event.y * (3/Game.BOARD_SIZE))

        if (p_column, p_row) in self.board:
            return

        self.move(p_column, p_row, True)
        # Player made a move, check if won
        if not self.check_game_ended():

            print("Not end, computer's move")

            c_column = random.randint(0, 2)
            c_row = random.randint(0, 2)
            while (c_column, c_row) in self.board:
                c_column = random.randint(0, 2)
                c_row = random.randint(0, 2)

            print("Computer moving to:", (c_column, c_row))

            self.move(c_column, c_row, False)
            self.check_game_ended()

    def move(self, column, row, player):
        if 0 <= column <= 2 and 0 <= row <= 2:
            if (column, row) not in self.board:
                if player:
                    player = "P"
                else:
                    player = "C"
                self.board[(column, row)] = player
                self.fill_grid(column, row, player)

    def update_status_line(self, text):
        self.status_line.config(text=text)

    def no_more_moves(self):
        return len(self.board) >= 9

    def check_game_ended(self):
        # Check if player won and tie
        end = False
        check = self.check_game()
        print("Check is:", check)
        no_more_moves = self.no_more_moves()
        if check:
            self.update_status_line("Congrats, you won!")
            end = True
        elif no_more_moves:
            self.update_status_line("It's a tie!")
            end = True
        elif not check and no_more_moves:
            self.update_status_line("You lost!")
        return end

    def check_game(self):
        # Check if the game is won or lost
        # Return True or False
        print("Printing", self.board)
        for coordinate in sorted(self.board, key=lambda x: x[0]):
            print("Checking coordinate:", coordinate)
            if (coordinate[0] == coordinate[1]) and \
                self.check_diagonal():
                return True
            if self.check_vertical() or \
               self.check_horizontal():
                return True
        return False

    def check_vertical(self):
        print("Checking vertically:")
        vals = self.get_column_vals()
        for row in vals:
            result = self.dict_to_vals(row)
            if len(result) == 3 and len(set(result)) == 1 and result[0] == "P":
                return True
        return False

    def check_horizontal(self):
        print("Checking horizontally:")
        vals = self.get_row_vals()
        for row in vals:
            result = self.dict_to_vals(row)
            if len(result) == 3 and len(set(result)) == 1 and result[0] == "P":
                return True
        return False

    def check_diagonal(self):
        print("Checking diag:")
        vals = self.get_diag_vals()
        for row in vals:
            result = self.dict_to_vals(row)
            if len(result) == 3 and len(set(result)) == 1 and result[0] == "P":
                return True
        return False

    def get_row_vals(self):
        return [[(k, line) for k in range(0,3)] for line in range(0,3)]

    def get_column_vals(self):
        return [[(line, k) for k in range(0,3)] for line in range(0,3)]

    def get_diag_vals(self):
        return (((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0)))

    def dict_to_vals(self, arr):
        return [v for k, v in self.board.items() if k in arr]

    def fill_grid(self, column, row, player):
        print("Filling:", (column, row), player)

        grid_start = (column * Game.PADDING, row * Game.PADDING)
        grid_end = (grid_start[0] + Game.PADDING, grid_start[1] + Game.PADDING)

        print(grid_start, grid_end)

        color = "green"
        if player != "P":
            color = "blue"

        self.board_canvas.create_rectangle(grid_start[0],
                                           grid_start[1],
                                           grid_end[0],
                                           grid_end[1],
                                           fill=color)
    # Add your method definitions here


def main():
    # Instantiate a root window
    root = tkinter.Tk()

    # Instantiate a Game object
    game = Game(root)


    # Enter the main event loop
    root.mainloop()

if __name__ == '__main__':
    main()