import unittest
from unittest import mock
import pygame
from player import Player
from constants import PLAYER_SHOOT_COOLDOWN


class TestPlayer(unittest.TestCase):
	def setUp(self):
		self.player = Player(x=0, y=0)
		self.player.position = pygame.Vector2(0, 0)

	def test_initialization(self):
		"""Test that the Player initializes with correct default values."""
		self.assertEqual(self.player.position.x, 0)
		self.assertEqual(self.player.position.y, 0)
		self.assertEqual(self.player.rotation, 0)
		self.assertEqual(self.player.shoot_cooldown, 0)
		self.assertEqual(self.player.score, 0)

	def test_score_increments(self):
		"""Test that the player's score increments correctly."""
		self.player.score += 10
		self.assertEqual(self.player.score, 10)
		self.player.score += 20
		self.assertEqual(self.player.score, 30)

	def test_shoot_sets_cooldown(self):
		"""Test that shooting sets the cooldown and creates a Shot."""
		with mock.patch("player.Shot") as MockShot:
			self.player.shoot()
			self.assertEqual(self.player.shoot_cooldown, PLAYER_SHOOT_COOLDOWN)
			MockShot.assert_called_once_with(self.player.position.x, self.player.position.y)

	@mock.patch("pygame.key.get_pressed", return_value=[1 if i == pygame.K_w else 0 for i in range(256)])
	def test_update_reduces_cooldown(self, mock_keys):
		"""Test that update reduces the shoot cooldown over time."""
		self.player.shoot_cooldown = 5
		self.player.update(deltatime=1)
		self.assertEqual(self.player.shoot_cooldown, 4)

	def test_triangle_calculation(self):
		"""Test that the triangle method returns three points forming a triangle."""
		triangle = self.player.triangle()
		self.assertEqual(len(triangle), 3)
		for point in triangle:
			self.assertIsInstance(point, pygame.Vector2)

	def test_rotate_changes_rotation(self):
		"""Test that rotate changes the player's rotation."""
		initial_rotation = self.player.rotation
		self.player.rotate(deltatime=1)
		self.assertNotEqual(self.player.rotation, initial_rotation)

	def test_move_changes_position(self):
		"""Test that move changes the player's position."""
		initial_position = self.player.position.copy()
		self.player.move(deltatime=1)
		self.assertNotEqual(self.player.position, initial_position)

	def test_draw_calls_pygame_draw_polygon(self):
		"""Test that the draw method calls pygame.draw.polygon with correct arguments."""
		mock_screen = mock.Mock()
		with mock.patch("pygame.draw.polygon") as mock_draw_polygon:
			self.player.draw(mock_screen)
		mock_draw_polygon.assert_called_once_with(mock_screen, "white", self.player.triangle(), 2)

if __name__ == "__main__":
	unittest.main()