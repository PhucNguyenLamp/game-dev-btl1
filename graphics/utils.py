import pygame


def scale_background_to_screen(bg_img: pygame.Surface, screen: pygame.Surface):
    screen_width, screen_height = screen.get_size()
    bg_width, bg_height = bg_img.get_size()
    scale = max(screen_width / bg_width, screen_height / bg_height)
    new_size = (int(bg_width * scale), int(bg_height * scale))
    bg_img = pygame.transform.smoothscale(bg_img, new_size)
    bg_offset_x = (new_size[0] - screen_width) // 2
    bg_offset_y = (new_size[1] - screen_height) // 2
    return bg_img, (-bg_offset_x, -bg_offset_y)


