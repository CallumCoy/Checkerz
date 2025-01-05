from pprint import pprint


def main():

    boardLayout = initCheckerBoard(9, 9)
    playerBoard = initGame(2, 2, boardLayout)

    pprint(boardLayout)
    pprint(playerBoard)


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


if __name__ == "__main__":
    main()
