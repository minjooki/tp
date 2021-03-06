from cmu_112_graphics import *
from PIL import Image
import pygame
import pickle
import copy
from plant import *
from terrain import *
from helper import *
from pathfinding import *
from bgm import *

# getBoardRowCol and getCellBounds from cmu 112 animations website
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html 
# pygame sound demo code from cmu 112 animations pt 4
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
# dijkstra's algorithm pseudocode + explaination from 
# https://www.youtube.com/watch?v=pVfj6mxhdMw
# file read/wrtie/save guide from w3schools
# https://www.w3schools.com/python/python_file_handling.asp
# pickling guide/helps
# https://ianlondon.github.io/blog/pickling-basics/
# https://stackoverflow.com/questions/6568007/how-do-i-save-and-restore-multiple-variables-in-python
# sprite imaging crop and move player adapted from 112 mini-lecture on PIL and images
# https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=8a3ab4e2-c322-4f04-86e1-ae6a014ddc64
# background music by Starry Attic
# https://www.youtube.com/watch?v=xaDkoBzA4mo&t=26s

# all art by me

def appStarted(app):
    
    pygame.mixer.init()
    app.sound = Sound("design-components/CozyPlace.mp3")
    app.sound.start()

    app.timeElapsed = 0
    app.day = 1

    app.width,app.height = 900,700

    app.mode = 'startMode'

    app.isNewGame = True

    app.newX0,app.newY0,app.newWidth,app.newHeight = (350,325,200,75)
    app.oldX0,app.oldY0 = (350,450)

    app.openInventory = False
    app.closeInvHeight = 25

    app.invItems = [[ ['apple', 0],['peach',0],['lemon',0]],
                    [['strawberry',0],['tomato',0],['blackberry',0]] ]
    
    app.exitHeight = 50
    app.exitWidth = 50
    app.exitSaveX0,app.exitSaveY0 = (350,325)
    app.exitSaveWidth,app.exitSaveHeight = (200,75)
    app.exitCloseX0,app.exitCloseY0 = (350,450)
    app.exitCancelX0,app.exitCancelY0 = (400,575)
    app.exitCancelWidth,app.exitCancelHeight = (100,30)

    app.menuButtonHeight = 50
    app.menuButtonWidth = 100
    
    app.plantButtonX0 = 150
    app.plantButtonY0 = 0
    app.wateringX0 = 250
    app.wateringY0 = 0
    app.harvestingX0 = 350
    app.harvestingY0 = 0

    app.isHarvest = False
    app.harvestStopX0,app.harvestStopY0 = (500,10)
    app.harvestStopWidth,app.harvestStopHeight = (90,30)

    app.openPlanting = False
    app.closePlantingHeight = 25
    app.closePlantX0 = 825
    app.closePlantY0 = 200
    app.plantingSlot = 75
    app.plantingMarginTop = 200
    app.plantingMarginSide = 50
    app.plantingX0,app.plantingX1,app.plantingY0,app.plantingY1 = (50,850,
                                                                    200,500)
    app.unplantX0,app.unplantY0 = (750,475)
    app.unplantWidth = 100
    app.unplantHeight = 25
    app.removingPlants = False

    app.stopRemoveX0,app.stopRemoveY0 = (500,10)
    app.stopRemoveWidth = 90
    app.stopRemoveHeight = 30

    app.waterStartX0,app.waterStartY0 = (250,0)
    app.waterStartWidth,app.waterStartHeight = (100,50)
    app.waterStopX0,app.waterStopY0 = (500,10)
    app.waterStopWidth,app.waterStopHeight = (90,30)
    app.isWatering = False

    app.homeRow,app.homeCol = (0,0)
    app.pathHome = None
    app.graph = None
    app.goHome = False
    app.isHome = False
    app.homeOkX0,app.homeOkY0 = 600,65
    app.homeOkWidth,app.homeOkHeight = (100,15)

    app.plantingSide = ((app.plantingX1-app.plantingX0)-(app.plantingSlot*3))/4
    app.plantingTop = ((app.plantingY1-app.plantingY0)-(app.plantingSlot*2))/3

    app.seedInv = [ [['apple seed',0],['peach seed',0],['lemon seed',0]],
                [['strawberry seed',0],['tomato seed',0],['blackberry seed',0]] ]
    
    app.treePoints = {'apple':[],'peach':[],'lemon':[]}
    app.plantPoints = {'strawb':[],'blackb':[],'tomato':[]}
    app.allSeedClasses = {} # map points to class
    app.allPlantClasses = {} # map points to class

    app.appleSeeds = 5
    app.apples = 0
    app.appleSeedInvX0 = (app.plantingX0+app.plantingSide)
    app.appleSeedInvY0 = (app.plantingY0+app.plantingTop)

    app.peachSeeds = 5
    app.peaches = 0
    app.peachSeedInvX0 = (app.plantingX0+app.plantingSlot+app.plantingSide*2)
    app.peachSeedInvY0 = (app.plantingY0+app.plantingTop)

    app.lemonSeeds = 5
    app.lemons = 0
    app.lemonSeedInvX0 = (app.plantingX0+app.plantingSlot*2+app.plantingSide*3)
    app.lemonSeedInvY0 = (app.plantingY0+app.plantingTop)

    app.strawbSeeds = 5
    app.strawberries = 0
    app.strawbSeedInvX0 = (app.plantingX0+app.plantingSide)
    app.strawbSeedInvY0 = (app.plantingY0+app.plantingSlot+app.plantingTop*2)

    app.tomatoSeeds = 5
    app.tomatoes = 0
    app.tomatoSeedInvX0 = (app.plantingX0+app.plantingSlot+app.plantingSide*2)
    app.tomatoSeedInvY0 = (app.plantingY0+app.plantingSlot+app.plantingTop*2)

    app.blackbSeeds = 5
    app.blackberries = 0
    app.blackbSeedInvX0 = (app.plantingX0+app.plantingSlot*2+app.plantingSide*3)
    app.blackbSeedInvY0 = (app.plantingY0+app.plantingSlot+app.plantingTop*2)

    # BLACKBERRIES
    app.blackb = app.loadImage('design-components/blackb.png')
    app.blackb = app.scaleImage(app.blackb,5)

    app.blackbSprout = app.loadImage('design-components/blackbsprout.png')
    app.blackbSprout = app.scaleImage(app.blackbSprout,3)

    app.blackbSmall = app.loadImage('design-components/blackbSmall.png')
    app.blackbSmall = app.scaleImage(app.blackbSmall,3)

    app.blackbMed = app.loadImage('design-components/blackbMed.png')
    app.blackbMed = app.scaleImage(app.blackbMed,3)

    app.blackbMat = app.loadImage('design-components/blackbMat.png')
    app.blackbMat = app.scaleImage(app.blackbMat,3)

    app.blackbFlower = app.loadImage('design-components/blackbFlower.png')
    app.blackbFlower = app.scaleImage(app.blackbFlower,3)

    app.blackbUnripe = app.loadImage('design-components/blackbUnripe.png')
    app.blackbUnripe = app.scaleImage(app.blackbUnripe,3)

    app.blackbFruit = app.loadImage('design-components/blackbFruit.png')
    app.blackbFruit = app.scaleImage(app.blackbFruit,3)

    app.blackb1 = app.loadImage('design-components/blackb1.png')
    app.blackb1 = app.scaleImage(app.blackb1,3)

    app.blackb2 = app.loadImage('design-components/blackb2.png')
    app.blackb2 = app.scaleImage(app.blackb2,3)

    app.blackb3 = app.loadImage('design-components/blackb3.png')
    app.blackb3 = app.scaleImage(app.blackb3,3)

    app.blackb4 = app.loadImage('design-components/blackb4.png')
    app.blackb4 = app.scaleImage(app.blackb4,3)

    app.blackb5 = app.loadImage('design-components/blackb5.png')
    app.blackb5 = app.scaleImage(app.blackb5,3)

    app.blackb6 = app.loadImage('design-components/blackb6.png')
    app.blackb6 = app.scaleImage(app.blackb6,3)

