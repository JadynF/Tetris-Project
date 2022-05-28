import pygame
import random
import pygame_widgets
from pygame_widgets.button import Button

pygame.init()
window = pygame.display.set_mode((710, 820))
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 26)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (100, 100, 255)
ORANGE = (255, 120, 0)
PURPLE = (255, 0, 255)

# map class
class Map:
    # initialize map with 2D matrix
    def __init__(self, map):
        self.map = map
        self.locked = []
	
    # draw the map onto the screen with the matrix
    def draw(self):
        for i in range(0, 20):
            for j in range(0, 10):
                pygame.draw.rect(window, self.map[i][j][0], (2 * j + 150 + j * 39, 2 * i + i * 39, 40, 40))
        for i in range(0, 10):
            pygame.draw.rect(window, (50, 50, 50), (i + 190 + 40 * i, 0, 1, 820))
        for i in range(0, 20):
            pygame.draw.rect(window, (50, 50, 50), (150, (i - 1) + 40 * i, 420, 1))
            
    # change the state and color of the block on the map
    def changeBlock(self, x, y, block, color, state):
        for i in range(0, 4):
            for j in range(0, 4):
                if block[i][j] == 1:
                    if x + j >= 0 and x + j < 10 and y + i >= 0 and y + i < 20:
                        self.map[y+i][x+j] = [color, state]
                    if state == 2 and y + i < 0:
                        global playing
                        playing = False

    # check if a row is full
    def checkRows(self):
        count = 0
        for i in range(0, 20):
            total = 0
            for j in range(0, 10):
                if self.map[i][j][1] == 2:
                    total += 1
            if total == 10:
                self.clearRow(i)
                count += 1
        return count
    
    # clear specefied row and shift everything above down
    def clearRow(self, rowNum):
        newLocked = []
        for i in range(0, 10):
            self.map[rowNum][i] = (BLACK, 0)
        for coord in self.locked:
            if coord[1] != rowNum:
                newLocked.append(coord)
        for i in reversed(range(0, rowNum)):
            for j in range(0, 10):
                if self.map[i][j][1] == 2:
                    curColor = self.map[i][j][0]
                    self.map[i][j] = [BLACK, 0]
                    self.map[i + 1][j] = [curColor, 2]
        for coord in newLocked:
            if coord[1] < rowNum:
                coord[1] += 1
                
        self.locked = newLocked
    
    def drawQueue(self, block, color, name):
        pygame.draw.rect(window, (255, 255, 255), (575, 70, 120, 250))
        for i in range(0, 4):
            for j in range(0, 4):
                if block[i][j] == 1:
                    if name == "Z" or name == "S" or name == "T":
                        pygame.draw.rect(window, color, (576 + 39 * j, 80 + 39 * i, 39, 39))
                    else:
                        pygame.draw.rect(window, color, (560 + 39 * j, 80 + 39 * i, 39, 39))
        
