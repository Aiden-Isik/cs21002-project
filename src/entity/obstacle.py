from math import sin, cos, pi
import random

class Obstacle:
    @staticmethod
    def radius() -> float:
        """
        returns the radius of the obstacle in pixels
        """
        return 20.0

    """
    An obstacle that has to be avoided by the vehicle that is being driven
    """
    def __init__(self, relative_X: float, relative_Y: float, sandboxSize: float = 2000.0, minimumDistance: float = 500.0) -> None:
        """
        position of the object is relative to the vehicle

        ifi relative_X is Infinity then this signals to the obstacle that it must respawn itself
        """
        self.relX = relative_X
        self.relY = relative_Y

        self.sandboxSize = sandboxSize
        self.minSpawnDistance = minimumDistance

        self.screenSpaceX = 0.0
        self.screenSpaceY = 0.0

        self.collidingWithCar = False

    def makeScreenSpacePoints(self, screen_X, screen_Y) -> None:
        """
        converts the relative positioning of the obstacle into screen space coordinates
        """
        self.screenSpaceX = self.relX + (screen_X / 2)
        self.screenSpaceY = self.relY + (screen_Y / 2)

    def move(self, speed, direction) -> None:
        """
        move the object with the speed and direcetion of the car given to it
        """
        self.relX -= speed * sin(direction)
        self.relY += speed * cos(direction)

    def respawn(self, vehicleDirection: float, position=None) -> None:
        """
        respawn the obstacle either at a random point in the general direction of the car or at a given position
        """
        if position is not None:
            self.relX = position[0]
            self.relY = position[1]
            return

        if (vehicleDirection > pi / 4) and (vehicleDirection < ((3 / 4) * pi)):
            self.relX = random.randint(round(self.minSpawnDistance), round(self.sandboxSize))
            self.relY = random.randint(-round(self.sandboxSize), round(self.sandboxSize))

        elif (vehicleDirection > pi / 4) and  vehicleDirection < ((5 / 4) * pi):
            self.relY = random.randint(round(self.minSpawnDistance), round(self.sandboxSize))
            self.relX = random.randint(-round(self.sandboxSize), round(self.sandboxSize))
        elif (vehicleDirection > pi / 4) and  vehicleDirection < ((7 / 4) * pi):
            self.relX = -random.randint(round(self.minSpawnDistance), round(self.sandboxSize))
            self.relY = random.randint(-round(self.sandboxSize), round(self.sandboxSize))
        else:
            self.relY = -random.randint(round(self.minSpawnDistance), round(self.sandboxSize))
            self.relX = random.randint(-round(self.sandboxSize), round(self.sandboxSize))
