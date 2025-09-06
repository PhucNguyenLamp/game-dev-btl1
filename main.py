import pygame
import os
import numpy as np
from entities.zombie import ZState, Zombie, spawn_zombie
from pathlib import Path
from audio.sound import play_bgm
from ui.ui import MuteButton, MouseCursor
from ui.timer import CountdownTimer
from ui.hud import HUDPanel
from ui.overlay import GameOverOverlay
from ui.start_screen import run_start_screen

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Whack a Zombie")

assets_path = Path(__file__).parent / "assets"
play_bgm(assets_path)

# Run start screen before game loop
run_start_screen(screen, assets_path)

clock = pygame.time.Clock()

mute_button = MuteButton(0, 0)
mute_button.rect.topright = (screen.get_width() - 10, 10)
mouse_cursor = MouseCursor(mute_button)
pygame.mouse.set_visible(False)

font = pygame.font.Font("assets/fonts/Terraria.TTF", 32)
font_large = pygame.font.Font("assets/fonts/Terraria.TTF", 64)
hud = HUDPanel(font, (screen.get_width() // 2, screen.get_height() // 4 + 40))
overlay = GameOverOverlay(font_large, font)
# score = font.render('Whack a Zombie!', True, (255, 255, 255))

bg_img = pygame.image.load("assets/sprites/bg.png")
#scaler
screen_width, screen_height = screen.get_size()
bg_width, bg_height = bg_img.get_size()
scale = max(screen_width / bg_width, screen_height / bg_height)
new_size = (int(bg_width * scale), int(bg_height * scale))
bg_img = pygame.transform.smoothscale(bg_img, new_size)
bg_offset_x = (new_size[0] - screen_width) // 2
bg_offset_y = (new_size[1] - screen_height) // 2

tombstone_img = pygame.image.load("assets/sprites/tombstone.png")
# Tombstone size forcer
orig_w, orig_h = tombstone_img.get_size()
TARGET_TOMBSTONE_HEIGHT = 96 #pĩels
if orig_h > 0:
    scale_ratio = TARGET_TOMBSTONE_HEIGHT / orig_h
    new_size = (int(orig_w * scale_ratio), int(orig_h * scale_ratio))
    tombstone_img = pygame.transform.smoothscale(tombstone_img, new_size)

grass_mask = pygame.image.load("assets/sprites/grass_mask.png")
grass_mask = pygame.transform.scale(grass_mask, (96, 40))

SPAWN_LOCATIONS = [
    (150, 325),
    (400, 325),
    (650, 325),
    (150, 475),
    (400, 475),
    (650, 475),
]

# 10 seconds
LIFE_DURATION = 3000  # ms
SPAWN_INTERVAL = 1000  # ms


class GameState:
    def __init__(self):
        self.running = True
        self.game_over = False
        self.score = 0
        self.miss = 0
        self.particles = []
        self.last_spawn_time = 0
        self.zombies = []
        self.occupied_locations = set()
        self.time_left_ms = 0
        self.timer = CountdownTimer(60000)


def reset_run(state: "GameState") -> None:
    run_start_screen(screen, assets_path)
    state.zombies = []
    state.occupied_locations = set()
    state.score = 0
    state.miss = 0
    state.particles = []
    state.last_spawn_time = 0
    state.timer.reset()
    state.game_over = False


def handle_events(state: "GameState") -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False

        if not state.game_over:
            for zombie in state.zombies:
                if zombie.handle_event(event, state.particles):
                    state.score += 1
        else:
            if overlay.handle_event(event):
                reset_run(state)

        mute_button.toggle(event)
        mouse_cursor.handle_event(event)


def update_state(state: "GameState") -> None:
    state.zombies = [z for z in state.zombies if z.state != ZState.EXPIRED]
    state.occupied_locations = {z.position for z in state.zombies if z.state != ZState.EXPIRED}

    current_time = pygame.time.get_ticks()
    state.time_left_ms = state.timer.time_left_ms()
    if not state.game_over and current_time - state.last_spawn_time > SPAWN_INTERVAL:
        zombie = spawn_zombie(
            SPAWN_LOCATIONS, LIFE_DURATION, state.occupied_locations, mute_button
        )
        if zombie:
            state.zombies.append(zombie)
            state.last_spawn_time = current_time
    if not state.game_over and state.time_left_ms == 0:
        state.game_over = True

    for zombie in state.zombies:
        if not state.game_over:
            status = zombie.update()
            if status == -1:
                state.miss += 1

    for p in list(state.particles):
        p.update()
        if not p.alive:
            state.particles.remove(p)


def render(state: "GameState") -> None:
    screen.blit(bg_img, (-bg_offset_x, -bg_offset_y))

    for loc in SPAWN_LOCATIONS:
        # Draw tombstone base first
        screen.blit(tombstone_img, loc)

    for zombie in state.zombies:
        zombie.draw(screen)

    # Draw hit particles 
    for p in state.particles:
        p.draw(screen)

    # Draw grass mask in front of spawn/despawn animations (foreground)
    for loc in SPAWN_LOCATIONS:
        mask_pos = (
            loc[0],
            loc[1] + tombstone_img.get_height(),
        )
        screen.blit(grass_mask, mask_pos)

    # Timer 
    seconds_left = state.time_left_ms // 1000
    minutes = seconds_left // 60
    seconds = seconds_left % 60
    timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))

    # HUD 
    accuracy = state.score / (state.score + state.miss) if state.score + state.miss != 0 else 1
    hud.set_center((screen.get_width() // 2, screen.get_height() // 4 + 40))
    hud.draw(screen, state.score, accuracy)

    # Mute
    mute_button.draw(screen)

    # Game end
    if state.game_over:
        overlay.draw(screen, state.score, accuracy)

    mouse_cursor.update()
    mouse_cursor.draw(screen)

    pygame.display.flip()

# loop de nhin` hon
state = GameState()
while state.running:
    handle_events(state)
    update_state(state)
    render(state)
    clock.tick(60)

pygame.quit()
