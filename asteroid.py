import pygame
from circleshape import CircleShape
import random
ASTEROID_MIN_RADIUS = 5

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, velocity=None):
        super().__init__(x, y, radius)
        self.radius = radius
        surface_size = int(radius * 2 + 4)
        self.velocity = velocity if velocity else pygame.math.Vector2(0, 0)
        self.image = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        # Draw the circle on self.image
        pygame.draw.circle(self.image, (255, 255, 255), (surface_size//2, surface_size//2), radius, 2)
        self.rect = self.image.get_rect(center=(x, y))    




    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.position.x, self.position.y), self.radius, width=2)

    def update(self, dt):
        self.position = self.position + (self.velocity * dt)


    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)

        new_vel1 = self.velocity.rotate(random_angle)
        new_vel2 = self.velocity.rotate(-random_angle)

        new_vel1 *= 1.2
        new_vel2 *= 1.2

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius, new_vel1)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius, new_vel2)

    
        for group in self.groups():
            group.add(asteroid1)
            group.add(asteroid2)


