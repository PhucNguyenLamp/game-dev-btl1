import pygame as pg
from pathlib import Path

sprites_path = Path("assets/sprites")

class MuteButton: 
    def __init__(self, x, y):
        self.image = pg.image.load(sprites_path / "sound.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_muted = False

    def toggle(self, mpos):
        if mpos is None:
            return False
        if not self.rect.collidepoint(mpos):
            return 
        
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.image = pg.image.load(sprites_path / "mute.png").convert_alpha()
            pg.mixer.music.set_volume(0)
        else:
            self.image = pg.image.load(sprites_path / "sound.png").convert_alpha()
            pg.mixer.music.set_volume(0.2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
