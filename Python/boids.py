import random
import tkinter
import time

width = 900
height = 800

boids = []
preds = []


def initBoids(numBoids):
    for i in range(numBoids):
        boids.append( {
            "x": random.random() * width,
            "y": random.random() * height,
            "dx": random.random() * 10 - 5,
            "dy": random.random() * 10 - 5,
            "history": [],
        } )


def initPredators(numPredators):
    for i in range(numPredators):
        preds.append( {
            "x": random.random() * width,
            "y": random.random() * height,
            "dx": random.random() * 10 - 5,
            "dy": random.random() * 10 - 5,
            "history": [],
        } )


def distance(boid1, boid2):
    number = ( (boid1["x"] - boid2["x"]) * (boid1["x"] - boid2["x"]) +
               (boid1["y"] - boid2["y"]) * (boid1["y"] - boid2["y"])
             ) ** (1/2)
    return number


def nClosestBoids(boid, n):

    # Copy of the boids list
    newBoids = boids

    # Sorting by distance
    newBoids2 = sorted(newBoids, key=lambda e: distance(e, boid))

    # Return the "n" closest
    return newBoids2[0:n+1]


def keepWithinBounds(boid):
    margin = 200
    turnFactor = 1.

    if boid["x"] < margin:
        boid["dx"] += turnFactor

    if boid["x"] > (width - margin):
        boid["dx"] -= turnFactor

    if boid["y"] < margin:
        boid["dy"] += turnFactor

    if boid["y"] > (height - margin):
        boid["dy"] -= turnFactor


def flyTowardsCenter(boid):
    centerX = 0
    centerY = 0
    numNeighbors = 0

    for otherBoid in boids:
        if distance(boid, otherBoid) < visualRange:
            centerX += otherBoid["x"]
            centerY += otherBoid["y"]
            numNeighbors += 1

    if numNeighbors != 0:
        centerX = centerX / numNeighbors
        centerY = centerY / numNeighbors

        boid["dx"] += (centerX - boid["x"]) * centeringFactor
        boid["dy"] += (centerY - boid["y"]) * centeringFactor


def flyTowardsCenterPredators(boid):
    centerX = 0
    centerY = 0
    numNeighbors = 0

    for otherBoid in preds:
        if distance(boid, otherBoid) < visualRange:
            centerX += otherBoid["x"]
            centerY += otherBoid["y"]
            numNeighbors += 1

    if numNeighbors != 0:
        centerX = centerX / numNeighbors
        centerY = centerY / numNeighbors

        boid["dx"] += (centerX - boid["x"]) * centeringFactor
        boid["dy"] += (centerY - boid["y"]) * centeringFactor


def avoidOthers(boid):
    minDistance = 20
    moveX = 0
    moveY = 0

    for otherBoid in boids:
        if otherBoid != boid:
            if distance(boid, otherBoid) < minDistance:
                moveX += boid["x"] - otherBoid["x"]
                moveY += boid["y"] - otherBoid["y"]

    boid["dx"] += moveX * avoidFactor
    boid["dy"] += moveY * avoidFactor


def avoidPredators(boid):
    minDistance = 40
    moveX = 0
    moveY = 0

    for pred in preds:
        if distance(boid, pred) < minDistance:
            moveX += boid["x"] - pred["x"]
            moveY += boid["y"] - pred["y"]

    boid["dx"] += moveX * avoidPredatorFactor
    boid["dy"] += moveY * avoidPredatorFactor


def avoidOthersPredators(boid):
    minDistance = 20
    moveX = 0
    moveY = 0

    for otherBoid in preds:
        if otherBoid != boid:
            if distance(boid, otherBoid) < minDistance:
                moveX += boid["x"] - otherBoid["x"]
                moveY += boid["y"] - otherBoid["y"]

    boid["dx"] += moveX * avoidFactor
    boid["dy"] += moveY * avoidFactor


