# This game is the Minesweeper
# The objective is to find all the mines within a grid,
# based on the help of cues that provide the number of mines in the adjacent squares.
import random
import tkinter as tk
from tkinter import messagebox
from tkmacosx import Button

WIDTH = 9
HEIGHT = 9
BOMB_NUM = 10

class Cell(Button):
    def __init__(self, x: int, y: int, value, open: bool, flagged: bool, *args, **kwargs):
        self.__x = x
        self.__y = y
        self.__value = value
        self.__open = open
        self.__flagged = flagged
        super().__init__(*args, **kwargs)
    
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, value):
        if value != '*' and (value > 8 or value < 0):
            raise ValueError("Value must be either * or from 0 to 8")
        self.__value = value
    
    @property
    def open(self):
        return self.__open
    @open.setter
    def open(self, open):
        if not isinstance(open, bool):
            raise ValueError("Value boolean")
        self.__open = open
    
    @property
    def flagged(self):
        return self.__flagged
    @flagged.setter
    def flagged(self, flagged):
        if not isinstance(flagged, bool):
            raise ValueError("Value boolean")
        self.__flagged = flagged


def open_space(board, x: int, y: int):
    """
    open cell, change its color to identify that cell was opened
    recursively open other cells that are near if they are empty ()
    """
    board[x][y].open = True
    board[x][y].configure(bg="grey")
    
    if board[x][y].value == 0:
        board[x][y]["text"] = ' '
        for a in range(x - 1, x + 2):
            for b in range(y - 1, y + 2):
                if 0 <= a < HEIGHT and 0 <= b < WIDTH:
                    if not (board[a][b].value == "*" or board[a][b].open or board[a][b].flagged):
                        open_space(board, a, b)
    else: board[x][y]["text"] = board[x][y].value

def all_opened(board):
    """
    check if all cells except for ones with bombs were opened
    """
    c = sum(1 for i in range(HEIGHT) for j in range(WIDTH) if board[i][j].open) # count how many elements(cells) are open 
    state = c == HEIGHT * WIDTH - BOMB_NUM
    return state

def reveal_position(board, won=False):
    """
    in the end of game change background of cell
    if it is bomb and was flagged, it become green
    otherwise red
    if non bomb cell was flagged, it will be red indicating wrong decision
    """
    for i in range(HEIGHT):
        for j in range(WIDTH):
            board[i][j].open = True
            if board[i][j].value == '*':
                board[i][j]['text'] = '*'
                if board[i][j].flagged or won: # won for case all non bomb cells were opened but still not all bombs are flagged
                    board[i][j].configure(disabledbackground="green")
                else:
                    board[i][j].configure(disabledbackground="red")
            elif board[i][j].flagged:
                board[i][j].configure(disabledbackground="red")

def bombs_flagged(board):
    """
    check if all bombs are flagged
    """
    all_flagged = True
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j].value == '*' and not board[i][j].flagged:
                all_flagged = False
    return all_flagged

def disable_cells(board):
    """
    in the end of game disable all cells
    """
    for i in range(HEIGHT):
        for j in range(WIDTH):
            board[i][j]['state'] = "disabled"

def create_root():
    """
    create non resizable root window and menu to restart the game
    """
    root = tk.Tk()
    root.geometry("270x270")
    root.resizable(False, False)
    root.configure(bg="#ececec")
    root.title("Minesweeper")
    root.eval("tk::PlaceWindow . center")
    my_menu = tk.Menu()
    root.config(menu=my_menu)
    options_menu = tk.Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label='Options', menu=options_menu)
    options_menu.add_command(label="Restart Game", command=lambda:game(root))
    return root

def create_board(root):
    """
    create two-dimensional list of cells (class inherited from Button)
    plant bombs
    return finished board
    """
    board = [[Cell(j, i, 0, False, False, root, text=' ', font=("Helvetica", 20), height=30, width=30, bg="SystemButtonFace") for i in range(WIDTH)] for j in range(HEIGHT)]

    mines = set()  # set of locations of bombs
    while len(mines) < BOMB_NUM:
        x = random.randint(0, HEIGHT - 1)
        y = random.randint(0, WIDTH - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            board[x][y].value = '*'
            for a in range(x - 1, x + 2):
                for b in range(y - 1, y + 2):
                    if 0 <= a < HEIGHT and 0 <= b < WIDTH:  # check if cell is not out of board
                        if board[a][b].value != '*':
                            board[a][b].value += 1  # increase value of cell is there is a bomb around

    return board

def click(event, board):
    """
    open cell by left click
    flag/unflagg cell by right click
    control the game (if player won or lost) and inform user about it
    """
    if event.num == 1:
        if not (event.widget.flagged or event.widget.open):
            open_space(board, event.widget.x, event.widget.y)
            
            if event.widget.value == '*':
                reveal_position(board)
                disable_cells(board)
                messagebox.showinfo("You lost", "You have lost the game")
            elif all_opened(board):
                reveal_position(board, won=True)
                messagebox.showinfo("You won", "You have won the game, congratulations")
                disable_cells(board)
    elif event.num == 2:
        if not event.widget.open:
            if not event.widget.flagged:
                event.widget["text"] = 'F'
                event.widget.flagged = True
                if bombs_flagged(board):
                    messagebox.showinfo("You won", "You have won the game, congratulations")
                    reveal_position(board, won=True)
                    disable_cells(board)
            else:
                event.widget["text"] = ' '
                event.widget.flagged = False

def game(root):
    """
    create board
    place buttons on root window
    define left and right click on button
    """
    
    board = create_board(root)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            board[i][j].grid(row=i, column=j)
            board[i][j].bind("<Button-1>", lambda event: click(event, board))
            board[i][j].bind("<Button-2>", lambda event: click(event, board))
    root.mainloop()
            

try:
    root = create_root()
    game(root)
except BaseException as e:
    print('\nSomething unexpected happened, try to start game from the beginning')
    print(e)
