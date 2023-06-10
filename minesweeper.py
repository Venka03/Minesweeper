# This game is the Minesweeper
# The objective is to find all the mines within a grid,
# based on the help of cues that provide the number of mines in the adjacent squares.
import random
import time


def open_cell(board, x: int, y: int):
    """
    open cell
    check if it is already opened, flagged or there is a bomb in it,
    """
    global GAME_OVER
    if board[x][y]['flagged']:
        print("Cell is flagged, you cannot open it")
    elif board[x][y]['value'] == '*':
        board[x][y]["open"] = True
        GAME_OVER = True
    elif board[x][y]["open"]:
        print("Cell is already opened")
    else:
        open_space(board, x, y)


def open_space(board, x: int, y: int):
    """
    open cell and recursively open other cells that are near if they are empty
    """
    board[x][y]["open"] = True
    if board[x][y]["value"] == 0:
        for a in range(x - 1, x + 2):
            for b in range(y - 1, y + 2):
                if 0 <= a < HEIGHT and 0 <= b < WIDTH:  # check if cell is not out of board
                    if not (board[a][b]["value"] == "*" or board[a][b]['open'] or board[a][b]['flagged']):
                        open_space(board, a, b)


def flag_cell(board, x: int, y: int):
    """
    flag cell if it is not flagged and unflag cell if it is flagged
    add/delete coordinated of flagged/unflagged cell
    """

    if board[x][y]["open"]:
        print(f"It is not possible to flag cell ({x}, {y}) because it is opened ")
    elif board[x][y]["flagged"]:
        board[x][y]["flagged"] = False
        FLAGGED.remove((x, y))
    else:
        if len(FLAGGED) < BOMB_NUM:
            board[x][y]["flagged"] = True
            FLAGGED.add((x, y))
        else:
            print(f"It is not possible to flag cell ({x}, {y}) because you have already flagged {BOMB_NUM} cells")


def hint(board):
    """
    give user hint where is a bomb and automatically flag it
    """
    not_found = MINES.difference(FLAGGED)  # so we do not give a hint(cell with bomb) what is already flagged
    bomb = random.choice(list(not_found))
    print(f"Bomb is located at position {bomb}")
    FLAGGED.add(bomb)
    x, y = bomb
    board[x][y]['flagged'] = True


def print_board(board, lost=False):
    """
    output to console board with coordinates
    """
    print("     ", end='')
    for i in range(WIDTH):
        print(i, end=' ')
    print('')

    print("     ", end='')
    for i in range(WIDTH):
        if i > 9:
            print(" ", end='')
        print('_', end=' ')
    print('')

    for i in range(HEIGHT):
        print(i, end=' ')
        if i < 10:
            print(" | ", end='')
        else:
            print("| ", end='')
        for j in range(WIDTH):
            if j > 9:
                print(" ", end='')
            if board[i][j]['open']:
                val = board[i][j]['value']
                if val == 0:
                    val = ' '
                print(val, end=' ')
            elif board[i][j]['flagged']:
                print('F', end=' ')
            else:
                if lost and board[i][j]['value'] == '*':
                    print('*', end=' ')
                else:
                    print('X', end=' ')
                    
        print()


def get_coordinates():
    """
    ask user to introduce x, y coordinates of cell and check if input is valid or not
    """
    coordinates = input("Write coordinates of cell: ").split()
    while len(coordinates) != 2:
        print("Introduce two variables")
        coordinates = input("Write coordinates of cell: ").split()
    return int(coordinates[0]), int(coordinates[1])


def all_opened(board):
    """
    check if all cells except for ones with bombs were opened
    """
    c = 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if (board[i][j]["open"]):
                c += 1
    state = c == HEIGHT * WIDTH - BOMB_NUM
    return state


def game_play(board):
    """
    while user has not lost or lost, offer 3 option of what to do (open/flag cell and have a hint)
    check if coordinates are valid and perform operation on them
    every step check if all bomb cells are flagged - it is a sign of win
    """
    global GAME_OVER
    GAME_OVER = False
    won = False

    while not (GAME_OVER or won):
        print_board(board)
        action = input("open - o, flag - f, hint - h: ")
        while action not in ['o', 'f', 'h']:
            print(f"There is no such option as {action}")
            action = input("open - o, flag - f, hint - h: ")

        if action == "h":
            hint(board)
        else:
            x, y = get_coordinates()
            while x >= HEIGHT or x < 0 or y < 0 or y > WIDTH:
                print(f"Coordinate x should be between 0 and {HEIGHT - 1} and y between 0 and {WIDTH - 1}")
                x, y = get_coordinates()

            if action == 'f':
                flag_cell(board, x, y)
            else:
                open_cell(board, x, y)

        print(f"There are {BOMB_NUM - len(FLAGGED)} flags left")

        if MINES == FLAGGED or all_opened(board):
            won = True

    
    if won:
        print_board(board)
        print("You won")
    else:
        print_board(board, lost=True)
        print("You lose")


def record_time(board):
    """
    record the time taken to win and return it
    """
    start = time.time()
    game_play(board)
    # subtract time when game started from time now to know difference(time spent in game)
    time_in_game = time.time() - start
    time_in_game = time.gmtime(time_in_game)
    return time.strftime('%H:%M:%S', time_in_game)


def create_board():
    """
    ask for level of difficulty
    create board(list two-dimensional where elements are dictionaries) according to level
    plant bombs
    return finished board
    """
    global MINES, WIDTH, HEIGHT, BOMB_NUM, level

    level = input("Choose level(beginner - b, intermediate - i, expert - e): ")
    while level not in ['b', 'i', 'e']:
        print(f"There is no such option as {level}")
        level = input("Choose level(beginner - b, intermediate - i, expert - e): ")
    if level == 'b':
        WIDTH = 9
        HEIGHT = 9
        BOMB_NUM = 10
    elif level == 'i':
        WIDTH = 16
        HEIGHT = 16
        BOMB_NUM = 40
    else:
        WIDTH = 30
        HEIGHT = 16
        BOMB_NUM = 99

    board = [[{'value': 0, 'open': False, 'flagged': False} for i in range(WIDTH)] for j in range(HEIGHT)]
    MINES = set()  # set of locations of bombs
    while len(MINES) < BOMB_NUM:
        x = random.randint(0, HEIGHT - 1)
        y = random.randint(0, WIDTH - 1)
        if (x, y) not in MINES:
            MINES.add((x, y))
            board[x][y]['value'] = '*'
            for a in range(x - 1, x + 2):
                for b in range(y - 1, y + 2):
                    if 0 <= a < HEIGHT and 0 <= b < WIDTH:  # check if cell is not out of board
                        if board[a][b]['value'] != '*':
                            board[a][b]['value'] += 1  # increase value of cell is there is a bomb around

    return board


def game():
    """
    ask for username
    perform all functions(the whole process of game)
    create or append file with data of winners
    """
    global FLAGGED, level

    name = input("What is your username: ")
    FLAGGED = set()  # set of locations of flagged cells
    board = create_board()
    time_spent = record_time(board)

    match level:
        case 'e':
            level = 'expert'
        case 'i':
            level = 'intermediate'
        case 'b':
            level = 'beginner'

    # think about it
    if FLAGGED == MINES or all_opened:
        with open('record.txt', 'a') as f:
            text = f"{name} {level} {time_spent}\n"
            f.write(text)


try:
    game() # run the function game which is responsible for execution of program
except BaseException:
    print('\nSomething unexpected happened, try to start game from the beginning')