def matchVelocity(boid):
    avgDX = 0
    avgDY = 0
    numNeighbors = 0

    for otherBoid in boids:
        if distance(boid, otherBoid) < visualRange:
            avgDX += otherBoid["dx"]
            avgDY += otherBoid["dy"]
            numNeighbors += 1

    if numNeighbors != 0:
        avgDX = avgDX /numNeighbors
        avgDY = avgDY / numNeighbors

        boid["dx"] += (avgDX - boid["dx"]) * matchingFactor
        boid["dy"] += (avgDY - boid["dy"]) * matchingFactor

    else:
        boid["dx"] += boid["dx"] * 0.5
        boid["dy"] += boid["dy"] * 0.5


def matchVelocityPredators(boid):
    avgDX = 0
    avgDY = 0
    numNeighbors = 0

    for otherBoid in preds:
        if distance(boid, otherBoid) < visualRange:
            avgDX += otherBoid["dx"]
            avgDY += otherBoid["dy"]
            numNeighbors += 1

    if numNeighbors != 0:
        avgDX = avgDX /numNeighbors
        avgDY = avgDY / numNeighbors

        boid["dx"] += (avgDX - boid["dx"]) * matchingFactor
        boid["dy"] += (avgDY - boid["dy"]) * matchingFactor

    else:
        boid["dx"] += boid["dx"] * 0.5
        boid["dy"] += boid["dy"] * 0.5


def limitSpeed(boid):
    speedLimit = 15

    speed = ((boid["dx"] * boid["dx"]) + (boid["dy"] * boid["dy"])) ** (1/2)
    if speed > speedLimit:
        boid["dx"] = (boid["dx"] / speed) * speedLimit
        boid["dy"] = (boid["dy"] / speed) * speedLimit


def strongWind(boid):
    boid["dx"] = boid["dx"] + (windX * windFactor)
    boid["dy"] = boid["dy"] + (windY * windFactor)

# Main loop
def animationLoop():
    global loopCount

    # Update each boid
    for boid in boids:
        # Velocity updates
        flyTowardsCenter(boid)
        avoidOthers(boid)
        avoidPredators(boid)
        matchVelocity(boid)
        strongWind(boid)
        limitSpeed(boid)
        keepWithinBounds(boid)

        # Position updates
        boid["x"] += boid["dx"]
        boid["y"] += boid["dy"]
        boid["history"].append((boid["x"], boid["y"]))
        boid["history"] = boid["history"][-50:]

    # Update each predator
    for pred in preds:
        # Velocity updates
        flyTowardsCenterPredators(pred)
        avoidOthersPredators(pred)
        matchVelocityPredators(pred)
        strongWind(pred)
        limitSpeed(pred)
        keepWithinBounds(pred)

        # Position updates
        pred["x"] += pred["dx"]
        pred["y"] += pred["dy"]
        pred["history"].append((pred["x"], pred["y"]))
        pred["history"] = pred["history"][-50:]

    # Clear the canvas and redraw all the boids and predators with their new positions
    myCanvas.delete("all")
    for boid in boids:
        myCanvas.create_oval(boid["x"], boid["y"],
                             boid["x"] + 10, boid["y"] + 10,
                             fill="blue")

        if (draw_trail) and loopCount > 1:
            myCanvas.create_line(boid["history"])

    for pred in preds:
        myCanvas.create_oval(pred["x"], pred["y"],
                             pred["x"] + 10, pred["y"] + 10,
                             fill="red")

        if (draw_trail) and loopCount > 1:
            myCanvas.create_line(pred["history"])

    # Next loop
    time.sleep(0.01)
    loopCount += 1
    root.update()
    animationLoop()


def reset():
    global boids
    global preds
    global numBoids
    global numPredators
    global visualRange
    global centeringFactor
    global avoidFactor
    global matchingFactor
    global avoidPredatorFactor
    global windX
    global windY
    global windFactor
    global loopCount

    boids = []
    preds = []
    numBoids = int(entryBoids.get())
    numPredators = int(entryPreds.get())
    visualRange = int(entryVR.get())
    centeringFactor = float(entryCF.get())
    avoidFactor = float(entryAF.get())
    matchingFactor = float(entryMF.get())
    avoidPredatorFactor = float(entryAPF.get())
    windX = float(entryWX.get())
    windY = float(entryWY.get())
    windFactor = float(entryWF.get())
    loopCount = 0

    initBoids(numBoids)
    initPredators(numPredators)


