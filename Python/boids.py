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
        if distance(boid, otherBoid) < visualRangePred:
            centerX += otherBoid["x"]
            centerY += otherBoid["y"]
            numNeighbors += 1

    if numNeighbors != 0:
        centerX = centerX / numNeighbors
        centerY = centerY / numNeighbors

        boid["dx"] += (centerX - boid["x"]) * centeringFactorPred
        boid["dy"] += (centerY - boid["y"]) * centeringFactorPred


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

    boid["dx"] += moveX * avoidFactorPred
    boid["dy"] += moveY * avoidFactorPred


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
        if distance(boid, otherBoid) < visualRangePred:
            avgDX += otherBoid["dx"]
            avgDY += otherBoid["dy"]
            numNeighbors += 1

    if numNeighbors != 0:
        avgDX = avgDX / numNeighbors
        avgDY = avgDY / numNeighbors

        boid["dx"] += (avgDX - boid["dx"]) * matchingFactorPred
        boid["dy"] += (avgDY - boid["dy"]) * matchingFactorPred

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
            myCanvas.create_line(boid["history"], fill="blue")

    for pred in preds:
        myCanvas.create_oval(pred["x"], pred["y"],
                             pred["x"] + 10, pred["y"] + 10,
                             fill="red")

        if (draw_trail) and loopCount > 1:
            myCanvas.create_line(pred["history"], fill="red")

    labelNumBoids.config(text=str(len(boids)))
    labelNumPreds.config(text=str(len(preds)))

    # Next loop
    time.sleep(0.01)
    loopCount += 1
    root.update()
    animationLoop()


def reset():
    # Boids variables
    global boids
    global numBoids
    global centeringFactor
    global avoidFactor
    global matchingFactor
    global avoidPredatorFactor
    global visualRange

    boids = []
    numBoids = int(entryBoids.get())
    centeringFactor = float(entryCF.get())
    avoidFactor = float(entryAF.get())
    matchingFactor = float(entryMF.get())
    avoidPredatorFactor = float(entryAPF.get())
    visualRange = int(entryVR.get())

    # Predator variables
    global preds
    global numPredators
    global centeringFactorPred
    global avoidFactorPred
    global matchingFactorPred
    global avoidPredatorFactorPred
    global visualRangePred

    preds = []
    numPredators = int(entryPreds.get())
    centeringFactorPred = float(entryCFPred.get())
    avoidFactorPred = float(entryAFPred.get())
    matchingFactorPred = float(entryMFPred.get())
    avoidPredatorFactorPred = float(entryAPFPred.get())
    visualRangePred = int(entryVRPred.get())

    # Wind variables
    global windX
    global windY
    global windFactor

    windX = float(entryWX.get())
    windY = float(entryWY.get())
    windFactor = float(entryWF.get())

    # Other things
    global loopCount
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
myCanvas.grid(row=0, column=0, columnspan=5, rowspan=20)

# Reset button
resetButton = tkinter.Button(root, text="Reset", command=reset)
resetButton.grid(row=0, column=7)

# Trail
draw_trail = False
loopCount = 0

trailButton = tkinter.Button(root, text="Trails", command=drawTrail)
trailButton.grid(row=0, column=8)

# Boids title
labelBoidsTitle = tkinter.Label(root, text="Boids")
labelBoidsTitle.grid(row=1, column=6, columnspan=6)

# Entry the number of boids
numBoids = 100

labelBoids = tkinter.Label(root, text="Boids:")
labelBoids.grid(row=2, column=6)
entryBoids = tkinter.Entry(root, bd=5)
entryBoids.insert(0, str(numBoids))
entryBoids.grid(row=2, column=7)

# Entry the centering factor for the boids
centeringFactor = 0.005

labelCF = tkinter.Label(root, text="Coherence:")
labelCF.grid(row=2, column=8)
entryCF = tkinter.Entry(root, bd=5)
entryCF.insert(0, str(centeringFactor))
entryCF.grid(row=2, column=9)

# Entry the avoid factor for the boids
avoidFactor = 0.05

labelAF = tkinter.Label(root, text="Separation:")
labelAF.grid(row=2, column=10)
entryAF = tkinter.Entry(root, bd=5)
entryAF.insert(0, str(avoidFactor))
entryAF.grid(row=2, column=11)

# Entry the match speed factor for the boids
matchingFactor = 0.05

labelMF = tkinter.Label(root, text="Alignment:")
labelMF.grid(row=3, column=6)
entryMF = tkinter.Entry(root, bd=5)
entryMF.insert(0, str(matchingFactor))
entryMF.grid(row=3, column=7)

# Entry the avoid predator factor for the boids
avoidPredatorFactor = 0.5

