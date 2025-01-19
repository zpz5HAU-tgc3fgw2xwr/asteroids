import pygame

from asteroids.constants import SHOT_RADIUS
from asteroids.entities.base.circleshape import CircleShape

class Shot(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, SHOT_RADIUS)

	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, SHOT_RADIUS)

	def update(self, deltatime):
		self.position += self.velocity * deltatime