from statistics import mean
import numpy

validChads = []
validAlpha = []
board = []
playerboard = []

chadCount = 2
alphaCount = 2


def main():

    global board, playerBoard, validAlphas, validChads

    board = initCheckerBoard(9, 9)
    playerBoard = initGame(chadCount, alphaCount)

    validChads, validAlphas = initialValidMoves(
        chadCount, alphaCount)

    printBoard(board)
    printBoard(playerBoard)
    printBoard(validChads)
    printBoard(validAlphas)
    print(int(True))


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


def initGame(chadRows, alphaRows):

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


def initialValidMoves(chadCount, alphaCount):
    # Makes two arrays that tracks valid moves for either side
    validChads = [[0 for _ in row] for row in board]
    validAlpha = [[0 for _ in row] for row in board]

    chadFrontline = chadCount
    alphaFrontline = len(board)-(alphaCount+1)

    print(board)

    for col in range(len(board[chadFrontline])):
        if board[chadFrontline][col] == "w":
            validChads[chadFrontline][col] = 1
        continue

    for col in range(len(board[alphaFrontline])):
        if board[alphaFrontline][col] == "w":
            validAlpha[alphaFrontline][col] = 1
        continue

    return (validChads, validAlpha)


def renewValidMoves(squareToCheck):
    global validChads, validAlphas

    # only need to check withing 2 squares of the changed squares
    NormalMoves = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
    TakingMoves = [[2, 2], [-2, 2], [-2, -2], [2, -2]]

    validChadMove = False
    validAlphaMove = False

    # Looks at surrounding pieces for possible moves
    for square in MovingCoords:
        # If both teams can move there we don't need to move there
        if validAlphaMove and validChadMove:
            break

        # Catches and out of bounds moves we may try
        try:
            if board[square[0], square[1]] == "":
                continue
            elif board[square[0], square[1]] == "C":
                validChadMove = True
            elif board[square[0], square[1]] == "A":
                validAlphaMove = True
            elif board[square[0], square[1]] == "c" and square[1] < squareToCheck[1]:
                validChadMove = True
            elif board[square[0], square[1]] == "a" and square[1] > squareToCheck[1]:
                validAlphaMove = True
        except IndexError:
            continue

    # Changes to taking moves
    MovingCoords = numpy.add(squareToCheck, TakingMoves)
    middleSpot = numpy.divide(numpy.add(MovingCoords, squareToCheck), 2)

    # Looking at surrounding squares
    for square in MovingCoords:
        # If both sides can move there no need to do so
        if validAlphaMove and validChadMove:
            break

        # Catches any out of bounds movements we may check
        try:
            if board[square[0], square[1]] == "":
                continue
            elif board[square[0], square[1]] == "C" and board[middleSpot[0], middleSpot[1]].lower() == "a":
                validChadMove = True
            elif board[square[0], square[1]] == "A" and board[middleSpot[0], middleSpot[1]].lower() == "c":
                validAlphaMove = True
            elif board[square[0], square[1]] == "c" and square[1] < squareToCheck[1] and board[middleSpot[0], middleSpot[1]].lower() == "a":
                validChadMove = True
            elif board[square[0], square[1]] == "a" and square[1] > squareToCheck[1] and board[middleSpot[0], middleSpot[1]].lower() == "c":
                validAlphaMove = True
        except IndexError:
            continue

    # Updates the square if we can move there
    validAlphas[MovingCoords[0], MovingCoords[1]] = int(validAlphaMove)
    validChads[MovingCoords[0], MovingCoords[1]] = int(validChadMove)
    return


# Old code, may or may not use
'''
def pieceValidMoves(initialCoords, pieceType, board):

    if pieceType != pieceType.lower():
        movements = [[1, 1], [-1, 1], [-1, -1],
            [1, -1], [2, 2], [-2, 2], [-2, -2], [2, -2]]
    elif pieceType == "c":
        movements = [[1, -1], [-1, -1], [2, -2], [-2, -2]]
    elif pieceType == "a":
        movements = [[1, 1], [-1, 1], [2, 2], [-2, 2]]
    else:
        return []

    return [isValidMoveQuick(initialCoords,movements,pieceType,board)]


def isValidMoveQuick(initialCoords, movement, pieceType, board):

    validmoves = []

    for coords in movement:

        # Checks if it's in Range
        try:
            targetCoords = numpy.add(initialCoords,coords)

            # Checks basic moves
            if (abs(coords[0]) == 1):
                    # If square is empty it is add it to the valid move list
                    if board(targetCoords) == "":
                        validmoves.append([targetCoords])
            
            # Check taking moves 
            if (abs(coords[0]) == 2):
                # Gets the middle coords
                middleCoords = numpy.divide(numpy.add(initialCoords, targetCoords),2)

                #Is their a valid piece between these pieces
                if board[middleCoords[0],middleCoords[1]].lower() != pieceType.lower() and board[middleCoords[0],middleCoords[1]] != "":
                    validmoves.append(targetCoords)
                    
                    nextMoves = []

                    # Piece can keep taking pieces, so we extract the taking moves.  May remove in future in aid of taking one pieces at a time
                    for move in movement:
                        if abs(move[0]) == 2:
                            nextMoves.append(move)
                    
                    validmoves.append(isValidMoveQuick(targetCoords, nextMoves, board))
             
        except IndexError:
            continue

                    
'''


def isValidMove(initialCoords, endCoords):

    initialXCoord = initialCoords[0]
    initialYCoords = initialCoords[1]
    endXCoords = endCoords[0]
    endYCoords = endCoords[1]

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


def printBoard(inputtedBoard):
    lines = ["\n|\t"]

    # index elements
    count = len(inputtedBoard)
    xIndex = [chr(val+97) for val in range(len(inputtedBoard[0]))]


    for row in inputtedBoard:
        # Place yIndex at the front of each line.
        editedRow = [str(count)]
        for element in row: editedRow.append(element)
        
        # Convert each element to string, using a blank space for empty cells(None).
        line = '\t|\t'.join(
            str(cell) if cell is not None else '\t' for cell in editedRow)
        lines.append(line)

        count -= 1

    # Adds x index to the table.
    line = '\t|\t' + '\t|\t'.join(
        str(cell) if cell is not None else '\t' for cell in xIndex)
    lines.append(line)

    # Join all lines into a single string with newline characters separating rows.
    print('\n|\t'.join(lines))


if __name__ == "__main__":
    main()
