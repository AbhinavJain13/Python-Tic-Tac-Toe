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
    BOARD_SIZE = 1000
    DIMENSION = 3
    PADDING = BOARD_SIZE // DIMENSION
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

        # Create a canvas widget
        self.board_canvas = tkinter.Canvas(center_frame,
                                           width=Game.BOARD_SIZE,
                                           height=Game.BOARD_SIZE)

        # Create the restart button widget
        restart_button = tkinter.Button(top_frame, text="Restart")
        restart_button.bind("<Button-1>", self.restart)
        restart_button.pack()


        # Bind action
        self.board_canvas.bind("<Button-1>", self.play)

        # Create a label widget for the win/lose message
        status_line = tkinter.Label(bottom_frame, text="")
        status_line.pack()

        self.status_line = status_line

        self.initialize_game()

    def initialize_game(self):
        # These are the initializations that need to happen
        # at the beginning and after restarts

        # Horizontal lines
        self.board_canvas.create_line(0,
                                 Game.PADDING,
                                 Game.BOARD_SIZE,
                                 Game.PADDING)
        self.board_canvas.create_line(0,
                                 Game.PADDING * 2,
                                 Game.BOARD_SIZE,
                                 Game.PADDING * 2)

        # Vertical lines
        self.board_canvas.create_line(Game.PADDING,
                                 0,
                                 Game.PADDING,
                                 Game.BOARD_SIZE)
        self.board_canvas.create_line(Game.PADDING * 2,
                                 0,
                                 Game.PADDING * 2,
                                 Game.BOARD_SIZE)
        self.board_canvas.pack()


    def restart(self, event):
        # This method is invoked when the user clicks on the RESTART button.
        # Erase the canvas
        # invoke initialize_game
        print("Restarting")
        self.board_canvas.delete("all")
        self.initialize_game()
        self.board = dict()
        self.update_status_line("")

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
                print("Got",(c_column, c_row),"Repicking for computer")
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

        no_more_moves = self.no_more_moves()
        if check is not None:
            if no_more_moves:
                self.update_status_line("It's a tie!")
                end = True
            elif check:
                self.update_status_line("Congrats, you won!")
                end = True
            elif not check:
                self.update_status_line("You lost!")
                end = True
        return end

    def check_game(self):
        # Check if the game is won or lost
        # Return True or False
        diag_winner = self.check_diagonal()
        vert_winner = self.check_vertical()
        hori_winner = self.check_horizontal()

        winner = [diag_winner, vert_winner, hori_winner]

        if "P" in winner:
            return True
        elif "C" in winner:
            return False

    def check_vertical(self):
        for row in self.get_column_vals():
            result = self.dict_to_vals(row)
            if len(result) == 3 and len(set(result)) == 1:
                return result[0]

    def check_horizontal(self):
        for row in self.get_row_vals():
            result = self.dict_to_vals(row)
            if len(result) == 3 and len(set(result)) == 1:
                return result[0]

    def check_diagonal(self):
        for row in self.get_diag_vals():
            result = self.dict_to_vals(row)
            if len(result) == 3 and len(set(result)) == 1:
                return result[0]

    def get_row_vals(self):
        return [[(k, line) for k in range(0,3)] for line in range(0,3)]

    def get_column_vals(self):
        return [[(line, k) for k in range(0,3)] for line in range(0,3)]

    def get_diag_vals(self):
        return [[(i, 2-i) for i in range(2,-1,-1)], [(i, i) for i in range(
            0,3)]]

    def dict_to_vals(self, arr):
        return [v for k, v in self.board.items() if k in arr]

    def fill_grid(self, column, row, player):
        grid_start = (column * Game.PADDING, row * Game.PADDING)
        grid_end = (grid_start[0] + Game.PADDING, grid_start[1] + Game.PADDING)

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