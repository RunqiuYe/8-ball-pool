from cmu_graphics import *

def initializeTableGeometry(app):
    app.width = 850
    app.height = 650
    app.tableCenterX = app.width / 2
    app.tableCenterY = app.height / 2
    app.tableWidth = 178 * 2
    app.tableLength = 357 * 2
    app.lineLocation = 74 * 2
    app.regionRadius = 29.7 * 2
    app.pocketRadius = 10 / 2 * 2


def drawPlayArea(app):
    length = app.tableLength
    width = app.tableWidth
    lineLocation = app.lineLocation
    lineX = app.tableCenterX - length / 2 + lineLocation
    regionRadius = app.regionRadius
    drawRect(
        app.tableCenterX,
        app.tableCenterY,
        length,
        width,
        fill="lightGreen",
        align="center",
        border="black",
        borderWidth=2,
    )
    drawLine(
        lineX,
        app.tableCenterY + width / 2,
        lineX,
        app.tableCenterY - width / 2,
        fill="white",
    )
    drawArc(
        lineX,
        app.tableCenterY,
        regionRadius * 2,
        regionRadius * 2,
        90,
        180,
        fill=None,
        border="white",
    )


def drawPocket(app):
    length = app.tableLength
    width = app.tableWidth
    pocketRadius = app.pocketRadius
    drawCircle(
        app.tableCenterX + length / 2,
        app.tableCenterY + width / 2,
        pocketRadius,
        fill="black",
    )
    drawCircle(
        app.tableCenterX + length / 2,
        app.tableCenterY - width / 2,
        pocketRadius,
        fill="black",
    )
    drawCircle(
        app.tableCenterX - length / 2,
        app.tableCenterY + width / 2,
        pocketRadius,
        fill="black",
    )
    drawCircle(
        app.tableCenterX - length / 2,
        app.tableCenterY - width / 2,
        pocketRadius,
        fill="black",
    )
    drawCircle(
        app.tableCenterX, app.tableCenterY + width / 2, pocketRadius, fill="black"
    )
    drawCircle(
        app.tableCenterX, app.tableCenterY - width / 2, pocketRadius, fill="black"
    )


def drawTableBorder(app):
    length = app.tableLength * 1.05
    width = app.tableWidth * 1.1
    drawRect(
        app.tableCenterX, app.tableCenterY, length, width, fill="brown", align="center"
    )


def drawSnookerTable(app):
    drawTableBorder(app)
    drawPlayArea(app)
    drawPocket(app)


def onAppStart(app):
    newGame(app)

def newGame(app):
    initializeTableGeometry(app)


def redrawAll(app):
    drawSnookerTable(app)


def main():
    runApp()


main()
