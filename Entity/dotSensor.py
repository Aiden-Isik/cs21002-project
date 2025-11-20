import Entity.obstacle

from math import cos, sin, sqrt

class DotSensor:
    """
    This class attempts to detect dots along a line from the centre point of the car up to a maximum given length

    self.detect is a value representing how close the nearest obstacle along the line is to the base of the sensor
    when it is 0 there is no obstacle detected, when it is 1, the obstacle is exactly on top of it, with linear interpolation in between
    """
    def __init__(self, length: float = 250.0):
        self.facingDirection = 0.0       # direction the vehicle is facing
        self.offsetAngle = 0.0           # offset of the ray from the vehicle direction
        self.length = length             # length of the ray from the centre of the car
        self.lengthSquared = length ** 2 # used in calculations
        self.detect = 0.0                # value of detection to feed into the AI
        self.farCorner = (0.0, 0.0)      # the relative coordinates of the far corner of the ray
        self.d_r_2 = 0.0                 # also used in calculations

    def faceDirection(self, direction: float):
        """
        update the direction of the sensor and recalculate the far corner
        """
        self.facingDirection = direction + self.offsetAngle

        cornerX = sin(self.facingDirection) * self.length
        cornerY = -(cos(self.facingDirection) * self.length)

        self.farCorner = (cornerX, cornerY)
        self.d_r_2 = ((self.farCorner[0] ** 2) + (self.farCorner[1] ** 2))

    def setOffset(self, offsetAngle):
        """
        set the offset to use from the direction given to the sensor
        """
        self.offsetAngle = offsetAngle

    def updateDetect(self, obstacleList: list[Entity.obstacle.Obstacle]):
        """
        goes through every obstacle in the list and finds the nearest one that will be detected, then updates self.detect with respect to it
        """

        nearestDistanceSquaredSoFar = float("Infinity")
        radiusSquared = (obstacleList[0].radius() ** 2)

        constantPart = radiusSquared * self.d_r_2

        for obstacle in obstacleList:
            # first check to see if the obstacle is in range
            distanceSquared = ((obstacle.relX ** 2) + (obstacle.relY ** 2))
            if (distanceSquared < nearestDistanceSquaredSoFar):
                # closer than what is currently closest, so check if it collides
                # mathematical theory taken from https://mathworld.wolfram.com/Circle-LineIntersection.html
                # because this assumes that the circle is centred at (0, 0), all of the positions of the corners have to be offset to make it work

                # see Vehicle.collidedWith, this is an optimised version of that

                D = (obstacle.relY * self.farCorner[0]) - (obstacle.relX * self.farCorner[1])

                # (delta > 0) means collision
                #    constantPart - (D * D) == delta
                if ((constantPart - (D * D)) > 0) and (distanceSquared <= self.lengthSquared):
                    # closer to the centre than any previous, so now check distance to far end with a small buffer (10%)
                    # this makes sure the direction is correct
                    if ((((self.farCorner[0] - obstacle.relX) ** 2) + ((self.farCorner[1] - obstacle.relY) ** 2)) * 1.1) < self.lengthSquared:
                        # we have a new closest colliding point!
                        nearestDistanceSquaredSoFar = distanceSquared

        # end of for loop
        if nearestDistanceSquaredSoFar == float("Infinity"):
            # no collision
            self.detect = 0.0
            return

        actualDistance = sqrt(nearestDistanceSquaredSoFar) # this is the distance from the centre, which is what we really care about for detect

        self.detect = min(1.0, max(0.0, (1.0 - (actualDistance / self.length))))

        print(f"collided {self.detect} {nearestDistanceSquaredSoFar} {self.farCorner[0]} {self.farCorner[1]}")
