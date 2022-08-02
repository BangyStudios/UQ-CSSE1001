"""
CSSE1001 Assignment 1
Semester 2, 2020
"""

from a1_support import *

# Fill these in with your details
__author__ = "James Chen-Smith s4648132"
__email__ = "james@icbix.com"
__date__ = "2020/08/18"

# Write your code here (i.e. functions)

debug = False    #Debug/cheat mode. True: Increase verbosity, print chosen word. False: Production.
autoquit = False #For debugging, terminates program immediately, loads methods into RAM.

def getWord(gameMode):
    """
    Returns a random word from the Word Index using the a1_support function.
    Usage: getWord(gameMode)
    Dependencies: a1_support.py
    """
    wordIndex = []  #Basically creates an array for the words in the file.
    wordTuple = load_words(gameMode) #Uses support module "load_words" to load words into RAM.
    wordIndex = list(wordTuple) #Transfers words from tuple to array.
    randIndex = random.randrange(0, len(wordTuple)) #Pseudo-randomly selects a word position from word index.
    wordSelected = wordTuple[randIndex] #Relates word position to word.
    wordLength = len(wordSelected)   #Gets the length (number of characters) of the word.
    
    if debug == True:   #Conditional verbosity for debugging.
        print(len(wordTuple),"words loaded...")
        print("Word",randIndex,"selected...")
        print("Word ",randIndex," selected is '",wordSelected,"'",sep="")
        print("Word ",randIndex," selected is ",wordLength," characters long...",sep="")

    return wordSelected, wordLength

def printWall(wordLength):
    """
    Prints a horizontal wall (--------...)
    Usage: printWall(wordLength)
    Dependencies: null
    """
    print((9 + 4 * wordLength) * WALL_HORIZONTAL) #Wall equation 4 times wordLength + 9 extra (-)

def printTitle(wordLength):
    """
    Prints the title of score grid (...| 1 | 2 | 3 |...)
    Usage: printTitle(wordLength)
    Dependencies: null
    """
    titleLine = []
    titleLine.append("       | ") #TODO: Fix amount of spaces here after testing.
    x = 1
    while (x <= wordLength):
        if (x != wordLength):
            titleLine.append(str(x)) #Appends a set of natural numbers x (1, 2, 3) to titleLine.
            titleLine.append(" | ") #Appends horizontal spacers (| | |...) to titleLine.
        else:
            titleLine.append(str(x))
            titleLine.append(" |")
        x = x + 1
    print("".join(titleLine))   #Prints the combined titleLine.
    printWall(wordLength)   #Prints initial horizontal wall.

def getVoid(wordLength, guessRound):
    """
    Gets the range and size of the parts of the text required to solve for each round given the word length.
    Please note void is denoted by "*" in "--***--"
    Dependencies: null
    """
    guessRound = guessRound - 1    #Due to the nature of tuples, round 1 is mapped to position 0.
    if (wordLength == 6):   #If the wordLength is x.
        voidSet = GUESS_INDEX_TUPLE[0]  #Select void (--***--) set from GUESS_INDEX_TUPLE position 0.
        voidRange = voidSet[(guessRound)]   #Selects position guessRound in GUESS_INDEX_TUPLE[0].
    elif (wordLength == 7): #Else if wordLength is x. Same process as before.
        voidSet = GUESS_INDEX_TUPLE[1]
        voidRange = voidSet[(guessRound)]
    elif (wordLength == 8): #Else if wordLength is x. Same process as before.
        voidSet = GUESS_INDEX_TUPLE[2]
        voidRange = voidSet[(guessRound)]
    elif (wordLength == 9): #Else if wordLength is x. Same process as before.
        voidSet = GUESS_INDEX_TUPLE[3]
        voidRange = voidSet[(guessRound)]
    else:
        quit(code="getVoid() tuple mismatch.")  #Else code is broken and i'm completely retarded and will fail.
    voidRange = tuple([1+x for x in voidRange]) #Adds 1 to the elements of the tuple such that 0 becomes 1
    (voidRangeBegin, voidRangeEnd) = voidRange
    voidSize = (voidRange[1] - voidRange[0]) + 1    #Computes voidSize.
    return voidRangeBegin, voidRangeEnd, voidSize

