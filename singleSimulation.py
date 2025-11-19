from Entity.obstacle import Obstacle
from Entity.vehicle import Vehicle

from math import pi, cos

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


    def __init__(self, numberOfObstacles, sandboxSize: float = 2000.0, minDistance: float = 500.0):
        self.car = Vehicle()
        self.sandboxSize = sandboxSize
        self.fitness = 0.0

        self.crashed = False

        self.obstacleList: list[Obstacle] = []
        for _ in range(numberOfObstacles):
            self.obstacleList.append(Obstacle(float("Infinity"), 0.0, self.sandboxSize))

    def tick(self, turning: float = 0.0, forward: float = 0.0) -> None:
        """
        perform one tick of the simulation, with inputs given to the tick for the car
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
                obstacle.respawn(self.car.direction)

            # once the obstacle has been respawned (if necessary), move it in the given direction
            obstacle.move(self.car.speed, self.car.direction)

            # and check to see if the car has collided with the obstacle
            if self.car.collidedWith(obstacle):
                # if it has then this simulation is done
                self.crashed = True
                obstacle.collidingWithCar = True

        # go through every dot sensor and check to see if there are any being detected
        for sensor in self.car.dotSensorList:
            sensor.updateDetect(self.obstacleList)

        self.fitness += (cos(self.car.direction) * self.car.speed)

    def run(self, maxTicks: int = 5_000_000):
        """
        run an entire simulation either until the car crashes or until it hits a tick limit
        """
        for i in range(maxTicks):
            self.tick()
            if self.crashed:
                break
