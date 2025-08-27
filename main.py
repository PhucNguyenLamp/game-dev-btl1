import pygame
import os
import numpy as np

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (-500, 400)
os.environ["SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"] = "0"

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Whack a Zombie")

pygame.mixer.music.load('assets/audio/bg_music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0) # 0.2 là đẹp

clock = pygame.time.Clock()

font = pygame.font.Font('assets/fonts/Terraria.TTF', 32)
# score = font.render('Whack a Zombie!', True, (255, 255, 255))

bg_img = pygame.image.load("assets/sprites/bg.png")
zombie_img = pygame.image.load("assets/sprites/zombie.png")
tombstone_img = pygame.image.load("assets/sprites/tombstone.png")

SPAWN_LOCATIONS = [(100,100), (200, 100), (300, 100),
                   (100, 200), (200, 200), (300, 200)]

LIFE_TIME = 1_000 # ms

running = True
last_click_pos = None

while running:
    click_pos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = event.pos

    screen.blit(bg_img, (0, 0))
    for location in SPAWN_LOCATIONS:
        screen.blit(tombstone_img, location)

    if click_pos: 
        last_click_pos = click_pos

    text = font.render(f'Pos: {last_click_pos}', True, (255, 255, 255))
    screen.blit(text, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
