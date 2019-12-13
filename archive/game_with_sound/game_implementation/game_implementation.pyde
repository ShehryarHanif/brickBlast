# Cannonballs have a certain randomness to them, so as to limit the risk of an infnite turn.

import math, os, time, random

PATH = os.getcwd()
EPS = 1
WIDTH, HEIGHT = 500, 700 #5:7 must be maintained
print PATH

class Cannon:
    
    def __init__(self, base_x, base_y, cannon_width, cannon_height): #cannon_width:cannon_height = 1:3 
        self.__base_x = base_x
        self.__base_y = base_y
        self.__width = cannon_width
        self.__height = cannon_height
        self.__cannonBarrelImg =  loadImage(PATH + "/Resources/Cannon/Cannon.png")
        self.__cannonBaseImg = loadImage(PATH + "/Resources/Cannon/CannonBase.png")
    
    def __specialCannonBarrelDisplay(self):
        image(self.__cannonBarrelImg, - self.__width / 2, -self.__height, self.__width, self.__height)
        
    def __specialCannonBaseImage(self):
        image(self.__cannonBaseImg, self.__base_x - self.__width / 2, int(self.__base_y - self.__height / 300.0 * 115.0), self.__width, int(self.__height / 300.0 * 115.0))
        
    def changePosition(self, newPosition):
        
        self.__base_x = newPosition[0]
        
        if self.__base_x > 450:
            
            self.__base_x = 450
            
        elif self.__base_x < 50:
            
            self.__base_x = 50
        
    def rotation(self):
        angle = self.__angleCalculator()

        pushMatrix()
        translate(self.__base_x,self.__base_y - (self.__height / 300.0 * 64.0)) #to have the cannon pivot correctly, the end of the cannon is at 364 relative to base_y
        rotate(radians(90-angle))
        self.__specialCannonBarrelDisplay()
        popMatrix()
        self.__specialCannonBaseImage()
        
    def __angleCalculator(self):
        angle = math.degrees(math.atan2(abs(mouseY - (self.__base_y - (self.__height / 300.0 * 64.0))),(mouseX - self.__base_x)))
        
        if angle < 30:
            angle = 30
            
        elif angle > 150:
            angle = 150
        
        return angle
    
    def requisiteForCannonBall(self):
        angle = radians(self.__angleCalculator())
        return (angle, self.__base_x,self.__base_y - (self.__height / 300.0 * 64.0))
    
    def getCannonHeight(self):
        return self.__height

class Demarcator:
    def __init__(self):
        self.__height = 2 
        self.__color = "#25331F"
        self.__topCorner = (0, int(HEIGHT / 700.0 * 500.0 - self.__height / 2.0))
        self.__bottomCorner = (WIDTH, int(HEIGHT / 700.0 * 500.0 + self.__height / 2.0))
    
    def getBottomEnd(self):
        return self.__bottomCorner[1]
    
    def display(self):
        fill(self.__color)
        rectMode(CORNERS)
        rect(self.__topCorner[0], self.__topCorner[1], self.__bottomCorner[0], self.__bottomCorner[1])
        
class Score:
    def __init__(self):
        
        self.__scoreAmount = 0
        
    def change(self, changeAmount):
        
        self.__scoreAmount += changeAmount
        
    def display(self):
        
        fill(0, 0, 0) # This gives the font its black color.
        textSize(12) # This is the font's size.
                
        score_string = "SCORE:   " + str(self.__scoreAmount * 10) # This is the string we will show on the screen.
        
        text(score_string, WIDTH * 17 / 20, HEIGHT / 20) # This will show the score on the screen.
        
    def getScore(self):
        
        return self.__scoreAmount

