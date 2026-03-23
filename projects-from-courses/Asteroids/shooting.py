from circleshape import *
import pygame
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, velocity, radius):
        super().__init__(x, y, radius)
        self.velocity = velocity
        self.SHOT_RADIUS = 5

    def draw(self, screen):
        pygame.draw.circle(screen, color='white', center = self.position, radius = self.SHOT_RADIUS, width = self.radius)

    def update(self, dt):
        self.position += self.velocity*dt


