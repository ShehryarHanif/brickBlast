import math, os, random

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
        
        
    def rotation(self):
        angle = self.__angleCalculator()
        line(self.__base_x, self.__base_y - (self.__height / 300.0 * 64.0), mouseX, mouseY)
        #print(angle)
        pushMatrix()
        translate(self.__base_x,self.__base_y - (self.__height / 300.0 * 64.0)) #to have the cannon pivot correctly, the end of the cannon is at 364 relative to base_y
        rotate(radians(90-angle))
        self.__specialCannonBarrelDisplay()
        popMatrix()
        self.__specialCannonBaseImage()
        
    def __angleCalculator(self):
        return math.degrees(math.atan2(abs(mouseY - (self.__base_y - (self.__height / 300.0 * 64.0))),(mouseX - self.__base_x)))
    
    def requisiteForCannonBall(self):
        angle = radians(self.__angleCalculator())
        return (angle, self.__base_x,self.__base_y - (self.__height / 300.0 * 64.0))
    
    def getCannonHeight(self):
        return self.__height

class Demarcator:
    def __init__(self):
        self.__height = 10 
        self.__color = "#25331F"
        self.__topCorner = (0, int(HEIGHT / 700.0 * 500.0 - self.__height / 2.0))
        print self.__topCorner
        self.__bottomCorner = (WIDTH, int(HEIGHT / 700.0 * 500.0 + self.__height / 2.0))
        print self.__bottomCorner
        
    def display(self):
        fill(self.__color)
        rectMode(CORNERS)
        rect(self.__topCorner[0], self.__topCorner[1], self.__bottomCorner[0], self.__bottomCorner[1])

class CannonBall:
    
    def __init__(self, usrCannon, cannonBallCount):
        self.__img = loadImage(PATH  + "/Resources/CannonBall/Cannonball.png")
        self.__radius = 8.0
        self.__vectorDirection, self.__baseX, self.__baseY = usrCannon.requisiteForCannonBall()
        self.__cannonHeight = usrCannon.getCannonHeight()
        self.__xCenter = float(self.__baseX) + float(self.__cannonHeight) * math.cos(self.__vectorDirection) - 2.0 * (float(self.__radius) + 5) * cannonBallCount * cos(self.__vectorDirection)
        self.__yCenter = float(self.__baseY) - float(self.__cannonHeight) * math.sin(self.__vectorDirection) + 2.0 * (float(self.__radius) + 5)* cannonBallCount * sin(self.__vectorDirection)
        self.__velocity = 5
        self.__xVelocity = self.__velocity * math.cos(self.__vectorDirection)
        self.__yVelocity = -self.__velocity * math.sin(self.__vectorDirection)
        
    def checkCollisions(self, blockList):
        for block in blockList:
            leftX, topY, rightX, bottomY = block.corners()
            closestPoint = [-1, -1]
            
            if self.__yCenter - self.__radius >= bottomY and leftX <= self.__xCenter <= rightX:
                closestPoint = [self.__xCenter, bottomY]
            elif self.__yCenter + self.__radius <= topY and leftX <= self.__xCenter <= rightX:
                closestPoint = [self.__xCenter, topY]
                
            if self.__xCenter - self.__radius >= rightX and topY <= self.__yCenter <= bottomY:
                closestPoint = [rightX, self.__yCenter]
            elif self.__xCenter + self.__radius <= leftX and topY <= self.__yCenter <= bottomY:
                closestPoint = [leftX, self.__yCenter]
            
            if math.sqrt((self.__xCenter - closestPoint[0]) ** 2 + (self.__yCenter - closestPoint[1])) <= self.__radius:
                if closestPoint[0] == leftX or closestPoint[0] == rightX:
                    self.__xVelocity *= -1
                if closestPoint[1] == bottomY or closestPoint[1] == topY:
                    self.__yVelocity *= -1 
                
            
    
    def updatePosition(self):
        self.__xCenter += self.__xVelocity
        self.__yCenter += self.__yVelocity
        
    def display(self):
        circle(int(self.__xCenter), int(self.__yCenter), self.__radius * 2)
        
class CannonShot(list):
    def __init__(self, usrCannon, cannonShootQuantity):
        for ballCount in range(cannonShootQuantity):
            self.append(CannonBall(usrCannon, ballCount))
    
    def updateAndDisplay(self, blockList):
        for cBall in self:
            cBall.updatePosition()
            cBall.display()
            cBall.checkCollisions(blockList)
    
class tempBlock:
    
    def __init__(self, leftX, topY, bW, bH):
        self.__originPoint = [leftX, topY]
        self.__terminalPoint = [leftX + bW, topY - bH]
        
    def corners(self):
        return self.__originPoint[0], self.__originPoint[1], self.__terminalPoint[0], self.__terminalPoint[1]
    
    def display(self):
        rectMode(CORNERS)
        fill(0)
        rect(self.__originPoint[0], self.__originPoint[1], self.__terminalPoint[0], self.__terminalPoint[1])
        
class tempBlockList(list):
    
    def __init__(self):
        self.append(tempBlock(0, 100, 100, 75))
        self.append(tempBlock(200, 300, 100, 75))

    def display(self):
        for block in self:
            block.display()

class Game:
    def __init__(self):
        self.__playerCannon = Cannon(x, y, WIDTH / 10.0, WIDTH / 10.0 * 3)
        self.__playerCannonShotQuanity = 15
        self.__playerShot = CannonShot(self.__playerCannon, 0)
        self.__gameEndLine = Demarcator()
        self.__blockList = tempBlockList()
        
    def __updateAndDisplayCannon(self):
        self.__playerCannon.rotation()
    
    def shootCannon(self):
        self.__playerShot = CannonShot(self.__playerCannon, self.__playerCannonShotQuanity)
        
    def display(self):
        self.__gameEndLine.display()
        self.__playerShot.updateAndDisplay(self.__blockList)
        self.__updateAndDisplayCannon()
        self.__blockList.display()


def setup():
    size(WIDTH, HEIGHT)
    frameRate(120)
    smooth()
    background(255)
    
x, y = WIDTH / 2, HEIGHT
brickBlast = Game()

def draw():
    background(255)
    brickBlast.display()
    
def mouseClicked():
    brickBlast.shootCannon()
  
