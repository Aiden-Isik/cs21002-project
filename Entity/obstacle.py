import pygame

class Obstacle:
	@staticmethod
	def radius() -> float:
		"""
		returns the radius of the obstacle in pixels
		"""
		return 15.0

	"""
	An obstacle that has to be avoided by the vehicle that is being driven
	"""
	def __init__(self, relative_X: float, relative_Y: float) -> None:
		"""
		position of the object is relative to the vehicle
		"""
		self.relX = relative_X
		self.relY = relative_Y