## strawberrries
    app.strawb = app.loadImage('design-components/strawb.png')
    app.strawb = app.scaleImage(app.strawb,5)

    app.strawbSprout = app.loadImage('design-components/strawbsprout.png')
    app.strawbSprout = app.scaleImage(app.strawbSprout,3)

    app.strawbSmall = app.loadImage('design-components/strawbSmall.png')
    app.strawbSmall = app.scaleImage(app.strawbSmall,3)

    app.strawbMed = app.loadImage('design-components/strawbMed.png')
    app.strawbMed = app.scaleImage(app.strawbMed,3)

    app.strawbMat = app.loadImage('design-components/strawbMat.png')
    app.strawbMat = app.scaleImage(app.strawbMat,3)

    app.strawbFlower = app.loadImage('design-components/strawbFlower.png')
    app.strawbFlower = app.scaleImage(app.strawbFlower,3)

    app.strawbUnripe = app.loadImage('design-components/strawbUnripe.png')
    app.strawbUnripe = app.scaleImage(app.strawbUnripe,3)

    app.strawbFruit = app.loadImage('design-components/strawbFruit.png')
    app.strawbFruit = app.scaleImage(app.strawbFruit,3)

    app.strawb1 = app.loadImage('design-components/strawb1.png')
    app.strawb1 = app.scaleImage(app.strawb1,3)

    app.strawb2 = app.loadImage('design-components/strawb2.png')
    app.strawb2 = app.scaleImage(app.strawb2,3)

    app.strawb3 = app.loadImage('design-components/strawb3.png')
    app.strawb3 = app.scaleImage(app.strawb3,3)

    app.strawb4 = app.loadImage('design-components/strawb4.png')
    app.strawb4 = app.scaleImage(app.strawb4,3)

    app.strawb5 = app.loadImage('design-components/strawb5.png')
    app.strawb5 = app.scaleImage(app.strawb5,3)

    ## Tomatoes
    app.tomato = app.loadImage('design-components/tomato.png')
    app.tomato = app.scaleImage(app.tomato,5)

    app.tomatoSprout = app.loadImage('design-components/tomatoSprout.png')
    app.tomatoSprout = app.scaleImage(app.tomatoSprout,3)

    app.tomatoSmall = app.loadImage('design-components/tomatoSmall.png')
    app.tomatoSmall = app.scaleImage(app.tomatoSmall,3)

    app.tomatoMed = app.loadImage('design-components/tomatoMed.png')
    app.tomatoMed = app.scaleImage(app.tomatoMed,3)

    app.tomatoMat = app.loadImage('design-components/tomatoMat.png')
    app.tomatoMat = app.scaleImage(app.tomatoMat,3)

    app.tomatoFlower = app.loadImage('design-components/tomatoFlower.png')
    app.tomatoFlower = app.scaleImage(app.tomatoFlower,3)

    app.tomatoUnripe = app.loadImage('design-components/tomatoUnripe.png')
    app.tomatoUnripe = app.scaleImage(app.tomatoUnripe,3)

    app.tomatoFruit = app.loadImage('design-components/tomatoFruit.png')
    app.tomatoFruit = app.scaleImage(app.tomatoFruit,3)

    app.tomato1 = app.loadImage('design-components/tomato1.png')
    app.tomato1 = app.scaleImage(app.tomato1,3)

    app.tomato2 = app.loadImage('design-components/tomato2.png')
    app.tomato2 = app.scaleImage(app.tomato2,3)

    app.tomato3 = app.loadImage('design-components/tomato3.png')
    app.tomato3 = app.scaleImage(app.tomato3,3)

    app.tomato4 = app.loadImage('design-components/tomato4.png')
    app.tomato4 = app.scaleImage(app.tomato4,3)

    app.tomato5 = app.loadImage('design-components/tomato5.png')
    app.tomato5 = app.scaleImage(app.tomato5,3)


    ## APPLES
    app.apple = app.loadImage('design-components/apple.png')
    app.apple = app.scaleImage(app.apple,5)

    app.appleSprout = app.loadImage('design-components/appleSprout.png')
    app.appleSprout = app.scaleImage(app.appleSprout,3)

    app.appleSmall = app.loadImage('design-components/appleSmall.png')
    app.appleSmall = app.scaleImage(app.appleSmall,3)

    app.appleMed = app.loadImage('design-components/appleMed.png')
    app.appleMed = app.scaleImage(app.appleMed,3)

    app.appleMat = app.loadImage('design-components/appleMat.png')
    app.appleMat = app.scaleImage(app.appleMat,3)

    app.appleFlower = app.loadImage('design-components/appleFlower.png')
    app.appleFlower = app.scaleImage(app.appleFlower,3)

    app.appleUnripe = app.loadImage('design-components/appleUnripe.png')
    app.appleUnripe = app.scaleImage(app.appleUnripe,3)

    app.appleFruit = app.loadImage('design-components/appleFruit.png')
    app.appleFruit = app.scaleImage(app.appleFruit,3)

    app.apple1 = app.loadImage('design-components/apple1.png')
    app.apple1 = app.scaleImage(app.apple1,3)

    app.apple2 = app.loadImage('design-components/apple2.png')
    app.apple2 = app.scaleImage(app.apple2,3)

    app.apple3 = app.loadImage('design-components/apple3.png')
    app.apple3 = app.scaleImage(app.apple3,3)

    app.apple4 = app.loadImage('design-components/apple4.png')
    app.apple4 = app.scaleImage(app.apple4,3)

    app.apple5 = app.loadImage('design-components/apple5.png')
    app.apple5 = app.scaleImage(app.apple5,3)

    ## LEMONS
    app.lemon = app.loadImage('design-components/lemon.png')
    app.lemon = app.scaleImage(app.lemon,5)

    app.lemonSprout = app.loadImage('design-components/lemonSprout.png')
    app.lemonSprout = app.scaleImage(app.lemonSprout,3)

    app.lemonSmall = app.loadImage('design-components/lemonSmall.png')
    app.lemonSmall = app.scaleImage(app.lemonSmall,3)

    app.lemonMed = app.loadImage('design-components/lemonMed.png')
    app.lemonMed = app.scaleImage(app.lemonMed,3)

    app.lemonMat = app.loadImage('design-components/lemonMat.png')
    app.lemonMat = app.scaleImage(app.lemonMat,3)

    app.lemonFlower = app.loadImage('design-components/lemonFlower.png')
    app.lemonFlower = app.scaleImage(app.lemonFlower,3)

    app.lemonUnripe = app.loadImage('design-components/lemonUnripe.png')
    app.lemonUnripe = app.scaleImage(app.lemonUnripe,3)

    app.lemonFruit = app.loadImage('design-components/lemonFruit.png')
    app.lemonFruit = app.scaleImage(app.lemonFruit,3)

    app.lemon1 = app.loadImage('design-components/lemon1.png')
    app.lemon1 = app.scaleImage(app.lemon1,3)

    app.lemon2 = app.loadImage('design-components/lemon2.png')
    app.lemon2 = app.scaleImage(app.lemon2,3)

    app.lemon3 = app.loadImage('design-components/lemon3.png')
    app.lemon3 = app.scaleImage(app.lemon3,3)

    app.lemon4 = app.loadImage('design-components/lemon4.png')
    app.lemon4 = app.scaleImage(app.lemon4,3)

    app.lemon5 = app.loadImage('design-components/lemon5.png')
    app.lemon5 = app.scaleImage(app.lemon5,3)

    ## PEACHES
    app.peach = app.loadImage('design-components/peach.png')
    app.peach = app.scaleImage(app.peach,5)

    app.peachSprout = app.loadImage('design-components/peachSprout.png')
    app.peachSprout = app.scaleImage(app.peachSprout,3)

    app.peachSmall = app.loadImage('design-components/peachSmall.png')
    app.peachSmall = app.scaleImage(app.peachSmall,3)

    app.peachMed = app.loadImage('design-components/peachMed.png')
    app.peachMed = app.scaleImage(app.peachMed,3)

    app.peachMat = app.loadImage('design-components/peachMat.png')
    app.peachMat = app.scaleImage(app.peachMat,3)

    app.peachFlower = app.loadImage('design-components/peachFlower.png')
    app.peachFlower = app.scaleImage(app.peachFlower,3)

    app.peachUnripe = app.loadImage('design-components/peachUnripe.png')
    app.peachUnripe = app.scaleImage(app.peachUnripe,3)

    app.peachFruit = app.loadImage('design-components/peachFruit.png')
    app.peachFruit = app.scaleImage(app.peachFruit,3)

    app.peach1 = app.loadImage('design-components/peach1.png')
    app.peach1 = app.scaleImage(app.peach1,3)

    app.peach2 = app.loadImage('design-components/peach2.png')
    app.peach2 = app.scaleImage(app.peach2,3)

    app.peach3 = app.loadImage('design-components/peach3.png')
    app.peach3 = app.scaleImage(app.peach3,3)

    app.invImages = [[app.apple,app.peach,app.lemon],
        [app.strawb,app.tomato,app.blackb]]

    app.isPlanting = False
    app.currSeed = None

    app.currTemp = 75
    app.minTemp = 40
    app.maxTemp = 100

    app.level = 1
    app.oldLevel = 0

    # dictionary mapping level to generated terrain
    app.terrain = makeTerrain(app)
    app.cellSize = 10
    app.rows,app.cols = 70,90
    app.board = [[0]*app.cols for row in range(app.rows)]
    updateBoard(app.terrain,app.board)
    updateSeedInv(app)

    app.completeWidth,app.completeHeight = getFullTerrain(app)

    # for screen scrolling
    app.displayRows = [0,70]
    app.displayCols = [0,90]
    app.walkBoxX0,app.walkBoxX1 = (200,700)

    app.charX,app.charY = (400,450)
    app.spriteCounter = 0
    app.cameraOffsetX = 0
    app.direction = 'Down'
 
    # sprite sheet
    playerSpriteSheet = 'design-components/sprites.png'
    app.spriteSheet = app.loadImage(playerSpriteSheet)
    app.spriteSheet = app.scaleImage(app.spriteSheet,2.5) 
    app.spriteHeight,app.spriteWidth = app.spriteSheet.size

    app.sprites = {}
    spriteCrop(app)

