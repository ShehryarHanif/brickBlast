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
minVal = 1000000000000
class CannonBall:
    
    def __init__(self, usrCannon, cannonBallCount):
        self.__img = loadImage(PATH  + "/Resources/CannonBall/Cannonball.png")
        self.__separationDistance = 10
        self.__radius = 8.0
        self.__vectorDirection, self.__baseX, self.__baseY = usrCannon.requisiteForCannonBall()
        self.__cannonHeight = usrCannon.getCannonHeight()
        self.__xCenter = float(self.__baseX) + float(self.__cannonHeight) * math.cos(self.__vectorDirection) - 2.0 * (float(self.__radius) + self.__separationDistance) * cannonBallCount * cos(self.__vectorDirection)
        self.__yCenter = float(self.__baseY) - float(self.__cannonHeight) * math.sin(self.__vectorDirection) + 2.0 * (float(self.__radius) + self.__separationDistance)* cannonBallCount * sin(self.__vectorDirection)
        self.__velocity = 3
        self.__xVelocity = self.__velocity * math.cos(self.__vectorDirection)
        self.__yVelocity = -self.__velocity * math.sin(self.__vectorDirection)
        
    def checkCollisions(self, blockList):
        for block in blockList:
            leftX, topY, rightX, bottomY = block.corners()
            closestPoint = [0, 0]
            horizontal, vertical = False, False
            
            if self.__yCenter - self.__radius >= bottomY and leftX - 2.0 * self.__radius <= self.__xCenter <= rightX + 2.0 * self.__radius:
                if self.__yCenter - self.__radius + self.__yVelocity <= bottomY:
                    self.__xCenter += 2 * self.__xVelocity
                    # print("hell")
                    # newPositionCoordinates = [self.__xCenter + self.__xVelocity, self.__yCenter + self.__yVelocity]
                    # closestPositionCoordinates = [self.__xCenter + float(self.__xVelocity) * float(self.__yCenter - bottomY - self.__radius) / float(self.__yVelocity), bottomY + self.__radius]
                    
                    # fill(0,255,0)
                    # circle(closestPositionCoordinates[0],closestPositionCoordinates[1], 20)
                    
                    # self.__giveBoost(newPositionCoordinates, closestPositionCoordinates)
                    
                    # self.__yCenter =  bottomY + self.__radius
                    # self.__yCenter += (abs(self.__yCenter + self.__yVelocity - bottomY)) - self.__radius
                    
                    # self.__xCenter += (self.__xVelocity * (self.__yCenter - bottomY - self.__radius) / self.__yVelocity)
                    # self.__xCenter += self.__xVelocity * ((abs(self.__yCenter + self.__yVelocity - bottomY)) - self.__radius) / self.__yVelocity
                    
                vertical = True
                closestPoint = [self.__xCenter, bottomY]
            elif self.__yCenter + self.__yVelocity + self.__radius <= topY and leftX - 2.0 * self.__radius <= self.__xCenter <= rightX + 2.0 * self.__radius:
                if self.__yCenter + self.__radius + self.__yVelocity >= topY:
                    self.__xCenter += 2 * self.__xVelocity
                vertical = True
                closestPoint = [self.__xCenter, topY]
                
            if self.__xCenter - self.__radius + self.__xVelocity >= rightX and topY - 2.0 * self.__radius <= self.__yCenter <= bottomY + 2.0 * self.__radius:
                if self.__xCenter - self.__radius + self.__xVelocity <= rightX:
                    self.__yCenter -= 2 * self.__yVelocity
                horizontal = True
                closestPoint = [rightX, self.__yCenter]
            elif self.__xCenter + self.__radius + self.__xVelocity <= leftX and topY  - 2.0 * self.__radius <= self.__yCenter <= bottomY + 2.0 * self.__radius:
                if self.__xCenter + self.__radius + self.__xVelocity >= leftX:
                    self.__yCenter -= 2 * self.__yVelocity
                horizontal = True
                closestPoint = [leftX, self.__yCenter]
            
            ellipse(closestPoint[0], closestPoint[1], 10, 10)
            
            if math.sqrt((self.__xCenter + self.__xVelocity - closestPoint[0]) ** 2 + (self.__yCenter + self.__yVelocity - closestPoint[1]) ** 2) <= self.__radius + 1:
                fill(0,255,255)
                ellipse(closestPoint[0], closestPoint[1], 10, 10)
                # # print "HELLO"
                # # if closestPoint[0] == leftX:
                # #     self.__xCenter = leftX - self.__radius
                # #     self.__xVelocity *= -1
                # # elif closestPoint[0] == rightX:
                # #     self.__xCenter = rightX + self.__radius
                # #     self.__xVelocity *= -1
                # # print closestPoint[1], bottomY    
                # # if closestPoint[1] == bottomY:
                # #     print "HI"
                    
                # #     self.__yCenter = bottomY + self.__radius
                # #     self.__yVelocity *= -1
                # # elif closestPoint[1] == topY:
                # #     self.__yCenter = topY - self.__radius
                # #     self.__yVelocity *= -1
                # print horizontal, vertical
                if horizontal:
                    self.__xVelocity *= -1.0
                if vertical:
                    self.__yVelocity *= -1.0
            
    def __giveBoost(self, newPosition, closestPosition):
        pendingMagnitudeChange = self.__getMagnitude(newPosition) - self.__getMagnitude(closestPosition)
        
        # print (pendingMagnitudeChange)
        
        theta = math.atan2(self.__yVelocity, self.__xVelocity)
        
        self.__xCenter = closestPosition[0] + float(pendingMagnitudeChange) * float(math.cos(theta))
        
        print(self.__xCenter)
        
        self.__yCenter = closestPosition[1] + float(pendingMagnitudeChange) * float(math.sin(theta))
        
    def __getMagnitude(self, position):
        return math.sqrt((position[0] - self.__xCenter) ** 2 + ((position[1] - self.__yCenter) ** 2))
    
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
            cBall.checkCollisions(blockList)
            cBall.updatePosition()
            cBall.display()
    
class tempBlock:
    
    def __init__(self, leftX, topY, bW, bH):
        self.__originPoint = [leftX, topY]
        self.__terminalPoint = [leftX + bW, topY + bH]
        
    def corners(self):
        return self.__originPoint[0], self.__originPoint[1], self.__terminalPoint[0], self.__terminalPoint[1]
    
    def display(self):
        rectMode(CORNERS)
        fill(0)
        rect(self.__originPoint[0], self.__originPoint[1], self.__terminalPoint[0], self.__terminalPoint[1])
        
class tempBlockList(list):
    
    def __init__(self):
        self.append(tempBlock(100, 100, 400, 75))
        self.append(tempBlock(300, 300, 100, 75))

    def display(self):
        for block in self:
            block.display()

class Game:
    def __init__(self):
        self.__playerCannon = Cannon(x, y, WIDTH / 10.0, WIDTH / 10.0 * 3)
        self.__playerCannonShotQuanity = 10
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
    frameRate(60)
    smooth()
    background(255)
    
x, y = WIDTH / 2, HEIGHT
brickBlast = Game()

def draw():
    background(255)
    brickBlast.display()
    
def mouseClicked():
    brickBlast.shootCannon()
  
