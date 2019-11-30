cx = 0
cy = 0
r = 30

sx = 200
sy = 100
sw = 200   
sh = 200

flags = {"Top": False, "Bottom" : False, "Right" : False, "Left" : False}

def setup():
    
    size(600,400)
    noStroke()

def draw():

    background(255)
    
    cx = mouseX
    cy = mouseY
    hit = circleRect(cx,cy,r, sx,sy,sw,sh)
    
    if (hit):
      
        if flags["Top"] and flags["Left"]:
            
            fill(0,0,124)
            
        elif flags["Top"] and flags["Right"]:
            
            fill(0,0,255)
            
        elif flags["Bottom"] and flags["Left"]:
            
            fill(111,111,111)
            
        elif flags["Bottom"] and flags["Right"]:
            
            fill(0,124,255)
      
        elif flags["Top"]:
            
            fill(124, 0, 0)
            
        elif flags["Bottom"]:
            
            fill(225, 0, 0)

        elif flags["Left"]:
            
            fill(0, 124, 0)
            
        elif flags["Right"]:
            
            fill(0, 225, 0)
        

  
    else:
        
        fill(0,150,255)
    rect(sx,sy, sw,sh)

    fill(0, 150)
    ellipse(cx,cy, r*2,r*2)


def circleRect(cx, cy, radius, rx, ry, rw, rh):
    
    global flags

    testX = cx
    testY = cy
    
    if (cx < rx):
        testX = rx      
    elif (cx > rx+rw):
        testX = rx+rw   
    if (cy < ry):
        testY = ry      
    elif (cy > ry+rh):
        testY = ry+rh

    distX = cx-testX
    distY = cy-testY
    distance = sqrt( (distX*distX) + (distY*distY) )

    if (distance <= radius):
        
        if testX == rx:
            
            flags["Left"] = True
            
        if testX == rx + rw:
            
            flags["Right"] = True
            
        if testY == ry:
            
            flags["Top"] = True
            
        if testY == ry + rh:
            
            flags["Bottom"] = True
        
        return True
    
    flags = {"Top": False, "Bottom" : False, "Right" : False, "Left" : False}

    
    return False
