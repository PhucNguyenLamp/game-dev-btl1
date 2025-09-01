import numpy as np
import pygame


# Whack-a-Zombie Game Entity
class Zombie:
    def __init__(self, image, hit_image, position, lifetime):
        self.image = image.convert_alpha()
        self.hit_image = hit_image.convert_alpha()
        self.position = position
        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()
        self.alive = True
        self.getHit = False
        self.hit_time = None
        self.hitbox = pygame.Rect(
            position[0], position[1], image.get_width(), image.get_height()
        )
        self.alpha = 0
        self.fade_duration = 300

    def draw(self, screen):
        if self.alive:
            img = self.image.copy()
            img.set_alpha(self.alpha)
            screen.blit(img, self.position)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        else:
            img = self.hit_image.copy()
            img.set_alpha(self.alpha)
            screen.blit(img, self.position)


    def check_hit(self, mpos):
        if (mpos is None):
            return False
        if self.alive and self.hitbox.collidepoint(mpos):
            self.getHit = True
            self.hit_time = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.spawn_time

        # Fade in
        if elapsed < self.fade_duration:
            self.alpha = int((elapsed / self.fade_duration) * 255)
        # Fade out
        elif elapsed > self.lifetime - self.fade_duration:
            remaining = self.lifetime - elapsed
            self.alpha = max(0, int((remaining / self.fade_duration) * 255))
        else:
            self.alpha = 255

        if self.getHit:
            if current_time - self.hit_time > 200:
                self.alive = False
                return 1
            return 0

        if current_time - self.spawn_time > self.lifetime:
            self.alive = False
            if self.getHit:
                return 1
            return -1
        return 0


# Spawn Zombie at Random Locations
def spawn_zombie(zombie_img, hitzombie_img, locations, lifetime, occupied_locations):
    # Filter out occupied locations
    free_locations = [loc for loc in locations if loc not in occupied_locations]
    if not free_locations:
        return None
    location = free_locations[np.random.randint(len(free_locations))]
    return Zombie(zombie_img, hitzombie_img, location, lifetime)
