from cmu_graphics import *
import math, copy


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
    app.width = 1000
    app.height = 800
    app.tableCenterX = app.width / 2
    app.tableCenterY = app.height / 2
    app.tableWidth = 120 * 3
    app.tableLength = 250 * 3
    app.lineLocation = app.tableCenterX - app.tableLength / 4
    app.pocketRadius = 10 / 2 * 3
    app.pocketLocations = [
        (
            app.tableCenterX + app.tableLength / 2 - app.pocketRadius / 2,
            app.tableCenterY + app.tableWidth / 2 - app.pocketRadius / 2,
        ),
        (
            app.tableCenterX + app.tableLength / 2 - app.pocketRadius / 2,
            app.tableCenterY - app.tableWidth / 2 + app.pocketRadius / 2,
        ),
        (
            app.tableCenterX - app.tableLength / 2 + app.pocketRadius / 2,
            app.tableCenterY + app.tableWidth / 2 - app.pocketRadius / 2,
        ),
        (
            app.tableCenterX - app.tableLength / 2 + app.pocketRadius / 2,
            app.tableCenterY - app.tableWidth / 2 + app.pocketRadius / 2,
        ),
        (
            app.tableCenterX,
            app.tableCenterY + app.tableWidth / 2 - app.pocketRadius / 2.5,
        ),
        (
            app.tableCenterX,
            app.tableCenterY - app.tableWidth / 2 + app.pocketRadius / 2.5,
        ),
    ]


# draw play area (Mat)
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


# draw pocket
def drawPocket(app):
    for pocketX, pocketY in app.pocketLocations:
        drawCircle(pocketX, pocketY, app.pocketRadius, fill="black")


# draw table border
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


# draw Pool Table
def drawPoolTable(app):
    drawTableBorder(app)
    drawPlayArea(app)
    drawPocket(app)


# ========================================================================
# Pool balls functions (class, intialization, drawing)
# ========================================================================

# class of Pool Balls
# ========================================================================


class Ball:
    def __init__(self, color, cx, cy):
        self.color = color
        self.cx = cx
        self.cy = cy
        self.vx = 0
        self.vy = 0
        self.radius = 6.8 * 1.5

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
        if (self.vx**2 + self.vy**2) ** 0.5 > 0.1:
            deceleration = 0.2
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

        for pocketX, pocketY in app.pocketLocations:
            if distance(self.cx, self.cy, pocketX, pocketY) <= app.pocketRadius:
                ballIndex = app.ballList.index(self)
                app.pottedBall.append(app.ballList.pop(ballIndex))

    # Collision check functinos
    # When checking the collision we will follow the order of a list.
    # ===============================================================
    def collide(self, other, app):
        self.speed = (self.vx**2 + self.vy**2) ** 0.5
        other.speed = (other.vx**2 + other.vy**2) ** 0.5
        if self.speed < 10 ** (-3) and other.speed < 10 ** (-3):
            self.vx = 0
            self.vy = 0
            other.vx = 0
            other.vy = 0
            return
        ballDistance = distance(self.cx, self.cy, other.cx, other.cy)
        normalDirection = [
            (self.cx - other.cx) / ballDistance,
            (self.cy - other.cy) / ballDistance,
        ]
        relVelocityMag = distance(self.vx, self.vy, other.vx, other.vy)
        newRelVelocity = [
            normalDirection[0] * relVelocityMag,
            normalDirection[1] * relVelocityMag,
        ]
        self.vx = self.vx + newRelVelocity[0]
        self.vy = self.vy + newRelVelocity[1]
        other.vx = other.vx - newRelVelocity[0] / 1.2
        other.vy = other.vy - newRelVelocity[1] / 1.2


# Drawing and initlization functions
# ========================================================================


# Initialize pool balls
def initializeBalls(app):
    colorList = [[1], [0, 1], [1, 8, 0], [0, 1, 0, 1], [1, 0, 1, 0, 0]]
    app.targetBallList = []
    ballRadius = 6.8 * 1.5
    initialX = app.tableCenterX + app.tableLength / 4
    initialY = app.tableCenterY
    dx = ballRadius * (math.sqrt(3) + 0.18)
    dy = ballRadius * 1.18
    for i in range(1, 6):
        for j in range(1, i + 1):
            ballCordX = initialX + (i - 1) * dx
            ballCordY = initialY + (i - 1) * dy - ballRadius * 2.1 * (j - 1)
            colorIndex = colorList[i - 1][j - 1]
            if colorIndex == 8:
                color = "black"
            elif colorIndex == 0:
                color = "yellow"
            else:
                color = "red"
            newRedBall = Ball(color, ballCordX, ballCordY)
            app.targetBallList.append(newRedBall)

    app.whiteBall = Ball(
        "white", app.tableCenterX - app.tableLength / 3, app.tableCenterY
    )

    app.ballList = [app.whiteBall] + app.targetBallList


