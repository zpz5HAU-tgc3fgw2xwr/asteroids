import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        screen.fill((0, 0, 0))

        for object in updatable:
            object.update(deltatime)
        for asteroid in asteroids:
            for shot in shots:
                if shot.collision(asteroid):
                    asteroid.kill()
                    shot.kill()
            if player.collision(asteroid):
                running = False
                print("Game over!")                
        for object in drawable:
            object.draw(screen)

        pygame.display.update()
        deltatime = clock.tick(60) / 1000
    
    pygame.quit()

if __name__ == "__main__":
    main()