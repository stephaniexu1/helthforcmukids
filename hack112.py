from cmu_112_graphics import *
from PIL import Image
import math, random, time, os

#Citations:
#Images: Flaticon.com. This game has been designed using resources from Flaticon.com
#<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>


###HELTH FOR CMU KIDS###
# Name: Stephanie Xu (stephanx)
# Date: April 11, 2021
# Event: Hack-112 S21

#Game Dimensions
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 30
    margin = 25
    return (rows,cols,cellSize,margin)

##MODEL##
#Custom Colors
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

#Extracting Images from Folder
def listFiles(path):
    files = [ ]
    for filename in os.listdir(path):
        files.append(path + '/' +filename)
    return files

def removeTempFiles(L, suffix='.DS_Store'):
    for filename in L:
        if suffix in filename:
            L.remove(filename)
    return L

def healthyImages():
    result = listFiles('healthy')
    new = removeTempFiles(result)
    return new

def junkImages():
    result = listFiles('junk')
    new = removeTempFiles(result)
    return new

###################################
def appStarted(app):
    (app.rows,app.cols,app.cellSize,app.margin) = gameDimensions()
    app.emptyColor = 'white'
    app.board = [ [app.emptyColor] * app.cols for row in range(app.rows) ]
    app.welcome = True
    app.time0 = time.time()
    restartApp(app)

def restartApp(app):
    #time tracker:
    app.time0 = time.time()
    #gamemode:
    app.score = 0
    app.pause = False
    app.gameOver = False
    #the pieces:
    app.white1 = rgbString(248,248,255) #color for healthy food
    app.white2 = rgbString(255,250,250) #color for junk food
    app.foodPieces = [app.white1,app.white2]
    app.fallingPiece = None
    app.foodImage = None
    app.fallingPieceRow = app.fallingPieceCol = None
    app.bowl = 'brown'
    app.bowlRow = app.rows-1
    app.bowlCol = app.cols//2
    newFallingPiece(app)
    #messages:
    app.goodMessages = ['monch','helth +1','delicious','gud food','chomp']
    app.missedMessages = ['cri','excuse me','feed me','i need helth','big sad']
    app.badMessages = ['gags','just no','ur bad','disgusting','shameful']



##CONTROLER##
#Getting New Random Food
def newFallingPiece(app):
    randomIndex = random.randint(0,len(app.foodPieces)-1)
    app.fallingPiece = app.foodPieces[randomIndex]
    if app.fallingPiece == app.white1:
        app.foodImage = random.choice(healthyImages())
    else:
        app.foodImage = random.choice(junkImages())
    app.fallingPieceRow = 0
    app.fallingPieceCol = random.randint(0,app.cols-1)

#Dropping the Piece
def moveFallingPiece(app):
    if app.gameOver: return
    if not app.welcome and not app.pause:
        app.fallingPieceRow += 1
        checkTarget(app)
        if not fallingPieceIsLegal(app):
            if app.fallingPiece == app.white1:
                app.score -= 1
                num = random.randint(0,4)
                print(app.missedMessages[num])
            newFallingPiece(app)
    
#Check If Food Was Caught
def checkTarget(app):
    if app.gameOver: return
    if not app.welcome and not app.pause:
        if app.fallingPieceRow == app.bowlRow and app.fallingPieceCol == app.bowlCol:
            if app.fallingPiece == app.white1:
                if 'coffee' in app.foodImage:
                    app.score += 10
                    print('coffeeeeee boooooosttttt :-) u will need it')
                else:
                    num = random.randint(0,4)
                    print(app.goodMessages[num])
                if time.time() - app.time0 < 20:
                    app.score += 1
                elif time.time() - app.time0 < 40:
                    app.score += 2
                elif time.time() - app.time0 < 80:
                    app.score += 3
                elif time.time() - app.time0 < 160:
                    app.score += 4
                elif time.time() - app.time0 < 350: 
                    app.score += 5
                else:
                    app.score += 6
            elif app.fallingPiece == app.white2:
                if 'spicy' in app.foodImage:
                    app.score -= 5
                    print('u attended spicy recitation, bad helth')
                else:
                    app.score -= 2
                    num = random.randint(0,4)
                    print(app.badMessages[num])
            newFallingPiece(app)

#Checking If Food Is Within Bounds
def fallingPieceIsLegal(app):
    if app.gameOver: return
    if not app.welcome and not app.pause:
        row,col = app.fallingPieceRow, app.fallingPieceCol
        if row >= app.rows or col >= app.cols:
            return False
        return True

#Place Food Piece On Board
def placeFallingPiece(app):
    if app.gameOver: return
    if not app.welcome and not app.pause:
        row,col = app.fallingPieceRow, app.fallingPieceCol
        app.board[row][col] = app.fallingPiece