# Draw pool balls
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
    cueLength = 150 * 2
    startX = app.whiteBall.cx + 2 * ballRad * unitX
    startY = app.whiteBall.cy + 2 * ballRad * unitY
    endX = app.whiteBall.cx + cueLength * unitX
    endY = app.whiteBall.cy + cueLength * unitY
    drawLine(startX, startY, endX, endY, lineWidth=5)


def findBestHit(app):
    tableLeft = app.tableCenterX - app.tableLength / 2
    tableRight = app.tableCenterX + app.tableLength / 2
    tableTop = app.tableCenterY - app.tableWidth / 2
    tableBot = app.tableCenterY + app.tableWidth / 2
    resultList = [0] * 73
    aimingBallList = copy.copy(app.ballList[1:])

    for i in range(73):
        aimingAngle = i * 5
        aimingAngleRad = aimingAngle * math.pi / 180
        aimingDirection = [math.cos(aimingAngleRad), math.sin(aimingAngleRad)]
        unitX = aimingDirection[0]
        unitY = aimingDirection[1]

        collisionPointList = []
        collisionBallList = []

        curX = app.whiteBall.cx
        curY = app.whiteBall.cy

        for t in range(600):
            curX = curX - unitX
            curY = curY - unitY
            if curX > tableRight or curX < tableLeft:
                collisionPointList.append((curX, curY))
                unitX = -unitX
            if curY > tableBot or curY < tableTop:
                collisionPointList.append((curX, curY))
                unitY = -unitY
            if t == 599:
                collisionPointList.append((curX, curY))
            for ball in aimingBallList:
                if distance(curX, curY, ball.cx, ball.cy) < ball.radius * 2:
                    collisionPointList.append((curX, curY))
                    ballIndex = aimingBallList.index(ball)
                    aimingBallList.pop(ballIndex)
                    unitX = - (ball.cx - curX) / distance(curX, curY, ball.cx, ball.cy)
                    unitY = - (ball.cy - curY) / distance(curX, curY, ball.cx, ball.cy)

        LineList = [(app.whiteBall.cx, app.whiteBall.cy)] + collisionPointList



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

    app.hittingPlayer = 0
    app.hittingTarget = [None, None]
    app.pottedBall = []
    app.gameOver = False
    app.win = False
    app.winner = None


def newGame(app):
    initializeTableGeometry(app)
    initializeBalls(app)
    initializeGamePlay(app)


def blackBallPotted(app):
    for ball in app.pottedBall:
        if ball.color == "black":
            return True
    return False


def whiteBallPotted(app):
    for ball in app.pottedBall:
        if ball.color == "white":
            return True
    return False


def targetBallLeft(app):
    if app.hittingTarget[0] == None:
        return True
    else:
        for ball in app.ballList:
            if ball.color == app.hittingTarget[0]:
                return True
        return False


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
        app.whiteBall.vx = -app.hitForce * app.aimingDirection[0]
        app.whiteBall.vy = -app.hitForce * app.aimingDirection[1]
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
        if whiteBallPotted(app):
            app.gameOver = True
            app.win = False
        if app.pottedBall == []:
            pass
        elif blackBallPotted(app):
            app.gameOver = True
            if targetBallLeft(app):
                app.win = False
            else:
                app.win = True
        elif app.hittingTarget[app.hittingPlayer] == None:
            app.hittingTarget[app.hittingPlayer] = app.pottedBall[0].color
        app.moving = False
        app.aiming = True


def onKeyPress(app, key):
    if key == "s":
        takeStep(app)
    if key == "r":
        newGame(app)
    testBlack = Ball("black", app.tableCenterX, app.tableCenterY)
    if key == "w":
        app.moving = True
        app.ballList = []


def redrawAll(app):
    if app.gameOver == False:
        drawPoolTable(app)
        drawBalls(app)
        if app.aiming == True:
            drawCueStick(app, app.aimingDirection)
        drawLabel(f"Force: {app.hitForce}", app.width - 150, 150, size=32)
        drawLabel(f"Target: {app.hittingTarget[0]}", app.width - 150, 120, size=32)
        drawLabel(f"Hitting Player: {app.hittingPlayer}", app.width - 150, 90, size=32)
    else:
        msg = "WIN" if app.win == True else "LOSE"
        drawLabel(msg, app.width / 2, app.height / 2, size=40)


def main():
    runApp()


main()