def appStopped(app):
    # stop bgm when closing
    app.sound.stop()

def getFullTerrain(app):
    # get size of full terrain
    terrainHeight = app.cellSize * len(app.board[0])
    terrainWidth = app.cellSize * len(app.board)
    return terrainWidth,terrainHeight

def spriteCrop(app):
    # sprite sheet cropping
    app.sprites = {}
    imageWidth,imageHeight = app.spriteSheet.size
    for direction in ('Down0','Left1','Right2','Up3'):
        ind = int(direction[-1:])
        newDir = direction[:-1]
        topLeftY = ind*imageHeight/4
        botRightY = (ind + 1)*imageHeight/4
        tempSprites = []
        for j in range(4):
            topLeftX = j * imageWidth/4
            botRightX = (j+1) * imageWidth/4
            sprite = app.spriteSheet.crop((topLeftX,topLeftY,botRightX,botRightY))
            tempSprites.append(sprite)
        app.sprites[newDir] = tempSprites

def updateDisplay(app):
    # move camera function adapted for row/col display
    if app.level>1:
        dcol = app.cameraOffsetX // app.cellSize
        app.displayCols[0] += dcol
        app.displayCols[1] += dcol

def timerFired(app):
    # initiate night mode and check for plant growth and level up
    app.timeElapsed += 10  
        
    if (app.mode!='exitMode' and app.mode!='startMode' and app.mode!='nightMode'
         and app.timeElapsed >= 1200 and app.isHome==False) or (app.isHome):
         # check of everything (growth, level) at night
        app.goHome = False
        checkForGrowth(app)
        totalPlants =  (len(app.allSeedClasses) + len(app.allPlantClasses))
        newLevel = totalPlants//5 + 1
        app.oldLevel = app.level
        if newLevel > app.level:
            levelUp(app)
            app.level = newLevel
        app.mode = 'nightMode'
        nightMode_reduceWater(app)
        app.timeElapsed = 0
    

def makeTerrain(app):
    # makes terrain to app.terrain dict
    gameHeight = app.height-app.menuButtonHeight
    voronoiPoints = voronoiSeeds(app.width,gameHeight)
    return getClosestSeeds(voronoiPoints,app.width,gameHeight)

def updateBoard(terrain,board):
    # makes terrain representative on board with numbers
    terrains = [0,1,2,3,4]
    colorPairs = []
    i = 0
    # seed point
    for seed in terrain:
        terrainType = terrains[i]
        i += 1
        # list of point and terrain type number tuples
        colorPairs.append((seed,terrainType))
    
    for seedPair in colorPairs:
        terrainType = seedPair[1]
        seed = seedPair[0]
        for (row,col) in terrain[seed]:
            board[row][col] = terrainType
    return board

def movePlayer(app,dy,dx):
    # move player and check for bounds
    app.spriteCounter = (app.spriteCounter + 1)%4
    app.charX += dx
    app.charY += dy

    if (app.level>1 and ((app.charX <= app.walkBoxX0 and app.direction=='Left') or 
        (app.charX>=app.walkBoxX1 and app.direction=='Right'))):
    
        if ((app.displayCols[0]==0 and app.direction=='Left') or 
            (app.displayCols[1]==app.cols and app.direction=='Right')):
            # if traveling towards edge and reach the end
            app.cameraOffsetX = 0
            if (app.charX<=5 or app.charX>app.width-10):
                app.charX -= dx
            if (app.charY < app.menuButtonHeight + 10 or 
                app.charY+30 > app.height):
                app.charY -= dy

        elif ((app.displayCols[0]==0 and app.displayCols[1]!=app.cols) or 
            (app.displayCols[0]!=0 and app.displayCols[1]==app.cols) or 
            (app.displayCols[0]!=0 and app.displayCols[0]!=0)):
            # if display cols are not the edges of the screen
            app.charX -= dx
            app.cameraOffsetX = dx
            updateDisplay(app)

    else:
        if (app.charX<=5 or app.charX>app.width-10):
            app.charX -= dx
        if (app.charY < app.menuButtonHeight + 10 or 
            app.charY+30 > app.height):
            app.charY -= dy
    
    
def keyPressed(app,event):
    # moved character and ends the day early if 'h'
    dy,dx = 0,0
    if event.key == 'Up':
        dy = -10
        app.direction = 'Up'
        movePlayer(app,dy,dx)
    elif event.key == 'Down':
        app.direction = 'Down'
        dy = +10
        movePlayer(app,dy,dx)
    elif event.key == 'Right':
        app.direction = 'Right'
        dx = +10
        movePlayer(app,dy,dx)
    elif event.key == 'Left':
        app.direction = 'Left'
        dx = -10
        movePlayer(app,dy,dx)
    
    if event.key in {'H','h'}:
        app.graph = makeGraphFromBoard(app.board)
        startRow,startCol = getBoardRowCol(app,app.charX,app.charY)
        start = (startRow,startCol)
        target = (app.homeRow,app.homeCol)
        app.pathHome = dijkstra(app.graph,start,target)
        app.goHome = True
        app.isHome = False
        app.timeElapsed = 0

    # use enter key to pick seed and start planting
    if app.openPlanting and app.currSeed!=None and event.key=='Enter':
        app.openPlanting = False
        app.isPlanting = True

def getCoord(app,row,col):
    # get coords from row col
    offset = app.displayCols[0]*app.cellSize
    x0 =  col * app.cellSize - offset
    y0 = row * app.cellSize + app.menuButtonHeight
    return (x0, y0)


