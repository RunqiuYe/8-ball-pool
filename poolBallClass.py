from cmu_graphics import *
import math


class Ball:
    def __init__(self, color, cx, cy):
        self.color = color
        self.cx = cx
        self.cy = cy
        self.vx = 0
        self.vy = 0
        self.radius = 6.8 * 1.5


def initializeTableGeometry(app):
    app.width = 1000
    app.height = 800
    app.tableCenterX = app.width / 2
    app.tableCenterY = app.height / 2
    app.tableWidth = 120 * 3
    app.tableLength = 250 * 3
    app.lineLocation = app.tableCenterX - app.tableLength / 4
    app.pocketRadius = 10 / 2 * 3


def initializeBalls(app):
    colorList = [[1], [0, 1], [1, 8, 0], [0, 1, 0, 1], [1, 0, 1, 0, 0]]
    app.ballList = []
    ballRadius = 6.8 * 1.5
    initialX = app.tableCenterX + app.tableLength / 4
    initialY = app.tableCenterY
    dx = ballRadius * (math.sqrt(3) + 0.05)
    dy = ballRadius * 1.05
    for i in range(1, 6):
        for j in range(1, i + 1):
            ballCordX = initialX + (i - 1) * dx
            ballCordY = (
                initialY + (i - 1) * dy - ballRadius * 2.1 * (j - 1)
            )
            colorIndex = colorList[i - 1][j - 1]
            if colorIndex == 8:
                color = 'black'
            elif colorIndex == 0:
                color = 'yellow'
            else:
                color = 'red'
            newRedBall = Ball(color, ballCordX, ballCordY)
            app.ballList.append(newRedBall)


def drawPlayArea(app):
    length = app.tableLength
    width = app.tableWidth
    lineLocation = app.lineLocation
    drawRect(
        app.tableCenterX,
        app.tableCenterY,
        length,
        width,
        fill="lightSkyBlue",
        align="center",
        border="black",
        borderWidth=2,
    )
    drawLine(
        lineLocation,
        app.tableCenterY + width / 2,
        lineLocation,
        app.tableCenterY - width / 2,
        fill="black",
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
    length = app.tableLength * 1.1
    width = app.tableWidth * 1.2
    drawRect(
        app.tableCenterX,
        app.tableCenterY,
        length,
        width,
        fill="sienna",
        align="center",
        border="black",
    )


def drawSnookerTable(app):
    drawTableBorder(app)
    drawPlayArea(app)
    drawPocket(app)


def drawBalls(app):
    for ball in app.ballList:
        drawCircle(
            ball.cx,
            ball.cy,
            ball.radius,
            fill = ball.color,
            border = "black",
            borderWidth = 1,
        )


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