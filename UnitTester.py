import Checkers


def main():
    checksplitCoords()


def checksplitCoords():

    passCount = 0
    failCount = 0

    unitTests = [
        {"test": "a1 a1", "result": (False, [8, 0], [8, 0])},
        {"test": "A1 I6", "result": (False, [8, 0], [3, 8])},
        {"test": "a9 i9", "result": (False, [0,0], [0, 8])},
        {"test": "a1 a2 a3", "result": (False, [8,0], [7,0])},
        {"test": "9i 9a", "result": (True, [], [])},
        {"test": "a1a1", "result": (True, [], [])},
        {"test": "4 a2", "result": (True, [], [])},
        {"test": "*2 s1", "result": (True, [], [])},
        {"test": "a6 a0", "result": (True, [], [])},
        {"test": "1a 1a", "result": (True, [], [])},
        {"test": "a-1 a3", "result": (True, [], [])},
    ]

    print("Testing function splitCoords, it takes in a string, and returns a array continine a booleon value and 2 cooridnates.  Their are " +
          str(len(unitTests)) + " tests.")

    # Runs each unit test
    for unitTest in unitTests:
        # Runs the function and tracks the returned value
        funcResult = Checkers.splitCoords(unitTest["test"])

        # Tracks if it passed or failed
        if funcResult == unitTest["result"]:
            result = "Passed"
            passCount += 1
        else:
            result = "Failed"
            failCount += 1
        
        # Test results
        print("\nTest result: " + str(result) +
              "\nInputted: " + str(unitTest["test"]) +
              "\nThe function returned: " + str(funcResult) +
              "\nThe expected result was: " + str(unitTest["result"]) +
              "\n------------------------------------------------------------------")

    # Summerise function results
    print('\n*********************************************************************' +
          '\nTesting of splitCoords function complete.' +
          '\nOf the ' + str(len(unitTests)) + " tests " + str(passCount) + " test/s passed and " + str(failCount) + " test/s failed.")

    return failCount

if __name__ == "__main__":
    main()