class CannonBall:
    
    def __init__(self, usrCannon, cannonBallCount):
        self.__img = loadImage(PATH  + "/Resources/CannonBall/Cannonball.png")
        self.__separationDistance = 10.0
        self.__radius = 8.0
        self.__displayRadius = 10.0
        self.__vectorDirection, self.__baseX, self.__baseY = usrCannon.requisiteForCannonBall()
        self.__cannonHeight = usrCannon.getCannonHeight()
        self.__xCenter = float(self.__baseX) + float(self.__cannonHeight) * math.cos(self.__vectorDirection) - 2.0 * (float(self.__radius) + self.__separationDistance) * cannonBallCount * cos(self.__vectorDirection)
        self.__yCenter = float(self.__baseY) - float(self.__cannonHeight) * math.sin(self.__vectorDirection) + 2.0 * (float(self.__radius) + self.__separationDistance)* cannonBallCount * sin(self.__vectorDirection)
        self.__velocity = 4.0
        self.__xVelocity = self.__velocity * math.cos(self.__vectorDirection)
        self.__yVelocity = -self.__velocity * math.sin(self.__vectorDirection)
        self.__isDead = False
        self.__isAmmoCollision = False
        
    def isBallDead(self):
        return self.__isDead
        
    def checkCollisions(self, blockList, score): # Checks if a collision occurs and decrements block's durability accordingly. If durability becomes zero, the block is destroyed from the block_list and the score is added to the player's score.
        blockTempList = blockList[:]
        for index, block in enumerate(blockTempList):
            leftX, topY, rightX, bottomY = block.corners()
            closestPoint = [0, 0]
            horizontal, vertical = False, False
            
            if self.__yCenter - self.__radius >= bottomY and leftX - math.floor(self.__velocity / self.__radius + 1) * self.__radius <= self.__xCenter <= rightX + math.floor(self.__velocity / self.__radius + 1) * self.__radius:
                if self.__yCenter - self.__radius + self.__yVelocity <= bottomY:
                    self.__xCenter += 2.0 * self.__xVelocity
                vertical = True
                closestPoint = [self.__xCenter, bottomY]
            elif self.__yCenter + self.__radius <= topY and leftX - math.floor(self.__velocity / self.__radius + 1) * self.__radius <= self.__xCenter <= rightX + math.floor(self.__velocity / self.__radius + 1) * self.__radius:
                if self.__yCenter + self.__radius + self.__yVelocity >= topY:
                    self.__xCenter += 2.0 * self.__xVelocity
                vertical = True
                closestPoint = [self.__xCenter, topY]
                
            if self.__xCenter - self.__radius >= rightX and topY - self.__radius <= self.__yCenter <= bottomY + self.__radius:
                #print(self.__xCenter, self.__xVelocity, rightX)
                if self.__xCenter - self.__radius + self.__xVelocity <= rightX:
                    self.__yCenter -= 2.0 * self.__yVelocity
                horizontal = True
                closestPoint = [rightX, self.__yCenter]
            elif self.__xCenter + self.__radius <= leftX and topY  - self.__radius <= self.__yCenter <= bottomY + self.__radius:
                if self.__xCenter + self.__radius + self.__xVelocity >= leftX:
                    self.__yCenter -= 2.0 * self.__yVelocity
                horizontal = True
                closestPoint = [leftX, self.__yCenter]
                        
            if math.sqrt((self.__xCenter + self.__xVelocity - closestPoint[0]) ** 2 + (self.__yCenter + self.__yVelocity - closestPoint[1]) ** 2) <= self.__radius + 1: # Will decrement block durability and destroy blocks as need be
                if isinstance(block, BrickBlock):
                    block.decrementDurability()
                    if block.isBlockDead():
                        if isinstance(block, AmmoBlock):
                            self.__isAmmoCollision = True
                        else:
                            score.change(block.getOriginalDurability())
                        self.__isDead = True
                        del blockList[index]

                if horizontal:
                    self.__xVelocity *= -1.0
                if vertical:
                    self.__yVelocity *= -1.0
                    
    def getCenterPosition(self):
            return self.__xCenter, self.__yCenter

    def isAmmoCollision(self):
        return self.__isAmmoCollision
    
    def updatePosition(self):
        self.__xCenter += self.__xVelocity
        self.__yCenter += self.__yVelocity
        
    def lowerBoundaryCollision(self):        
        return self.__yCenter - self.__radius > HEIGHT and self.__yVelocity >= 0
        
    def display(self):
        circle(int(self.__xCenter), int(self.__yCenter), self.__displayRadius * 2)
        
class CannonShot(list):
    def __init__(self, usrCannon, cannonShootQuantity):
        for ballCount in range(cannonShootQuantity):
            self.append(CannonBall(usrCannon, ballCount))
        self.__increment = False
    
    def updateAndDisplay(self, blockList, cannon, score):
        
        tempList = [] + self
        
        
        for index,cBall in enumerate(tempList):
            cBall.checkCollisions(blockList, score)
            cBall.updatePosition()
            if cBall.lowerBoundaryCollision() or cBall.isBallDead():
                if len(self) == 1:
                    cannon.changePosition(self[index].getCenterPosition())
                if cBall.isAmmoCollision():
                    self.setIncrementStatus(True)
                del self[index] 
                
                
            cBall.display()
    
    def getIncrementStatus(self):
        return self.__increment
    
    def setIncrementStatus(self, status):
        self.__increment = status
        
            
    
