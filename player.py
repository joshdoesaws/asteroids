import pygame
from circleshape import * 
from constants import *
from main import * 
from shot import Shot

class Player(CircleShape):
    #def __init__(self, x, y):
        #super().__init__(x, y, PLAYER_RADIUS)
    #self.rotation = 0
        #self.image = pygame.Surface((50, 50))  # Example: A simple square
        #self.image.fill((255, 0, 0))  # Fill it with a color (red in this case)
        #self.rect = self.image.get_rect()
        #self.rect.center = (x, y)    
    def __init__(self, x, y, shot_group, updatable_group, drawable_group):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.position = pygame.Vector2(100, 100)
        self.shots = []
        self.shot_group = shot_group
        self.updatable_group = updatable_group
        self.drawable_group = drawable_group
        # Create a transparent surface
        self.image = pygame.Surface((PLAYER_RADIUS * 3, PLAYER_RADIUS * 3), pygame.SRCALPHA)
        # Draw the triangle onto the surface
        # Update the rect
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_triangle()

        self.timer = 0





    def update_triangle(self):
        # Clear the surface
        self.image.fill((0,0,0,0))  # Fill with transparent color
        # Get triangle points
        points = self.triangle()
        # Convert world coordinates to surface coordinates
        center = self.image.get_width() // 2
        surface_points = [(p[0] - self.position.x + center, p[1] - self.position.y + center) for p in points]
        # Draw triangle on surface
        pygame.draw.polygon(self.image, "white", surface_points, 2)
    def rotate(self, dt, direction):
        self.rotation += PLAYER_TURN_SPEED * dt * direction

    def move(self, dt, direction):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * direction
        
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt, -1)
        if keys[pygame.K_d]:
            self.rotate(dt, 1)
        if keys[pygame.K_w]:
            self.move(dt, 1)
        if keys[pygame.K_s]:
            self.move(dt, -1)
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()
            self.timer = PLAYER_SHOOT_COOLDOWN
        
        self.update_triangle()
        self.rect.center = self.position
        self.timer = max(0, self.timer - dt)

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

# in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def shoot(self):
        # Create direction vector
        direction = pygame.Vector2(0, 1)
        # Rotate the direction based on player's rotation
        direction = direction.rotate(-self.rotation)  # Negative because pygame's rotation is clockwise
        # Scale the direction to create velocity
        velocity = direction * PLAYER_SHOOT_SPEED
        # Create new shot with position and velocity
        shot = Shot(self.position.x, self.position.y, velocity)
        self.shot_group.add(shot)
        self.updatable_group.add(shot)
        self.drawable_group.add(shot)

class Shot(CircleShape):
    def __init__(self, x, y, velocity):
        # Initialize with x, y coordinates as numbers
        super().__init__(x, y, SHOT_RADIUS)
        # Store the velocity vector
        self.velocity = velocity
        # Create the shot's image
        self.image = pygame.Surface((SHOT_RADIUS * 2, SHOT_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (SHOT_RADIUS, SHOT_RADIUS), SHOT_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Create a position vector
        self.position = pygame.Vector2(x, y)

    def update(self, dt):
        # Update position using vectors
        self.position += self.velocity * dt
        # Update the rect position
        self.rect.center = (self.position.x, self.position.y)