labelAPF = tkinter.Label(root, text="Pred separation:")
labelAPF.grid(row=3, column=8)
entryAPF = tkinter.Entry(root, bd=5)
entryAPF.insert(0, str(avoidPredatorFactor))
entryAPF.grid(row=3, column=9)

# Entry the visual range for the boids
visualRange = 75

labelVR = tkinter.Label(root, text="Visual range:")
labelVR.grid(row=3, column=10)
entryVR = tkinter.Entry(root, bd=5)
entryVR.insert(0, str(visualRange))
entryVR.grid(row=3, column=11)

# Predator title
labelPredators = tkinter.Label(root, text="Predators")
labelPredators.grid(row=4, column=6, columnspan=6)

# Entry the number of predators
numPredators = 0

labelPreds = tkinter.Label(root, text="Predators:")
labelPreds.grid(row=5, column=6)
entryPreds = tkinter.Entry(root, bd=5)
entryPreds.insert(0, str(numPredators))
entryPreds.grid(row=5, column=7)

# Entry the centering factor for the predators
centeringFactorPred = 0.005

labelCFPred = tkinter.Label(root, text="Coherence:")
labelCFPred.grid(row=5, column=8)
entryCFPred = tkinter.Entry(root, bd=5)
entryCFPred.insert(0, str(centeringFactorPred))
entryCFPred.grid(row=5, column=9)

# Entry the avoid factor for the predators
avoidFactorPred = 0.05

labelAFPred = tkinter.Label(root, text="Separation:")
labelAFPred.grid(row=5, column=10)
entryAFPred = tkinter.Entry(root, bd=5)
entryAFPred.insert(0, str(avoidFactorPred))
entryAFPred.grid(row=5, column=11)

# Entry the match speed factor for the predators
matchingFactorPred = 0.05

labelMFPred = tkinter.Label(root, text="Alignment:")
labelMFPred.grid(row=6, column=6)
entryMFPred = tkinter.Entry(root, bd=5)
entryMFPred.insert(0, str(matchingFactorPred))
entryMFPred.grid(row=6, column=7)

# Entry the avoid predator factor for the predators
avoidPredatorFactorPred = 0.5

labelAPFPred = tkinter.Label(root, text="Pred separation:")
labelAPFPred.grid(row=6, column=8)
entryAPFPred = tkinter.Entry(root, bd=5)
entryAPFPred.insert(0, str(avoidPredatorFactorPred))
entryAPFPred.grid(row=6, column=9)

# Entry the visual range for the predators
visualRangePred = 75

labelVRPred = tkinter.Label(root, text="Visual range:")
labelVRPred.grid(row=6, column=10)
entryVRPred = tkinter.Entry(root, bd=5)
entryVRPred.insert(0, str(visualRangePred))
entryVRPred.grid(row=6, column=11)

# Wind title
labelWind = tkinter.Label(root, text="Wind")
labelWind.grid(row=7, column=6, columnspan=6)

# Entry the wind X direction
windX = 1

labelWX = tkinter.Label(root, text="Wind X:")
labelWX.grid(row=8, column=6)
entryWX = tkinter.Entry(root, bd=5)
entryWX.insert(0, str(windX))
entryWX.grid(row=8, column=7)

# Entry the wind Y direction
windY = 1

labelWY = tkinter.Label(root, text="Wind Y:")
labelWY.grid(row=8, column=8)
entryWY = tkinter.Entry(root, bd=5)
entryWY.insert(0, str(windY))
entryWY.grid(row=8, column=9)

# Entry the wind factor
windFactor = 0

labelWF = tkinter.Label(root, text="Wind force:")
labelWF.grid(row=8, column=10)
entryWF = tkinter.Entry(root, bd=5)
entryWF.insert(0, str(windFactor))
entryWF.grid(row=8, column=11)

# Statistics title
labelWind = tkinter.Label(root, text="Statistics")
labelWind.grid(row=9, column=6, columnspan=6)

# Boids numbers in screen
labelShowBoids = tkinter.Label(root, text="Boids:")
labelShowBoids.grid(row=10, column=6)
labelNumBoids = tkinter.Label(root, text=str(len(boids)))
labelNumBoids.grid(row=10, column=7)

# Predator numbers in screen
labelShowPreds = tkinter.Label(root, text="Preds:")
labelShowPreds.grid(row=10, column=8)
labelNumPreds = tkinter.Label(root, text=str(len(preds)))
labelNumPreds.grid(row=10, column=9)

# Obtain first batch of boids and predators
initBoids(numBoids)
initPredators(numPredators)

# Start the loop
animationLoop()

# Show
root.mainloop()
