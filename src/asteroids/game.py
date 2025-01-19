import pygame
from asteroids.constants import *
from asteroids.entities.player import Player
from asteroids.entities.asteroid import Asteroid
from asteroids.entities.asteroidfield import AsteroidField
from asteroids.entities.shot import Shot
from asteroids.utils.rendering import create_game_over_surface, display_score

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