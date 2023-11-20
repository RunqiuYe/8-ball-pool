from cmu_graphics import *

def drawPlayArea(app):
    length = app.tableLength * app.scaleFactor
    width = app.tableWidth * app.scaleFactor
    lineLocation = app.lineLocation * app.scaleFactor
    lineX = app.tableCenterX - length/2 + lineLocation
    regionRadius = app.regionRadius * app.scaleFactor
    drawRect(app.tableCenterX, app.tableCenterY, length, width, fill = 'green', align = 'center', border = 'black', borderWidth = 2)
    drawLine(lineX, app.tableCenterY + width/2, lineX, app.tableCenterY - width/2, fill = 'white')
    drawArc(lineX, app.tableCenterY, regionRadius*2, regionRadius*2, 90, 180, fill = None, border = 'white')


def drawPocket(app):
    length = app.tableLength * app.scaleFactor
    width = app.tableWidth * app.scaleFactor
    pocketRadius = app.pocketRadius * app.scaleFactor
    drawCircle(app.tableCenterX + length/2, app.tableCenterY + width/2, pocketRadius, fill = 'black')
    drawCircle(app.tableCenterX + length/2, app.tableCenterY - width/2, pocketRadius, fill = 'black')
    drawCircle(app.tableCenterX - length/2, app.tableCenterY + width/2, pocketRadius, fill = 'black')
    drawCircle(app.tableCenterX - length/2, app.tableCenterY - width/2, pocketRadius, fill = 'black')
    drawCircle(app.tableCenterX, app.tableCenterY + width/2, pocketRadius, fill = 'black')
    drawCircle(app.tableCenterX, app.tableCenterY - width/2, pocketRadius, fill = 'black')


def drawTableBorder(app):
    length = app.tableLength * app.scaleFactor * 1.1
    width = app.tableWidth * app.scaleFactor * 1.2
    drawRect(app.tableCenterX, app.tableCenterY, length, width, fill = 'brown', align = 'center')


def drawSnookerTable(app):
    drawTableBorder(app)
    drawPlayArea(app)
    drawPocket(app)



def onAppStart(app):
    app.width = 850
    app.height = 650
    app.tableCenterX = app.width/2
    app.tableCenterY = app.height/2
    app.tableWidth = 178
    app.tableLength = 357
    app.lineLocation = 74
    app.regionRadius = 29.7
    app.pocketRadius = 8.6
    app.scaleFactor = 2

def redrawAll(app):
    drawSnookerTable(app)

def main():
    runApp()

main()