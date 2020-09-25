from bangtal import *
import random
import time
import os
import sys

# Game Options
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

### Global Variables
userSelectImage = 'football' # Default, 없으면 Error
puzzles = [[None, None, None], [None, None, None], [None, None, None]]
whiteRow = None
whiteCol = None
WhitePuzzleImage = 'white.png'
startTime = None
endTime = None

rank = [sys.maxsize, sys.maxsize, sys.maxsize]
dir = os.path.dirname(os.path.abspath(__file__)) + "\\rank.txt"
f = open(dir, 'r')
for i in range(3):
    line = f.readline()
    rank[i] = float(line)
f.close()


###
### Select Scene
###
selectScene = Scene('선택 화면', 'select_background.png')
backgroundObject = Object('select_background.png')
backgroundObject.locate(selectScene, 0, 0)
backgroundObject.show()

# 선택 화면에서 이미지 외 다른 것 클릭 시
def backgroundObject_onMouseAction(x, y, action):
    pass
    #endGame()
backgroundObject.onMouseAction = backgroundObject_onMouseAction

# 선택할 이미지들
class Choice(Object):
    def __init__(self, file):
        super().__init__(file)
        self.image = file
        
    def onMouseAction(self, x, y, action):
        global userSelectImage, puzzles, startTime
        userSelectImage = self.image[:-4] # delete .png
        print('userSelectImage : ', userSelectImage)
        puzzleScene.setImage(userSelectImage + '.png')

        createPuzzle()
        
        puzzleScene.enter()
        startTime = time.time()

choices = [Choice('football.png'), Choice('mickey.png'), Choice('minions.png')]
for i in range(len(choices)):
    choices[i].locate(selectScene, 100 + i * 375, 300)
    choices[i].setScale(0.25)
    choices[i].show()


###
### Puzzle Scene
###
puzzleScene = Scene('맞춰봐', userSelectImage + '.png')

# White BackGround (600*600)
puzzleBackground = Object('puzzle_background2.png')
puzzleBackground.locate(puzzleScene, 340 - 2, 60 - 2)
puzzleBackground.show()

# Buttons
restartButton = Object('restart.png')
restartButton.locate(puzzleScene, 120, 360)
restartButton.setScale(1.3)
restartButton.show()

def restartButton_onMouseAction(x, y, action):
    global puzzles, whiteRow, whiteCol
    puzzles = [[None, None, None], [None, None, None], [None, None, None]]
    whiteRow = None
    whiteCol = None
    selectScene.enter()
    restartButton.show()
    endButton.hide()
restartButton.onMouseAction = restartButton_onMouseAction

endButton = Object('end.png')
endButton.locate(puzzleScene, 120, 220)
endButton.setScale(1.3)
endButton.hide()
def endButton_onMouseAction(x, y, action):
    endGame()
endButton.onMouseAction = endButton_onMouseAction


class Puzzle(Object):
    def __init__(self, file, row, col):
        global userSelectImage
        super().__init__(file)
        self.image = file       # filenmae
        self.row = int(row)
        self.col = int(col)
        self.num = (self.row * 3) + self.col

    def locate(self, scene):
        super().locate(scene, 340 + (self.col * 200), 460 - (self.row * 200))

    def onMouseAction(self, x, y, action):
        print("Click -> image : " + self.image + "\nrow : ", self.row, ", col : ", self.col, ", num : ", self.num)

        # 빈칸 옆이라면
        if canMove(self.row, self.col):
            swapImage(self.row, self.col)
        
        checkPuzzle()

    def setImage(self, file):
        super().setImage(file)
        self.image = file

def canMove(row, col):
    global whiteRow, whiteCol
    x = [1, -1, 0, 0]
    y = [0, 0, 1, -1]
    
    for i in range(len(x)):
        newRow = row + x[i]
        newCol = col + y[i]
        if 0 <= newRow < 3 and 0 <= newCol < 3 and newRow == whiteRow and newCol == whiteCol:
            return True
    return False

def swapImage(row, col):
    global whiteRow, whiteCol, puzzles
    puzzles[whiteRow][whiteCol].setImage(puzzles[row][col].image)
    puzzles[row][col].setImage(WhitePuzzleImage)
    whiteRow = row
    whiteCol = col
    print('white row : ', whiteRow, ', col : ', whiteCol)

def createPuzzle():
    original = [
        [(0, 0), (0, 1), (0, 2)], 
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)]]

    arr = [
        [(0, 0), (0, 1), (0, 2)], 
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)]]

    isShaked = False
    while not isShaked:
        random.shuffle(arr)
        print('random 결과 : ', arr)

        for i in range(len(arr)):
            for j in range(len(arr[i])):
                for k in range(2):
                    if arr[i][j][k] != original[i][j][k]:
                        isShaked = True
                        break
                if isShaked:
                    break
            if isShaked:
                break

    # Create puzzles
    for i in range(len(puzzles)):
        for j in range(len(puzzles[i])):
            puzzles[i][j] = Puzzle(userSelectImage + '/' + userSelectImage + '-' + str(arr[i][j][0]) + '-' + str(arr[i][j][1]) + '.png', i, j)
            puzzles[i][j].locate(puzzleScene)
            puzzles[i][j].show()
    
    # Create blank in puzzle
    global whiteRow, whiteCol
    whiteRow = random.randrange(0, 3)
    whiteCol = random.randrange(0, 3)
    
    puzzles[whiteRow][whiteCol].setImage(WhitePuzzleImage)

def checkPuzzle():
    global puzzles

    isComplete = True
    
    for i in range(len(puzzles)):
        for j in range(len(puzzles[i])):
            if puzzles[i][j].image != WhitePuzzleImage:
                row = int(puzzles[i][j].image[-7])
                col = int(puzzles[i][j].image[-5])
                if row != puzzles[i][j].row or col != puzzles[i][j].col:
                    print("error in : ", i, " ", j)
                    isComplete = False
                    break
        if not isComplete:
            break

    if isComplete:
        completeTime = format(time.time() - startTime, ".2f")
        record(float(completeTime))
        restartButton.show()
        endButton.show()

def record(completeTime):
    global rank, dir
    msg = "성공 : " + str(completeTime) + "\n"

    if completeTime < rank[2]:
        rank[2] = completeTime
        rank.sort()
        num = None
        f = open(dir, 'w')
        for i in range(3):
            if float(rank[i]) == completeTime:
                num = i + 1
            f.write(str(rank[i]) + "\n")
        f.close
        msg += str(num) + "등 갱신!\n"

    for i in range(3):
        if float(rank[i]) != float(sys.maxsize):
            msg += str(i + 1) + "등 : " + str(rank[i]) + "\n"
    showMessage(msg)


showMessage('플레이할 이미지를 골라봐')
startGame(selectScene)
