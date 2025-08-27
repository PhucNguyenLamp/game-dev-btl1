import numpy as np
import pygame


# Whack-a-Zombie Game Entity
class Zombie:
    def __init__(self, image, position, lifetime):
        self.image = image
        self.position = position
        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()
        self.alive = True
        self.getHit = False
        self.hitbox = pygame.Rect(
            position[0], position[1], image.get_width(), image.get_height()
        )

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.position)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def check_hit(self, mpos):
        if (mpos is None):
            return False
        if self.alive and self.hitbox.collidepoint(mpos):
            self.getHit = True
            return True
        return False

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime or self.getHit:
            self.alive = False
            if self.getHit:
                return 1
            return -1
        return 0


# Spawn Zombie at Random Locations
def spawn_zombie(zombie_img, locations, lifetime, occupied_locations):
    # Filter out occupied locations
    free_locations = [loc for loc in locations if loc not in occupied_locations]
    if not free_locations:
        return None
    location = free_locations[np.random.randint(len(free_locations))]
    return Zombie(zombie_img, location, lifetime)
