import time
import pygame
import random

pygame.init()
window = pygame.display.set_mode((400, 800))
playing = True

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

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
                pygame.draw.rect(window, self.map[i][j][0], (j * 40, i * 40, 40, 40))
            
    # change the state and color of the block on the map
    def changeBlock(self, x, y, block, color, state):
        for i in range(0, 4):
            for j in range(0, 4):
                if block[i][j] == 1:
                    if x + j >= 0 and x + j < 10 and y + i >= 0 and y + i < 20:
                        self.map[y+i][x+j] = [color, state]

    # check if a row is full
    def checkRows(self):
        for i in range(0, 20):
            total = 0
            for j in range(0, 10):
                if map[i][j][1] == 2:
                    total += 1
            if total == 10:
                self.clearRow(i)
    
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
                if map[i][j][1] == 2:
                    curColor = map[i][j][0]
                    map[i][j] = [BLACK, 0]
                    map[i + 1][j] = [curColor, 2]
        for coord in newLocked:
            if coord[1] < rowNum:
                coord[1] += 1
                
        self.locked = newLocked
        
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
    
    blockI = (((0, 0, 1, 0),
               (0, 0, 1, 0),
               (0, 0, 1, 0),
               (0, 0, 1, 0)),
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
               (0, 1, 1, 0),
               (0, 0, 1, 1),
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
    def __init__(self, name, x, y, color):
        if (name == "L"):
            self.block = Shape.blockL
        elif (name == "T"):
            self.block = Shape.blockT
        elif (name == "J"):
            self.block = Shape.blockJ
        elif (name == "I"):
            self.block = Shape.blockI
        elif (name == "S"):
            self.block = Shape.blockS
        elif (name == "Z"):
            self.block = Shape.blockZ
        elif (name == "O"):
            self.block = Shape.blockO
        self.x = x
        self.y = y
        self.color = color
        self.r = 0
        self.setBlock(self.color, 1)
	
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
        
# create map
map = []
for i in range(0, 20):
	map.append([])
	for j in range(0, 10):
		map[i].append([BLACK, 0])
mapObj = Map(map)

# block types
shapes = ("L", "T", "J", "I", "S", "Z", "O")
colors = (RED, BLUE, GREEN)

# main loop
activeBlock = False
time = pygame.time.get_ticks()
while playing:
    # check to see if need to create new block
    if activeBlock == False:
        block = Shape(random.choice(shapes), 3, -4, random.choice(colors))
        activeBlock = True
        activeBlock = True
    mapObj.draw()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                block.move("d")
            elif event.key == pygame.K_a:
                block.move("l")
            elif event.key == pygame.K_d:
                block.move("r")
            elif event.key == pygame.K_r:
                block.rotate()
    mapObj.checkRows()
    if pygame.time.get_ticks() > time + 500:
        block.move("d")
        time = pygame.time.get_ticks()