# shape class
class Shape:
    # each block
    blockL = (((0, 0, 0, 0),
               (0, 1, 0, 0),
			   (0, 1, 0, 0),
			   (0, 1, 1, 0)),
			  ((0, 0, 0, 0),
			   (0, 0, 0, 1),
			   (0, 1, 1, 1),
			   (0, 0, 0, 0)),
			  ((0, 1, 1, 0),
			   (0, 0, 1, 0),
			   (0, 0, 1, 0),
			   (0, 0, 0, 0)),
			  ((0, 0, 0, 0),
			   (1, 1, 1, 0),
			   (1, 0, 0, 0),
			   (0, 0, 0, 0)))
               
    blockT = (((0, 0, 0, 0),
               (1, 1, 1, 0),
               (0, 1, 0, 0),
               (0, 0, 0, 0)),
              ((0, 0, 0, 0),
               (0, 1, 0, 0),
               (0, 1, 1, 0),
               (0, 1, 0, 0)),
              ((0, 0, 0, 0),
               (0, 0, 1, 0),
               (0, 1, 1, 1),
               (0, 0, 0, 0)),
              ((0, 0, 1, 0),
               (0, 1, 1, 0),
               (0, 0, 1, 0),
               (0, 0, 0, 0)))
               
    blockJ = (((0, 0, 0, 0),
			   (0, 0, 1, 0),
			   (0, 0, 1, 0),
			   (0, 1, 1, 0)),
			  ((0, 0, 0, 0),
			   (0, 1, 1, 1),
			   (0, 0, 0, 1),
			   (0, 0, 0, 0)),
			  ((0, 1, 1, 0),
			   (0, 1, 0, 0),
			   (0, 1, 0, 0),
			   (0, 0, 0, 0)),
			  ((0, 0, 0, 0),
			   (1, 0, 0, 0),
			   (1, 1, 1, 0),
			   (0, 0, 0, 0)))
    
    blockI = (((0, 1, 0, 0),
               (0, 1, 0, 0),
               (0, 1, 0, 0),
               (0, 1, 0, 0)),
              ((0, 0, 0, 0),
               (0, 0, 0, 0),
               (1, 1, 1, 1),
               (0, 0, 0, 0)))
               
    blockS = (((0, 0, 0, 0),
               (0, 1, 1, 0),
               (1, 1, 0, 0),
               (0, 0, 0, 0)),
              ((0, 0, 0, 0),
               (0, 1, 0, 0),
               (0, 1, 1, 0),
               (0, 0, 1, 0)))
    
    blockZ = (((0, 0, 0, 0),
               (1, 1, 0, 0),
               (0, 1, 1, 0),
               (0, 0, 0, 0)),
              ((0, 0, 1, 0),
               (0, 1, 1, 0),
               (0, 1, 0, 0),
               (0, 0, 0, 0)))
               
    blockO = (((0, 0, 0, 0),
               (0, 1, 1, 0),
               (0, 1, 1, 0),
               (0, 0, 0, 0)), 
              ((0, 0, 0, 0),
               (0, 1, 1, 0),
               (0, 1, 1, 0),
               (0, 0, 0, 0)))
			   
    # initialize with name that specefies block, coordinates, and color
    def __init__(self, name, queue, x = 3, y = -4):
        if (name == "L"):
            self.block = Shape.blockL
            self.color = ORANGE
        elif (name == "T"):
            self.block = Shape.blockT
            self.color = PURPLE
        elif (name == "J"):
            self.block = Shape.blockJ
            self.color = BLUE
        elif (name == "I"):
            self.block = Shape.blockI
            self.color = LIGHT_BLUE
        elif (name == "S"):
            self.block = Shape.blockS
            self.color = GREEN
        elif (name == "Z"):
            self.block = Shape.blockZ
            self.color = RED
        elif (name == "O"):
            self.block = Shape.blockO
            self.color = YELLOW
        self.x = x
        self.y = y
        self.r = 0
        if queue == False:
            self.setBlock(self.color, 1)
        else:
            mapObj.drawQueue(self.block[0], self.color, name)
	
    # move the block in a certain direction
    def move(self, dir):
        global activeBlock
        state = 1
        self.setBlock(BLACK, 0)
        if (dir == "d"):
            self.y += 1
            if self.checkIfLocked() == False:
                activeBlock = False
                self.y -= 1
                state = 2
                self.setNewLocked()
        elif (dir == "l"):
            self.x -= 1
            if self.checkPos() == False:
                self.x += 1
        elif (dir == "r"):
            self.x += 1
            if self.checkPos() == False:
                self.x -= 1
        elif (dir == "a"):
            while True:
                self.y += 1
                if self.checkIfLocked() == False:
                    activeBlock = False
                    self.y -= 1
                    state = 2
                    self.setNewLocked()
                    break
        self.setBlock(self.color, state)
	
    # rotate the block
    def rotate(self):
        self.setBlock(BLACK, 0)
        self.r += 1
        if self.r == len(self.block):
            self.r = 0
        if self.checkPos() == False:
            self.r -= 1
        self.setBlock(self.color, 1)
	
    # sets the block on the map and draws it to the screen
    def setBlock(self, color, state):
        mapObj.changeBlock(self.x, self.y, self.block[self.r], color, state)
        mapObj.draw()
        
    # checks if the block is going out of bounds
    def checkPos(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.block[self.r][i][j] == 1:
                    if self.x + j < 0 or self.x + j > 9 or self.y + i > 19:
                        return False
                    for k in mapObj.locked:
                        if k[0] == self.x + j and k[1] == self.y + i:
                            return False
        return True
        
    # checks if the block is locked
    def checkIfLocked(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.block[self.r][i][j] == 1:
                    if self.y + i > 19:
                        return False
                    for k in mapObj.locked:
                        if k[0] == self.x + j and k[1] == self.y + i:
                            return False

    # add new locked block
    def setNewLocked(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.block[self.r][i][j] == 1:
                    mapObj.locked.append([self.x + j, self.y + i])
                
class Frames:
    def __init__(self):
        self.drawGame(False)
        self.drawMain()
        
    def drawMain(self):
        titleLabel = font.render("Tetris", False, (255, 255, 255))
        startButton = Button(window, 270, 240, 200, 50, text = "Start New Game", onClick = lambda: self.drawGame(True))
        exitButton = Button(window, 270, 300, 200, 50, text = "Exit", onClick = lambda: pygame.QUIT())
        window.blit(titleLabel, (320, 150))
        
    def drawPause(self):
        pausedLabel = font.render("Paused", False, (255, 255, 255))
        window.blit(pausedLabel, (300, 240))
        pygame.display.update()
        
    def drawGame(self, play):
        newMap = []
        for i in range(0, 20):
            newMap.append([])
            for j in range(0, 10):
                newMap[i].append([BLACK, 0])
        mapObj.map = newMap
        mapObj.locked = []
        mapObj.draw()
        global playing, score, level, totalLines
        score = 0
        level = 0
        totalLines = 0
        playing = play
        pygame.draw.rect(window, (0, 0, 0), (0, 0, 710, 820))
        pygame.draw.rect(window, (50, 50, 50), (0, 0, 150, 820))
        pygame.draw.rect(window, (50, 50, 50), (560, 0, 150, 820))
        pygame.draw.rect(window, (255, 255, 255), (15, 17, 120, 80))
        pygame.draw.rect(window, (255, 255, 255), (15, 110, 120, 80))
        pygame.draw.rect(window, (255, 255, 255), (15, 203, 120, 80))
        pygame.draw.rect(window, (255, 255, 255), (575, 17, 120, 250))
        scoreLabel = font.render("Score", False, (0, 0, 0))
        window.blit(scoreLabel, (28, 113))
        levelLabel = font.render("Level", False, (0, 0, 0))
        window.blit(levelLabel, (30, 20))
        nextLabel = font.render("Next", False, (0, 0, 0))
        window.blit(nextLabel, (595, 20))
        linesLabel = font.render("Lines", False, (0, 0, 0))
        window.blit(linesLabel, (30, 206))
    
    
def incScore(score, rows, level):
    if rows == 1:
        return score + 40 * (level + 1)
    elif rows == 2:
        return score + 100 * (level + 1)
    elif rows == 3:
        return score + 300 * (level + 1)
    elif rows == 4:
        return score + 1200 * (level + 1)
    else:
        return score
        
def setPaused(paused):
    if paused == True:
        return False
    else:
        return True
        
# create map
originalMap = []
for i in range(0, 20):
	originalMap.append([])
	for j in range(0, 10):
		originalMap[i].append([BLACK, 0])
mapObj = Map(originalMap)

shapes = ("L", "T", "J", "I", "S", "Z", "O")
colors = (RED, BLUE, GREEN)
playing = False
paused = False
activeBlock = False
lineUp = []
time = pygame.time.get_ticks()
wait = 1000
score = 0
level = 0
totalLines = 0
lineUp.append(random.choice(shapes))
frame = Frames()

while True:
    if paused:
        frame.drawPause()
    elif playing:
        # check to see if need to create new block
        scoreCounter = font2.render(str(score), False, (0, 0, 0))
        levelCounter = font.render(str(level), False, (0, 0, 0))
        lineCounter = font.render(str(totalLines), False, (0, 0, 0))
        pygame.draw.rect(window, (255, 255, 255), (15, 50, 120, 50))
        pygame.draw.rect(window, (255, 255, 255), (15, 140, 120, 50))
        pygame.draw.rect(window, (255, 255, 255), (15, 235, 120, 50))
        window.blit(lineCounter, (28, 237))
        window.blit(levelCounter, (28, 57))
        window.blit(scoreCounter, (28, 148))
        if activeBlock == False:
            lineUp.append(random.choice(shapes))
            block = Shape(lineUp[0], False)
            nextBlock = Shape(lineUp[1], True)
            activeBlock = True
            del lineUp[0]
        mapObj.draw()
        pygame.display.flip()
        cleared = mapObj.checkRows()
        totalLines += cleared
        level = totalLines // 10
        score = incScore(score, cleared, level)
        if wait > 200:
            wait = 1000 - 100 * level
        if pygame.time.get_ticks() > time + wait:
            block.move("d")
            time = pygame.time.get_ticks()
    else:
        events = pygame.event.get()
        pygame_widgets.update(events)
        pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                block.move("d")
            elif event.key == pygame.K_LEFT:
                block.move("l")
            elif event.key == pygame.K_RIGHT:
                block.move("r")
            elif event.key == pygame.K_UP:
                block.rotate()
            elif event.key == pygame.K_SPACE:
                block.move("a")
            elif event.key == pygame.K_p and playing == True:
                paused = setPaused(paused)