###################################
def keyPressed(app,event):
    if event.key == 'r':
        restartApp(app)
    if app.gameOver: return
    if event.key == 'Enter':
        app.welcome = False
    if event.key == 'Space':
        app.pause = not app.pause
    if not app.pause:
        if event.key == 'Left':
            app.bowlCol -= 1
            if app.bowlCol < 0:
                app.bowlCol = app.cols - 1
            elif app.bowlCol > app.cols - 1:
                app.bowlCol = 0
        elif event.key == 'Right':
            app.bowlCol += 1
            if app.bowlCol < 0:
                app.bowlCol = app.cols - 1
            elif app.bowlCol > app.cols - 1:
                app.bowlCol = 0
    
def timerFired(app):
    if app.gameOver: return
    if not app.welcome and not app.pause:
        moveFallingPiece(app)
        if app.score < 0:
            app.gameOver = True
            app.fallingPiece = None



##VIEW##
#Get Bounds to Place Image
def getCellBounds(app, row, col):
    #get cell bounds for image
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth + app.cellSize//2
    y0 = app.margin + row * cellHeight
    return (x0, y0)

def drawCell(app,canvas,row,col,color):
    if not app.welcome:
        x1 = app.margin + app.cellSize*col
        y1 = app.margin + app.cellSize*row
        x2 = app.margin + app.cellSize*(col+1)
        y2 = app.margin + app.cellSize*(row+1)
        canvas.create_rectangle(x1,y1,x2,y2,fill=color,outline='')

def drawWelcome(app,canvas):
    if app.welcome:
        canvas.create_rectangle(0,0,app.width,app.height,fill='lightBlue')
        canvas.create_text(app.width/2,app.height/2-170,text='helth for cmu kids',
                            font='arial 30 bold')
        canvas.create_text(app.width/2,app.height/2-145,
                            text="press Enter to begin",
                            font='arial 15 bold')
        canvas.create_text(app.width/2,app.height/2+160,
                            text='''use left and right arrows to move ur bowl\npress Space to pause the game\nmake sure to catch the helth fud\ndon't catch the bad fud (duh)\nsince it's cmu, catch coffee for extra boost''',
                            font='arial 10')
        newImg = PhotoImage(file='bowl.png')
        canvas.create_image(app.width/2, app.height/2, image=newImg)

def drawPause(app,canvas):
    if not app.welcome:
        if app.pause:
            width = (app.cols*app.cellSize - 3*app.margin)/2
            height = (5*app.cellSize)/2
            canvas.create_rectangle(app.width/2-width,app.height/2-height,
                                    app.width/2+width,app.height/2+height,
                                    fill='light Blue',outline='')
            canvas.create_text(app.width/2,app.height/2,
                                text='ur paused...',
                                font='arial 25 bold')
            canvas.create_text(app.width/2,app.height/2+app.cellSize,
                                text='press Space to continue\nor you can restart lol',
                                font='arial 10')

def drawBoard(app,canvas):
    if not app.welcome:
        for row in range(app.rows):
            for col in range(app.cols):
                drawCell(app,canvas,row,col,app.board[row][col])

def drawFallingPiece(app,canvas):
    if not app.welcome and not app.gameOver:
        row,col = app.fallingPieceRow, app.fallingPieceCol
        (x,y) = getCellBounds(app,row,col)
        drawCell(app,canvas,row,col,app.fallingPiece)
        newImg = PhotoImage(file=app.foodImage)
        canvas.create_image(x,y,image=newImg)

def drawBowl(app,canvas):
    if not app.welcome:
        row,col = app.bowlRow, app.bowlCol
        (x,y) = getCellBounds(app,row,col)
        drawCell(app,canvas,row,col,app.bowl)
        newImg = PhotoImage(file='smolbowl.png')
        canvas.create_image(x,y,image=newImg)

def drawScore(app,canvas):
    if not app.welcome:
        canvas.create_text(app.width//2,app.margin//2,text=f'Score: {app.score}',
                        fill='black',font='arial 17 bold')

def drawGameOver(app,canvas):
    if app.gameOver:
        x1 = 0
        y1 = 2*app.cellSize
        x2 = app.width
        y2 = y1 + 2*app.cellSize
        canvas.create_rectangle(x1,y1,x2,y2,fill='blue',outline='')
        canvas.create_text(app.width//2,(y2+y1)//2,text='u unhealthy loser >:(',
                            font='arial 20 bold', fill='white')

###################################
def redrawAll(app,canvas):
    drawWelcome(app,canvas)
    drawBoard(app,canvas)
    drawFallingPiece(app,canvas)
    drawScore(app,canvas)
    drawBowl(app,canvas)
    drawPause(app,canvas)
    drawGameOver(app,canvas)


##RUN GAME :D##
def playGame():
    (rows,cols,cellSize,margin) = gameDimensions()
    runApp(width=cols*cellSize + 2*margin, height=rows*cellSize + 2*margin)

playGame()