class Block:
    
    def __init__(self, leftX, topY, bW, bH):
        self.__originPoint = [leftX, topY]
        self.__terminalPoint = [leftX + bW, topY + bH]
    
    def getOriginPoint(self):
        return self.__originPoint
    
    def getTerminalPoint(self):
        return self.__terminalPoint
    
    def corners(self):
        return self.__originPoint[0], self.__originPoint[1], self.__terminalPoint[0], self.__terminalPoint[1]
    
    def display(self):
        rectMode(CORNERS)
        stroke(0,255,0)
        fill(0)
        rect(self.__originPoint[0], self.__originPoint[1], self.__terminalPoint[0], self.__terminalPoint[1])
    
    def moveDownwards(self):
        shiftHeight = self.__terminalPoint[1] - self.__originPoint[1]
        self.__originPoint[1] += shiftHeight
        self.__terminalPoint[1] += shiftHeight
        
    def demarcationCollision(self, demarcationLine):
        print(self.__terminalPoint[1], demarcationLine.getBottomEnd())
        return demarcationLine.getBottomEnd() <= self.__terminalPoint[1]
      
class BrickBlock(Block):
    def __init__(self, leftX, topY, bW, bH, durability):
        Block.__init__(self, leftX, topY, bW, bH)
        self.__durability = durability
        self.__originalDurability = durability
        self.__backgroundImage = loadImage(PATH + "/Resources/Block/latestBrick.jpg")
        self.__diameter = 30
        
    def getOriginalDurability(self):
        return self.__originalDurability
        
    def decrementDurability(self):
        self.__durability -= 1
        
    def isBlockDead(self):
        return self.__durability == 0
    
    def getCircleDiameter(self):
        return self.__diameter
    
    def display(self):
        originPoint = self.getOriginPoint()
        terminalPoint = self.getTerminalPoint()
        rectMode(CORNERS)
        stroke(255)
        fill(0)
        rect(originPoint[0], originPoint[1], terminalPoint[0], terminalPoint[1])
        imageMode(CORNERS)
        image(self.__backgroundImage, originPoint[0], originPoint[1], terminalPoint[0], terminalPoint[1])
        imageMode(CORNER)
        
        fill(0)
        circle((originPoint[0] + terminalPoint[0]) / 2.0, (terminalPoint[1] + originPoint[1]) / 2.0, self.__diameter)
        fill(0, 255, 0)

        
        fill(255)
        textSize(18)
        message = str(self.__durability)
        
        if len(message) == 1:
            message = "0" + message
        textMode(LEFT)    
        text(message, (originPoint[0] + terminalPoint[0]) / 2.0 - self.__diameter / 2.0 / math.sqrt(2), (originPoint[1] + terminalPoint[1]) / 2.0 + self.__diameter / 4.0)        
        
            
class AmmoBlock(BrickBlock):
    def __init__(self, leftX, topY, bW, bH):
        BrickBlock.__init__(self, leftX, topY, bW, bH, 1)
        self.__backgroundImage = loadImage(PATH + "/Resources/Block/latestBrick.jpg")
        self.__foregroundImage = loadImage(PATH + "/Resources/CannonBall/Cannonball.png")
        
    def display(self):
        originPoint = self.getOriginPoint()
        terminalPoint = self.getTerminalPoint()
        rectMode(CORNERS)
        stroke(255)
        fill(0)
        rect(originPoint[0], originPoint[1], terminalPoint[0], terminalPoint[1])
        imageMode(CORNERS)
        image(self.__backgroundImage, originPoint[0], originPoint[1], terminalPoint[0], terminalPoint[1])
        imageMode(CORNER)
        image(self.__foregroundImage, (originPoint[0] + terminalPoint[0]) / 2 - self.getCircleDiameter() / 2, (originPoint[1] + terminalPoint[1]) / 2 - self.getCircleDiameter() / 2, self.getCircleDiameter(), self.getCircleDiameter())
        

        
