import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def create_game_over_surface(screen, drawable, score):
	"""Create a surface for the Game Over screen with all final positions and text."""
	final_frame = screen.copy()

	# Draw all objects in their final positions
	for obj in drawable:
		obj.draw(final_frame)

	# Add "Game Over" text
	font = pygame.font.Font(None, 74)
	text = font.render("Game Over!", True, (255, 255, 255))
	text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
	final_frame.blit(text, text_rect)

	# Add final score as a sub-message
	sub_font = pygame.font.Font(None, 36)
	sub_text = sub_font.render(f"Score: {score} | Press any key to exit", True, (255, 255, 255))
	sub_text_rect = sub_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
	final_frame.blit(sub_text, sub_text_rect)

	return final_frame

def display_score(screen, score):
	"""Displays the player's score at the top-left corner."""
	font = pygame.font.Font(None, 36)
	score_text = font.render(f"Score: {score}", True, (255, 255, 255))
	screen.blit(score_text, (10, 10))

def main():
	pygame.init()

	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	print("Starting asteroids!")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")

	clock = pygame.time.Clock()
	deltatime = 0

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

	asteroids = pygame.sprite.Group()
	Asteroid.containers = (asteroids, updatable, drawable)
	
	AsteroidField.containers = (updatable)
	asteroidfield = AsteroidField()

	shots = pygame.sprite.Group()
	Shot.containers = (shots, updatable, drawable)

	running = True
	collision_quit = False
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		screen.fill((0, 0, 0))

		for obj in updatable:
			obj.update(deltatime)
			for asteroid in asteroids:
				for shot in shots:
					if shot.collision(asteroid):
						player.score += 10
						asteroid.split()
						shot.kill()
				if player.collision(asteroid):
					running = False
					collision_quit = True
					break
			if not running:
				break

		for obj in drawable:
			obj.draw(screen)

		display_score(screen, player.score)
		pygame.display.update()
		deltatime = clock.tick(60) / 1000

	# Game Over
	if collision_quit:
		final_frame = create_game_over_surface(screen, drawable, player.score)
		print("Game over!\nFinal score:", player.score)

		game_over_running = True
		while game_over_running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
					game_over_running = False

			screen.blit(final_frame, (0, 0))
			pygame.display.flip()

	pygame.quit()

if __name__ == "__main__":
	main()