# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from Player import Player
from asteroid import *
from asteroidfield import *
from shooting import *




def main():
    pygame.init()
    print('Starting Asteroids!')
    print(f'Screen width: {SCREEN_WIDTH}')
    print(f'Screen height: {SCREEN_HEIGHT}')
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()


    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable,drawable,shots)


    player = Player(x,y)
    asteroidField = AsteroidField()
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill(color = 0x000000)
        updatable.update(dt)
        
        for object in asteroids:
            if object.does_collide(player):
                print("Game over!")
                return
            
        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.does_collide(bullet):
                    asteroid.split()
                    bullet.kill()

        for object in drawable:
            object.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)/1000
    
if __name__ == "__main__":
    main()