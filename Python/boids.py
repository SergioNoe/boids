import random
import tkinter
import time

width = 900;
height = 800;

numBoids = 100
visualRange = 75

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
    centeringFactor = 0.005

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
    avoidFactor = 0.05
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
    matchingFactor = 0.05

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
        boid["dy"] += (avgDX - boid["dy"]) * matchingFactor

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
    root.update()
    animationLoop()


# init tk
root = tkinter.Tk()

# create canvas
myCanvas = tkinter.Canvas(root, bg="white", height=height, width=width)
myCanvas.pack()

initBoids(numBoids)

animationLoop()

# Show
root.mainloop()
