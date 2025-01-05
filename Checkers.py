from pprint import pprint
from statistics import mean


def main():
    chadCount = 2
    alphaCount = 2

    boardLayout = initCheckerBoard(9, 9)
    playerBoard = initGame(chadCount, alphaCount, boardLayout)
    validChads, validAlphas = initialValidMoves(
        chadCount, alphaCount, boardLayout)

    printBoard(boardLayout)
    printBoard(playerBoard)
    printBoard(validChads)
    printBoard(validAlphas)


def initCheckerBoard(xMax, yMax):
    # Makes a basic checker board using the specified diemensions
    board = []

    for y in range(yMax):
        curRow = []
        for x in range(xMax):

            # Alternates between square colors, using the the row # to offset every other row.
            if (x+y) % 2:
                curRow.append("b")
            else:
                curRow.append("w")
            continue

        # Inputs the new row into the board
        board.append(curRow)

    return (board)


def initGame(chadRows, alphaRows, board):

    # Populates the board chips based upon the requested rows
    # Errors out if invalid inputs
    if chadRows+alphaRows >= len(board) or chadRows < 1 or alphaRows < 1:
        return (SystemError)

    playBoard = []
    count = 0

    for row in board:

        playrow = []

        if count < chadRows:
            inputCar = "c"
        elif count < len(board) - alphaRows:
            inputCar = ""
        else:
            inputCar = "a"

        for square in row:
            if square == "w":
                playrow.append(inputCar)
            else:
                playrow.append("")
            continue

        playBoard.append(playrow)
        count = count + 1
        continue

    return (playBoard)


def initialValidMoves(chadCount, alphaCount, board):
    # Makes two arrays that tracks valid moves for either side
    validChads = [[0 for _ in row] for row in board]
    validAlpha = [[0 for _ in row] for row in board]

    chadFrontline = chadCount
    alphaFrontline = len(board)-(alphaCount+1)

    for col in range(len(board[chadFrontline])):
        if board[chadFrontline][col] == "w":
            validChads[chadFrontline][col] = 1
        continue

    for col in range(len(board[alphaFrontline])):
        if board[alphaFrontline][col] == "w":
            validAlpha[alphaFrontline][col] = 1
        continue

    return (validChads, validAlpha)


def isValidMove(initialCoords, endCoords, board):

    initialXCoord = initialCoords["x"]
    initialYCoords = initialCoords["y"]
    endXCoords = endCoords["x"]
    endYCoords = endCoords["y"]

    # sees if the initial square is valid
    pieceType = board[initialXCoord, initialYCoords]

    try:
        # Is there a piece on the initial coords
        if (pieceType == ""):
            return False
        # Is there a piece on the target coord, also sees if the end spot exists on the board
        elif (board[endXCoords, endYCoords] != ""):
            return False
        #  Is the initial space a white square
        elif (initialXCoord + initialYCoords) % 2 - 1:
            return False
        # Is the end space a white square
        elif (endXCoords+endYCoords) % 2 - 1:
            return False
        # Are Alpha pieces moving up
        elif (pieceType == "a") and (initialYCoords <= endYCoords):
            return False
        # Are the Chad pieces moving down
        elif (pieceType == "c") and (initialYCoords >= endCoords):
            return False
        # Is it moving within the 2 spaces limit
        elif abs(initialYCoords - endCoords) > 2 & abs(initialXCoord - endXCoords) > 2:
            return False
        # Is it moving diagnolly
        elif abs(initialYCoords - endCoords) != abs(initialXCoord - endXCoords):
            return False
        # Is it jumping a piece
        elif abs(initialYCoords - endCoords) == 2 and not ((board[mean(initialXCoord, endXCoords), mean(initialYCoords, endYCoords)]).lower == (pieceType).lower):
            return False
    except IndexError:
        return False

    return (True)

def printBoard(board):
    lines = ["\n|\t"] 
    
    for row in board:
         # Convert each element to string, using a blank space for empty cells(None)
        line = '\t|\t'.join(str(cell) if cell is not None else '\t' for cell in row)
        lines.append(line)
        
        # Join all lines into a single string with newline characters separating rows
    print('\n|\t'.join(lines))

if __name__ == "__main__":
    main()
