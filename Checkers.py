import re
from statistics import mean
import time
import numpy

board = []
playerBoard = []
curPlayer = ""
player1 = ""
player2 = ""
acceptableChads = ["yes", "y", "a", "alpha", "ye", "yeah"]
acceptableAlphas = ["no", "n", "c", "chad", "nay", "nee"]
chadSoldiers = 0
alphaSoldiers = 0

chadCount = 2
alphaCount = 2


def main():

    global board, playerBoard

    board = initCheckerBoard(9, 9)
    playerBoard = initGame(chadCount, alphaCount)


    playGame()

# TODO split up this section


def playGame():
    global player1, player2, curPlayer

    for i in range(4):
        # Ask for players prefered type
        response = input("Are you a Chad or on an Alpha?")

        # Checks if they responded correctly
        if response in acceptableAlphas or response in acceptableChads:
            if response in acceptableAlphas:
                player1 = curPlayer = "Alpha"
                player2 = "Chad"
            else:
                player1 = curPlayer = "Chad"
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

    while chadSoldiers > 0 and alphaSoldiers > 0:

        # Prints the board and asks for the players move
        printBoard(playerBoard)
        coords = input("It is " + curPlayer +
                       "'s turn, please state which piece you would like to move and to where in the following format |A1 B2| (capitilization doe not matter): ")

        # Setting up some variables for the upcoming while loops
        moving = "Move"
        moveTaken = False

        # When Move = "end" the turn is other, otherwise continue on
        while moving.lower() != "end" and not moveTaken:
            # Keep trying to get a valid coord
            invalidCoords = True
            while invalidCoords:
                invalidCoords, initialCoords, endCoords = splitCoords(coords)

                if invalidCoords:
                    coords = input("Invalid text, please try again: ")

            # Actually implement the move
            moving = movePiece(initialCoords, endCoords, moving)

            # If move was successful update two of the locations, otherwise ask for valid coords
            if moving != "Fail":
                moveTaken = True
            else:
                coords = input(
                    "This move is invalid, please provide another two coordinates: ")

            # If the move took a unit update the missing spot, and ask for the next coords or if they end.
            if moving == "Taken":
                printBoard(playerBoard)
                coords = input(
                    "We have taken out an enemy, you can try capturing another enemy or end your turn with 'end': ")
                if coords.lower() == "end":
                    moving = "end"

        # Swaps the players
        if curPlayer == player1:
            curPlayer = player2
        else:
            curPlayer = player1


def splitCoords(coords):
    # Makes everything lowercase
    modifiedCoords = coords.lower()

    # Checks if the coords are in a valid format
    if not re.search("[a-i][1-9]+ [a-i][1-9]+", modifiedCoords):
        print("Invalid input please try again.")
        return (True, [], [])

    # Seperates numbers from letters
    ycoords = re.findall("[0-9]+", modifiedCoords)
    alphabets = re.findall("[a-z]", modifiedCoords)

    # Extra processing for letter to number
    xcoords = [(ord(letter)-ord("a")) for letter in alphabets]

    # combine into coordinates, array is backwards, and y is reversed
    initialCoords = [9-int(ycoords[0]), xcoords[0]]
    endCoords = [9-int(ycoords[1]), xcoords[1]]

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
            chadSoldiers += checkerCount
        elif inputCar == "a":
            alphaSoldiers += checkerCount

        playBoard.append(playrow)
        count = count + 1
        continue

    return (playBoard)

def movePiece(initialCoords, endcoords, moveType):

    global playerBoard, chadSoldiers, alphaSoldiers

    player = playerBoard[initialCoords[0]][initialCoords[1]]

    #  Check if it is a valid move
    if not isValidMove(initialCoords, endcoords) or (moveType == "Taken" and abs(initialCoords[0]-endcoords[0]) != 2):
        return "Fail"  # Move was invalid request new move

    # Kings the corrisponding pieces
    if endcoords[0] == 0 and player == "a":
        player = "A"
    elif endcoords[0] == len(playerBoard)-1 and player == "c":
        player = "C"

    # Clears old space and moves the piece
    playerBoard[initialCoords[0]][initialCoords[1]] = ""
    playerBoard[endcoords[0]][endcoords[1]] = player

    # Checks if it was a taking move if so remove taken piece and send request for next turn.
    if abs(initialCoords[0]-endcoords[0]) == 2:
        takenSpot = numpy.add(initialCoords, endcoords)/2
        # Could set to "x" to prevent backpeddling
        playerBoard[int(takenSpot[0])][int(takenSpot[1])] = ""

        # adjust score after a take
        if player.lower() == "c":
            alphaSoldiers -= 1
        else:
            chadSoldiers -= 1

        return "Taken"
    else:
        return "End"


def isValidMove(initialCoords, endCoords):

    initialXCoord = initialCoords[1]
    initialYCoords = initialCoords[0]
    endXCoords = endCoords[1]
    endYCoords = endCoords[0]

    # sees if the initial square is valid
    pieceType = playerBoard[initialYCoords][initialXCoord]
    apposingType = "c" if pieceType.lower() == "a" else "a"

    try:
        # Is there a piece on the initial coords
        if (pieceType.lower() != curPlayer[0].lower()):
            return False
        # Is there a piece on the target coord, also sees if the end spot exists on the board
        elif (playerBoard[endYCoords][endXCoords] != ""):
            return False
        #  Is the initial space a white square
        elif board[endYCoords][endXCoords] == "b":
            return False
        # Is the end space a white square
        elif board[endYCoords][endXCoords] == "b":
            return False
        # Are Alpha pieces moving up
        elif (pieceType == "a") and (initialYCoords <= endYCoords):
            return False
        # Are the Chad pieces moving down
        elif (pieceType == "c") and (initialYCoords >= endYCoords):
            return False
        # Is it moving within the 2 spaces limit
        elif abs(initialYCoords - endYCoords) > 2 & abs(initialXCoord - endXCoords) > 2:
            return False
        # Is it moving diagnollychad
        elif abs(initialYCoords - endYCoords) != abs(initialXCoord - endXCoords):
            return False
        # Is it jumping a piece
        elif abs(initialYCoords - endYCoords) == 2 and playerBoard[int((initialYCoords+endYCoords)/2)][int((initialXCoord+endXCoords)/2)].lower() != (apposingType).lower():
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
