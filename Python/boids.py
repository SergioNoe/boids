import random
import tkinter
import time

width = 900
height = 800

boids = []


def initBoids(numBoids):
    for i in range(numBoids):
        boids.append( {
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
    #centeringFactor = 0.005

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


def avoidOthers(boid):
    minDistance = 20
    #avoidFactor = 0.05
    moveX = 0
    moveY = 0

    for otherBoid in boids:
        if otherBoid != boid:
            if distance(boid, otherBoid) < minDistance:
                moveX += boid["x"] - otherBoid["x"]
                moveY += boid["y"] - otherBoid["y"]

    boid["dx"] += moveX * avoidFactor
    boid["dy"] += moveY * avoidFactor


def matchVelocity(boid):
    #matchingFactor = 0.05

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


def limitSpeed(boid):
    speedLimit = 15

    speed = ((boid["dx"] * boid["dx"]) + (boid["dy"] * boid["dy"])) ** (1/2)
    if speed > speedLimit:
        boid["dx"] = (boid["dx"] / speed) * speedLimit
        boid["dy"] = (boid["dy"] / speed) * speedLimit


# Main loop
def animationLoop():

    # Update each boid
    for boid in boids:
        # Velocity updates
        flyTowardsCenter(boid)
        avoidOthers(boid)
        matchVelocity(boid)
        limitSpeed(boid)
        keepWithinBounds(boid)

        # Position updates
        boid["x"] += boid["dx"]
        boid["y"] += boid["dy"]
        boid["history"].append((boid["x"], boid["y"]))
        boid["history"] = boid["history"][-50:]

    # Clear the canvas and redraw all the boids with their new positions
    myCanvas.delete("all")
    for boid in boids:
        myCanvas.create_oval(boid["x"], boid["y"],
                             boid["x"] + 10, boid["y"] + 10,
                             fill="blue")

    # Next loop
    time.sleep(0.009)
    root.update()
    animationLoop()


def reset():
    global boids
    global numBoids
    global visualRange
    global centeringFactor
    global avoidFactor
    global matchingFactor

    boids = []
    numBoids = int(entryBoids.get())
    visualRange = int(entryVR.get())
    centeringFactor = float(entryCF.get())
    avoidFactor = float(entryAF.get())
    matchingFactor = float(entryMF.get())

    initBoids(numBoids)


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

# Entry the centering factor
centeringFactor = 0.005

labelCF = tkinter.Label(root, text="Coherence:")
labelCF.grid(row=1, column=3)
entryCF = tkinter.Entry(root, bd=5)
entryCF.insert(0, str(centeringFactor))
entryCF.grid(row=1, column=4)

# Entry the avoid factor
avoidFactor = 0.05

labelAF = tkinter.Label(root, text="Separation:")
labelAF.grid(row=2, column=1)
entryAF = tkinter.Entry(root, bd=5)
entryAF.insert(0, str(avoidFactor))
entryAF.grid(row=2, column=2)

# Entry the match speed factor
matchingFactor = 0.05

labelMF = tkinter.Label(root, text="Alignment:")
labelMF.grid(row=2, column=3)
entryMF = tkinter.Entry(root, bd=5)
entryMF.insert(0, str(matchingFactor))
entryMF.grid(row=2, column=4)

# Entry the visual range
visualRange = 75

labelVR = tkinter.Label(root, text="Visual range:")
labelVR.grid(row=3, column=1)
entryVR = tkinter.Entry(root, bd=5)
entryVR.insert(0, str(visualRange))
entryVR.grid(row=3, column=2)

# Obtain first batch of boids
initBoids(numBoids)

# Start the loop
animationLoop()

# Show
root.mainloop()
