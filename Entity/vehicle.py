import Entity.obstacle
import Entity.dotSensor

from math import cos, sin, sqrt, radians

class Vehicle:
    # every value in this list is an offset from forwards that a detection ray will be spawned in
    dotSensorAngleList = [-90, -70, -50, -30, -15, 0, 15, 30, 50, 70, 90]
    """
    A vehicle being controlled by something
    """
    def __init__(self):
        self.speed:     float = 0                       # pixels per tick
        self.direction: float = 0                       # radians away from pointing up, clockwise
        self.maxSpeed:  float = Vehicle.getHeight() / 2 # maximum speed of the car. keep it slow for now

        # the real location of the corners of the rectangle
        self.topLeft:     tuple = (0.0, 0.0)
        self.topRight:    tuple = (0.0, 0.0)
        self.bottomLeft:  tuple = (0.0, 0.0)
        self.bottomRight: tuple = (0.0, 0.0)

        # the locations of the four corners of the rectangle when no rotation is applied
        self.topLeftDatum:     tuple = ((0 - (Vehicle.getWidth() / 2)), (0 - (Vehicle.getHeight() / 2)))
        self.topRightDatum:    tuple = ((0 + (Vehicle.getWidth() / 2)), (0 - (Vehicle.getHeight() / 2)))
        self.bottomLeftDatum:  tuple = ((0 - (Vehicle.getWidth() / 2)), (0 + (Vehicle.getHeight() / 2)))
        self.bottomRightDatum: tuple = ((0 + (Vehicle.getWidth() / 2)), (0 + (Vehicle.getHeight() / 2)))

        # the locations of the four corners of the rectangle in screen space coordinates
        self.screenSpaceTopLeft:     tuple = (0.0, 0.0)
        self.screenSpaceTopRight:    tuple = (0.0, 0.0)
        self.screenSpaceBottomLeft:  tuple = (0.0, 0.0)
        self.screenSpaceBottomRight: tuple = (0.0, 0.0)
        self.screenSpaceCentre:      tuple = (0.0, 0.0)

        self.dotSensorList = []
        for angle in Vehicle.dotSensorAngleList:
            self.dotSensorList.append(Entity.dotSensor.DotSensor())
            self.dotSensorList[-1].setOffset(radians(angle))

    def rotatePoints(self) -> None:
        """
        Calculate the position of the points on the rectangle representing the car, given the rotation that it currently has

        also update the angle and positioning of any sensors attached to the car
        """
        self.topLeft     = (((self.topLeftDatum[0]     * cos(self.direction)) - (self.topLeftDatum[1]     * sin(self.direction))), ((self.topLeftDatum[0]     * sin(self.direction)) + (self.topLeftDatum[1]     * cos(self.direction))))
        self.topRight    = (((self.topRightDatum[0]    * cos(self.direction)) - (self.topRightDatum[1]    * sin(self.direction))), ((self.topRightDatum[0]    * sin(self.direction)) + (self.topRightDatum[1]    * cos(self.direction))))
        self.bottomLeft  = (((self.bottomLeftDatum[0]  * cos(self.direction)) - (self.bottomLeftDatum[1]  * sin(self.direction))), ((self.bottomLeftDatum[0]  * sin(self.direction)) + (self.bottomLeftDatum[1]  * cos(self.direction))))
        self.bottomRight = (((self.bottomRightDatum[0] * cos(self.direction)) - (self.bottomRightDatum[1] * sin(self.direction))), ((self.bottomRightDatum[0] * sin(self.direction)) + (self.bottomRightDatum[1] * cos(self.direction))))

        for sensor in self.dotSensorList:
            sensor.faceDirection(self.direction)

    def makeScreenSpacePoints(self, screen_X, screen_Y) -> None:
        """
        takes the width and height of the screen and turns normal coordinates into screen space coordinates
        """
        self.screenSpaceTopLeft     = ((self.topLeft[0]     + (screen_X / 2)), (self.topLeft[1]     + (screen_Y / 2)))
        self.screenSpaceTopRight    = ((self.topRight[0]    + (screen_X / 2)), (self.topRight[1]    + (screen_Y / 2)))
        self.screenSpaceBottomLeft  = ((self.bottomLeft[0]  + (screen_X / 2)), (self.bottomLeft[1]  + (screen_Y / 2)))
        self.screenSpaceBottomRight = ((self.bottomRight[0] + (screen_X / 2)), (self.bottomRight[1] + (screen_Y / 2)))
        self.screenSpaceCentre      = ((screen_X / 2),                         (screen_Y / 2))

    def collidedWith(self, obstacle: Entity.obstacle.Obstacle) -> bool:
        """
        checks the obstacle for collision with the vehicle

        mathematical theory taken from https://mathworld.wolfram.com/Circle-LineIntersection.html
        because this assumes that the circle is centred at (0, 0), all of the positions of the corners have to be offset to make it work
        """

        # these all check to see if the extended line intersects the circle
        # that means that if there is an intersection on both axes, then the circle is colliding with a corner of the rectangle
        # this does fail for when it hits a long edge but as long as the turn radius is larger than the circle radius this is not an issue
        collidesHorizontal = False
        collidesVertical = False

        # there is a collision if the discriminant is > 0
        # discriminant = (r * r) * (d_r * d_r) - (D * D)
        # where r is the radius of the circle
        # D = (x_1 * y_2) - (x_2 * y_1)
        # d_r = sqrt((d_x * d_x) + (d_y * d_y))
        # d_x = x_2 - x_1
        # d_y = y_2 - y_1

        r = Entity.obstacle.Obstacle.radius()

        # front vector
        d_x = (self.topRight[0] - obstacle.relX) - (self.topLeft[0] - obstacle.relX)
        d_y = (self.topRight[1] - obstacle.relY) - (self.topLeft[1] - obstacle.relY)

        d_r = sqrt((d_x * d_x) + (d_y * d_y))
        D = ((self.topLeft[0] - obstacle.relX) * (self.topRight[1] - obstacle.relY)) - ((self.topRight[0] - obstacle.relX) * (self.topLeft[1] - obstacle.relY))
        discriminant = (r * r) * (d_r * d_r) - (D * D)

        if discriminant > 0:
            collidesHorizontal = True



        # bottom vector
        d_x = (self.bottomLeft[0] - obstacle.relX) - (self.bottomRight[0] - obstacle.relX)
        d_y = (self.bottomLeft[1] - obstacle.relY) - (self.bottomRight[1] - obstacle.relY)

        d_r = sqrt((d_x * d_x) + (d_y * d_y))
        D = ((self.bottomRight[0] - obstacle.relX) * (self.bottomLeft[1] - obstacle.relY)) - ((self.bottomLeft[0] - obstacle.relX) * (self.bottomRight[1] - obstacle.relY))
        discriminant = (r * r) * (d_r * d_r) - (D * D)

        if discriminant > 0:
            collidesHorizontal = True



        # can break out of the function early here, since if there is no horizontal collision then the function will return false anyways
        if not collidesHorizontal:
            return False



        # right vector
        d_x = (self.bottomRight[0] - obstacle.relX) - (self.topRight[0] - obstacle.relX)
        d_y = (self.bottomRight[1] - obstacle.relY) - (self.topRight[1] - obstacle.relY)

        d_r = sqrt((d_x * d_x) + (d_y * d_y))
        D = ((self.topRight[0] - obstacle.relX) * (self.bottomRight[1] - obstacle.relY)) - ((self.bottomRight[0] - obstacle.relX) * (self.topRight[1] - obstacle.relY))
        discriminant = (r * r) * (d_r * d_r) - (D * D)

        if discriminant > 0:
            collidesVertical = True



        # left vector
        d_x = (self.topLeft[0] - obstacle.relX) - (self.bottomLeft[0] - obstacle.relX)
        d_y = (self.topLeft[1] - obstacle.relY) - (self.bottomLeft[1] - obstacle.relY)

        d_r = sqrt((d_x * d_x) + (d_y * d_y))
        D = ((self.bottomLeft[0] - obstacle.relX) * (self.topLeft[1] - obstacle.relY)) - ((self.topLeft[0] - obstacle.relX) * (self.bottomLeft[1] - obstacle.relY))
        discriminant = (r * r) * (d_r * d_r) - (D * D)

        if discriminant > 0:
            collidesVertical = True



        # more than one intersection means that it is colliding with a corner
        if collidesHorizontal and collidesVertical:
            return True

        return False

    @staticmethod
    def getWidth() -> float:
        """
        Return the width of the vehicle in pixels
        """
        return 30.0

    @staticmethod
    def getHeight() -> float:
        """
        Return the height of the vehicle in pixels
        """
        return 60.0
