import pygame
import random
from asteroids.entities.asteroid import Asteroid
from asteroids.constants import *

class AsteroidField(pygame.sprite.Sprite):
	edges = [
		[
			pygame.Vector2(1, 0),
			lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
		],
		[
			pygame.Vector2(-1, 0),
			lambda y: pygame.Vector2(
				SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
			),
		],
		[
			pygame.Vector2(0, 1),
			lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
		],
		[
			pygame.Vector2(0, -1),
			lambda x: pygame.Vector2(
				x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
			),
		],
	]

	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.spawn_timer = 0.0

	def spawn(self, radius, position, velocity):
		asteroid = Asteroid(position.x, position.y, radius)
		asteroid.velocity = velocity

	def update(self, dt):
		self.spawn_timer += dt
		if self.spawn_timer > ASTEROID_SPAWN_RATE:
			self.spawn_timer = 0

			# Spawn a new asteroid at a random edge
			edge = random.choice(self.edges)
			speed = random.randint(40, 100)
			velocity = edge[0] * speed
			velocity = velocity.rotate(random.randint(-30, 30))
			position = edge[1](random.uniform(0, 1))

			# Randomize the radius
			radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
			self.spawn(radius, position, velocity)