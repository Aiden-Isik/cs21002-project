import Entity.obstacle

from math import cos, sin

class Vehicle:
	"""
	A vehicle being controlled by something
	"""
	def __init__(self):
		self.speed: float     = 0 # pixels per tick
		self.direction: float = 0 # radians away from pointing up, clockwise

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

	def rotatePoints(self) -> None:
		"""
		Calculate the position of the points on the rectangle representing the car, given the rotation that it currently has
		"""
		self.topLeft     = (((self.topLeftDatum[0]     * cos(self.direction)) - (self.topLeftDatum[1]     * sin(self.direction))), ((self.topLeftDatum[0]     * sin(self.direction)) + (self.topLeftDatum[1]     * cos(self.direction))))
		self.topRight    = (((self.topRightDatum[0]    * cos(self.direction)) - (self.topRightDatum[1]    * sin(self.direction))), ((self.topRightDatum[0]    * sin(self.direction)) + (self.topRightDatum[1]    * cos(self.direction))))
		self.bottomLeft  = (((self.bottomLeftDatum[0]  * cos(self.direction)) - (self.bottomLeftDatum[1]  * sin(self.direction))), ((self.bottomLeftDatum[0]  * sin(self.direction)) + (self.bottomLeftDatum[1]  * cos(self.direction))))
		self.bottomRight = (((self.bottomRightDatum[0] * cos(self.direction)) - (self.bottomRightDatum[1] * sin(self.direction))), ((self.bottomRightDatum[0] * sin(self.direction)) + (self.bottomRightDatum[1] * cos(self.direction))))

	def makeScreenSpacePoints(self, screen_X, screen_Y):
		"""
		takes the width and height of the screen and turns normal coordinates into screen space coordinates
		"""
		self.screenSpaceTopLeft     = ((self.topLeft[0]     + (screen_X / 2)), (self.topLeft[1]     + (screen_Y / 2)))
		self.screenSpaceTopRight    = ((self.topRight[0]    + (screen_X / 2)), (self.topRight[1]    + (screen_Y / 2)))
		self.screenSpaceBottomLeft  = ((self.bottomLeft[0]  + (screen_X / 2)), (self.bottomLeft[1]  + (screen_Y / 2)))
		self.screenSpaceBottomRight = ((self.bottomRight[0] + (screen_X / 2)), (self.bottomRight[1] + (screen_Y / 2)))

	def collidedWith(self, obstacle: Entity.obstacle.Obstacle) -> bool:
		"""
		checks the obstacle for collision with the vehicle
		"""
		frontVector = ((self.topRight[0]    - self.topLeft[0]),    (self.topRight[1]    - self.topLeft[1]))
		rightVector = ((self.bottomRight[0] - self.topRight[0]),   (self.bottomRight[1] - self.topRight[1]))
		backVector  = ((self.bottomLeft[0]  - self.bottomRight[0], (self.bottomLeft[1]  - self.bottomRight[1])))
		leftVector  = ((self.topLeft[0]     - self.bottomLeft[0]), (self.topLeft[1]     - self.bottomLeft[1]))

		return True

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