def printDataLine(wordLength, guessRound, score):
    """
    Returns a line of scored by printing guess matrix and querying global guessScores.
    Usage: printDataLine(wordLength, guessRound, score)
    Dependencies: null
    """
    voidRangeBegin, voidRangeEnd, voidSize = getVoid(wordLength, guessRound)
    line = []
    line.append("Guess ")
    line.append(str(guessRound))
    line.append("| ")
    x = 1
    while (x <= wordLength):
        if (x < wordLength):
            if x in range(voidRangeBegin, (voidRangeEnd + 1)): #If character position is in range of void (*).
                line.append("*")    #Appends * to line.
            else:
                line.append("-")    #If character position is not in range of void (- not *).
            line.append(" | ")  #Appends - to line.
        else:
            if x in range(voidRangeBegin, (voidRangeEnd + 1)):
                line.append("*")
            else:
                line.append("-")
            line.append(" |") #Space after | eliminated for automated marking system.
        x = x + 1
    if (score == "No" or guessRound == wordLength):
        line.append("")
    else:
        line.append("   ")
        line.append(str(score)) #Appends score to end of line.
        if (guessRound < wordLength):
            line.append(" Points")
    print("".join(line))    #Prints completed line.

def printData(guessRound):
    """
    Returns a matrix of all scores up to global guessRound by using printDataLine().
    Usage: printData(guessRound)
    Dependencies: null
    """
    printTitle(wordLength)
    x = 1
    while (x <= guessRound):
        printDataLine(wordLength, x, guessScores[x])
        printWall(wordLength) #Prints horizontal wall.
        x = x + 1

def recordScore(guessRound, score):
    """
    Updates score of each round when called.
    Usage: recordScore(guessRound, score)
    Dependencies: null
    """
    global guessScores #Loads global variable guessScores.
    guessScores[(guessRound)] = score #Updates guessScores array based on the score given to function.

def computeScore(guessString, guessRound):
    """
    Computes and returns score for user guess by comparing to wordSelected.
    Usage: computeScore(guessString, guessRound)
    Dependencies: null
    """
    global wordSelected #Loads global variable wordSelected.
    voidRangeBegin, voidRangeEnd, voidSize = getVoid(wordLength, guessRound)
    wordVoid = wordSelected[(voidRangeBegin - 1):(voidRangeEnd)]    #Gets only letters of wordSelected present in the void (***)
    wordList = []   
    for char in wordVoid:
        wordList.append(char)   #Appends every character in wordVoid to array wordList.
    guessChars = []
    for char in guessString:
        guessChars.append(char) #Appends every character in guessString to array guessChar.
    score = 0
    pos = 0
    for pos in range(0, voidSize):
        if (wordList[pos] == guessChars[pos]):  #If character matches in same position.
            if (guessString[pos] in VOWELS):    #If character is a vowel.
                score = score + 14 #Add 14 points to score.
            else:   #Else if character is a consonant.
                score = score + 12 #Add 12 points to score.
        elif (guessChars[pos] in wordList): #If character matches in different position.
            score = score + 5  #Add 5 points to score.
        else:   #Else, does not match at all.
            score = score + 0  #Add 0 points to score.
    return score

def guess():
    """
    Top level user interaction loop up to the last guessRound.
    Usage: guess()
    Dependencies: null
    """
    global guessRound #Loads global variable guessRound.
    while (guessRound < wordLength):
        voidRangeBegin, voidRangeEnd, voidSize = getVoid(wordLength, guessRound)
        maxAllowedChars = (voidRangeEnd - voidRangeBegin + 1)
        prompt = []
        prompt.append("Now enter Guess ")
        prompt.append(str(guessRound))
        prompt.append(": ")
        prompt = "".join(prompt)
        while True:
            guess = input(prompt)
            if (len(guess) != maxAllowedChars):   #Input validation ensuring correct character count.
                continue
            else:
                break
        guessString = guess.lower()
        score = computeScore(guessString, guessRound)   #Computes score using computeScore.
        recordScore(guessRound, score)  #Records score using recordScore.
        guessRound = guessRound + 1
        printData(guessRound)   #Prints matrix up to guessRound.
    finalGuess()    #Runs interaction loop for last guessRound.

