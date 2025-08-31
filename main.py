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

hit_sound = pygame.mixer.Sound("assets/audio/hit.mp3")
pygame.mixer.music.load("assets/audio/bg_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)  # 0.2 là đẹp

clock = pygame.time.Clock()

font = pygame.font.Font("assets/fonts/PressStart2P-Regular.TTF", 10)
# score = font.render('Whack a Zombie!', True, (255, 255, 255))

bg_img = pygame.image.load("assets/sprites/bg.png")
zombie_img = pygame.image.load("assets/sprites/zombie.png")
tombstone_img = pygame.image.load("assets/sprites/tombstone.png")
mute_icon = pygame.image.load("assets/sprites/mute.png")
unmute_icon = pygame.image.load("assets/sprites/unmute.png")

mute_icon = pygame.transform.scale(mute_icon, (20, 20))
unmute_icon = pygame.transform.scale(unmute_icon, (20, 20))
mute_button_rect = mute_icon.get_rect(topright=(390, 10))

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
sound_enabled = True

running = True
last_click_pos = None
score = 0
miss = 0

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
        if mute_button_rect.collidepoint(click_pos):
            sound_enabled = not sound_enabled

    for loc in SPAWN_LOCATIONS:
        screen.blit(tombstone_img, loc)

    zombies = [z for z in zombies if z.alive]
    occupied_locations = {z.position for z in zombies if z.alive}

    if current_time - last_spawn_time > SPAWN_INTERVAL:
        zombie = spawn_zombie(
            zombie_img,zombie_img, SPAWN_LOCATIONS, LIFE_TIME, occupied_locations
        )
        if zombie:
            zombies.append(zombie)
            last_spawn_time = current_time

    for zombie in zombies:
        if zombie.check_hit(click_pos):
            if sound_enabled:
                hit_sound.play()
            score += 1

    for zombie in zombies:
        status = zombie.update()  # 1 = hit, -1 = miss, 0 = nothing
        if status == -1:
            miss += 1
        zombie.draw(screen)

    """debug = font.render(
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
    screen.blit(accuracy_text, (0, 120))"""

        # Render text
    accuracy = score / (score + miss) if score + miss != 0 else 1
    score_text = font.render(f"Hit: {score}", True, (0, 0, 0))
    miss_text = font.render(f"Miss: {miss}", True, (0, 0, 0))
    accuracy_text = font.render(f"Accuracy: {accuracy * 100:.2f}%", True, (0, 0, 0))

    # Vẽ lên màn hình
    screen.blit(score_text, (10, 10))
    screen.blit(miss_text, (10, 30))
    screen.blit(accuracy_text, (10, 50))
    if sound_enabled:
        screen.blit(unmute_icon, mute_button_rect)
        pygame.mixer.music.set_volume(0.2)
    else:
        screen.blit(mute_icon, mute_button_rect)
        pygame.mixer.music.set_volume(0)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
