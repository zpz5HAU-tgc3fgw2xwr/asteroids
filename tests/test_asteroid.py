import unittest
from unittest import mock
import pygame
from asteroid import Asteroid

class TestAsteroid(unittest.TestCase):
	def setUp(self):
		pygame.init()
		pygame.display.set_mode((800, 600))
		Asteroid.containers = mock.Mock()
		self.asteroid = Asteroid(x=0, y=0, radius=20)

	def test_initialization(self):
		"""Test that the Asteroid initializes with the correct values."""
		self.assertEqual(self.asteroid.radius, 20)
		self.assertEqual(self.asteroid.position.x, 0)
		self.assertEqual(self.asteroid.position.y, 0)

	def test_split_calls_kill_when_splitting(self):
		"""Test that the split method calls kill on the asteroid."""
		self.asteroid.kill = mock.Mock()
		self.asteroid.radius = 25
		self.asteroid.split()
		self.asteroid.kill.assert_called_once()

	def test_split_creates_new_asteroids_for_large_radius(self):
		"""Test that split spawns new asteroids if the radius is large."""
		self.asteroid.radius = 25
		self.asteroid.kill = mock.Mock()
		self.asteroid.velocity = pygame.Vector2(1, 0)

		Asteroid.containers = mock.Mock()
		with mock.patch("asteroid.Asteroid", wraps=Asteroid) as MockAsteroid:
			self.asteroid.split()
			MockAsteroid.assert_any_call(0, 0, 5)

	def test_draw_calls_pygame_draw_circle(self):
		"""Test that the draw method calls pygame's draw.circle with correct parameters."""
		mock_screen = mock.Mock()
		with mock.patch("pygame.draw.circle") as mock_draw_circle:
			self.asteroid.draw(mock_screen)
		mock_draw_circle.assert_called_once_with(mock_screen, "white", self.asteroid.position, self.asteroid.radius)

if __name__ == "__main__":
	unittest.main()
