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
    app.blackLocation = 32.5 * 2


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
        fill="lightSeaGreen",
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
        self.point = Ball.pointDict[self.color] if color != "white" else -1
        self.radius = 5.3

    def __repr__(self):
        return f"{self.color} Ball"

    def move(self, app, coef=+1):
        tableLeft = app.tableCenterX - app.tableLength / 2
        tableRight = app.tableCenterX + app.tableLength / 2
        tableTop = app.tableCenterY - app.tableWidth / 2
        tableBot = app.tableCenterY + app.tableWidth / 2

        self.speed = (self.vx**2 + self.vy**2) ** 0.5

        # Deceleration function
        # Question: bound for almost equal? how to guarantee that it will stop?
        # Current Solution: make sure the bound is larger than deceleration.
        # =====================================================================
        if (self.vx**2 + self.vy**2) ** 0.5 > 0.25:
            deceleration = 0.5
            decelerationX = -deceleration * self.vx / self.speed
            decelerationY = -deceleration * self.vy / self.speed
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
        self.speed = (self.vx**2 + self.vy**2) ** 0.5
        self.cx += self.vx * coef
        self.cy += self.vy * coef

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

    # Collision check functinos
    # When checking the collision we will follow the order of a list.
    # ===============================================================
    def collide(self, other, app):
        self.speed = (self.vx**2 + self.vy**2) ** 0.5
        other.speed = (other.vx**2 + other.vy**2) ** 0.5
        if self.speed < 10 ** (-3) and other.speed < 10 ** (-3):
            return
        CoefRes = 1  # Coefficient of restitution — 1 means elastic collision
        ballDistance = distance(self.cx, self.cy, other.cx, other.cy)
        normalDirection = [
            (self.cx - other.cx) / ballDistance,
            (self.cy - other.cy) / ballDistance,
        ]
        CMVelocity = [(self.vx + other.vx) / 2, (self.vy + other.vy) / 2]
        relVelocityMag = distance(self.vx, self.vy, other.vx, other.vy) / 2
        newRelVelocity = [
            normalDirection[0] * relVelocityMag * CoefRes,
            normalDirection[1] * relVelocityMag * CoefRes,
        ]
        self.vx = CMVelocity[0] + newRelVelocity[0]
        self.vy = CMVelocity[1] + newRelVelocity[1]
        other.vx = CMVelocity[0] - newRelVelocity[0]
        other.vy = CMVelocity[1] - newRelVelocity[1]


# Drawing and initlization functions
# ========================================================================


# Initialize snooker balls
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

    app.redBallList = []
    dx = app.pinkBall.radius * (math.sqrt(3) + 0.1)
    dy = app.pinkBall.radius * 1.1
    for i in range(1, 6):
        for j in range(1, i + 1):
            ballCordX = app.pinkBall.cx + app.pinkBall.radius * 2.2 + (i - 1) * dx
            ballCordY = (
                app.pinkBall.cy + (i - 1) * dy - app.pinkBall.radius * 2.1 * (j - 1)
            )
            newRedBall = Ball("red", ballCordX, ballCordY)
            app.redBallList.append(newRedBall)

    app.whiteBall = Ball("white", 180, app.tableCenterY)

    app.ballList = [app.whiteBall] + app.colorBallList + app.redBallList


# Draw snooker balls
def drawBalls(app):
    for ball in app.ballList:
        drawCircle(
            ball.cx,
            ball.cy,
            ball.radius,
            fill=ball.color,
            border="black",
            borderWidth=1,
        )


# ========================================================================
# Game initializations (newGame)
# ========================================================================


def onAppStart(app):
    newGame(app)


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

def isAppStop(app):
    for ball in app.ballList:
        if ball.vx != 0 and ball.vy != 0:
            return False
    return True

# ========================================================================
# Main functions (onAppStart, redrawAll, takeStep, onKeyPress)
# ========================================================================
def initializeGamePlay(app):
    app.mouseX = 0
    app.mouseY = 0
    app.aiming = True
    app.holding = False
    app.moving = False
    app.aimingDirection = [1, 1]
    app.hitForce = 0


def newGame(app):
    initializeTableGeometry(app)
    initializeBalls(app)
    initializeGamePlay(app)


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
        for i in range(len(app.ballList) - 1):
            for j in range(i + 1, len(app.ballList)):
                ball1 = app.ballList[i]
                ball2 = app.ballList[j]
                if distance(ball1.cx, ball1.cy, ball2.cx, ball2.cy) <= 2 * ball1.radius:
                    ball1.move(app, -1)
                    ball2.move(app, -1)
                    ball1.collide(ball2, app)

        for ball in app.ballList:
            ball.move(app)
    if app.moving == True and isAppStop(app):
        app.moving = False
        app.aiming = True


def onKeyPress(app, key):
    if key == "z":
        app.brownBall.vy = 10
    if key == "s":
        takeStep(app)


def redrawAll(app):
    drawSnookerTable(app)
    drawBalls(app)


def main():
    runApp()


main()