def mousePressed(app,event):
    # most of gameplay -- changes boolean flags for graphics, planting, watering, etc.
    app.cx,app.cy = event.x,event.y

    # exit game
    if clickedOn(app.cx,app.cy,0,0,app.exitWidth,app.exitHeight):
        app.mode = 'exitMode'

    # open/close inventory
    elif clickedOn(app.cx,app.cy,50,0,50+app.menuButtonWidth,
        app.menuButtonHeight):
        app.openInventory = True
        app.openPlanting = False 
        app.isPlanting = False
        app.isHarvest = False
        app.isWatering = False
    elif (app.openInventory) and clickedOn(app.cx,app.cy,app.closePlantX0,
        app.closePlantY0,app.closePlantingHeight,app.closePlantingHeight):
        app.openInventory = False
    
    #open/close planting
    if clickedOn(app.cx,app.cy,app.plantButtonX0,app.plantButtonY0,
                                app.menuButtonWidth,app.menuButtonHeight):
        app.openPlanting = True
        app.openInventory = False
        app.isPlanting = False
        app.isHarvest = False
        app.isWatering = False
    elif (app.openPlanting) and clickedOn(app.cx,app.cy,app.closePlantX0,
        app.closePlantY0,app.closePlantingHeight,app.closePlantingHeight):
        app.openPlanting = False
    
    if (app.openPlanting):
        # pick the seed to plant only if there are seeds
        if clickedOn(app.cx,app.cy,app.appleSeedInvX0,app.appleSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'apple'
            if app.appleSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.peachSeedInvX0,app.peachSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'peach'
            if app.peachSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.lemonSeedInvX0,app.lemonSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'lemon'
            if app.lemonSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.strawbSeedInvX0,app.strawbSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'strawb'
            if app.strawbSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.tomatoSeedInvX0,app.tomatoSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'tomato'
            if app.tomatoSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.blackbSeedInvX0,app.blackbSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'blackb'
            if app.blackbSeeds < 1:
                app.currSeed = None
        
        # start removing plants
        if clickedOn(app.cx,app.cy,app.unplantX0,app.unplantY0,
            app.unplantWidth,app.unplantHeight):
            app.removingPlants = True
            app.openPlanting = False
            app.isPlanting = False
            app.isWatering = False
            app.isHarvest = False
    
    if app.isPlanting and app.openPlanting==False:
        # planting seed 
        (row,col) = getBoardRowCol(app,app.cx,app.cy)

        # if in the right terrain
        if (app.currSeed in ['apple','lemon','peach'] and (app.board[row][col]==1
                 or app.board[row][col]==3)):
            if isLegalTree(app,row,col,5,1,3):
                treeOnBoard(app,row,col,5)
                app.treePoints[app.currSeed].append((row+2,col))
                startSeed(app,row+2,col)
                app.isPlanting = False
                updateSeeds(app)

        elif (app.currSeed in ['strawb','blackb','tomato'] and 
                (app.board[row][col]==2 or app.board[row][col]==4)):
            if isLegalPlant(app,row,col,6,2,4):
                plantOnBoard(app,row,col,6)
                app.plantPoints[app.currSeed].append((row+1,col))
                startSeed(app,row+1,col)
                app.isPlanting = False
                updateSeeds(app)

    if app.openPlanting==False and app.removingPlants:
        # remove plants
        (row,col) = getBoardRowCol(app,app.cx,app.cy)

        if app.board[row][col] in (50,51,52,53,54,55,56,'apple','lemon','peach'):
            removeTree(app,row,col)
        elif app.board[row][col] in (60,61,62,63,64,65,66,'tomato','strawb','blackb'):
            removePlant(app,row,col)
        elif clickedOn(app.cx,app.cy,app.stopRemoveX0,app.stopRemoveY0,
            app.stopRemoveWidth,app.stopRemoveHeight):
            app.removingPlants = False

    # water plants
    if (app.isPlanting==False and 
        clickedOn(app.cx,app.cy,app.waterStartX0,app.waterStartY0,
            app.waterStartWidth,app.waterStartHeight)):
        app.isWatering = True
        app.openPlanting = False
        app.currSeed = None
        app.isPlanting = False
        app.openInventory = None
        app.isHarvest = False
        app.removingPlants = False
    
    elif clickedOn(app.cx,app.cy,app.waterStopX0,app.waterStopY0,
        app.waterStopWidth,app.waterStopHeight) and app.isWatering:
        app.isWatering = False
    
    if app.isWatering:
        # update class and water
        (row,col) = getBoardRowCol(app,app.cx,app.cy)
        changeWaterLevel(app,row,col,True)

    # start harvesting fruits
    if clickedOn(app.cx,app.cy,app.harvestingX0,app.harvestingY0,
        app.menuButtonWidth,app.menuButtonHeight):
        app.isHarvest = True
        app.openPlanting = False
        app.isWatering = False
        app.openInventory = False
        app.removingPlants = False
        app.isPlanting = False
    elif clickedOn(app.cx,app.cy,app.harvestStopX0,app.harvestStopY0,
        app.harvestStopWidth,app.harvestStopHeight):
        app.isHarvest = False
    
    if app.isHarvest:
        # update fruit and seeds from harvest
        (row,col) = getBoardRowCol(app,app.cx,app.cy)

        if (row,col) in app.allPlantClasses:
            plant = app.allPlantClasses[(row,col)]
            if plant.stage==7 and plant.numFruits > 0:
                plant.pickFruit()
                fruit = plant.type
                updateFruits(app,fruit)
    
    # click ok button to go home
    if app.goHome and app.isHome==False:
        if clickedOn(app.cx,app.cy,app.homeOkX0,app.homeOkY0,
            app.homeOkWidth,app.homeOkHeight):
            app.isHome = True

def levelUp(app):
    # extend board for additional terrain when leveling up
    newBoard = [[0]*90 for row in range(70)]
    newTerrain = makeTerrain(app)
    newBoard = updateBoard(newTerrain,newBoard)

    for row in range(app.rows):
        app.board[row] += newBoard[row]
    app.rows,app.cols = len(app.board),len(app.board[0])

    app.completeWidth,app.completeHeight = getFullTerrain(app)


def updateFruitInv(app):
    # update inventory display
    app.invItems[0][0][1] = app.apples
    app.invItems[0][1][1] = app.peaches
    app.invItems[0][2][1] = app.lemons
    app.invItems[1][0][1] = app.strawberries
    app.invItems[1][1][1] = app.tomatoes
    app.invItems[1][2][1] = app.blackberries
            
def updateFruits(app,type):
    # update fruit/seed counds when harvesting
    if type=='apple':
        app.apples += 1
        app.appleSeeds += 1
    elif type=='peach':
        app.peaches += 1
        app.peachSeeds += 1
    elif type=='lemon':
        app.lemons += 1
        app.lemonSeeds += 1
    elif type=='strawb':
        app.strawberries += 1
        app.strawbSeeds += 1
    elif type=='tomato':
        app.tomatoes += 1
        app.tomatoSeeds += 1
    elif type=='blackb':
        app.blackberries += 1
        app.blackbSeeds += 1
    updateFruitInv(app)

def changeWaterLevel(app,row,col,watering):
    # change water and change soil
        for treeType in app.treePoints:
            coord = (row,col)
            if (coord in app.treePoints[treeType] and 
                coord in app.allSeedClasses): # if seed
                seed = app.allSeedClasses[coord]
                if watering: # water the plant
                    seed.waterPlant()
                status = getWaterState(seed)
                changeSoilColor(app,row,col,'tree',status)
            elif (coord in app.treePoints[treeType] and 
                coord in app.allPlantClasses): # if plant (aka grew from seed)
                plant = app.allPlantClasses[coord]
                if watering:
                    plant.waterPlant()
                status = getWaterState(plant)
                changeSoilColor(app,row,col,'tree',status)
        
        for plantType in app.plantPoints:
            coord = (row,col)
            if (coord in app.plantPoints[plantType] and 
                coord in app.allSeedClasses):
                seed = app.allSeedClasses[coord]
                if watering:
                    seed.waterPlant()
                status = getWaterState(seed)
                changeSoilColor(app,row,col,'plant',status)
            elif (coord in app.plantPoints[plantType] and 
                coord in app.allPlantClasses):
                plant = app.allPlantClasses[coord]
                if watering:
                    plant.waterPlant()
                status = getWaterState(plant)
                changeSoilColor(app,row,col,'plant',status)

def getWaterState(plant):
    # get water state of plant
    if plant.isOverwatered:
        return 'overwatered'
    elif plant.isDry:
        return 'dry'


def changeSoilColor(app,row,col,type,status):
    # change soil color once watered
    if type=='tree':
        for drow in range(-4,+1):
            for dcol in range(-2,3):
                newRow = row + drow
                newCol = col + dcol
                if newCol!=col or newRow!=row:
                    if status=='overwatered':
                        app.board[newRow][newCol] = 101
                    elif status=='dry':
                        app.board[newRow][newCol] = 99
                    else:
                        app.board[newRow][newCol] = 100
    elif type=='plant':
        for drow in range(-2,+1):
            for dcol in range(-1,2):
                newRow = row + drow
                newCol = col + dcol
                if newCol!=col or newRow!=row:
                    if newCol!=col or newRow!=row:
                        if status=='overwatered':
                            app.board[newRow][newCol] = 101
                        elif status=='dry':
                            app.board[newRow][newCol] = 99
                        else:
                            app.board[newRow][newCol] = 100


def removeTree(app,row,col):
    # remove tree from board and update lists/dictionaries holding it
    for drow in range(-5,1):
        for dcol in range(-2,4):
            newRow = row + drow
            newCol = col + dcol
            app.board[newRow][newCol] = 1
    for treeType in app.treePoints:
        if (row,col) in app.treePoints[treeType]:
            app.treePoints[treeType].remove((row,col))
            if treeType == 'apple':
                app.appleSeeds += 1
            elif treeType == 'peach':
                app.peachSeeds += 1
            elif treeType == 'lemon':
                app.lemonSeeds += 1
    if (row,col) in app.allSeedClasses:
        app.allSeedClasses.pop((row,col))
    elif (row,col) in app.allPlantClasses:
        app.allPlantClasses.pop((row,col))
    updateSeeds(app)

def removePlant(app,row,col):
    # remove plant and update lists/dictionaries holding it
    for drow in range(-2,1):
        for dcol in range(-1,3):
            newRow = row + drow
            newCol = col + dcol
            app.board[newRow][newCol] = 2
    for plantType in app.plantPoints:
        if (row,col) in app.plantPoints[plantType]:
            app.plantPoints[plantType].remove((row,col))
            if plantType == 'strawb':
                app.strawbSeeds += 1
            elif plantType == 'tomato':
                app.tomatoSeeds += 1
            elif plantType == 'blackb':
                app.blackbSeeds += 1
    if (row,col) in app.allSeedClasses:
        app.allSeedClasses.pop((row,col))
    elif (row,col) in app.allPlantClasses:
        app.allPlantClasses.pop((row,col))
    updateSeeds(app)



def updateSeedInv(app):
    # update seed inventory for display
    app.seedInv[0][0][1]= app.appleSeeds
    app.seedInv[0][1][1] = app.peachSeeds
    app.seedInv[0][2][1] = app.lemonSeeds
    app.seedInv[1][0][1] = app.strawbSeeds
    app.seedInv[1][1][1] = app.tomatoSeeds
    app.seedInv[1][2][1] = app.blackbSeeds


def updateSeeds(app):
    # update seed inventory
    if app.currSeed=='apple':
        app.appleSeeds -= 1
    elif app.currSeed =='peach':
        app.peachSeeds -= 1
    elif app.currSeed == 'lemon':
        app.lemonSeeds -= 1
    elif app.currSeed == 'strawb':
        app.strawbSeeds -= 1
    elif app.currSeed == 'tomato':
        app.tomatoSeeds -= 1
    elif app.currSeed == 'blackb':
        app.blackbSeeds -= 1
    app.currSeed = None
    updateSeedInv(app)

def treeOnBoard(app,row,col,plantType):
    # place tree on app.board
    for drow in (-2,-1,0,+1,+2):
        for dcol in (-2,-1,0,+1,+2):
            newRow = row + drow
            newCol = col + dcol
            if ((drow == +2) and (dcol==0)):
                app.board[newRow][newCol] = 50
            else:
                app.board[newRow][newCol] = plantType

def plantOnBoard(app,row,col,plantType):
    # place plant on app.board
    for drow in (-1,0,+1):
        for dcol in (-1,0,+1):
            newRow = row + drow
            newCol = col + dcol
            if ((drow == +1) and (dcol==0)):
                app.board[newRow][newCol] = 60
            else:
                app.board[newRow][newCol] = plantType

def isLegalTree(app,row,col,plantType,terrainType1,terrainType2):
    # plots cannot overlap and must be spaced out
    for drow in (list(range(-8,8))):
        for dcol in (list(range(-5,5))):
            newRow = row + drow
            newCol = col + dcol
            if (newRow<2 or newCol<2 or newRow>(app.rows-3) or 
                                            newCol>(app.cols-3)):
                return False
            elif ((app.board[newRow][newCol]==plantType or 
                (app.board[newRow][newCol]!=terrainType1 and 
                app.board[newRow][newCol]!=terrainType2))):
                return False

    return True

def isLegalPlant(app,row,col,plantType,terrainType1,terrainType2):
    # plots cannot overlap and must be spaced out
    for drow in (list(range(-6,6))):
        for dcol in (list(range(-4,4))):
            newRow = row + drow
            newCol = col + dcol
            if (newRow<2 or newCol<2 or newRow>(app.rows-3) or 
                                            newCol>(app.cols-3)):
                return False
            elif ((app.board[newRow][newCol]==plantType or 
                (app.board[newRow][newCol]!=terrainType1 and 
                app.board[newRow][newCol]!=terrainType2))):
                return False

    return True


def getBoardRowCol(app,x,y):
    # get row col given x y
    row = int((y - app.menuButtonHeight) / app.cellSize)
    col = int(x / app.cellSize) + app.displayCols[0]
    return (row,col)


def startSeed(app,row,col):
    # start a new seed class
    coord = (row,col)
    newSeed = NewPlant(coord,app.currSeed)
    app.allSeedClasses[coord] = newSeed

def checkForGrowth(app):
    # check plant's growth state every night and update board
    removing = []
    for coord in app.allPlantClasses:
        # check all plants
        plant = app.allPlantClasses[coord]
        if isinstance(plant,Seed) and plant.growth>=4:
            # manually upgrade seed to plant
            if plant.type in {'peach','apple','lemon'}:
                newPlant = Tree(plant.coord,plant.type)
                app.allPlantClasses[coord] = newPlant

            else:
                newPlant = Plant(plant.coord,plant.type)
                app.allPlantClasses[coord] = newPlant

        plant.checkTemp(app.currTemp)
        plant.growPlant()
        plant.checkGrowth(plant.type)
        (row,col) = plant.coord

        if plant.stage == 2:
            # if small plant/tree
            if plant.type in {'apple','peach','lemon'}:
                app.board[row][col] = 51
            elif plant.type in {'strawb','blackb','tomato'}:
                app.board[row][col] = 61
        elif plant.stage == 3:
            # if med plant/tree
            if plant.type in {'apple','peach','lemon'}:
                app.board[row][col] = 52
            elif plant.type in {'strawb','blackb','tomato'}:
                app.board[row][col] = 62
        elif plant.stage == 4:
            # if mature plant/tree
            if plant.type in {'apple','peach','lemon'}:
                app.board[row][col] = 53
            elif plant.type in {'strawb','blackb','tomato'}:
                app.board[row][col] = 63
        elif plant.stage == 5:
            # flowering
            if plant.type in {'apple','peach','lemon'}:
                app.board[row][col] = 54
            elif plant.type in {'strawb','blackb','tomato'}:
                app.board[row][col] = 64
        elif plant.stage == 6:
            # unripe
            if plant.type in {'apple','peach','lemon'}:
                app.board[row][col] = 55
            elif plant.type in {'strawb','blackb','tomato'}:
                app.board[row][col] = 65
        elif plant.stage == 7:
            # fruiting
            app.board[row][col] = plant.type
            if plant.numFruits==0:
                plant.growFruit()


    removing = [] # remove seeds when they become plants
    for coord in app.allSeedClasses:
        # check all seeds, upgrade to plant if needed
        plant = app.allSeedClasses[coord]
        plant.checkTemp(app.currTemp) 
        plant.growPlant() 
        if plant.growth>=4:
            sprout = Seed(coord,plant.type)
            removing.append((coord))
            app.allPlantClasses[coord] = sprout

    if removing != []:
        for coord in removing:
            app.allSeedClasses.pop(coord)
        removing = []


####################
#### START MODE ####
####################

def startMode_redrawAll(app,canvas):
    # starting screen
    drawStartScreen(app,canvas)

def drawStartScreen(app,canvas):
    # drawing start screen and option to load a saved file or start new
    x0,y0,x1,y1 = (0,0,app.width,app.height)
    canvas.create_rectangle(x0,y0,x1,y1,fill='#bcdba2')
    titleX0 = 150
    titleY0 = 100
    titleWidth = 600
    titleHeight = 150
    canvas.create_rectangle(titleX0,titleY0,titleX0+titleWidth,
                            titleY0+titleHeight,width=2)
    canvas.create_text(titleX0+(titleWidth/2),titleY0+(titleHeight/2),
                text='GENTLE GARDEN',font='Courier 50 bold italic',fill='black')
    
    canvas.create_rectangle(app.newX0,app.newY0,app.newX0+app.newWidth,
                            app.newY0+app.newHeight,fill='white')
    canvas.create_text(app.newX0+(app.newWidth/2),app.newY0+(app.newHeight/2),
                    text='start new game',font='Courier 18')

    canvas.create_rectangle(app.oldX0,app.oldY0,app.oldX0+app.newWidth,
                        app.oldY0+app.newHeight,fill='white')
    canvas.create_text(app.oldX0+(app.newWidth/2),app.oldY0+(app.newHeight/2),
                    text='load saved game',font='Courier 18')

def startMode_mousePressed(app,event):
    app.cx,app.cy = (event.x,event.y)
    # new game
    if clickedOn(app.cx,app.cy,app.newX0,app.newY0,app.newWidth,app.newHeight):
        app.isNewGame = True
        app.mode = None
    # load saved game
    elif clickedOn(app.cx,app.cy,app.oldX0,app.oldY0,
                                            app.newWidth,app.newHeight):
        app.isNewGame = False
        openFile(app)
        app.mode = None

###################
#### EXIT MODE ####
###################

def exitMode_redrawAll(app,canvas):
    # draw exiting screen with option to save or not save or return
    canvas.create_rectangle(0,0,app.width,app.height,fill='#bcdba2')
    canvas.create_text(450,175,text='LEAVING GENTLE GARDEN...',
        font='Courier 40 bold italic',fill='black')

    canvas.create_rectangle(app.exitSaveX0,app.exitSaveY0,
        app.exitSaveX0+app.exitSaveWidth,
        app.exitSaveY0+app.exitSaveHeight,fill='white')
    canvas.create_text(app.exitSaveX0+app.exitSaveWidth/2,
        app.exitSaveY0+app.exitSaveHeight/2,text='save progress',
        font='Courier 14')
    
    canvas.create_rectangle(app.exitCloseX0,app.exitCloseY0,
        app.exitCloseX0+app.exitSaveWidth,
        app.exitCloseY0+app.exitSaveHeight,fill='white')
    canvas.create_text(app.exitCloseX0+app.exitSaveWidth/2,
        app.exitCloseY0+app.exitSaveHeight/2,
        text='exit without saving',font='Courier 14')
    
    canvas.create_text(app.exitCancelX0+app.exitCancelWidth/2,
        app.exitCancelY0+app.exitCancelHeight/2,
        text='cancel',font='Courier 12',fill='black')

def exitMode_mousePressed(app,event):
    app.cx,app.cy = (event.x,event.y)
    
    # don't save
    if clickedOn(app.cx,app.cy,app.exitCloseX0,app.exitCloseY0,
                app.exitSaveWidth,app.exitSaveHeight):
        return
    # save progress
    elif clickedOn(app.cx,app.cy,app.exitSaveY0,app.exitSaveY0,
        app.exitSaveWidth,app.exitSaveHeight):
        saveFile(app)
    elif clickedOn(app.cx,app.cy,app.exitCancelX0,app.exitCancelY0,
        app.exitCancelWidth,app.exitCancelHeight):
        app.mode = None


def updateTemp(app):
    # change temperature
    tempChange = random.randint(-10,10)
    newTemp = app.currTemp + tempChange
    if newTemp>app.maxTemp:
        newTemp = app.maxTemp
    elif newTemp<app.minTemp:
        newTemp = app.minTemp
    app.currTemp = newTemp

def saveFile(app):
    # save game state
    saveItems = (app.day,app.width,app.height,app.invItems,app.seedInv,
        app.treePoints,app.plantPoints,app.allSeedClasses,app.allPlantClasses,
        app.appleSeeds,app.apples,app.peachSeeds,app.peaches,app.lemonSeeds,
        app.lemons,app.strawbSeeds,app.strawberries,app.tomatoSeeds,
        app.tomatoes,app.blackbSeeds,app.blackberries,app.currTemp,app.level,
        app.board,app.rows,app.cols,app.displayRows,app.displayCols,app.spriteCounter,
        app.cameraOffsetX)
    f = open('gamestate.pickle','wb')
    pickle.dump(saveItems,f)
    f.close()

def openFile(app):
    # reload past game state
    f = open('gamestate.pickle','rb')
    (app.day,app.width,app.height,app.invItems,app.seedInv,
        app.treePoints,app.plantPoints,app.allSeedClasses,app.allPlantClasses,
        app.appleSeeds,app.apples,app.peachSeeds,app.peaches,app.lemonSeeds,
        app.lemons,app.strawbSeeds,app.strawberries,app.tomatoSeeds,
        app.tomatoes,app.blackbSeeds,app.blackberries,app.currTemp,app.level,
        app.board,app.rows,app.cols,app.displayRows,app.displayCols,app.spriteCounter,
        app.cameraOffsetX) = pickle.load(f)
    f.close()

####################
#### NIGHT MODE ####
####################

def nightMode_timerFired(app):
    # end night, increase day, and reposition character if needed
    app.timeElapsed += 10
    if app.timeElapsed >= 350:
        updateTemp(app)
        app.day += 1
        app.isHome = False
        if app.level > app.oldLevel:
            app.charX,app.charY = (400,450)
        app.mode = None
        app.timeElapsed = 0

def nightMode_reduceWater(app):
    # decrease water level each night so user must water again when needed
    for coord in app.allPlantClasses:
        plant = app.allPlantClasses[coord]
        plant.waterOvernight()
        row,col = coord
        changeWaterLevel(app,row,col,False)
    
    for coord in app.allSeedClasses:
        seed = app.allSeedClasses[coord]
        seed.waterOvernight()
        row,col = coord
        changeWaterLevel(app,row,col,False)
        
def nightMode_redrawAll(app,canvas):
    # draw night screen
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')
    canvas.create_text(app.width/2,app.height/2,text='it is night.',
        font='Courier 16',fill='white')
    canvas.create_text(app.width/2,app.height/2+50,
        text='your plants are growing!',font='Courier 16',fill='white')

#################

def redrawAll(app,canvas):
    # call helper drawing functions with boolean flags
    drawTerrain(app,canvas)
    drawMenuHead(app,canvas)

    spriteImage = app.sprites[app.direction][app.spriteCounter]
    canvas.create_image(app.charX,
        app.charY,image=ImageTk.PhotoImage(spriteImage))

    if app.openInventory:
        drawInventory(app,canvas)
    elif app.openPlanting:
        drawPlanting(app,canvas)
    elif app.removingPlants:
        drawStopRemove(app,canvas)
    elif app.isWatering:
        drawStopWater(app,canvas)
    elif app.isHarvest:
        drawStopHarvest(app,canvas)
    
    if app.goHome:
        drawGoHome(app,canvas)

def drawGoHome(app,canvas):
    # draw pop up with path home to end the day early
    for (row,col) in app.pathHome:
        x0,y0 = getCoord(app,row,col)

        canvas.create_rectangle(x0,y0,x0+app.cellSize,y0+app.cellSize,
                fill='#ffd9ee')
    canvas.create_rectangle(300,10,700,80,fill='white')
    canvas.create_text(500,30,text="it's the end of the day!",font='Courier 12')
    canvas.create_text(500,40,text="here is the path you will have taken to go home.",
        font='Courier 12')
    canvas.create_rectangle(app.homeOkX0,app.homeOkY0,
        app.homeOkX0+app.homeOkWidth,app.homeOkY0+app.homeOkHeight)
    canvas.create_text(app.homeOkX0+app.homeOkWidth/2,
        app.homeOkY0+app.homeOkHeight/2,text='ok',font='Courier 13')
    
def drawStopHarvest(app,canvas):
    # button to stop picking fruits
    canvas.create_rectangle(app.harvestStopX0,app.harvestStopY0,
        app.harvestStopX0+app.harvestStopWidth,
        app.harvestStopY0+app.harvestStopHeight)
    canvas.create_text(app.harvestStopX0+app.harvestStopWidth/2,
        app.harvestStopY0+app.harvestStopHeight/2,text='finish harvest',
            font='Courier 10')

def drawStopWater(app,canvas):
    # button to stop watering
    canvas.create_rectangle(app.waterStopX0,app.waterStopY0,
        app.waterStopX0+app.waterStopWidth,app.waterStopY0+app.waterStopHeight)
    canvas.create_text(app.waterStopX0+app.waterStopWidth/2,
        app.waterStopY0+app.waterStopHeight/2,text='finish watering',
            font='Courier 10')

def drawStopRemove(app,canvas):
    # button to stop removing plants
    canvas.create_rectangle(app.stopRemoveX0,app.stopRemoveY0,
        app.stopRemoveX0+app.stopRemoveWidth,  
        app.stopRemoveY0+app.stopRemoveHeight)
    canvas.create_text(app.stopRemoveX0+app.stopRemoveWidth/2,
        app.stopRemoveY0+app.stopRemoveHeight/2,text='finish',font='Courier')


def drawTerrain(app,canvas):
    # draw terrain based on row,col value on board
    images = []
    offset = app.displayCols[0]*app.cellSize
    for row in range(app.displayRows[1]):
        for col in range(app.displayCols[0],app.displayCols[1]):
            color = getTerrainColor(app,row,col)
            x0 = col*app.cellSize - offset
            y0 = row*app.cellSize + app.menuButtonHeight
            x1 = x0 + app.cellSize
            y1 = y0 + app.cellSize + app.menuButtonHeight

            if isinstance(color,tuple)==False:
                canvas.create_rectangle(x0,y0,x1,y1,fill=color)

            else:
                img = getImage(app,color)
                images.append([img,x0,y0])
    for image in images: # if an image/plant
        img = image[0]
        x0 = image[1]
        y0 = image[2]
        canvas.create_image(x0+app.cellSize/2,y0+app.cellSize/2,
            image=ImageTk.PhotoImage(img),anchor='s')
        

def getImage(app,imagePair):
    # get the right image depending on the plant type and growth stage
    plantType = imagePair[0]
    stage = imagePair[1]
    if plantType=='apple':
        if stage=='sprout':
            return app.appleSprout
        elif stage=='small':
            return app.appleSmall
        elif stage=='med':
            return app.appleMed
        elif stage=='mat':
            return app.appleMat
        elif stage=='flower':
            return app.appleFlower
        elif stage=='unripe':
            return app.appleUnripe
        elif stage=='fruit' or stage==6:
            return app.appleFruit
        elif stage==1: # if there is one apple (user has picked the rest)
            return app.apple1
        elif stage==2:
            return app.apple2
        elif stage==3:
            return app.apple3
        elif stage==4:
            return app.apple4
        elif stage==5:
            return app.apple5
    elif plantType=='peach':
        if stage=='sprout':
            return app.peachSprout
        elif stage=='small':
            return app.peachSmall
        elif stage=='med':
            return app.peachMed
        elif stage=='mat':
            return app.peachMat
        elif stage=='flower':
            return app.peachFlower
        elif stage=='unripe':
            return app.peachUnripe
        elif stage=='fruit' or stage==4: 
            return app.peachFruit
        elif stage==1:
            return app.peach1
        elif stage==2:
            return app.peach2
        elif stage==3:
            return app.peach3

    elif plantType=='lemon':
        if stage=='sprout':
            return app.lemonSprout
        elif stage=='small':
            return app.lemonSmall
        elif stage=='med':
            return app.lemonMed
        elif stage=='mat':
            return app.lemonMat
        elif stage=='flower':
            return app.lemonFlower
        elif stage=='unripe':
            return app.lemonUnripe
        elif stage=='fruit' or stage==6: 
            return app.lemonFruit
        elif stage==1:
            return app.lemon1
        elif stage==2:
            return app.lemon2
        elif stage==3:
            return app.lemon3
        elif stage==4:
            return app.lemon4
        elif stage==5:
            return app.lemon5

    elif plantType=='strawb':
        if stage=='sprout':
            return app.strawbSprout
        elif stage=='small':
            return app.strawbSmall
        elif stage=='med':
            return app.strawbMed
        elif stage=='mat':
            return app.strawbMat
        elif stage=='flower':
            return app.strawbFlower
        elif stage=='unripe':
            return app.strawbUnripe
        elif stage=='fruit' or stage==7: 
            return app.appleFruit
        elif stage==1:
            return app.strawb1
        elif stage==2:
            return app.strawb2
        elif stage==3:
            return app.strawb3
        elif stage==4:
            return app.strawb4
        elif stage==5:
            return app.strawb5
        elif stage==6:
            return app.strawb6
    elif plantType=='tomato':
        if stage=='sprout':
            return app.tomatoSprout
        elif stage=='small':
            return app.tomatoSmall
        elif stage=='med':
            return app.tomatoMed
        elif stage=='mat':
            return app.tomatoMat
        elif stage=='flower':
            return app.tomatoFlower
        elif stage=='unripe':
            return app.tomatoUnripe
        elif stage=='fruit' or stage==6: 
            return app.tomatoFruit
        elif stage==1:
            return app.tomato1
        elif stage==2:
            return app.tomato2
        elif stage==3:
            return app.tomato3
        elif stage==4:
            return app.tomato4
        elif stage==5:
            return app.tomato5
    elif plantType=='blackb':
        if stage=='sprout':
            return app.blackbSprout
        elif stage=='small':
            return app.blackbSmall
        elif stage=='med':
            return app.blackbMed
        elif stage=='mat':
            return app.blackbMat
        elif stage=='flower':
            return app.blackbFlower
        elif stage=='unripe':
            return app.blackbUnripe
        elif stage=='fruit' or stage==7: 
            return app.blackbFruit
        elif stage==1:
            return app.blackb1
        elif stage==2:
            return app.blackb2
        elif stage==3:
            return app.blackb3
        elif stage==4:
            return app.blackb4
        elif stage==5:
            return app.blackb5
        elif stage==6:
            return app.blackb6


def getTerrainColor(app,row,col):
    # return terrain color or indicator for display
    terrainNum = app.board[row][col]
    # GRASS
    if terrainNum==0:
        return '#c1e0b7'
    # TREE
    elif terrainNum==1 or terrainNum==3:
        return '#6d5647'
    # PLANT
    elif terrainNum==2 or terrainNum==4:
        return '#7e5d47'
    
    # tree seed
    elif terrainNum==5:
        return rgbString(0,128,0)
    elif terrainNum==50:
        # sprout
        plant = getPlantType(app,row,col)
        return (plant,'sprout')
    elif terrainNum==51:
        # small tree 
        plant = getPlantType(app,row,col)
        return (plant,'small')
    elif terrainNum==52:
        # medium tree 
        plant = getPlantType(app,row,col)
        return (plant,'med')
    elif terrainNum==53:
        # mature tree
        plant = getPlantType(app,row,col)
        return (plant,'mat')
    elif terrainNum==54:
        # blooming
        plant = getPlantType(app,row,col)
        return (plant,'flower')
    elif terrainNum==55:
        # unripe
        plant = getPlantType(app,row,col)
        return (plant,'unripe')
    elif terrainNum==56:
        # fruits 
        plant = getPlantType(app,row,col)
        return (plant,'fruit')

    # plant seed
    elif terrainNum==6:
        return rgbString(0,255,127)
    elif terrainNum==60:
        # plant sprout
        plant = getPlantType(app,row,col)
        return (plant,'sprout')
    elif terrainNum==61:
        # small plant
        plant = getPlantType(app,row,col)
        return (plant,'small')
    elif terrainNum==62:
        # medium plant 
        plant = getPlantType(app,row,col)
        return (plant,'med')
    elif terrainNum==63:
        # mature plant
        plant = getPlantType(app,row,col)
        return (plant,'mat')
    elif terrainNum==64:
        # flowers
        plant = getPlantType(app,row,col)
        return (plant,'flower')
    elif terrainNum==65:
        # unripe
        plant = getPlantType(app,row,col)
        return (plant,'unripe')
    elif terrainNum==66:
        # fruit
        plant = getPlantType(app,row,col)
        return (plant,'fruit')
    
    elif terrainNum==100:
        # watered soil
        return '#3d3616'
    elif terrainNum==99:
        # dry soil
        return '#a89385'
    elif terrainNum==101:
        # overwatered soil
        return '#1e1007'
    
    elif terrainNum=='apple':
        # apple fruit, get the state of the tree when fruiting
        state = getFruitState(app,row,col)
        return (terrainNum,state)
    elif terrainNum=='peach':
        state = getFruitState(app,row,col)
        return (terrainNum,state)
    elif terrainNum=='lemon':
        state = getFruitState(app,row,col)
        return (terrainNum,state)
    elif terrainNum=='strawb':
        state = getFruitState(app,row,col)
        return (terrainNum,state)
    elif terrainNum=='tomato':
        state = getFruitState(app,row,col)
        return (terrainNum,state)
    elif terrainNum=='blackb':
        state = getFruitState(app,row,col)
        return (terrainNum,state)

def getFruitState(app,row,col):
    # counts how many fruits there are
    if (row,col) in app.allPlantClasses:
        plant = app.allPlantClasses[(row,col)]
        if plant.numFruits==0:
            return 'mat'
        return plant.numFruits

def getPlantType(app,row,col):
    # return plant type (apple, lemon, tomato, etc.)
    if (row,col) in app.allPlantClasses:
        plant = app.allPlantClasses[(row,col)]
        return plant.type
    elif (row,col) in app.allSeedClasses:
        plant = app.allSeedClasses[(row,col)]
        return plant.type

def drawMenuHead(app,canvas):
    # draw menu head + time + temp + level
    canvas.create_rectangle(0,0,app.exitWidth,app.exitHeight,
        fill='#bcdba2',width=2)
    canvas.create_text(app.exitWidth/2,app.exitHeight/2,text='exit',
        font='Courier')
    menuItems = ["inventory","plant","water","harvest"]
    for i in range(4):
        x0 = i*100 + app.exitWidth
        x1 = x0 + app.menuButtonWidth
        y0 = 0
        y1 = app.menuButtonHeight
        canvas.create_rectangle(x0,y0,x1,y1,fill='#bcdba2',width=2)
        canvas.create_text(x0+app.menuButtonWidth/2,y1/2,text=menuItems[i],
            font='Courier')
    
    timeX0 = 700
    timeX1 = timeX0 + app.menuButtonWidth
    timeY0 = 0
    timeY1 = timeY0 + app.menuButtonHeight
    canvas.create_rectangle(timeX0,timeY0,timeX1,timeY1,fill='#bcdba2',width=2)
    day = 'day ' + str(app.day)
    level = 'lvl ' + str(app.level)
    canvas.create_text(timeX0+app.menuButtonWidth/2,
                            timeY1/3,text=day,font='Courier')
    canvas.create_text(timeX0+app.menuButtonWidth/2,
                            timeY1/3*2,text=level,font='Courier')

    tempX0 = 800
    tempX1 = tempX0 + app.menuButtonWidth
    tempY0 = 0
    tempY1 = tempY0 + app.menuButtonHeight
    canvas.create_rectangle(tempX0,tempY0,tempX1,tempY1,fill='#bcdba2',width=3)
    tempStr = str(app.currTemp) + 'F'
    canvas.create_text(tempX0+app.menuButtonWidth/2,tempY1/2,
        text=tempStr,font='Courier')


def drawInventory(app,canvas):
    # draw inventory of food items, same layout as planting
    canvas.create_rectangle(app.plantingX0,app.plantingY0,
        app.plantingX1,app.plantingY1,fill='white')
    canvas.create_text(app.plantingX1-app.closePlantingHeight/2,
            app.plantingY0+app.closePlantingHeight/2,text='X',font='Courier')
    for j in range(2):
        for i in range(3):
            colX0 = (app.plantingX0+app.plantingSlot*i + app.plantingSide*(i+1))
            colY0 = (app.plantingY0+ app.plantingSlot*j + app.plantingTop*(j+1))

            itemName = app.invItems[j][i][0]
            itemCount = app.invItems[j][i][1]
            canvas.create_text(colX0+app.plantingSlot/2,
                colY0,text=itemName+' '+str(itemCount),font='Courier')
            image = app.invImages[j][i]
            canvas.create_image(colX0+app.plantingSlot/2,
                colY0+app.plantingSlot/2,image=ImageTk.PhotoImage(image))

def drawPlanting(app,canvas):
    # draw screen for seeds and to plant
    canvas.create_rectangle(app.plantingX0,app.plantingY0,
                            app.plantingX1,app.plantingY1,fill="white")
    canvas.create_text(app.plantingX1-app.closePlantingHeight/2,
            app.plantingY0+app.closePlantingHeight/2,text="X",font='Courier')
    
    for j in range(2):
        for i in range(3):
            colX0 = (app.plantingX0+app.plantingSlot*i + app.plantingSide*(i+1))
            colY0 = (app.plantingY0+ app.plantingSlot*j + app.plantingTop*(j+1))
            
            seedName = app.seedInv[j][i][0]
            seedCount = app.seedInv[j][i][1]
            canvas.create_text(colX0+app.plantingSlot/2,
                colY0+app.plantingSlot/2,text=seedName+': '+str(seedCount),
                font='Courier 12')
    
    canvas.create_rectangle(app.unplantX0,app.unplantY0,
        app.unplantX0+app.unplantWidth,app.unplantY0+app.unplantHeight)
    canvas.create_text(app.unplantX0+app.unplantWidth/2,
        app.unplantY0+app.unplantHeight/2,text='remove plants',font='Courier 12')
    canvas.create_text(app.plantingX0+(app.plantingX1-app.plantingX0)/2,
        app.plantingY0+20,
        text='select seed to plant and press enter to plant!',font='Courier')

runApp(width=900,height=700)
