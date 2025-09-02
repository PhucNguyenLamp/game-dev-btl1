import pygame as pg
import random


class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, -5)
        self.lifetime = 60
        self.image = pg.Surface((4,4), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 0, 0), (2,2), 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.lifetime -= 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    @property
    def alive(self):
        return self.lifetime > 0