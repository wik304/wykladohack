

def draw_text(text, font, color, surface, offset_x=0, offset_y=0):
    screen_width, screen_height = surface.get_size()
    center_x = screen_width // 2 + offset_x
    center_y = screen_height // 2 + offset_y
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    surface.blit(text_surface, text_rect)
    return text_rect


def draw_text_top_left_from_center(text, font, color, surface, offset_x=0, offset_y=0):
    screen_width, screen_height = surface.get_size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    topleft_x = center_x + offset_x
    topleft_y = center_y + offset_y
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(topleft_x, topleft_y))
    surface.blit(text_surface, text_rect)
    return text_rect


def draw_text_top_right_from_center(text, font, color, surface, offset_x=0, offset_y=0):
    screen_width, screen_height = surface.get_size()
    center_x = screen_width // 2
    center_y = screen_height // 2

    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect(topright=(center_x + offset_x, center_y + offset_y))

    surface.blit(text_surface, text_rect)
    return text_rect
