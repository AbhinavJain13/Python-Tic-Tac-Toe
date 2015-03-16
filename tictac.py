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
    GRID_SIZE = BOARD_SIZE // DIMENSION

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

        p_column = int(event.x * (Game.DIMENSION/Game.BOARD_SIZE))
        p_row = int(event.y * (Game.DIMENSION/Game.BOARD_SIZE))

        if (p_column, p_row) in self.board:
            return

        self.move((p_column, p_row), True)
        # Player made a move, check if won
        if not self.check_game_ended():

            print("Not end, computer's move")

            move = self.gen_random_move()

            print("Computer moving to:", (move))

            self.move(move, False)
            self.check_game_ended()

    def gen_random_move(self, column=-1, row=-1):
        if column < 0 or row < 0 or (column, row) in self.board:
            return self.gen_random_move(random.randint(0, Game.DIMENSION-1),
                                        random.randint(0, Game.DIMENSION-1))
        else:
            return (column, row)

    def move(self, move, player):
        column = move[0]
        row = move[1]

        if 0 <= column <= Game.DIMENSION and 0 <= row <= Game.DIMENSION:
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
        return len(self.board) >= Game.DIMENSION * Game.DIMENSION

    def check_game_ended(self):
        # Check if player won and tie
        end = False
        check = self.check_game()

        no_more_moves = self.no_more_moves()

        if no_more_moves:
            self.update_status_line("It's a tie!")
            end = True
        elif check is not None:
            if check:
                self.update_status_line("Congrats, you won!")
                end = True
            elif not check:
                self.update_status_line("You lost!")
                end = True
        return end

    def check_game(self):
        # Check if the game is won or lost
        # Return True or False
        d_winner = self.check_diagonal()
        v_winner = self.check_vertical()
        h_winner = self.check_horizontal()

        winner = [d_winner, v_winner, h_winner]

        if "P" in winner:
            return True
        elif "C" in winner:
            return False

    def check_vertical(self):
        for row in self.column_victories():
            result = self.extract_values(row)
            if len(result) == Game.DIMENSION and len(set(result)) == 1:
                return result[0]

    def check_horizontal(self):
        for row in self.row_victories():
            result = self.extract_values(row)
            if len(result) == Game.DIMENSION and len(set(result)) == 1:
                return result[0]

    def check_diagonal(self):
        for row in self.diagonal_victories():
            result = self.extract_values(row)
            if len(result) == Game.DIMENSION and len(set(result)) == 1:
                return result[0]

    def extract_values(self, arr):
        return [v for k, v in self.board.items() if k in arr]

    def fill_grid(self, column, row, player):

        print("Print size:", Game.BOARD_SIZE)

        grid_start = (column * Game.GRID_SIZE, row * Game.GRID_SIZE)
        grid_end = (grid_start[0] + Game.GRID_SIZE, grid_start[1] + Game.GRID_SIZE)
        print("Filling:", (grid_start, grid_end))
        color = "green"
        if player != "P":
            color = "blue"

        self.board_canvas.create_rectangle(grid_start[0],
                                           grid_start[1],
                                           grid_end[0],
                                           grid_end[1],
                                           fill=color)
    # Add your method definitions here
    @classmethod
    def row_victories(cls):
        return ([(k, line)
                for k in range(cls.DIMENSION)]
                for line in range(cls.DIMENSION))
    @classmethod
    def column_victories(cls):
        return ([(line, k)
                for k in range(cls.DIMENSION)]
                for line in range(cls.DIMENSION))
    @classmethod
    def diagonal_victories(cls):
        return ([(i, Game.DIMENSION-1-i)
                 for i in range(cls.DIMENSION-1, -1, -1)],
                [(i, i)
                 for i in range(cls.DIMENSION)])

def main():
    # Instantiate a root window
    root = tkinter.Tk()

    # Instantiate a Game object
    game = Game(root)

    # Enter the main event loop
    root.mainloop()

if __name__ == '__main__':
    main()