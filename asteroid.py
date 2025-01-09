import pygame
import random

from constants import ASTEROID_MIN_RADIUS
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def split(self):
        self.kill()

        if self.radius > ASTEROID_MIN_RADIUS:
            angle = random.uniform(20, 50)
            radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, radius).velocity(self.velocity.rotate(angle)) * 1.2
            asteroid2 = Asteroid(self.position.x, self.position.y, radius).velocity(self.velocity.rotate(-angle)) * 1.2

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, 2)

    def update(self, deltatime):
        self.position += self.velocity * deltatime