def finalGuess():
    """
    Top level user interaction loop for the last guessRound.
    Usage: finalGuess()
    Dependencies: null
    """
    global wordSelected #Loads global variable wordSelected.
    while (guessRound == wordLength):
        voidRangeBegin, voidRangeEnd, voidSize = getVoid(wordLength, guessRound)
        maxAllowedChars = (voidRangeEnd - voidRangeBegin + 1)
        guess = input("Now enter your final guess. i.e. guess the whole word: ")
        if (len(guess) != maxAllowedChars):   #Input validation ensuring correct character count.
            print("ILLEGAL INPUT!","Please enter exactly",maxAllowedChars,"characters!")
        elif (("".join([num for num in guess if num.isdigit()])) != ""):    #Input validation excluding numbers.
            print("ILLEGAL INPUT!","Please enter only alphabetical characters!")
        else:
            guessString = guess.lower()
            if (guessString == wordSelected): #If final guess is correct.
                recordScore(guessRound, "You Win!")
                print("You have guessed the word correctly. Congratulations.")
                break
            else: #Else if final guess is wrong.
                print('Your guess was wrong. The correct word was ','"', wordSelected, '"',sep="")
                break
        break

def startGame(gameMode):
    """
    Gets word and loads all necessary variables into RAM for game.
    Usage: startGame(gameMode)
    Dependencies: a1_support.py
    """
    global guessScores, guessRound, wordSelected, wordLength    #Loads all necessary global variables.
    guessRound = 1 #Sets guessRound to 1 initially.
    wordSelected, wordLength = getWord(gameMode)    #Gets word and length using getWord.
    guessScores = ["No"] * (wordLength)    #Creates empty array of length wordLength to store scores.
    guessScores.append("")
    print("Now try and guess the word, step by step!!")
    printData(guessRound)   #Prints data for first guess matrix.
    guess() #Executes guess function.
    
"""
Below this section are the implementations required by task outline but are unnecessary to the operation of game.
Please feel free to delete everything below this line if you hate looking at it.
"""

def select_word_at_random(word_select):
    """
    Returns a random word from the Word Index using the a1_support function.
    Usage: getWord(gameMode)
    Dependencies: a1_support.py
    """
    if word_select == "FIXED" or word_select == "ARBITRARY":
        wordIndex = []
        wordTuple = load_words(word_select)
        wordIndex = list(wordTuple)
        randIndex = random.randrange(0, len(wordTuple))
        wordSelected = wordTuple[randIndex]
        return wordSelected
    else:
        return None

def print_wall(word_length):
    """
    Prints a horizontal wall (--------...)
    Usage: printWall(wordLength)
    Dependencies: null
    """
    print((9 + 4 * word_length) * WALL_HORIZONTAL)

def create_head_line(word_length):
    """
    Prints the title of score grid (...| 1 | 2 | 3 |...)
    Usage: printTitle(wordLength)
    Dependencies: null
    """
    head_line = []
    head_line.append("       | ") #TODO: Fix amount of spaces here after testing.
    x = 1
    while (x <= word_length):
        if (x != word_length):
            head_line.append(str(x)) #Appends a set of natural numbers x (1, 2, 3) to titleLine.
            head_line.append(" | ") #Appends horizontal spacers (| | |...) to titleLine.
        else:
            head_line.append(str(x))
            head_line.append(" |")
        x = x + 1
    print("".join(head_line))   #Prints the combined titleLine.

def create_guess_line(guess_no, word_length):
    """
    Returns a line of scored by printing line guess_no of guess matrix.
    Usage: create_guess_line(guess_no, word_length)
    Dependencies: null
    """
    guess_no = guess_no - 1
    if (word_length == 6):
        voidSet = GUESS_INDEX_TUPLE[0]
        voidRange = voidSet[(guess_no)]
    elif (word_length == 7):
        voidSet = GUESS_INDEX_TUPLE[1]
        voidRange = voidSet[(guess_no)]
    elif (word_length == 8):
        voidSet = GUESS_INDEX_TUPLE[2]
        voidRange = voidSet[(guess_no)]
    elif (word_length == 9):
        voidSet = GUESS_INDEX_TUPLE[3]
        voidRange = voidSet[(guess_no)]
    voidRange = tuple([1 + x for x in voidRange])
    (voidRangeBegin, voidRangeEnd) = voidRange
    voidSize = (voidRange[1] - voidRange[0]) + 1

    guess_no = guess_no + 1 
    line = []
    line.append("Guess ")
    line.append(str(guess_no))
    line.append("|")
    x = 1
    while (x <= word_length):
        if x in range(voidRangeBegin, (voidRangeEnd + 1)):
            line.append(" * ")
        else:
            line.append(" - ")
        line.append("|")
        x = x + 1
    return("".join(line))

