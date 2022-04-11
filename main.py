from cmu_112_graphics import *

def appStarted(app):
    app.width,app.height = 900,700

    app.openInventory = False
    app.closeInvHeight = 25

    app.menuButtonHeight = 50
    app.menuButtonWidth = 100

    app.treePlotWidth = 700
    app.treePlotHeight = 200

    # (x0,y0,x1,y1) forms
    app.treeSpace1 = (0,app.menuButtonHeight,app.treePlotWidth,
                        app.menuButtonHeight+app.treePlotHeight)
    app.plotSize = 50
    app.plotSpacing = 100

    # individual plots to plant trees in
    app.treeplot1 = (100,175,100+app.plotSize,175+app.plotSize)

    app.treeplot2 = (app.treeplot1[2]+app.plotSpacing,150,
        app.treeplot1[2]+app.plotSpacing+app.plotSize,150+app.plotSize)

    app.treeplot3 = (app.treeplot2[2]+app.plotSpacing,175,
        app.treeplot2[2]+app.plotSpacing+app.plotSize,175+app.plotSize)

    app.treeplot4 = (app.treeplot3[2]+app.plotSpacing,125,
        app.treeplot3[2]+app.plotSpacing+app.plotSize,125+app.plotSize)

    # 'container' of the lower tree plots
    app.treeSpace2 = (0,app.height-app.treePlotHeight,
                    app.treePlotWidth,app.height)

    app.pathWidth = 50

    # non-tree plant plots
    app.plantPlotWidth = 600
    app.plantPlotHeight = 150
    app.plantPlot = (75,app.treeSpace1[3]+app.pathWidth,
      75+app.plantPlotWidth,app.treeSpace1[3]+app.pathWidth+app.plantPlotHeight)

    app.treeplot5 = (100,app.plantPlot[3]+app.pathWidth+100,
            100+app.plotSize,app.plantPlot[3]+app.pathWidth+100+app.plotSize)

    app.treeplot6 = (app.treeplot5[2]+app.plotSpacing,
                    app.plantPlot[3]+app.pathWidth+125,
                    app.treeplot5[2]+app.plotSpacing+app.plotSize,
                    app.plantPlot[3]+app.pathWidth+125+app.plotSize)

    app.treeplot7 = (app.treeplot6[2]+app.plotSpacing,
                    app.plantPlot[3]+app.pathWidth+75,
                    app.treeplot6[2]+app.plotSpacing+app.plotSize,
                    app.plantPlot[3]+app.pathWidth+75+app.plotSize)

    app.treeplot8 = (app.treeplot7[2]+app.plotSpacing,
                    app.plantPlot[3]+app.pathWidth+125,
                    app.treeplot7[2]+app.plotSpacing+app.plotSize,
                    app.plantPlot[3]+app.pathWidth+125+app.plotSize)
    
    # list of all the tree plots
    app.allTreePlots = [app.treeplot1,app.treeplot2,app.treeplot3,app.treeplot4,
                        app.treeplot5,app.treeplot6,app.treeplot7,app.treeplot8]
    
    app.sidePlot = (app.width-app.plantPlotHeight,65,app.width,
                    65+app.plantPlotWidth)

    app.invItems = [
                    [{'apple': 0},{'peach':1},{'lemon':3},{'strawberry':2},
                    {'orange':0},{'tomatoes':4}],

                    [{'apple seed':8},{'peach seeds':4},{'lemon seeds':8},
                    {'strawberry seeds':5},{'sample':0},{'sample':0}],

                    [{'sample':1},{'sample':1},{'sample':1},{'sample':1},
                    {'sample':1},{'sample':1}],

                    [{'sample':1},{'sample':1},{'sample':1},{'sample':1},
                    {'sample':1},{'sample':1}],
                    ]

def getInvRowCol(app,event):
    pass
    

def mousePressed(app,event):
    app.cx,app.cy = event.x,event.y

    # open/close inventory
    if app.cx<=app.menuButtonWidth and app.cy<=app.menuButtonHeight:
        app.openInventory = True
    elif (app.cx<=825+app.closeInvHeight and app.cx>=825 and 
                app.cy<=50+app.closeInvHeight and app.cy>=50):
        app.openInventory = False

def redrawAll(app,canvas):
    drawMenuHead(app,canvas)
    drawPlots(app,canvas)

    if app.openInventory==True:
        drawInventory(app,canvas)
    


def drawMenuHead(app,canvas):
    buttonWidth = 100
    buttonHeight = 40
    menuItems = ["inventory","plant","water","harvest"]
    for i in range(4):
        x0 = i*100
        x1 = x0 + app.menuButtonWidth
        y0 = 0
        y1 = app.menuButtonHeight
        canvas.create_rectangle(x0,y0,x1,y1)
        canvas.create_text(x0+app.menuButtonWidth/2,y1/2,text=menuItems[i])
    
    timeX0 = 700
    timeX1 = timeX0 + buttonWidth
    timeY0 = 0
    timeY1 = timeY0 + buttonHeight
    canvas.create_rectangle(timeX0,timeY0,timeX1,timeY1)
    canvas.create_text(timeX0+buttonWidth/2,timeY1/2,text="12:00 PM")

    tempX0 = 800
    tempX1 = tempX0 + buttonWidth
    tempY0 = 0
    tempY1 = tempY0 + buttonHeight
    canvas.create_rectangle(tempX0,tempY0,tempX1,tempY1)
    canvas.create_text(tempX0+buttonWidth/2,tempY1/2,text="temp #")

def drawInventory(app,canvas):
    invMargin = 50
    canvas.create_rectangle(invMargin,invMargin,
                app.width-invMargin,app.height-invMargin,fill="white")

    colWidth = 75
    rowSpace = 250/3
    colSpace = 60
    for i in range(4):
        for j in range(6):
            colX0 = invMargin + 25 + colWidth*j + colSpace*j
            colY0 = invMargin + 25 + colWidth*i + rowSpace*i
            canvas.create_rectangle(colX0,colY0,
                            colX0+colWidth,colY0+colWidth)

            for item in app.invItems[i][j]:
                itemCount = app.invItems[i][j][item]
                canvas.create_text(colX0+colWidth/2,colY0+colWidth/2,
                                    text=item+" "+str(itemCount))
    
    canvas.create_text(825+app.closeInvHeight/2,50+app.closeInvHeight/2,
                            text='X')

def drawPlots(app,canvas):
    canvas.create_rectangle(app.treeSpace1[0],app.treeSpace1[1],
                            app.treeSpace1[2],app.treeSpace1[3],outline="grey")

    canvas.create_rectangle(app.plantPlot[0],app.plantPlot[1],
                            app.plantPlot[2],app.plantPlot[3])

    canvas.create_rectangle(app.treeSpace2[0],app.treeSpace2[1],
                            app.treeSpace2[2],app.treeSpace2[3],outline="grey")

    canvas.create_rectangle(app.sidePlot[0],app.sidePlot[1],
                            app.sidePlot[2],app.sidePlot[3])
    
    for plot in app.allTreePlots:
        canvas.create_rectangle(plot[0],plot[1],plot[2],plot[3])


runApp(width=900,height=700)