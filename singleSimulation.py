from Entity.obstacle import Obstacle
from Entity.vehicle import Vehicle

class SingleSimulation:
    """
    A class to control one instance of a simulation of a car not hitting any obstacles
    """
    def __init__(self, numberOfObstacles):
        self.car = Vehicle()

        self.obstacleList = []
        for _ in range(numberOfObstacles):
            self.obstacleList.append(Obstacle(float("NaN"), float("NaN")))
