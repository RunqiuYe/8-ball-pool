# To-do: Red balls geometry

from cmu_graphics import *


class Ball:
    pointDict = {
        "red": 1,
        "yellow": 2,
        "green": 3,
        "brown": 4,
        "blue": 5,
        "pink": 6,
        "black": 7,
    }

    def __init__(self, color, cx, cy):
        self.color = color
        self.cx = cx
        self.cy = cy
        self.vx = 0
        self.vy = 0
        self.point = Ball.pointDict[self.color] if color != "white" else -1
        self.radius = 5.3


def initializeTableGeometry(app):
    app.width = 850
    app.height = 650
    app.tableCenterX = app.width / 2
    app.tableCenterY = app.height / 2
    app.tableWidth = 178 * 2
    app.tableLength = 370 * 2
    app.lineLocation = 74 * 2
    app.regionRadius = 29.7 * 2
    app.pocketRadius = 8.6 / 2 * 2
    app.blackLocation = 32.5 * 2


def initializeBalls(app):
    app.colorLocationDict = {
        "yellow": [
            app.tableCenterX - app.tableLength / 2 + app.lineLocation,
            app.tableCenterY - app.regionRadius,
        ],
        "green": [
            app.tableCenterX - app.tableLength / 2 + app.lineLocation,
            app.tableCenterY + app.regionRadius,
        ],
        "brown": [
            app.tableCenterX - app.tableLength / 2 + app.lineLocation,
            app.tableCenterY,
        ],
        "blue": [app.tableCenterX, app.tableCenterY],
        "pink": [app.tableCenterX + app.tableLength / 4, app.tableCenterY],
        "black": [
            app.tableCenterX + app.tableLength / 2 - app.blackLocation,
            app.tableCenterY,
        ],
    }
    
    app.yellowBall = Ball(
        "yellow", app.colorLocationDict["yellow"][0], app.colorLocationDict["yellow"][1]
    )
    app.greenBall = Ball(
        "green", app.colorLocationDict["green"][0], app.colorLocationDict["green"][1]
    )
    app.brownBall = Ball(
        "brown", app.colorLocationDict["brown"][0], app.colorLocationDict["brown"][1]
    )
    app.blueBall = Ball(
        "blue", app.colorLocationDict["blue"][0], app.colorLocationDict["blue"][1]
    )
    app.pinkBall = Ball(
        "pink", app.colorLocationDict["pink"][0], app.colorLocationDict["pink"][1]
    )
    app.blackBall = Ball(
        "black", app.colorLocationDict["black"][0], app.colorLocationDict["black"][1]
    )
    app.colorBallList = [
        app.yellowBall,
        app.greenBall,
        app.brownBall,
        app.blueBall,
        app.pinkBall,
        app.blackBall,
    ]


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
        app.tableCenterX, app.tableCenterY, length, width, fill="brown", align="center", border = 'black'
    )


def drawSnookerTable(app):
    drawTableBorder(app)
    drawPlayArea(app)
    drawPocket(app)


def drawBalls(app):
    for ball in app.colorBallList:
        drawCircle(ball.cx, ball.cy, ball.radius, fill=ball.color, border="black", borderWidth=1)


def onAppStart(app):
    newGame(app)


def newGame(app):
    initializeTableGeometry(app)
    initializeBalls(app)


def redrawAll(app):
    drawSnookerTable(app)
    drawBalls(app)


def main():
    runApp()


main()
