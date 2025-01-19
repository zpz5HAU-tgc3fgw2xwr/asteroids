import unittest
from unittest import mock
import pygame
from asteroidfield import AsteroidField
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_SPAWN_RATE, SCREEN_WIDTH, SCREEN_HEIGHT

class TestAsteroidField(unittest.TestCase):
	def setUp(self):
		"""Initialize pygame and set up the test environment."""
		pygame.init()
		pygame.display.set_mode((800, 600))
		AsteroidField.containers = mock.Mock()
		self.field = AsteroidField()

	def test_spawn_creates_asteroid_with_default_properties(self):
		"""Test that spawn creates an asteroid with the given properties."""
		with mock.patch("asteroidfield.Asteroid") as MockAsteroid:
			# Arrange
			position = pygame.Vector2(100, 100)
			velocity = pygame.Vector2(50, 50)

			# Act
			self.field.spawn(radius=ASTEROID_MIN_RADIUS, position=position, velocity=velocity)

			# Assert
			MockAsteroid.assert_called_once_with(100, 100, ASTEROID_MIN_RADIUS)
			asteroid_instance = MockAsteroid.return_value
			self.assertEqual(asteroid_instance.velocity, velocity)

	def test_update_spawns_asteroid_when_timer_expires(self):
		"""Test that the update method spawns asteroids when the timer expires."""
		# Arrange
		self.field.spawn = mock.Mock()

		# Act
		self.field.update(ASTEROID_SPAWN_RATE + 0.1)

		# Assert
		self.field.spawn.assert_called_once()

	def test_update_does_not_spawn_before_timer_expires(self):
		"""Test that update does not spawn an asteroid before the timer expires."""
		# Arrange
		self.field.spawn = mock.Mock()

		# Act
		self.field.update(ASTEROID_SPAWN_RATE - 0.1)

		# Assert
		self.field.spawn.assert_not_called()
	
	def test_edges_generate_positions(self):
		"""Test that edge definitions generate valid positions."""
		screen_width = SCREEN_WIDTH
		screen_height = SCREEN_HEIGHT

		for edge_vector, position_func in self.field.edges:
			position = position_func(0.5)

			# Assert that position is a valid pygame.Vector2
			self.assertIsInstance(position, pygame.Vector2)

			# Debugging: Log the edge and generated position
			print(f"Testing edge {edge_vector}, position: {position}")

			# Validate position based on the spawning edge
			if edge_vector == pygame.Vector2(1, 0):  # Left edge
				self.assertEqual(position.x, -ASTEROID_MAX_RADIUS)
				self.assertGreaterEqual(position.y, 0)
				self.assertLessEqual(position.y, screen_height)
			elif edge_vector == pygame.Vector2(-1, 0):  # Right edge
				expected_x = screen_width + ASTEROID_MAX_RADIUS
				self.assertEqual(position.x, expected_x)
				self.assertGreaterEqual(position.y, 0)
				self.assertLessEqual(position.y, screen_height)
			elif edge_vector == pygame.Vector2(0, 1):  # Top edge
				self.assertEqual(position.y, -ASTEROID_MAX_RADIUS)
				self.assertGreaterEqual(position.x, 0)
				self.assertLessEqual(position.x, screen_width)
			elif edge_vector == pygame.Vector2(0, -1):  # Bottom edge
				expected_y = screen_height + ASTEROID_MAX_RADIUS
				self.assertEqual(position.y, expected_y)
				self.assertGreaterEqual(position.x, 0)
				self.assertLessEqual(position.x, screen_width)

	def tearDown(self):
		"""Clean up pygame after each test."""
		pygame.quit()

if __name__ == "__main__":
	unittest.main()