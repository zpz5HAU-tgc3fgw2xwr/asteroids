import pygame
import random
from constants import ASTEROID_MIN_RADIUS

class Asteroid(pygame.sprite.Sprite):
	containers = None

	def __init__(self, x, y, radius):
		super().__init__(self.containers or [])
		self.position = pygame.Vector2(x, y)
		self.velocity = pygame.Vector2(0, 0)
		self.radius = radius

	def split(self):
		self.kill()
		if self.radius > ASTEROID_MIN_RADIUS:
			angle = random.uniform(20, 50)
			reduced_radius = self.radius - ASTEROID_MIN_RADIUS

			asteroid1 = Asteroid(self.position.x, self.position.y, reduced_radius)
			asteroid1.velocity = self.velocity.rotate(angle) * 1.2
			asteroid1.add(self.containers)

			asteroid2 = Asteroid(self.position.x, self.position.y, reduced_radius)
			asteroid2.velocity = self.velocity.rotate(-angle) * 1.2
			asteroid2.add(self.containers)

	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius)

	def update(self, deltatime):
		self.position += self.velocity * deltatime
