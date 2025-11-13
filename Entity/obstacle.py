from math import sin, cos

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
    def __init__(self, relative_X: float, relative_Y: float) -> None:
        """
        position of the object is relative to the vehicle
        """
        self.relX = relative_X
        self.relY = relative_Y

        self.screenSpaceX = 0.0
        self.screenSpaceY = 0.0

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