def drawTrail():
    global draw_trail

    if not draw_trail:
        draw_trail = True

    else:
        draw_trail = False


# init tk
root = tkinter.Tk()

# create canvas
myCanvas = tkinter.Canvas(root, bg="white", height=height, width=width)
myCanvas.grid(row=0, column=0, columnspan=5)

# Reset button
resetButton = tkinter.Button(root, text="Reset", command=reset)
resetButton.grid(row=1, column=0)

# Entry the number of boids
numBoids = 100

labelBoids = tkinter.Label(root, text="Boids:")
labelBoids.grid(row=1, column=1)
entryBoids = tkinter.Entry(root, bd=5)
entryBoids.insert(0, str(numBoids))
entryBoids.grid(row=1, column=2)

# Entry the number of boids
numPredators = 1

labelPreds = tkinter.Label(root, text="Predators:")
labelPreds.grid(row=1, column=3)
entryPreds = tkinter.Entry(root, bd=5)
entryPreds.insert(0, str(numPredators))
entryPreds.grid(row=1, column=4)

# Entry the centering factor
centeringFactor = 0.005

labelCF = tkinter.Label(root, text="Coherence:")
labelCF.grid(row=2, column=1)
entryCF = tkinter.Entry(root, bd=5)
entryCF.insert(0, str(centeringFactor))
entryCF.grid(row=2, column=2)

# Entry the avoid factor
avoidFactor = 0.05

labelAF = tkinter.Label(root, text="Separation:")
labelAF.grid(row=2, column=3)
entryAF = tkinter.Entry(root, bd=5)
entryAF.insert(0, str(avoidFactor))
entryAF.grid(row=2, column=4)

# Entry the match speed factor
matchingFactor = 0.05

labelMF = tkinter.Label(root, text="Alignment:")
labelMF.grid(row=3, column=1)
entryMF = tkinter.Entry(root, bd=5)
entryMF.insert(0, str(matchingFactor))
entryMF.grid(row=3, column=2)

# Entry the avoid predator factor
avoidPredatorFactor = 0.5

labelAPF = tkinter.Label(root, text="Pred separation:")
labelAPF.grid(row=3, column=3)
entryAPF = tkinter.Entry(root, bd=5)
entryAPF.insert(0, str(avoidPredatorFactor))
entryAPF.grid(row=3, column=4)

# Entry the wind X direction
windX = 1

labelWX = tkinter.Label(root, text="Wind X:")
labelWX.grid(row=4, column=1)
entryWX = tkinter.Entry(root, bd=5)
entryWX.insert(0, str(windX))
entryWX.grid(row=4, column=2)

# Entry the wind Y direction
windY = 1

labelWY = tkinter.Label(root, text="Wind Y:")
labelWY.grid(row=4, column=3)
entryWY = tkinter.Entry(root, bd=5)
entryWY.insert(0, str(windY))
entryWY.grid(row=4, column=4)

# Entry the wind factor
windFactor = 0

labelWF = tkinter.Label(root, text="Wind force:")
labelWF.grid(row=5, column=1)
entryWF = tkinter.Entry(root, bd=5)
entryWF.insert(0, str(windFactor))
entryWF.grid(row=5, column=2)

# Entry the visual range
visualRange = 75

labelVR = tkinter.Label(root, text="Visual range:")
labelVR.grid(row=5, column=3)
entryVR = tkinter.Entry(root, bd=5)
entryVR.insert(0, str(visualRange))
entryVR.grid(row=5, column=4)

# Trail
draw_trail = False
loopCount = 0

trailButton = tkinter.Button(root, text="Trails", command=drawTrail)
trailButton.grid(row=2, column=0)


# Obtain first batch of boids and predators
initBoids(numBoids)
initPredators(numPredators)

# Start the loop
animationLoop()

# Show
root.mainloop()
