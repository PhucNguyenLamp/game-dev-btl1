import pygame
import os
import numpy as np
from entities.zombie import Zombie, spawn_zombie

# os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (-500, 400)
# os.environ["SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"] = "0"

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

#10 seconds
LIFE_TIME = 1000 # ms
SPAWN_INTERVAL = np.random.randint(300,701) # ms
last_spawn_time = 0
zombies = []
occupied_locations = set()

running = True
last_click_pos = None

while running:
    click_pos = None
    screen.blit(bg_img, (0, 0))
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = event.pos

    if click_pos: 
        last_click_pos = click_pos

    for loc in SPAWN_LOCATIONS:
        screen.blit(tombstone_img, loc)

    occupied_locations = {z.position for z in zombies if z.alive}

    if current_time - last_spawn_time > SPAWN_INTERVAL:
        zombie = spawn_zombie(zombie_img, SPAWN_LOCATIONS, LIFE_TIME, occupied_locations)
        if zombie:
            zombies.append(zombie)
            last_spawn_time = current_time

    for zombie in zombies:
        zombie.update()
        zombie.draw(screen)

    zombies = [z for z in zombies if z.alive]

    debug = font.render('Number of Zombies: ' + str(len(zombies)), True, (255, 255, 255))
    fps_text = font.render(f'FPS: {int(clock.get_fps())}', True, (255, 255, 255))
    text = font.render(f'Pos: {last_click_pos}', True, (255, 255, 255))
    screen.blit(fps_text, (0, 0))
    screen.blit(debug, (0, 30))
    screen.blit(text, (0, 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
