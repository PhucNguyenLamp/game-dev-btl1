import pygame
import os
import numpy as np
from entities.zombie import Zombie, spawn_zombie
from pathlib import Path
from audio.sound import play_bgm
from ui.ui import MuteButton

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Whack a Zombie")

assets_path = Path(__file__).parent / "assets"
play_bgm(assets_path)

clock = pygame.time.Clock()

mute_button = MuteButton(350, 10)


font = pygame.font.Font("assets/fonts/Terraria.TTF", 32)
# score = font.render('Whack a Zombie!', True, (255, 255, 255))

bg_img = pygame.image.load("assets/sprites/bg.png")
zombie_img = pygame.image.load("assets/sprites/zombie.png")
tombstone_img = pygame.image.load("assets/sprites/tombstone.png")

SPAWN_LOCATIONS = [
    (100, 100),
    (200, 100),
    (300, 100),
    (100, 200),
    (200, 200),
    (300, 200),
]

# 10 seconds
LIFE_TIME = 3000  # ms
SPAWN_INTERVAL = 1000  # ms
last_spawn_time = 0
zombies = []
occupied_locations = set()

running = True
last_click_pos = None
score = 0
miss = 0

while running:
    click_pos = None
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = event.pos

    if click_pos:
        last_click_pos = click_pos

    for loc in SPAWN_LOCATIONS:
        screen.blit(tombstone_img, loc)

    zombies = [z for z in zombies if z.alive]
    occupied_locations = {z.position for z in zombies if z.alive}

    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > SPAWN_INTERVAL:
        zombie = spawn_zombie(
            zombie_img, SPAWN_LOCATIONS, LIFE_TIME, occupied_locations
        )
        if zombie:
            zombies.append(zombie)
            last_spawn_time = current_time

    for zombie in zombies:
        if zombie.check_hit(click_pos):
            score += 1

    for zombie in zombies:
        status = zombie.update()  # 1 = hit, -1 = miss, 0 = nothing
        if status == -1:
            miss += 1
        zombie.draw(screen)

    mute_button.toggle(click_pos)

    debug = font.render(
        "Number of Zombies: " + str(len(zombies)), True, (255, 255, 255)
    )

    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    text = font.render(f"Pos: {last_click_pos}", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    accuracy = score / (score + miss) if score + miss != 0 else 1
    accuracy_text = font.render(
        f"Accuracy: {accuracy * 100:.2f}%", True, (255, 255, 255)
    )

    screen.blit(fps_text, (0, 0))
    screen.blit(debug, (0, 30))
    screen.blit(text, (0, 60))
    screen.blit(score_text, (0, 90))
    screen.blit(accuracy_text, (0, 120))
    mute_button.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
