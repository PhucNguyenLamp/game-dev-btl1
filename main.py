import pygame
import os
import numpy as np
from entities.zombie import ZState, Zombie, spawn_zombie
from pathlib import Path
from audio.sound import play_bgm
from ui.ui import MuteButton, MouseCursor

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Whack a Zombie")

assets_path = Path(__file__).parent / "assets"
play_bgm(assets_path)

clock = pygame.time.Clock()

mute_button = MuteButton(350, 10)
mouse_cursor = MouseCursor(mute_button)
pygame.mouse.set_visible(False)

font = pygame.font.Font("assets/fonts/Terraria.TTF", 32)
# score = font.render('Whack a Zombie!', True, (255, 255, 255))

bg_img = pygame.image.load("assets/sprites/bg.png")
tombstone_img = pygame.image.load("assets/sprites/tombstone.png")
grass_mask_img = pygame.image.load("assets/sprites/grass_mask.png")
grass_mask_img = pygame.transform.scale(grass_mask_img, (50, 50))

SPAWN_LOCATIONS = [
    (100, 100),
    (200, 100),
    (300, 100),
    (100, 200),
    (200, 200),
    (300, 200),
]

# 10 seconds
LIFE_DURATION = 3000  # ms
SPAWN_INTERVAL = 1000  # ms
last_spawn_time = 0
zombies = []
occupied_locations = set()

running = True
score = 0
miss = 0

particles = []
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for zombie in zombies:
            if zombie.handle_event(event, particles):
                score += 1

        mute_button.toggle(event)
        mouse_cursor.handle_event(event)

    zombies = [z for z in zombies if z.state != ZState.EXPIRED]
    occupied_locations = {z.position for z in zombies if z.state != ZState.EXPIRED}

    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > SPAWN_INTERVAL:
        zombie = spawn_zombie(
            SPAWN_LOCATIONS, LIFE_DURATION, occupied_locations, mute_button
        )
        if zombie:
            zombies.append(zombie)
            last_spawn_time = current_time

    ## RENDERING
    screen.blit(bg_img, (0, 0))

    for loc in SPAWN_LOCATIONS:
        screen.blit(tombstone_img, loc)

    for zombie in zombies:
        status = zombie.update()
        if status == -1:
            miss += 1
        zombie.draw(screen)

    for loc in SPAWN_LOCATIONS:
        # GRASS MASK
        screen.blit(grass_mask_img, (loc[0] - tombstone_img.get_width() //2, loc[1] + tombstone_img.get_height()))

    for p in particles:
        p.update()
        if not p.alive:
            particles.remove(p)
        else: 
            p.draw(screen)

    mute_button.draw(screen)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    accuracy = score / (score + miss) if score + miss != 0 else 1
    accuracy_text = font.render(
        f"Accuracy: {accuracy * 100:.2f}%", True, (255, 255, 255)
    )

    screen.blit(score_text, (0, 0))
    screen.blit(accuracy_text, (0, 30))

    mouse_cursor.update()
    mouse_cursor.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