def display_guess_matrix(guess_no, word_length, scores):
    """
    Returns a matrix of all scores up to global guessRound by using printDataLine().
    Usage: printData(guessRound)
    Dependencies: null
    """
    create_head_line(word_length)
    print_wall(word_length)
    x = 1
    while (x <= guess_no):
        if (x != guess_no):
            toPrint = []
            toPrint.append(create_guess_line(x, word_length))
            toPrint.append("   ") #Adjust spaces to match marking script requirements.
            toPrint.append(str(scores[x - 1]))
            toPrint.append(" Points")
            print("".join(toPrint))
            print_wall(word_length) #Prints horizontal wall.
        else:
            print(create_guess_line(x, word_length))
            print_wall(word_length) #Prints horizontal wall.
        x = x + 1

def compute_value_for_guess(word, start_index, end_index, guess):
    """
    Computes score for user guess by comparing to word.
    Usage: compute_value_for_guess(word, start_index, end_index, guess)
    Dependencies: null
    """
    start_index = start_index + 1
    end_index = end_index + 1
    voidRangeBegin, voidRangeEnd = (start_index), (end_index)
    voidSize = (voidRangeEnd - voidRangeBegin) + 1
    wordVoid = word[(voidRangeBegin - 1):(voidRangeEnd)]
    wordList = []
    if (len(guess) != voidSize):
        quitCode = ("ILLEGAL INPUT!","Please enter exactly",voidSize,"characters!")
        quit(code=quitCode)
    elif (("".join([num for num in guess if num.isdigit()])) != ""):
        quitCode = ("ILLEGAL INPUT!","Please enter only alphabetical characters!")
        quit(code=quitCode)
    else:
        for char in wordVoid:
            wordList.append(char)
        guessChars = []
        for char in guess:
            guessChars.append(char)
        score = 0
        pos = 0
        for pos in range(0, voidSize):
            if (wordList[pos] == guessChars[pos]):
                if (guess[pos] in VOWELS):
                    score = score + 14
                else:
                    score = score + 12
            elif (guess[pos] in wordList):
                score = score + 5
            else:
                score = score + 0
    return score

"""
Above this section are the implementations required by task outline but are unnecessary to the operation of game.
Please feel free to delete everything above this line if you hate looking at it.
"""

def main():
    """
    Handles top-level interaction with user.
    """
    # Write the code for your main function here
    print(WELCOME)   #Prints initial menu.
    gameMenu = input(INPUT_ACTION)
#Gets user's desired option.
    while True:
        if gameMenu == "s":
            while True:
                getMode = input("Do you want a 'FIXED' or 'ARBITRARY' length word?: ")
                if getMode == "ARBITRARY":
                    gameMode = "ARBITRARY"  #Sets global gameMode to ARBITRARY.
                    startGame(gameMode) #Starts the Game.
                    break
                elif getMode == "FIXED":
                    gameMode = "FIXED"   #Sets global gameMode to FIXED.
                    startGame(gameMode)  #Starts the Game.
                    break
                else:
                    break
            break
        elif gameMenu == "h":
            print(HELP)
            while True:
                getMode = input("Do you want a 'FIXED' or 'ARBITRARY' length word?: ")
                if getMode == "ARBITRARY":
                    gameMode = "ARBITRARY"  #Sets global gameMode to ARBITRARY.
                    startGame(gameMode) #Starts the Game.
                    break
                elif getMode == "FIXED":
                    gameMode = "FIXED"   #Sets global gameMode to FIXED.
                    startGame(gameMode)  #Starts the Game.
                    break
                else:
                    break
            break
        elif gameMenu == "q":
            break  #Exits game, duh.
        else:
            print(INVALID)   #Alerts user regarding illegal input.
            gameMenu = input(INPUT_ACTION)  #Gets user's desired option.

if __name__ == "__main__":
    """
    Autoruns
    """
    if autoquit == True:
        print("Get a life :)")
        quit()
    else:
        main()
