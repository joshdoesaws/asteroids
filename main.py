import pygame
from constants import *
from player import *
from asteroidfield import AsteroidField
from asteroid import Asteroid
from circleshape import *
import sys
from shot import Shot

def main():
    pygame.init()
    print("Starting asteroids!")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Initialize groups
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()
    Player.containers = (updatable_group, drawable_group, shot_group)
    Shot.containers = (shot_group, updatable_group, drawable_group)
    Asteroid.containers = (asteroid_group, updatable_group, drawable_group)
    AsteroidField.containers = updatable_group
    asteroid_field = AsteroidField()

    # Initialize player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shot_group, updatable_group, drawable_group) 
    
    running = True
    clock = pygame.time.Clock()
    dt = 0



    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update all updatables
        updatable_group.update(dt)

        shot_group.update(dt)
        shot_group.draw(screen)

        # Clear the screen
        screen.fill((0,0,0))

        for asteroid in asteroid_group:
            for bullet in shot_group:
                if asteroid.collision(bullet):
                    asteroid.kill()  # Uses pygame.sprite.Sprite's kill method
                    bullet.kill()


                if player.collision(asteroid):
                    print("Game over!")
                    sys.exit()

        # Draw all drawables
        drawable_group.draw(screen)
        # Update the full display
        pygame.display.flip()

if __name__ == "__main__":
    main()
