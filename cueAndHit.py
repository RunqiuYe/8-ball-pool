from cmu_graphics import *
import math


# Distance Helper Function
def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


# ========================================================================
# Table functions (initialization, drawing)
# ========================================================================

# Drawing and initlization functions
# ========================================================================


# Initialize table geometry, including pocket locations
def initializeTableGeometry(app):
    app.width = 850
    app.height = 650
    app.tableCenterX = app.width / 2
    app.tableCenterY = app.height / 2
    app.tableWidth = 178 * 2
    app.tableLength = 357 * 2
    app.lineLocation = 74 * 2
    app.regionRadius = 29.7 * 2
    app.pocketRadius = 8.6 / 2 * 2
    app.pocketLocations = [
        (app.tableCenterX + app.tableLength / 2, app.tableCenterY + app.tableWidth / 2),
        (app.tableCenterX + app.tableLength / 2, app.tableCenterY - app.tableWidth / 2),
        (app.tableCenterX - app.tableLength / 2, app.tableCenterY + app.tableWidth / 2),
        (app.tableCenterX - app.tableLength / 2, app.tableCenterY - app.tableWidth / 2),
        (app.tableCenterX, app.tableCenterY + app.tableWidth / 2),
        (app.tableCenterX, app.tableCenterY - app.tableWidth / 2),
    ]


# draw play area (green mat)
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


# draw pocket
def drawPocket(app):
    for pocketX, pocketY in app.pocketLocations:
        drawCircle(pocketX, pocketY, app.pocketRadius, fill="black")


# draw table border
def drawTableBorder(app):
    length = app.tableLength * 1.05
    width = app.tableWidth * 1.1
    drawRect(
        app.tableCenterX, app.tableCenterY, length, width, fill="brown", align="center"
    )


# draw Snooker Table
def drawSnookerTable(app):
    drawTableBorder(app)
    drawPlayArea(app)
    drawPocket(app)


# ========================================================================
# Snooker balls functions (class, intialization, drawing)
# ========================================================================

# class of snooker Balls
# ========================================================================


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
        self.speed = 0
        self.point = Ball.pointDict[self.color] if color != "white" else -1
        self.radius = 5.3

    def move(self, app):
        tableLeft = app.tableCenterX - app.tableLength / 2
        tableRight = app.tableCenterX + app.tableLength / 2
        tableTop = app.tableCenterY - app.tableWidth / 2
        tableBot = app.tableCenterY + app.tableWidth / 2

        self.speed = (self.vx ** 2 + self.vy ** 2) ** 0.5

        # Deceleration function
        # Question: bound for almost equal? how to guarantee that it will stop?
        # Current Solution: make sure the bound is larger than deceleration.
        # =====================================================================
        if (self.vx ** 2 + self.vy ** 2) ** 0.5 > 0.25:
            deceleration = 0.5
            decelerationX = - deceleration * self.vx / self.speed
            decelerationY = - deceleration * self.vy / self.speed
            self.vx += decelerationX
            self.vy += decelerationY 
        else:
            self.vx = 0
            self.vy = 0
            deceleration = 0
            decelerationX = 0
            decelerationY = 0
        
        # Moving function
        # =====================================================================
        self.speed = (self.vx ** 2 + self.vy ** 2) ** 0.5
        self.cx += self.vx
        self.cy += self.vy

        # Collision with boundary function
        # =====================================================================
        if self.cx > tableRight - self.radius:
            self.cx = tableRight - self.radius
            self.vx = -self.vx
        elif self.cx < tableLeft + self.radius:
            self.cx = tableLeft + self.radius
            self.vx = -self.vx
        elif self.cy < tableTop + self.radius:
            self.cy = tableTop + self.radius
            self.vy = -self.vy
        elif self.cy > tableBot - self.radius:
            self.cy = tableBot - self.radius
            self.vy = -self.vy


# Drawing and initlization functions
# ========================================================================


# Intialize snooker balls
def initializeBalls(app):
    app.whiteBall = Ball("white", app.tableCenterX, app.tableCenterY)


# draw snooker balls
def drawBalls(app):
    drawCircle(
        app.whiteBall.cx,
        app.whiteBall.cy,
        app.whiteBall.radius,
        fill="white",
        border="black",
        borderWidth=1,
    )


# ========================================================================
# cue stick functions (drawing)
# ========================================================================


def drawCueStick(app, aimingDirection):
    ballRad = app.whiteBall.radius
    unitX = aimingDirection[0]
    unitY = aimingDirection[1]
    cueLength = 120 * 2
    startX = app.whiteBall.cx + 2 * ballRad * unitX
    startY = app.whiteBall.cy + 2 * ballRad * unitY
    endX = app.whiteBall.cx + cueLength * unitX
    endY = app.whiteBall.cy + cueLength * unitY
    drawLine(startX, startY, endX, endY, lineWidth=5)


# ========================================================================
# Game initializations (newGame)
# ========================================================================


def newGame(app):
    initializeTableGeometry(app)
    initializeBalls(app)


# ========================================================================
# Main functions (onAppStart, redrawAll, takeStep, onKeyPress)
# ========================================================================


def onAppStart(app):
    app.mouseX = 0
    app.mouseY = 0
    app.aiming = True
    app.holding = False
    app.moving = False
    app.aimingDirection = [1, 1]
    app.hitForce = 0
    newGame(app)


def redrawAll(app):
    drawSnookerTable(app)
    drawBalls(app)
    if app.aiming == True:
        drawCueStick(app, app.aimingDirection)


def onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY
    if app.aiming == True:
        aimingDistance = distance(
            app.mouseX, app.mouseY, app.whiteBall.cx, app.whiteBall.cy
        )
        app.aimingDirection = [
            (app.whiteBall.cx - app.mouseX) / aimingDistance,
            (app.whiteBall.cy - app.mouseY) / aimingDistance,
        ]


def onMousePress(app, mouseX, mouseY):
    if app.aiming == True:
        app.holding = True


def onMouseRelease(app, mouseX, mouseY):
    if app.aiming == True:
        app.aiming = False
        app.holding = False
        app.moving = True
        app.whiteBall.vx = - app.hitForce * app.aimingDirection[0]
        app.whiteBall.vy = - app.hitForce * app.aimingDirection[1]
        app.hitForce = 0


def onStep(app):
    takeStep(app)


def takeStep(app):
    if app.holding == True:
        app.hitForce += 1
    if app.moving == True:
        app.whiteBall.move(app)
    if app.moving == True and app.whiteBall.speed == 0:
        app.moving = False
        app.aiming = True


def onKeyPress(app, key):
    if key == "h":
        app.whiteBall.vx = 30
        app.whiteBall.vy = -10
    if key == "s":
        takeStep(app)


def main():
    runApp()


main()
