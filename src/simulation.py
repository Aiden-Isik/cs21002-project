from entity.obstacle import Obstacle
from entity.vehicle import Vehicle
from entity.dotsensor import DotSensor

from dataclasses import dataclass
from math import pi, cos, radians

class SingleSimulation:
    """
    A class to control one instance of a simulation of a car not hitting any obstacles
    """

    # how much the car will turn in one tick
    # radians
    TurnAmount = 0.1

    # how far the car will travel in one tick
    # px per tick
    CarSpeed = 10

    # how fast the floor is lava fail condition rises
    # px per tick
    FloorIsLavaSpeed = 1

    # where the floor is lava fail condition starts, to give a little bit of buffer
    # px
    FloorIsLavaStart = -100


    def __init__(self, numberOfObstacles, sandboxSize: float = 2000.0, minDistance: float = 500.0):
        # Make sure obstacles are not spawned outside a valid range
        if sandboxSize < minDistance:
            raise ValueError("Invalid sandboxSize/minDistance combination, minDistance must be less than sandboxSize")

        # Sandbox initialisation
        self.sandboxSize = sandboxSize
        self.obstacleRespawnCount = 0

        # Vehicle initialisation
        self.car = Vehicle()
        self.fitness = 0.0
        self.crashed = False
        self.floorIsLavaHeight = SingleSimulation.FloorIsLavaStart

        # Obstacle initialisation
        self.obstacleList: list[Obstacle] = []
        for _ in range(numberOfObstacles):
            self.obstacleList.append(Obstacle(float("Infinity"), 0.0, self.sandboxSize))

    def copy(self):
        returnInstance                      = SingleSimulation(0)
        returnInstance.sandboxSize          = self.sandboxSize
        returnInstance.obstacleRespawnCount = self.obstacleRespawnCount


        # copy over the car ==================================================================
        returnInstance.car             = Vehicle()
        returnInstance.car.direction   = self.car.direction
        returnInstance.car.speed       = self.car.speed
        returnInstance.car.maxSpeed    = self.car.maxSpeed

        returnInstance.car.topLeft     = self.car.topLeft
        returnInstance.car.topRight    = self.car.topRight
        returnInstance.car.bottomLeft  = self.car.bottomLeft
        returnInstance.car.bottomRight = self.car.bottomRight

        returnInstance.car.topLeftDatum     = self.car.topLeftDatum
        returnInstance.car.topRightDatum    = self.car.topRightDatum
        returnInstance.car.bottomLeftDatum  = self.car.bottomLeftDatum
        returnInstance.car.bottomRightDatum = self.car.bottomRightDatum

        returnInstance.car.screenSpaceTopLeft     = self.car.screenSpaceTopLeft
        returnInstance.car.screenSpaceTopRight    = self.car.screenSpaceTopRight
        returnInstance.car.screenSpaceBottomLeft  = self.car.screenSpaceBottomLeft
        returnInstance.car.screenSpaceBottomRight = self.car.screenSpaceBottomRight
        returnInstance.car.screenSpaceCentre      = self.car.screenSpaceCentre

        for angle in self.car.dotSensorAngleList:
            returnInstance.car.dotSensorList.append(DotSensor())
            returnInstance.car.dotSensorList[-1].setOffset(radians(angle))

        returnInstance.car.rotatePoints()

        for obstacle in self.obstacleList:
            returnInstance.obstacleList.append(Obstacle(obstacle.relX, obstacle.relY, obstacle.sandboxSize, obstacle.minSpawnDistance))
            returnInstance.obstacleList[-1].screenSpaceX     = obstacle.screenSpaceX
            returnInstance.obstacleList[-1].screenSpaceY     = obstacle.screenSpaceY
            returnInstance.obstacleList[-1].collidingWithCar = obstacle.collidingWithCar

        # finished copying over the car ======================================================

        return returnInstance

    def tick(self, turning: float = 0.0, forward: float = 0.0) -> None:
        """
        Perform one tick of the simulation, with inputs given to the tick for the car
        turning < -0.5 means turn left, turning > 0.5 means turn right
        forward > 0.5 means go forward
        """
        # no point running the tick if the car has already crashed
        if self.crashed:
            return

        if turning < -0.5:
            self.car.direction -= SingleSimulation.TurnAmount

        if turning > 0.5:
            self.car.direction += SingleSimulation.TurnAmount

        # this keeps the value of direction a sane value
        if self.car.direction > (2 * pi):
            self.car.direction -= (2 * pi)
        elif self.car.direction < 0:
            self.car.direction += (2 * pi)

        if forward > 0.5:
            self.car.speed = SingleSimulation.CarSpeed
        else:
            self.car.speed = 0.0

        # set up the car first
        self.car.rotatePoints()

        # go through every obstacle that is part of this simulation and check to see if it needs respawned
        for obstacle in self.obstacleList:
            # if the object has fallen outside of the bounds specified, or if it has x position infinity, signalling that it needs a respawn
            if (abs(obstacle.relX) > self.sandboxSize) or (abs(obstacle.relY) > self.sandboxSize) or (obstacle.relX == float("Infinity")):
                # Create a new obstacle every 20 respawns, this has the effect of gradually increasing the difficulty
                if(self.obstacleRespawnCount % 20 == 0 and self.obstacleRespawnCount != 0):
                    self.obstacleList.append(Obstacle(float("Infinity"), 0.0, self.sandboxSize))

                obstacle.respawn(self.car.direction)
                self.obstacleRespawnCount += 1

            # once the obstacle has been respawned (if necessary), move it in the given direction
            obstacle.move(self.car.speed, self.car.direction)

            # and check to see if the car has collided with the obstacle
            if self.car.collidedWith(obstacle):
                # if it has then this simulation is done
                self.crashed = True
                obstacle.collidingWithCar = True

        # if the car isnt going in the correct direction quickly enough, fail it
        # this most likely means it got stuck doing donuts instead of progressing, which would otherwise lead to an infinite session
        self.floorIsLavaHeight += SingleSimulation.FloorIsLavaSpeed
        if self.fitness < self.floorIsLavaHeight:
            self.crashed = True

        # go through every dot sensor and check to see if there are any being detected
        for sensor in self.car.dotSensorList:
            sensor.updateDetect(self.obstacleList)

        # Increase the fitness (up direction)
        self.fitness += (cos(self.car.direction) * self.car.speed)
