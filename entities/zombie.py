import numpy as np
import pygame
#Whack-a-Zombie Game Entity
class Zombie:
    def __init__(self, image, position, lifetime):
        self.image = image
        self.position = position
        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()
        self.alive = True

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.position)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.alive = False

#Spawn Zombie at Random Locations
def spawn_zombie(zombie_img, locations, lifetime, occupied_locations):
    # Filter out occupied locations
    free_locations = [loc for loc in locations if loc not in occupied_locations]
    if not free_locations:
        return None  
    location = free_locations[np.random.randint(len(free_locations))]
    return Zombie(zombie_img, location, lifetime)