class BlockList(list):
    
    def __init__(self):
        self.append(Block(-100, 0, 101, HEIGHT - WIDTH / 10.0 * 3 / 300.0 * 115)) # Left Boundary
        self.append(Block(WIDTH - 1, 0, 100, HEIGHT - WIDTH / 10.0 * 3 / 300.0 * 115)) # Right Boundary
        self.append(Block(0, -100, WIDTH, 101)) # Top Boundary

        for r in range(10):
            for c in range(5):
                if r % 2 and c % 2:
                    #self.append(BrickBlock(100 * c, 50 * r, 100, 50, 5))
                    continue
                        
        self.append(AmmoBlock(0, 450, 100, 50))
        
        self.__demarcationLineCollided = False

    def display(self):
        for block in self:
            block.display()
            
    def moveAllDownwardsAndFlagGameEnd(self, demarcationLine):
        for block in self[3:]:
            block.moveDownwards()
            if block.demarcationCollision(demarcationLine):
                self.__demarcationLineCollided = True
            
    def demarcationLineCollision(self):
        return self.__demarcationLineCollided        
            
    def createNewRow(self, playerScore, shotQuantity):
        
        score = playerScore.getScore()
        newBlockQuantity = 1
        availableColPositions = [0, 1, 2, 3, 4]
                                
        if score <= 25:
            newBlockQuantity = 2
                                
        elif score <= 150:
            newBlockQuantity = 3
                
        elif score <= 275:
            newBlockQuantity = 4
            
        else:
            newBlockQuantity = 5
            
        if score <= 100:
            bound = 3
            
        elif score >= 1000:
            bound = 4
            
        else:
            bound = 2
            
        for newBlock in range(newBlockQuantity):
            
            if  random.randint(1,4) <= bound or len(self) <= 6:
                newColPosition = availableColPositions.pop(random.randint(0, (len(availableColPositions) - 1)))
                
                if random.randint(1,4) == 1:
                    self.append(AmmoBlock(100 * newColPosition, 0, 100, 50))
                                                            
                else:
                    self.append(BrickBlock(100 * newColPosition, 0, 100, 50, shotQuantity + random.randint(1, newBlockQuantity)))                                           
            
        

class Game:
    def __init__(self):
        self.__playerCannon = Cannon(x, y, WIDTH  / 10.0, WIDTH / 10.0 * 3)
        self.__playerCannonShotQuantity = 1
        self.__playerShot = CannonShot(self.__playerCannon, 0)
        self.__gameEndLine = Demarcator()
        self.__blockList = BlockList()
        self.__turnInPlay = False
        self.__playerScore = Score()
        self.__gameContinue = True
        
    def __updateAndDisplayCannon(self):
        self.__playerCannon.rotation()
    
    def shootCannon(self):
        self.__playerShot = CannonShot(self.__playerCannon, self.__playerCannonShotQuantity)
        self.__turnInPlay = True
        
    def updateAndDisplay(self):
        self.__gameEndLine.display()
        self.__playerShot.updateAndDisplay(self.__blockList, self.__playerCannon, self.__playerScore)
        self.__updateAndDisplayCannon()
        self.__blockList.display()
        self.__playerScore.display()
        
        if len(self.__playerShot) == 0:
            if self.__turnInPlay:
                self.__blockList.moveAllDownwardsAndFlagGameEnd(self.__gameEndLine)
                self.__blockList.createNewRow(self.__playerScore, self.__playerCannonShotQuantity)
                self.__gameContinue = not(self.__blockList.demarcationLineCollision())
                print(self.__blockList.demarcationLineCollision())
            self.__turnInPlay = False
            
        if self.__playerShot.getIncrementStatus():
            self.__incrementCannonShot()
            self.__playerShot.setIncrementStatus(False)
            
    def __incrementCannonShot(self):
        self.__playerCannonShotQuantity += 1
        
    def inputStatus(self):
        return not (self.__turnInPlay)

    def getGameContinueStatus(self):
        return self.__gameContinue
    
    def gameOverDisplay(self):
        
        fill(0, 0, 0) # This gives the font its black color.
        textSize(44)  # This is the font's size.
                
        length_string = "GAME OVER \nSCORE: " + str(self.__playerScore.getScore() * 10)  # This is the string to be shown on the screen.
        
        text(length_string, WIDTH / 4, HEIGHT / 2) # This shows the score on the screen.

def setup():
    size(WIDTH, HEIGHT)
    frameRate(60)
    smooth()
    background(255)
    
x, y = WIDTH / 2, HEIGHT
brickBlast = Game()

def draw():
    background(255)
    
    if brickBlast.getGameContinueStatus():
        brickBlast.updateAndDisplay()
    else:
        brickBlast.gameOverDisplay()
    
def mouseClicked():
    if brickBlast.inputStatus() == True:
        brickBlast.shootCannon()
    if not brickBlast.getGameContinueStatus():
        global brickBlast
        
        brickBlast = Game()        
