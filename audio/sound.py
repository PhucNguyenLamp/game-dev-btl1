import pygame as pg

class Audio:
    def __init__(self, root):
        pass

def play_bgm(root):
    pg.mixer.music.load(root / "audio" / "bg_music.mp3")
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.2)
