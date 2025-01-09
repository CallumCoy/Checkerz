import re
from statistics import mean
import time
import numpy

invalidChads = []
validAlphas = []
board = []
playerboard = []
player1 = ""
player2 = ""
acceptableChads = ["yes", "y", "a", "alpha", "ye", "yeah"]
acceptableAlpha = ["no", "n", "c", "chad", "nay", "nee"]
chadSoldiers = 0
alphaSoldiers = 0

chadCount = 2
alphaCount = 2


def main():

    global board, playerBoard, validAlphas, invalidChads

    board = initCheckerBoard(9, 9)
    playerBoard = initGame(chadCount, alphaCount)

    invalidChads, validAlphas = initialValidMoves(
        chadCount, alphaCount)

    printBoard(board)
    printBoard(playerBoard)
    printBoard(invalidChads)
    printBoard(validAlphas)
    print(int(True))

# TODO split up this section


def playGame():
    global player1 player2

    for i in range[4]:
        # Ask for players prefered type
        response = input("Are you a Chad or on an Alpha?")

        # Checks if they responded correctly
        if response in acceptableAlpha or response in acceptableChads:
            if response in acceptableAlpha:
                player1 = "Alpha"
                player2 = "Chad"
            else:
                player1 = "Chad"
                player2 = "Alpha"
            break

        # After 3 fails pretent to stop
        if i == 2:
            print("Whelp pleasure meeting you, but we're closing shop now.")
            time.sleep(60)  # Wait a minute
            print("Wait you're still here, I'll give you another chance then.")

        # After 4 fails pretend to pretend to stop
        elif i == 3:
            print(
                "You really messed it up this time we're closing up for real this time.")
            time.sleep(70)  # Wait 70 seconds
            print("no its real this time Sigma")
            time.sleep(3600)  # Wait an hour before closing
            exit()

    print("Ofcourse I should have known, you look like a true " +
          player1 + ".  and like a true " + player1 + " I will let you go first")

    curPlayer = player1

    while chadCount > 0 and alphaCount > 0:

        printBoard(playerBoard)

        coords = input("It is " + curPlayer +
                       "'s turn, please state which piece you would like to move and to where in the following format |A1 B2| (capitilization doe not matter): ")

        invalidCoords = True
        moving = "Move"

        while moving:
            while invalidCoords:
                invalidCoords, initialCoords, endCoords = splitCoords(coords)

                if invalidCoords:
                    coords = input("Invalid text, please try again: ")

            moving = movePiece(initialCoords, endCoords, moving)

            if moving != "Fail":
                renewValidMoves(initialCoords)
                renewValidMoves(endCoords)
            else:
                coords = input("This move is an invalid")

            if moving == "Taken":
                renewValidMoves(numpy.add(initialCoords, endCoords)/2)
                coords = input(
                    "We have taken out an enemy, you can try capturing another enemy or end your turn with 'end': ")
                if coords.lower() == "end":
                    break

        if curPlayer == player1:
            curPlayer == player2
        else:
            curPlayer == player1


def splitCoords(coords):
    # Makes everything lowercase
    modifiedCoords = coords.lower()

    # Checks if the coords are in a valid format
    if not re.search("[0-9]+[a-z] [0-9]+[a-z]", modifiedCoords):
        print("Invalid input please try again.")
        return (True, [], [])

    # Seperates numbers from letters
    ycoords = re.findall("[0-9]+", modifiedCoords)-1
    alphabets = re.findall("[a-z]+", modifiedCoords)

    # Extra processing for letter to number
    xcoords = [(ord(letter)-ord("a")) for letter in alphabets]

    # combine into coordinates
    initialCoords = [xcoords[0], ycoords[0]]
    endCoords = [xcoords[1], ycoords[1]]

    return (False, initialCoords, endCoords)


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

# TODO Comment up this function


def initGame(chadRows, alphaRows):

    # Populates the board chips based upon the requested rows
    # Errors out if invalid inputs
    if chadRows+alphaRows >= len(board) or chadRows < 1 or alphaRows < 1:
        return ([])

    global chadSoldiers, alphaSoldiers

    playBoard = []
    count = 0

    for row in board:

        checkerCount = 0
        playrow = []

        # Sets tha character that will fill the slots as the squares are processed
        if count < chadRows:
            inputCar = "c"
        elif count < len(board) - alphaRows:
            inputCar = ""
        else:
            inputCar = "a"

        for square in row:
            # Only white squares are valid for differnt charaters
            if square == "w":
                checkerCount += 1
                playrow.append(inputCar)
            else:
                playrow.append("")
            continue

        # Adds the pices so the game knows how many pieces are in play
        if inputCar == "c":
            chadSoldiers = + checkerCount
        else:
            alphaSoldiers = + checkerCount

        playBoard.append(playrow)
        count = count + 1
        continue

    return (playBoard)


def initialValidMoves(chadCount, alphaCount):
    # Makes two arrays that tracks valid moves for either side
    global validChads, validAlphas

    validChads = [[0 for _ in row] for row in board]
    validAlphas = [[0 for _ in row] for row in board]

    chadFrontline = chadCount
    alphaFrontline = len(board)-(alphaCount+1)

    # Goes through the spaces infront of the chads checker pieces, acknowledging white spaces as the only valid space
    for col in range(len(board[chadFrontline])):
        if board[chadFrontline][col] == "w":
            validChads[chadFrontline][col] = 1
        continue

    # Goes through the spaces infront of the alpha checker pieces, acknowledging white spaces as the only valid space
    for col in range(len(board[alphaFrontline])):
        if board[alphaFrontline][col] == "w":
            validAlphas[alphaFrontline][col] = 1
        continue

    return (validChads, validAlphas)


def renewValidMoves(squareToCheck):
    global invalidChads, validAlphas

    # only need to check withing 2 squares of the changed squares
    NormalMoves = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
    TakingMoves = [[2, 2], [-2, 2], [-2, -2], [2, -2]]

    validChadMove = False
    validAlphaMove = False

    # sets up basic moves
    MovingCoords = numpy.add(squareToCheck, NormalMoves)

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
    invalidChads[MovingCoords[0], MovingCoords[1]] = int(validChadMove)
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

# TODO enforce take only moves


def movePiece(initialCoords, endcoords, moveType):

    global playerBoard, chadSoldiers, alphaSoldiers

    player = playerBoard[initialCoords[0], initialCoords[1]]

    #  Check if it is a valid move
    if not isValidMove(initialCoords, endcoords):
        return "Fail"  # Move was invalid request new move

    # Kings the corrisponding pieces
    if endcoords[1] == 0 and player == "a":
        player = "A"
    elif endcoords[1] == len(playerBoard)-1 and player == "c":
        player = "C"

    # Clears old space and moves the piece
    playerBoard[initialCoords[0], initialCoords[1]] = ""
    playerBoard[endcoords[0], endcoords[1]] = player

    # Checks if it was a taking move if so remove taken piece and send request for next turn.
    if abs(initialCoords[0]-endcoords[0]) == 2:
        takenSpot = numpy.add(initialCoords, endcoords)/2
        # Could set to "x" to prevent backpeddling
        playerBoard[takenSpot[0], takenSpot[1]] = ""

        # adjust score after a take
        if player.lower() == "c":
            alphaSoldiers = - 1
        else:
            chadSoldiers = -1

        return "Taken"
    else:
        return ""


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
        for element in row:
            editedRow.append(element)

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
