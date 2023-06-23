### Minesweeper

## Task
Write game minesweeper. The aim of game is to flag all bombs on map.
User has to open cells and in cell stores information about how many bombs are around(in surrounding 8 cells).
User loses by opening cell with bomb inside.
User can flag cell in which he/she thinks the bomb is.

User wins if:
- all cells without bomb were opened;
- all bombs were flagged.

# Console version
Program asks user for name and level (different size of board and number of bombs).
There are 3 options for user: open cell, flag cell or ask for hint.
Hint marks random cell with bomb. Their amount is limited.
Game records are stored in txt file in format: name - game level - time spent.
# GUI version
Window with 9x9 board of cells introduced to user.
Left click on cell opens it.
Right click marks it as flagged.
In menu user can restart game.
In the end of game, user ger message if she/he won or lost.
Bomb is marked green, if user flagged it correctly.
Bomb is marked red, if user did not flag it.
Cell without bomb is marked red if user flagged it.