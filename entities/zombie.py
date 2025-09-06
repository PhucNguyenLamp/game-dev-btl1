import numpy as np
import pygame
from enum import Enum, auto
from pathlib import Path
from particles.Particle import Particle

asset_path = Path("assets")
DEFAULT_ZOMBIE_HEIGHT = 96  # pixels


# Whack-a-Zombie Game Entity
class ZState(Enum):
    SPAWNING = auto()
    IDLE = auto()
    HIT = auto()
    DESPAWNING = auto()
    EXPIRED = auto()


class Zombie:

    def __init__(self, position, life_duration, mute_button):
        idle_img = pygame.image.load(asset_path / "sprites" / "zombie.png")
        spawn_img = pygame.image.load(asset_path / "sprites" / "zombie_spawn.png")
        despawn_img = pygame.image.load(asset_path / "sprites" / "zombie_despawn.png")

        def scale_to_height(img: pygame.Surface, target_h: int) -> pygame.Surface:
            w, h = img.get_size()
            if h == 0:
                return img
            ratio = DEFAULT_ZOMBIE_HEIGHT / h
            return pygame.transform.smoothscale(img, (int(w * ratio), int(h * ratio)))

        # Scaler
        self.idle_image = scale_to_height(idle_img, DEFAULT_ZOMBIE_HEIGHT)
        self.spawn_image = scale_to_height(spawn_img, DEFAULT_ZOMBIE_HEIGHT)
        self.despawn_image = scale_to_height(despawn_img, DEFAULT_ZOMBIE_HEIGHT)

        # Current sprite starts as spawning image
        self.image = self.spawn_image

        self.original_position = position
        self.position = (position[0], position[1] + 45)
        self.offset = (-5, -15)
        self.opacity = 255
        self.mute_button = mute_button

        self.state = ZState.SPAWNING 
        self.spawn_duration = 60 # 60 frames -> 1 sec
        self.remaining_spawn_duration = self.spawn_duration

        self.spawn_start_time = pygame.time.get_ticks()
        self.life_duration = life_duration # 3 sec - 1 - 0.5 = 1.5 sec idle
        self.despawn_duration = 30 # 30 frames -> 0.5 sec
        self.remaining_despawn_duration = self.despawn_duration

        self.movement_offset_y = -35 / self.spawn_duration

        self.hitbox = self.image.get_rect(
            topleft=(
                self.position[0] + self.offset[0],
                self.position[1] + self.offset[1],
            )
        )
        self.hit_sound = pygame.mixer.Sound(asset_path / "audio" / "zombie_hit.mp3")

    def draw(self, screen):
        if self.state != ZState.EXPIRED:
            self.image.set_alpha(self.opacity)
            screen.blit(
                self.image,
                (self.position[0] + self.offset[0], self.position[1] + self.offset[1]),
            )
            # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def handle_event(self, event, particles):
        mouse_pos = pygame.mouse.get_pos()
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        if (
            self.state in [ZState.IDLE, ZState.SPAWNING, ZState.DESPAWNING]
        ) and self.hitbox.collidepoint(mouse_pos):
            self.state = ZState.HIT
            # spawn particle for 1 sec
            if not self.mute_button.is_muted:
                self.hit_sound.play()
            for _ in range(10):
                particles.append(Particle(mouse_pos))

            # zombie get squished
            self.image = pygame.transform.scale_by(self.image, (1, 0.5))
            self.position = (
                self.position[0],
                self.position[1] + self.image.get_height(),
            )

            # remove hitbox
            self.hitbox = pygame.Rect(0, 0, 0, 0)

            return True
        return False

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.state == ZState.SPAWNING:

            self.position = (
                self.position[0],
                self.position[1] + self.movement_offset_y,
            )
            self.hitbox = self.image.get_rect(
                topleft=(
                    self.position[0] + self.offset[0],
                    self.position[1] + self.offset[1],
                )
            )
            self.remaining_spawn_duration -= 1

            if self.remaining_spawn_duration <= 0:
                self.state = ZState.IDLE
                # Switch to idle sprite after finish rising
                self.image = self.idle_image

        if (
            current_time - self.spawn_start_time > self.life_duration
            and self.state == ZState.IDLE
        ) or (self.state == ZState.HIT):
            return_value = -1
            if self.state == ZState.HIT:
                return_value = 1

            # Only when hit, switch to despawn sprite; otherwise keep idle
            if self.state == ZState.HIT:
                self.image = self.despawn_image
                self.position = (
                    self.position[0],
                    self.position[1] - 30,
                )

            self.state = ZState.DESPAWNING
            return return_value

        if self.state == ZState.DESPAWNING:
            self.remaining_despawn_duration -= 1
            self.opacity = int(
                255 * (self.remaining_despawn_duration / self.despawn_duration)
            )
            self.position = (
                self.position[0],
                self.position[1] - self.movement_offset_y,
            )
            # KO CHỈNH ĐỂ TẠO CẢM GIÁC CÔNG BẰNG CHO GAME THỦ :))
            # self.hitbox = self.image.get_rect(
            #     topleft=(
            #         self.position[0] + self.offset[0],
            #         self.position[1] + self.offset[1],
            #     )
            # )
            if self.remaining_despawn_duration <= 0:
                self.state = ZState.EXPIRED
            return 0
        return 0


# Spawn Zombie at Random Locations
def spawn_zombie(locations, life_duration, occupied_locations, mute_button):
    # Filter out occupied locations
    free_locations = [loc for loc in locations if loc not in occupied_locations]
    if not free_locations:
        return None
    location = free_locations[np.random.randint(len(free_locations))]
    return Zombie(location, life_duration, mute_button)
