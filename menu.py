import sys
import time
import pygame
from utilities import *
import json
import os
import random
from colloquium_bank import colloquium_bank
import requests


def download_leaderboard():
    url = "https://49750f73-1884-4a17-8781-14af8f9d6f26-00-zzy76itq5v3v.picard.replit.dev/leaderboard"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def submit_score(nickname, score):
    url = "https://49750f73-1884-4a17-8781-14af8f9d6f26-00-zzy76itq5v3v.picard.replit.dev/leaderboard"
    payload = {
        "nickname": nickname,
        "score": score
    }
    response = requests.post(url, json=payload)
    return response.status_code == 201


SETTINGS_FILE = "settings.json"
fullscreen_checked = False
easy_mode_checked = False
music_volume = 100
sound_volume = 100
day_counter = 0
completed_tasks = 0
status_achieved_time = None
current_hour = 8
current_minute = 0
day_start_time = None
previous_screen = None
settings_open = False
game_paused = False
grades_data = []
colloquium_data = []
selected_lines = []
colloquium_checked_lines = []
colloquium_errors = []
timer_flag = True
active_event = None
event_button_rect = None

blue = (20, 33, 61)
zolty = (252, 163, 17)
szary = (229, 229, 229)


def save_settings():
    settings = {
        "fullscreen": fullscreen_checked,
        "easy_mode": easy_mode_checked,
        "music_volume": music_volume,
        "sound_volume": sound_volume,
        # "day_counter": day_counter,
        # "completed_tasks": completed_tasks
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)


def load_settings():
    global fullscreen_checked, easy_mode_checked, music_volume, sound_volume, day_counter, completed_tasks
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
                fullscreen_checked = settings.get("fullscreen", False)
                easy_mode_checked = settings.get("easy_mode", False)
                music_volume = settings.get("music_volume", 100)
                sound_volume = settings.get("sound_volume", 100)
        except json.JSONDecodeError:
            print("Błąd: settings.json jest uszkodzony. Przywracam domyślne ustawienia.")
            os.remove(SETTINGS_FILE)


pygame.init()
clock = pygame.time.Clock()
os.environ["SDL_VIDEO_CENTERED"] = "1"
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
load_settings()

flags = pygame.FULLSCREEN if fullscreen_checked else 0
screen = pygame.display.set_mode((SCREEN_WIDTH - 10, SCREEN_HEIGHT - 50), flags)
pygame.display.set_caption("WykładoHack")


def toggle_fullscreen(enabled):
    global screen
    if enabled:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH - 10, SCREEN_HEIGHT - 50))


frame = pygame.image.load('images/frame.png')
plus_icon = pygame.image.load('images/plus_icon.png')
minus_icon = pygame.image.load('images/minus_icon.png')
checked_icon = pygame.image.load('images/checked_icon.png')
volume_bar_border_icon = pygame.image.load('images/volume_border.png')
question_mark_icon = pygame.image.load('images/question_mark.png')
switch_ok_icon = pygame.image.load('images/switch_ok.png')
switch_no_icon = pygame.image.load('images/switch_no.png')
red_frame = pygame.image.load('images/red_frame.png')
red_frame_checked = pygame.image.load('images/red_frame_checked.png')
calendar_icon = pygame.image.load('images/achievements/calendar_white.png')
clock_blue = pygame.image.load('images/achievements/clock_blue.png')
calendar_gold = pygame.image.load('images/achievements/calendar_gold.png')
bid_green = pygame.image.load('images/achievements/bid_green.png')
coins_incoming_red = pygame.transform.scale(pygame.image.load('images/achievements/coins_incoming_red.png'), (32, 32))
cancel_gold = pygame.transform.scale(pygame.image.load('images/cancel_gold.png'), (32, 32))
confirm_green = pygame.transform.scale(pygame.image.load('images/confirm_green.png'), (32, 32))
cancel_red = pygame.transform.scale(pygame.image.load('images/cancel_red.png'), (32, 32))
background_map = pygame.image.load('images/map.png')
map_width, map_height = background_map.get_size()
scale_factor = 1.08
background_map = pygame.transform.scale(
    background_map,
    (int(map_width * scale_factor), int(map_height * scale_factor))
)


def scale_image(image, scale_factor):
    width, height = image.get_size()
    return pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))


switch_ok_icon = scale_image(switch_ok_icon, 2)
switch_no_icon = scale_image(switch_no_icon, 2)
money = 1000

title_font = pygame.font.Font('font/VT323-Regular.ttf', 64)
text_font = pygame.font.Font('font/VT323-Regular.ttf', 32)
other_font = pygame.font.Font('font/VT323-Regular.ttf', 24)
info_font = pygame.font.Font('font/VT323-Regular.ttf', 20)

current_screen = "menu"

character1_img = pygame.transform.scale(pygame.image.load('images/character1.png'), (200, 200))
character2_img = pygame.transform.scale(pygame.image.load('images/character2.png'), (200, 200))
selected_character = None

login_nickname = ""
login_password = ""
active_input = None

show_info = False
global switch_buttons
correct_states = []
current_error_count = 0

statusy = [
    "Licencjat",
    "Magister",
    "Doktorant",
    "Doktor",
    "Dr habilitowany",
    "Profesor nadzwyczajny",
    "Profesor uczelni",
    "Profesor zwyczajny"
]
progi = [4, 7, 10, 15, 20, 30, 42, 57]
current_status_idx = 0
total_completed_tasks = 0
show_status_notification = False


LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)



def draw_checkbox_with_cancel(surface, x, y, checked):
    surface.blit(frame, (x, y))
    if checked:
        cancel_rect = confirm_green.get_rect(center=(x + frame.get_width() // 2 - 1, y + frame.get_height() // 2 - 1))
        surface.blit(confirm_green, cancel_rect)
    return pygame.Rect(x, y, frame.get_width(), frame.get_height())


def draw_image_top_left_from_center(image, surface, offset_x=0, offset_y=0):
    screen_width, screen_height = surface.get_size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    topleft_x = center_x + offset_x
    topleft_y = center_y + offset_y
    surface.blit(image, (topleft_x, topleft_y))
    return image.get_rect(topleft=(topleft_x, topleft_y))


def draw_menu():
    screen.fill((255, 255, 255))
    draw_text("WykładoHack", title_font, 'red', screen, 0, -200)
    play_rect = draw_text("Graj", text_font, 'black', screen, 0, -40)
    settings_rect = draw_text("Ustawienia", text_font, 'black', screen, 0, 0)
    exit_rect = draw_text("Wyjdź z gry", text_font, 'black', screen, 0, 40)
    return play_rect, settings_rect, exit_rect


def draw_settings():
    screen.fill((255, 255, 255))
    draw_text("Ustawienia", title_font, 'black', screen, 0, -200)

    tooltips = {
        "Tryb pełnoekranowy": "Przełącz na pełny ekran lub okno.",
        "Łatwy tryb gry": "Włącz łatwiejszy tryb – dodatkowe pieniądze i mniejsza kara za błędy.",
        "Muzyka": "Regulacja głośności muzyki.",
        "Dźwięki": "Regulacja głośności efektów dźwiękowych."
    }

    mouse_hover_text = None

    fullscreen_text_rect = draw_text_top_left_from_center("Tryb pełnoekranowy", text_font, 'black', screen, -200, -100)
    fullscreen_icon_rect = draw_checkbox_with_cancel(screen, SCREEN_WIDTH // 2 + 170, SCREEN_HEIGHT // 2 - 95, fullscreen_checked)
    if fullscreen_text_rect.collidepoint(mouse_pos):
        mouse_hover_text = tooltips["Tryb pełnoekranowy"]

    easy_mode_text_rect = draw_text_top_left_from_center("Łatwy tryb gry", text_font, 'black', screen, -200, -60)
    easy_mode_icon_rect = draw_checkbox_with_cancel(screen, SCREEN_WIDTH // 2 + 170, SCREEN_HEIGHT // 2 - 55, easy_mode_checked)
    if easy_mode_text_rect.collidepoint(mouse_pos):
        mouse_hover_text = tooltips["Łatwy tryb gry"]

    music_text_rect = draw_text_top_left_from_center("Muzyka", text_font, 'black', screen, -200, -20)
    volume_bar_border_rect = draw_image_top_left_from_center(volume_bar_border_icon, screen, 30, -13)
    minus_icon_rect = draw_image_top_left_from_center(minus_icon, screen, 130, -15)
    plus_icon_rect = draw_image_top_left_from_center(plus_icon, screen, 170, -15)
    fill_width = int(84 * (music_volume / 100))
    pygame.draw.rect(screen, 'black', pygame.Rect(volume_bar_border_rect.left + 3, volume_bar_border_rect.top + 3, fill_width, 20))
    if music_text_rect.collidepoint(mouse_pos):
        mouse_hover_text = tooltips["Muzyka"]

    sound_text_rect = draw_text_top_left_from_center("Dźwięki", text_font, 'black', screen, -200, 20)
    sound_bar_border_rect = draw_image_top_left_from_center(volume_bar_border_icon, screen, 30, 27)
    sound_minus_icon_rect = draw_image_top_left_from_center(minus_icon, screen, 130, 25)
    sound_plus_icon_rect = draw_image_top_left_from_center(plus_icon, screen, 170, 25)
    fill_width_sound = int(84 * (sound_volume / 100))
    pygame.draw.rect(screen, 'black', pygame.Rect(sound_bar_border_rect.left + 3, sound_bar_border_rect.top + 3, fill_width_sound, 20))
    if sound_text_rect.collidepoint(mouse_pos):
        mouse_hover_text = tooltips["Dźwięki"]

    back_rect = draw_text("Powrót", text_font, 'black', screen, 0, 150)

    if mouse_hover_text:
        draw_tooltip(mouse_hover_text, mouse_pos[0], mouse_pos[1] + 20)

    return (back_rect, fullscreen_icon_rect, easy_mode_icon_rect, minus_icon_rect, plus_icon_rect, sound_minus_icon_rect, sound_plus_icon_rect)


def wrap_text(text, font, max_width):
    words = text.split()
    lines, current_line = [], ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def draw_task_box_with_checkbox(screen, x, y, text, checkbox_checked=False):
    checkbox_margin = 20
    text_margin = 10
    right_padding = 20
    line_spacing = 5
    min_box_height = frame.get_height() + 20 + 20
    max_box_width = 600
    min_box_width = 150
    available_text_width = max_box_width - checkbox_margin - frame.get_width() - text_margin - right_padding
    wrapped_text = wrap_text(text, other_font, available_text_width)
    text_height = len(wrapped_text) * other_font.get_height() + (len(wrapped_text) - 1) * line_spacing
    box_height = max(text_height + 20, min_box_height)
    if len(wrapped_text) == 1:
        line_width = other_font.size(wrapped_text[0])[0]
        box_width = checkbox_margin + frame.get_width() + text_margin + line_width + right_padding
        box_width = max(min_box_width, min(box_width, max_box_width))
    else:
        box_width = max_box_width
    shadow_offset = 2
    border_radius = 10
    pygame.draw.rect(screen, (0, 0, 0), (x + shadow_offset, y + shadow_offset, box_width, box_height),
                     border_radius=border_radius)
    pygame.draw.rect(screen, (255, 255, 255), (x, y, box_width, box_height), border_radius=border_radius)
    checkbox_x = x + checkbox_margin
    checkbox_y = y + (box_height // 2) - (frame.get_height() // 2)
    draw_checkbox_with_cancel(screen, checkbox_x, checkbox_y, checkbox_checked)
    text_x = checkbox_x + frame.get_width() + text_margin
    current_y = y + (box_height - text_height) // 2 if text_height < box_height else y + 10
    for line in wrapped_text:
        text_surface = other_font.render(line, True, 'black')
        screen.blit(text_surface, (text_x, current_y))
        current_y += text_surface.get_height() + line_spacing


def draw_multiple_task_boxes(screen, tasks, start_x, start_y, vertical_spacing=10):
    y = start_y
    for task in tasks:
        draw_task_box_with_checkbox(screen, start_x, y, task["text"], task["checked"])
        wrapped_text = wrap_text(task["text"], other_font, 600 - 20 - frame.get_width() - 10 - 20)
        height = max(len(wrapped_text) * other_font.get_height() + (len(wrapped_text) - 1) * 5 + 20,
                     frame.get_height() + 40)
        y += height + vertical_spacing


def draw_top_bar():
    global show_status_notification
    bar_height = 60
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, bar_height))
    pygame.draw.rect(screen, (0, 0, 0), (0, bar_height, SCREEN_WIDTH, 1))
    spacing = 40

    tab_surfaces = [text_font.render(tab, True, (0, 0, 0)) for tab in tabs]
    total_width = sum(s.get_width() for s in tab_surfaces) + spacing * (len(tabs) - 1)
    x = SCREEN_WIDTH - total_width - 20
    tab_rects = []

    for i, surf in enumerate(tab_surfaces):
        rect = surf.get_rect(topleft=(x, 15))
        screen.blit(surf, rect.topleft)
        tab_rects.append((tabs[i], rect))
        x += surf.get_width() + spacing

    if day_counter > 0 and current_screen != "day_end_screen":
        money_font = pygame.font.Font('font/VT323-Regular.ttf', 40)
        money_surf = money_font.render(f"${money}", True, (0, 0, 0))
        money_rect = money_surf.get_rect()
        money_rect.topleft = (15, (bar_height - money_rect.height) // 2)
        screen.blit(money_surf, money_rect)

        if money_rect.collidepoint(mouse_pos):
            tooltip_text = "Aktualna wartość zaoszczędzonych pieniędzy."
            draw_tooltip(tooltip_text, mouse_pos[0], mouse_pos[1] + 20)

        status_x = 15 + money_surf.get_width() + 20
        status_text = f"Status: {statusy[current_status_idx]}"
        status_surf = text_font.render(status_text, True, (0, 0, 0))
        status_rect = status_surf.get_rect(topleft=(status_x, 15))
        screen.blit(status_surf, (status_x, 15))

        if status_rect.collidepoint(mouse_pos):
            bonus = current_status_idx
            tooltip_text = f"Dodatkowe +{bonus} monet za każde wykonane zadanie."
            draw_tooltip(tooltip_text, mouse_pos[0], mouse_pos[1] + 20)

        if show_status_notification:
            elapsed = (pygame.time.get_ticks() - status_achieved_time) / 1000
            if elapsed < 3:
                notif_surf = text_font.render("- osiągnięto nowy status", True, (255, 0, 0))
                screen.blit(notif_surf, (status_x + status_surf.get_width() + 10, 15))
            else:
                show_status_notification = False

    return tab_rects


def get_circular_surface(image):
    size = image.get_size()
    circle_surf = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.circle(circle_surf, (255, 255, 255, 255), (size[0] // 2, size[1] // 2), size[0] // 2)
    circle_surf.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return circle_surf


def draw_character_select():
    screen.blit(background_map, (0, 0))
    if timer_flag:
        draw_timer()
    draw_multiple_task_boxes(screen, tasks, 50, 180)
    char1_rect = char2_rect = None
    if selected_character is None:
        circular_char1 = get_circular_surface(character1_img)
        circular_char2 = get_circular_surface(character2_img)
        draw_rounded_rect_from_center_offset(screen, -400, -50, 420, 100, (255, 255, 255), 100)
        draw_rounded_rect_from_center_offset(screen, 300, -50, 490, 100, (255, 255, 255), 100)
        char1_rect = draw_image_top_left_from_center(circular_char1, screen, -500, -100)
        char2_rect = draw_image_top_left_from_center(circular_char2, screen, 300, -100)
        draw_text_top_left_from_center("Informatyk", title_font, 'black', screen, -280, -32)
        draw_text_top_left_from_center("Matematyk", title_font, 'black', screen, 520, -32)
    else:
        pygame.draw.rect(screen, szary,
                         pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 120, 200, 250))
        pygame.draw.rect(screen, szary, pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120, 200, 250))
    return char1_rect, char2_rect


def draw_rounded_rect_from_center_offset(surface, offset_x, offset_y, width, height, color, corner_radius,
                                         shadow_offset=(2, 2), shadow_color=(0, 0, 0)):
    screen_center_x = surface.get_width() // 2
    screen_center_y = surface.get_height() // 2
    x = screen_center_x + offset_x
    y = screen_center_y + offset_y
    shadow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, shadow_color, (0, 0, width, height), border_radius=corner_radius)
    surface.blit(shadow_surf, (x + shadow_offset[0], y + shadow_offset[1]))
    shape_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, (0, 0, width, height), border_radius=corner_radius)
    surface.blit(shape_surf, (x, y))
    return pygame.Rect(x, y, width, height)


def handle_character_selection(mouse_pos, mouse_clicked, char1_rect, char2_rect):
    global current_screen, selected_character
    if mouse_clicked:
        if char1_rect.collidepoint(mouse_pos):
            selected_character = "character1"
        elif char2_rect.collidepoint(mouse_pos):
            selected_character = "character2"
        else:
            return
        complete_task(0)
        if "Zaloguj" not in tabs:
            tabs.append("Zaloguj")
        tasks.append(
            {"text": "Zaloguj się do systemu klikając przycisk 'Zaloguj' w prawym górnym rogu", "checked": False})
        current_screen = "task_screen"


def complete_task(index):
    global completed_tasks, total_completed_tasks, current_status_idx, status_achieved_time, show_status_notification
    if 0 <= index < len(tasks) and not tasks[index]["checked"]:
        tasks[index]["checked"] = True
        completed_tasks += 1
        total_completed_tasks += 1

        next_idx = current_status_idx + 1
        if next_idx < len(statusy) and total_completed_tasks >= progi[next_idx]:
            current_status_idx = next_idx
            status_achieved_time = pygame.time.get_ticks()
            show_status_notification = True

        save_settings()


def draw_timer():
    text = f"Dzień {day_counter + 1} Godzina: {current_hour:02}:{current_minute:02}"
    text_surface = text_font.render(text, True, "black")
    draw_rounded_rect(screen, 50, 100, text_surface.get_width() + 40, 70, (255, 255, 255), 10, (2, 2), (0, 0, 0))
    screen.blit(text_surface, (70, 117))


def draw_task_screen():
    screen.fill(szary)
    draw_top_bar()
    if timer_flag:
        draw_timer()
    draw_multiple_task_boxes(screen, tasks, 50, 180)


def draw_rounded_rect(surface, x, y, width, height, color, corner_radius,
                      shadow_offset=(2, 2), shadow_color=(0, 0, 0)):
    shadow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, shadow_color, (0, 0, width, height), border_radius=corner_radius)
    surface.blit(shadow_surf, (x + shadow_offset[0], y + shadow_offset[1]))
    shape_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, (0, 0, width, height), border_radius=corner_radius)
    surface.blit(shape_surf, (x, y))


def draw_info_box(pos):
    info_text = "Login jest używany jako nazwa użytkownika do tabeli wyników. Maksymalna liczba znaków dla loginu i hasła wynosi 15."
    box_width = 300
    padding = 10
    corner_radius = 10
    box_color = (255, 255, 255)
    wrapped_info = wrap_text(info_text, info_font, box_width - 2 * padding)
    line_height = info_font.get_height() + 5
    box_height = len(wrapped_info) * line_height + 2 * padding
    x, y = pos
    draw_rounded_rect(
        surface=screen,
        x=x,
        y=y,
        width=box_width,
        height=box_height,
        color=box_color,
        corner_radius=corner_radius,
        shadow_offset=(2, 2),
        shadow_color=(0, 0, 0)
    )
    text_x = x + padding
    text_y = y + padding
    for line in wrapped_info:
        line_surface = info_font.render(line, True, 'black')
        screen.blit(line_surface, (text_x, text_y))
        text_y += line_height


def draw_login_form():
    global nickname_rect, password_rect, login_button_rect, show_info
    tabs.clear()
    draw_task_screen()
    draw_rounded_rect_from_center_offset(screen, -250, -200, 500, 400, (255, 255, 255), 10)
    draw_text("Logowanie", title_font, 'black', screen, 0, -130)
    draw_text_top_left_from_center("Login:", text_font, 'black', screen, -150, -50)
    nickname_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, 200, 30)
    pygame.draw.rect(screen, (255, 255, 255), nickname_rect)
    pygame.draw.rect(screen, (0, 0, 0), nickname_rect, 2)
    nickname_surface = text_font.render(login_nickname, True, 'black')
    nickname_text_rect = nickname_surface.get_rect()
    nickname_text_rect.topleft = (
        nickname_rect.x + 5, nickname_rect.y + (nickname_rect.height - nickname_text_rect.height) // 2 - 1)
    screen.blit(nickname_surface, nickname_text_rect)
    draw_text_top_left_from_center("Hasło:", text_font, 'black', screen, -150, 0)
    password_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 200, 30)
    pygame.draw.rect(screen, (255, 255, 255), password_rect)
    pygame.draw.rect(screen, (0, 0, 0), password_rect, 2)
    hidden_password = "*" * len(login_password)
    password_surface = text_font.render(hidden_password, True, 'black')
    password_text_rect = password_surface.get_rect()
    password_text_rect.topleft = (
        password_rect.x + 5, password_rect.y + (password_rect.height - password_text_rect.height) // 2 - 1)
    screen.blit(password_surface, password_text_rect)
    login_button_rect = draw_button("Akceptuj", 150, 50, SCREEN_WIDTH // 2 + 0, SCREEN_HEIGHT // 2 + 100)
    question_rect = draw_image_top_left_from_center(question_mark_icon, screen, 210, 160)
    if question_rect.collidepoint(mouse_pos):
        show_info = True
    else:
        show_info = False
    if show_info:
        draw_tooltip(
            "Login jest używany jako nazwa użytkownika do tabeli wyników. "
            "Maksymalna liczba znaków dla loginu i hasła wynosi 15.",
            mouse_pos[0], mouse_pos[1] + 20
        )


def calculate_final_grade(average):
    if 2.0 <= average < 2.25:
        return 2
    elif 2.25 <= average < 3.25:
        return 3
    elif 3.25 <= average < 3.75:
        return 3.5
    elif 3.75 <= average < 4.25:
        return 4
    elif 4.25 <= average < 4.75:
        return 4.5
    elif 4.75 <= average <= 5.0:
        return 5
    else:
        return None


def adjust_final_grade(final_grade, easy_mode_checked):
    possible_grades = [2, 3, 3.5, 4, 4.5, 5]

    if random.random() < 0.5:
        if easy_mode_checked:
            candidates = [g for g in possible_grades if abs(g - final_grade) == 0.5]
            if candidates:
                return random.choice(candidates)
            else:
                return final_grade
        else:
            wrong_choices = [g for g in possible_grades if g != final_grade]
            return random.choice(wrong_choices)
    else:
        return final_grade


switch_buttons = []
switches_initialized = False


class SwitchButton:
    def __init__(self, x, y, initial_state=False):
        self.state = initial_state
        self.rect = switch_ok_icon.get_rect(topleft=(x, y))

    def draw(self, screen):
        icon = switch_ok_icon if self.state else switch_no_icon
        screen.blit(icon, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state




global students_names
student_names = [
    'Michał Kiraga', 'Jakub Gadomski', 'Marcin Najman', 'Jacek Murański',
    'Denis Załęcki', 'Denis Labryga', 'Natan Marcoń', 'Gracjan Szadziński',
    'Michael Bagietson', 'Marek Jówko', 'Daniel Magical', 'Gosia Magical',
    'Bartosz Szachta', 'Piotr Szeliga', 'Mini Majk', 'Jaś Kapela', 'Tomek Czynsz',
    'Robert Patus', 'Alberto Simao', 'Josef Bratan', 'Mariusz Pudzianowski'
]



def get_grades_data(easy_mode_checked):
    grades_data_local = []
    available_names = student_names.copy()
    for _ in range(5):
        if available_names:
            name = random.choice(available_names)
            available_names.remove(name)
            grades = [random.randint(2, 5) for _ in range(random.randint(3, 6))]
            avg = round(sum(grades) / len(grades), 2)
            final_grade = calculate_final_grade(avg)
            final_grade_adjusted = adjust_final_grade(final_grade, easy_mode_checked)
            grades_data_local.append((name, grades, avg, final_grade_adjusted))
    return grades_data_local


def draw_grades_window(grades_data):
    draw_task_screen()
    rect = draw_rounded_rect_from_center_offset(screen, -250, -400, 500, 850, (255, 255, 255), 10)
    font = other_font
    xx, yy = 950, 530
    x, y = rect.left + 20, rect.top + 20
    draw_text_top_left_from_center("Oceny studentów:", font, (0, 0, 0), screen, x - xx, y - yy)
    y += 50
    for i, (name, grades, avg, final_grade_adjusted) in enumerate(grades_data):
        base_y = y + i * 140
        grades_str = ', '.join(map(str, grades))
        draw_text_top_left_from_center(f"Imię i nazwisko: {name}", font, (0, 0, 0), screen, x - xx, base_y - yy)
        draw_text_top_left_from_center(f"Oceny: {grades_str}", font, (0, 0, 0), screen, x - xx, base_y + 30 - yy)
        draw_text_top_left_from_center(f"Średnia: {avg}", font, (0, 0, 0), screen, x - xx, base_y + 60 - yy)
        draw_text_top_left_from_center(f"Ocena końcowa: {final_grade_adjusted}", font, (0, 0, 0), screen, x - xx,
                                       base_y + 90 - yy)
    accept_button_rect = draw_button("Akceptuj", 150, 50, SCREEN_WIDTH // 2 + 0, SCREEN_HEIGHT // 2 + 400)
    return accept_button_rect


def init_switches(persons, easy_mode_checked):
    global switch_buttons, switches_initialized
    switch_buttons.clear()
    base_x, base_y = SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 - 230
    row_h = 140
    for i, person in enumerate(persons):
        x = base_x
        y = base_y + i * row_h
        switch = SwitchButton(x, y, False)
        switch_buttons.append(switch)
    switches_initialized = True


def draw_switches():
    for switch in switch_buttons:
        switch.draw(screen)


money_per_task = 15
rent_price = 25
food_price = 15
penalty_for_error = 5
easy_mode_grant = 15

food_checkbox_checked = False
global fullscreen_icon_rect
global total_sum

achievements = [
    {"name": "Pierwszy dzień", "desc": "Ukończ pierwszy dzień gry.", "unlocked": False, "color": None},
    {"name": "Mistrz Zadań", "desc": "Wykonaj 10 zadań.", "unlocked": False, "color": None},
    {"name": "Wytrwały", "desc": "Przetrwaj 3 dni.", "unlocked": False, "color": None},
    {"name": "Bogacz", "desc": "Zdobądź 100 monet.", "unlocked": False, "color": None},
    {"name": "Bankrut", "desc": "Posiadaj ujemne saldo konta.", "unlocked": False, "color": None},
]


def update_achievements():
    conditions = [
        lambda: day_counter >= 1,
        lambda: total_completed_tasks >= 10,
        lambda: day_counter >= 3,
        lambda: money >= 100,
        lambda: money < 0,
    ]

    for i, condition in enumerate(conditions):
        if condition() and not achievements[i]["unlocked"]:
            achievements[i]["unlocked"] = True


family_members = [
    {"role": "Żona", "status": "Zdrowa", "hunger_days": 0, "sick_days": 0, "alive": True},
    {"role": "Syn", "status": "Zdrowy", "hunger_days": 0, "sick_days": 0, "alive": True},
    {"role": "Córka", "status": "Zdrowa", "hunger_days": 0, "sick_days": 0, "alive": True}
]


medicine_checkboxes_checked = {}


def draw_day_end_window(day_counter):
    global timer_flag, medicine_checkboxes_checked
    tabs.clear()
    tasks.clear()
    timer_flag = False
    draw_task_screen()
    timer_flag = True

    global medicine_price
    medicine_price = 5 if easy_mode_checked else 10

    draw_text(f"Koniec dnia {day_counter + 1}", title_font, "black", screen, 0, -350)

    fullscreen_icon_rect = pygame.Rect(0, 0, 0, 0)

    draw_rounded_rect_from_center_offset(screen, -275, -225, 550, 450, (255, 255, 255), 10)

    bonus_per_task = current_status_idx

    global day_end_data
    day_end_data = [
        {"text": "Oszczędności", "status": 0, "color": "black", "value": money},
        {"text": f"Wynagrodzenie ({completed_tasks})", "status": 0, "color": "black",
         "value": completed_tasks * (money_per_task + bonus_per_task)},
    ]

    if current_error_count > 0:
        day_end_data.append({
            "text": f"Błędy ({current_error_count})",
            "status": 0,
            "color": "red",
            "value": -penalty_for_error * current_error_count
        })

    day_end_data.extend([
        {"text": "Wynajem", "status": 0, "color": "red", "value": -rent_price},
        {"text": "Jedzenie", "status": 1, "color": "red", "value": -food_price},
    ])

    for member in family_members:
        role = member["role"]
        if "Chory" not in member["status"] and "Chora" not in member["status"]:
            if role in medicine_checkboxes_checked:
                del medicine_checkboxes_checked[role]

    for member in family_members:
        if "Chory" in member["status"] or "Chora" in member["status"]:
            role = member["role"]
            if role not in medicine_checkboxes_checked:
                medicine_checkboxes_checked[role] = False
            day_end_data.append({
                "text": f"Leki ({role})",
                "status": 1,
                "color": "red",
                "value": -medicine_price
            })

    tooltips = {
        "Oszczędności": "Stan Twoich oszczędności na koniec poprzedniego dnia.",
        "Wynagrodzenie": f"Zarobek za wykonane zadania w tym dniu."
                         f" Wykonane zadania ({completed_tasks}), podstawowa wartość za zadanie ({money_per_task}),"
                         f" dodatkowa gotówka za aktualny status ({bonus_per_task * completed_tasks})",
        "Wynajem": "Opłata za wynajem mieszkania.",
        "Jedzenie": "Koszt jedzenia – możesz zrezygnować, ale konsekwencje przyjdą później!",
        "Kwota końcowa": "Łączna suma dostępnych środków na następny dzień.",
        "Błędy": "Kara za błędy popełnione podczas pracy.",
    }

    tooltip_to_draw = None
    for idx, entry in enumerate(day_end_data):
        text_rect = draw_text_top_left_from_center(entry["text"], text_font, entry["color"], screen, -200,
                                                   idx * 40 - 200)
        entry["text_rect"] = text_rect
        draw_text_top_right_from_center(entry["value"], text_font, entry["color"], screen, 200, idx * 40 - 200)

        if entry["status"] == 1:
            frame_pos = draw_image_top_left_from_center(red_frame, screen, 220, idx * 40 - 198)

            if entry["text"].startswith("Leki ("):
                role = entry["text"].split("(")[1].split(")")[0]
                if medicine_checkboxes_checked.get(role, False):
                    confirm_rect = cancel_red.get_rect(center=frame_pos.center)
                    screen.blit(cancel_red, confirm_rect)

                entry["checkbox_rect"] = frame_pos
                entry["checkbox_role"] = role

                if text_rect.collidepoint(mouse_pos):
                    tooltip_to_draw = f"Opłata za leki dla: {role}"

            elif entry["text"] == "Jedzenie":
                if food_checkbox_checked:
                    cancel_rect = cancel_red.get_rect(center=frame_pos.center)
                    screen.blit(cancel_red, cancel_rect)
                food_toggle_rect = frame_pos

        tooltip_label = entry["text"].split()[0]
        if tooltip_label in tooltips and text_rect.collidepoint(mouse_pos):
            tooltip_to_draw = tooltips[tooltip_label]

    extra_lines = 0

    if easy_mode_checked:
        zap_idx = len(day_end_data)
        zap_rect = draw_text_top_left_from_center("Zapomoga (tryb łatwy)", text_font, "black", screen, -200,
                                                  zap_idx * 40 - 200)
        draw_text_top_right_from_center(easy_mode_grant, text_font, "black", screen, 200, zap_idx * 40 - 200)
        if zap_rect.collidepoint(mouse_pos):
            tooltip_to_draw = "Dodatkowy bonus w łatwym trybie. Pomaga przetrwać trudne początki!"
        extra_lines = 1

    separator_y = (len(day_end_data) + extra_lines) * 40 - 200
    draw_text_top_left_from_center("-------------------------------", text_font, "black", screen, -200, separator_y)

    total_sum = 0
    for entry in day_end_data:
        if entry["text"] == "Jedzenie":
            if food_checkbox_checked:
                total_sum += entry["value"]
        elif entry["text"].startswith("Leki ("):
            role = entry["text"].split("(")[1].split(")")[0]
            if medicine_checkboxes_checked.get(role, True):
                total_sum += entry["value"]
        else:
            total_sum += entry["value"]

    if easy_mode_checked:
        total_sum += easy_mode_grant

    total_lines = len(day_end_data) + extra_lines
    final_text = f"${total_sum}"
    final_text_rect = draw_text_top_right_from_center(final_text, text_font, "black", screen, 200,
                                                      (total_lines + 1) * 40 - 200)

    if final_text_rect.collidepoint(mouse_pos):
        tooltip_to_draw = tooltips["Kwota końcowa"]

    continue_rect = draw_button("Kontynuuj", 150, 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)

    status_colors = {
        "Zdrowa": (0, 200, 0), "Zdrowy": (0, 200, 0),
        "Chora": (255, 165, 0), "Chory": (255, 165, 0),
        "Głodna": (255, 215, 0), "Głodny": (255, 215, 0),
        "Martwa": (200, 0, 0), "Martwy": (200, 0, 0)
    }

    radius = 50
    spacing = 40
    total_height = len(family_members) * (2 * radius + spacing) - spacing
    start_y = SCREEN_HEIGHT // 2 - total_height // 2 + radius
    x = SCREEN_WIDTH - 180

    for i, member in enumerate(family_members):
        cy = start_y + i * (2 * radius + spacing)
        status = member["status"]

        statuses = status.split(", ")

        if "Martwy" in statuses or "Martwa" in statuses:
            pygame.draw.circle(screen, (0, 0, 0), (x + 2, cy + 2), radius)
            pygame.draw.circle(screen, (200, 0, 0), (x, cy), radius)
            status_text = other_font.render(statuses[0], True, (255, 255, 255))
            screen.blit(status_text, status_text.get_rect(center=(x, cy)))
        else:
            total_width = len(statuses) * (2 * radius + 10) - 10
            sx = x - total_width // 2 + radius
            for j, s in enumerate(statuses):
                cx = sx + j * (2 * radius + 10)
                color = status_colors.get(s, (0, 0, 0))
                pygame.draw.circle(screen, (0, 0, 0), (cx + 2, cy + 2), radius)
                pygame.draw.circle(screen, color, (cx, cy), radius)
                status_text = other_font.render(s, True, (0, 0, 0))
                screen.blit(status_text, status_text.get_rect(center=(cx, cy)))

        role_text = other_font.render(member["role"], True, (0, 0, 0))
        screen.blit(role_text, role_text.get_rect(center=(x, cy + radius + 20)))

    achievement_icons = [calendar_icon, clock_blue, calendar_gold, bid_green, coins_incoming_red]

    update_achievements()
    ach_size = 64
    ach_spacing = 10

    unlocked_achievements = [
        (ach, i) for i, ach in enumerate(achievements) if ach["unlocked"]
    ]

    ach_total_height = len(unlocked_achievements) * (
            ach_size + ach_spacing) - ach_spacing if unlocked_achievements else 0
    ach_start_y = (SCREEN_HEIGHT - ach_total_height) // 2
    ach_x = 130
    hovered_achievement = None

    for j, (ach, i) in enumerate(unlocked_achievements):
        top = ach_start_y + j * (ach_size + ach_spacing)
        rect = pygame.Rect(ach_x - ach_size // 2, top, ach_size, ach_size)
        if i < len(achievement_icons):
            icon = pygame.transform.scale(achievement_icons[i], (ach_size, ach_size))
            screen.blit(icon, rect)

        if rect.collidepoint(mouse_pos):
            hovered_achievement = ach

    if hovered_achievement:
        draw_tooltip(f"{hovered_achievement['name']}: {hovered_achievement['desc']}", mouse_pos[0], mouse_pos[1] + 20)

    if tooltip_to_draw:
        draw_tooltip(tooltip_to_draw, mouse_pos[0], mouse_pos[1] + 20)

    if not is_any_family_member_alive():
        return None, None, None
    return continue_rect, food_toggle_rect, total_sum



def generate_colloquium():
    global colloquium_data, colloquium_errors, selected_lines

    name = random.choice(student_names)
    entry = random.choice(colloquium_bank)
    variant = random.choice(entry["variants"])
    task = entry["task"]
    code = variant["code"]
    errors = variant["errors"]

    selected_lines = [False] * len(code)
    colloquium_data = (name, task, code)
    colloquium_errors = errors


def draw_colloquium_window():
    draw_task_screen()

    rect = draw_rounded_rect_from_center_offset(screen, -250, -400, 800, 850, (255, 255, 255), 10)
    font = other_font
    xx, yy = 950, 530
    x, y = rect.left + 20, rect.top + 20

    name, task, code_lines = colloquium_data
    draw_text_top_left_from_center("Kolokwium studenta:", font, (0, 0, 0), screen, x - xx, y - yy)
    y += 40
    draw_text_top_left_from_center(f"Imię i nazwisko: {name}", font, (0, 0, 0), screen, x - xx, y - yy)
    y += 40
    draw_text_top_left_from_center(f"Polecenie: {task}", font, (0, 0, 0), screen, x - xx, y - yy)
    y += 60

    line_rects = []
    for i, line in enumerate(code_lines):
        color = (255, 0, 0) if selected_lines[i] else (0, 0, 0)
        line_number = f"{i + 1}".rjust(2)
        line_text = f"{line_number}: {line}"
        text_rect = draw_text_top_left_from_center(line_text, font, color, screen, x - xx, y - yy)
        y += 40
        line_rects.append(text_rect)

    accept_button_rect = draw_button("Zatwierdź sprawdzanie", 300, 50, SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 400)

    return line_rects, accept_button_rect


def draw_button(text, width, height, center_x, center_y):
    shadow_offset = 2

    rect_shadow = pygame.Rect(0, 0, width, height)
    rect_shadow.center = (center_x + shadow_offset, center_y + shadow_offset)
    pygame.draw.rect(screen, (0, 0, 0), rect_shadow, border_radius=10)

    rect = pygame.Rect(0, 0, width, height)
    rect.center = (center_x, center_y)
    pygame.draw.rect(screen, zolty, rect, border_radius=10)

    text_surf = text_font.render(text, True, blue)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

    return rect


def draw_tooltip(text, x, y):
    padding = 10
    font = info_font
    lines = wrap_text(text, font, 300)
    width = max(font.size(line)[0] for line in lines) + 2 * padding
    height = len(lines) * font.get_height() + 2 * padding

    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))

    for i, line in enumerate(lines):
        line_surf = font.render(line, True, (255, 255, 255))
        screen.blit(line_surf, (x + padding, y + padding + i * font.get_height()))


medicine_checkboxes = {}


def update_family_health():
    for member in family_members:
        statuses = member["status"].split(", ")
        statuses_set = set(statuses)

        if food_checkbox_checked:
            statuses_set.discard("Głodny")
            statuses_set.discard("Głodna")
            member["days_without_food"] = 0
        else:
            member["days_without_food"] = member.get("days_without_food", 0) + 1

        if member["days_without_food"] >= 1 and not member["status"] in ["Martwy", "Martwa"]:
            hunger_status = "Głodny" if member["role"].endswith("n") else "Głodna"
            statuses_set.discard("Zdrowy")
            statuses_set.discard("Zdrowa")
            statuses_set.add(hunger_status)

            if "Chory" not in statuses_set and "Chora" not in statuses_set:
                if random.random() < 0.25:
                    illness_status = "Chory" if hunger_status == "Głodny" else "Chora"
                    statuses_set.add(illness_status)

        if food_checkbox_checked and ("Chory" in statuses_set or "Chora" in statuses_set):
            member["days_sick"] = member.get("days_sick", 0) + 1
            if member["days_sick"] >= 3:
                statuses_set.discard("Chory")
                statuses_set.discard("Chora")
                statuses_set.add("Zdrowy" if member["role"].endswith("n") else "Zdrowa")
                member["days_sick"] = 0
        else:
            member["days_sick"] = member.get("days_sick", 0)

        if ("Chory" in statuses_set or "Chora" in statuses_set) and \
           ("Głodny" in statuses_set or "Głodna" in statuses_set):
            member["sick_and_hungry_days"] = member.get("sick_and_hungry_days", 0) + 1
            if member["sick_and_hungry_days"] >= 2 and random.random() < 0.25:
                statuses_set = {"Martwy" if member["role"].endswith("n") else "Martwa"}
                member["alive"] = False
        else:
            member["sick_and_hungry_days"] = 0

        if not statuses_set:
            statuses_set.add("Zdrowy" if member["role"].endswith("n") else "Zdrowa")
        member["status"] = ", ".join(statuses_set)


def is_any_family_member_alive():
    return any(member["alive"] for member in family_members)


cups = [pygame.image.load(f'images/cup{i}.png') for i in range(1, 6)]
cups = [pygame.transform.scale(cup, (200, 200)) for cup in cups]
center_pos = ((SCREEN_WIDTH - 200) // 2, (SCREEN_HEIGHT - 200) // 2)


class ConfettiParticle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-SCREEN_HEIGHT, 0)
        self.size = random.randint(4, 8)
        self.color_base = random.choice([
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255)
        ])
        self.speed = random.uniform(0.5, 1.5)
        self.angle = random.uniform(-1.0, 1.0)

    def update(self):
        self.y += self.speed
        self.x += self.angle
        if self.y > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface, alpha):
        color = (*self.color_base, alpha)
        confetti_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(confetti_surface, color, (0, 0, self.size, self.size))
        surface.blit(confetti_surface, (self.x, self.y))


def draw_confetti_effect(surface, particles, elapsed_time, total_duration):
    if elapsed_time >= total_duration:
        alpha = 0
    else:
        alpha = int(255 * (1 - (elapsed_time / total_duration)))

    for p in particles:
        p.update()
        p.draw(surface, alpha)


def animate_cup_and_confetti():
    global clock
    total_duration = 3.5
    elapsed = 0
    intervals = []
    current_interval = 0.05
    while elapsed < total_duration:
        intervals.append(current_interval)
        current_interval += 0.02
        elapsed += current_interval

    global selected_cup_index
    selected_cup_index = random.randint(0, 4)
    current_index = 0

    for interval in intervals:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        screen.blit(cups[current_index], center_pos)
        pygame.display.flip()

        pygame.time.delay(int(interval * 1000))
        current_index = (current_index + 1) % len(cups)


final_screen_start_time = None
confetti_particles = [ConfettiParticle() for _ in range(100)]
selected_cup_index = random.randint(0, 4)
confetti_duration = 10
showing_confetti = True


def calculate_final_score(days_survived, tasks_completed, money_left, total_errors, status_idx, achievements_unlocked):
    status_bonus_table = [0, 50, 100, 150, 250, 400, 600, 800, 1000, 1500]
    status_bonus = status_bonus_table[status_idx] if 0 <= status_idx < len(status_bonus_table) else 0
    achievements_bonus = achievements_unlocked * 200
    return (days_survived * 50) + (tasks_completed * 20) + money_left - (total_errors * 10) + status_bonus + achievements_bonus


def draw_final_screen():
    global final_screen_start_time

    if final_screen_start_time is None:
        final_screen_start_time = time.time()

    elapsed = time.time() - final_screen_start_time

    screen.fill((255, 255, 255))

    days_survived = day_counter + 1
    tasks_completed_total = total_completed_tasks
    money_left = money
    total_errors_made = current_error_count
    current_status_index = current_status_idx
    achievements_unlocked_count = sum(1 for ach in achievements if ach["unlocked"])

    final_score = calculate_final_score(
        days_survived,
        tasks_completed_total,
        money_left,
        total_errors_made,
        current_status_index,
        achievements_unlocked_count
    )

    success_text = f"Wynik końcowy: {final_score}"
    success_surface = text_font.render(success_text, True, (0, 0, 0))
    success_rect = success_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    screen.blit(success_surface, success_rect)

    screen.blit(cups[selected_cup_index], center_pos)

    if elapsed < confetti_duration:
        draw_confetti_effect(screen, confetti_particles, elapsed, confetti_duration)

    menu_button_rect = draw_button("Menu główne", 300, 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250)

    leaderboard_button_rect = draw_button("Tablica wyników", 300, 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 330)

    return menu_button_rect, leaderboard_button_rect


cached_leaderboard = None


def draw_leaderboard_screen(local_leaderboard=None):
    global cached_leaderboard
    screen.fill((255, 255, 255))
    draw_text("Tablica wyników", title_font, 'black', screen, 0, -300)

    if cached_leaderboard is None:
        leaderboard = download_leaderboard()
        if not leaderboard:
            leaderboard = local_leaderboard
        cached_leaderboard = leaderboard
    else:
        leaderboard = cached_leaderboard

    sorted_leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

    top_10 = sorted_leaderboard[:10]
    y_offset = -200
    for i, entry in enumerate(top_10):
        text = f"{i+1}. {entry['nickname']} - {entry['score']}"
        draw_text(text, text_font, 'black', screen, 0, y_offset + i * 40)

    if login_nickname:
        your_entry = None
        for idx, entry in enumerate(sorted_leaderboard):
            if entry["nickname"] == login_nickname:
                your_entry = (idx + 1, entry)
                break
        if your_entry and your_entry[0] > 10:
            draw_text("...", text_font, 'black', screen, 0, y_offset + 10 * 40)
            idx, entry = your_entry
            text = f"{idx}. {entry['nickname']} - {entry['score']}"
            draw_text(text, text_font, 'black', screen, 0, y_offset + 11 * 40)

    back_button_rect = draw_button("Wróć", 300, 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
    return back_button_rect


tasks = [{"text": "Wybierz swój zawód", "checked": False}]
tabs = []

pause_start_time = None
run = True


def init_new_game():
    global selected_character, day_counter, completed_tasks, total_completed_tasks, current_status_idx, money, food_checkbox_checked, medicine_checkboxes_checked, family_members, login_nickname, login_password
    selected_character = None
    day_counter = 0
    completed_tasks = 0
    total_completed_tasks = 0
    current_status_idx = 0
    money = 1000
    food_checkbox_checked = False
    medicine_checkboxes_checked = {}
    family_members = [
        {"role": "Żona", "status": "Zdrowa", "hunger_days": 0, "sick_days": 0, "alive": True},
        {"role": "Syn", "status": "Zdrowy", "hunger_days": 0, "sick_days": 0, "alive": True},
        {"role": "Córka", "status": "Zdrowa", "hunger_days": 0, "sick_days": 0, "alive": True}
    ]
    login_nickname = ""
    login_password = ""
    answered_mails.clear()


def draw_failure_screen():
    global final_screen_start_time
    if final_screen_start_time is None:
        final_screen_start_time = time.time()

    elapsed = time.time() - final_screen_start_time
    screen.fill((255, 255, 255))

    failure_text = "Wszyscy członkowie rodziny zmarli!"
    retry_text = "Przegrałeś."

    failure_surface = text_font.render(failure_text, True, (0, 0, 0))
    retry_surface = text_font.render(retry_text, True, (0, 0, 0))

    failure_rect = failure_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    retry_rect = retry_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    screen.blit(failure_surface, failure_rect)
    screen.blit(retry_surface, retry_rect)

    menu_button_rect = draw_button("Menu główne", 300, 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
    leaderboard_button_rect = draw_button("Tablica wyników", 300, 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 230)

    return menu_button_rect, leaderboard_button_rect


def trigger_random_event():
    global active_event, current_screen
    event = random.choice(random_events)
    active_event = event
    current_screen = "event_popup"


event_images = {
    "sick_wife": pygame.image.load('images/event_sick_wife.png'),
    "lost_wallet": pygame.image.load('images/event_lost_wallet.png'),
    "found_money": pygame.image.load('images/event_found_money.png'),
    "side_job": pygame.image.load('images/event_side_job.png'),
    "work_mistake": pygame.image.load('images/event_work_mistake.png'),
    "sick_daughter": pygame.image.load('images/event_sick_daughter.png'),
    "pc_crash": pygame.image.load('images/event_pc_crash.png'),
    "work_bonus": pygame.image.load('images/event_work_bonus.png'),
    "cake_gift": pygame.image.load('images/event_cake_gift.png'),
    "car_damage": pygame.image.load('images/event_car_damage.png'),
    "dean_report": pygame.image.load('images/event_dean_report.png'),
    "snack_spending": pygame.image.load('images/event_snack_spending.png'),
    "mugging": pygame.image.load('images/event_mugging.png'),
    "son_fight": pygame.image.load('images/event_son_fight.png')
}

random_events = [
    {
        "text": "Ponieważ zapomniałeś zamknąć okno idąc spać, twoja żona zachorowała.",
        "effect": lambda: infect_family_member("Żona"),
        "image": event_images["sick_wife"]
    },
    {
        "text": "Zgubiłeś portfel w autobusie. Straciłeś 50 monet.",
        "effect": lambda: change_money(-50),
        "image": event_images["lost_wallet"]
    },
    {
        "text": "Twój syn znalazł 20 monet na ulicy i przyniósł je do domu.",
        "effect": lambda: change_money(20),
        "image": event_images["found_money"]
    },
    {
        "text": "Zadzwonił znajomy z ofertą drobnej pracy. Zarobiłeś 30 monet.",
        "effect": lambda: change_money(30),
        "image": event_images["side_job"]
    },
    {
        "text": "Z powodu zmęczenia popełniłeś błąd w zadaniu.",
        "effect": lambda: add_error(),
        "image": event_images["work_mistake"]
    },
    {
        "text": "Twoja córka zaraziła się w szkole i przez najbliższe kilka dni musi zostać w domu.",
        "effect": lambda: infect_family_member("Córka"),
        "image": event_images["sick_daughter"]
    },
    {
        "text": "Twój komputer się zawiesił. Straciłeś postęp w jednym zadaniu.",
        "effect": lambda: undo_random_task(),
        "image": event_images["pc_crash"]
    },
    {
        "text": "Otrzymałeś premię za dobre wyniki w pracy! +75 monet.",
        "effect": lambda: change_money(75),
        "image": event_images["work_bonus"]
    },
    {
        "text": "Sąsiad przyniósł ci ciasto i twoja rodzina czuje się lepiej.",
        "effect": lambda: heal_random_family_member(),
        "image": event_images["cake_gift"]
    },
    {
        "text": "Student przebił ci opony oraz wyciął katalizator. Musisz kupić nowy zestaw.",
        "effect": lambda: change_money(-75),
        "image": event_images["car_damage"]
    },
    {
        "text": "Student napisał na ciebie donos do Dziekana, straciłeś dzisiejszą premię.",
        "effect": lambda: change_money(-25),
        "image": event_images["dean_report"]
    },
    {
        "text": "Znalazłeś 5 monet pod uczelnią. Z tej okazji wydałeś 15 monet w żabce.",
        "effect": lambda: change_money(-10),
        "image": event_images["snack_spending"]
    },
    {
        "text": "Zaczepił Cię bezdomny, nie chciałeś dać mu 5 monet, więc zabrał ci portfel i Cię pobił.",
        "effect": lambda: change_money(-50),
        "image": event_images["mugging"]
    },
    {
        "text": "Syn wdał się w bójkę pod żabką.",
        "effect": lambda: infect_family_member("Syn"),
        "image": event_images["son_fight"]
    }
]



def change_money(amount):
    global money
    money += amount


def add_error():
    global current_error_count
    current_error_count += 1


def infect_family_member(role):
    for member in family_members:
        if member["role"] == role and "Chory" not in member["status"] and "Chora" not in member["status"]:
            member["status"] += ", " + ("Chory" if role.endswith("n") else "Chora")


def heal_random_family_member():
    random.shuffle(family_members)
    for member in family_members:
        if "Chory" in member["status"] or "Chora" in member["status"]:
            member["status"] = member["status"].replace("Chory", "Zdrowy").replace("Chora", "Zdrowa")
            break


def undo_random_task():
    global completed_tasks
    incomplete = [task for task in tasks if task["checked"]]
    if incomplete:
        task = random.choice(incomplete)
        task["checked"] = False
        completed_tasks = max(0, completed_tasks - 1)


def draw_event_popup():
    global event_button_rect
    screen.fill((240, 240, 240))

    if active_event:
        padding = 20
        max_text_width = SCREEN_WIDTH - 200
        image_height = 200
        image_padding = 20

        wrapped = wrap_text(active_event["text"], text_font, max_text_width)
        line_height = text_font.get_height()
        content_width = max(text_font.size(line)[0] for line in wrapped)
        box_width = content_width + 2 * padding
        box_height = image_height + image_padding + len(wrapped) * line_height + 2 * padding + 70

        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT - box_height) // 2

        draw_rounded_rect(screen, box_x, box_y, box_width, box_height, (255, 255, 255), 10)

        y_offset = box_y + padding

        if "image" in active_event and active_event["image"]:
            original_image = active_event["image"]
            original_width, original_height = original_image.get_size()
            target_height = 200
            scale_ratio = target_height / original_height
            scaled_width = int(original_width * scale_ratio)

            scaled_image = pygame.transform.scale(original_image, (scaled_width, target_height))
            image_rect = scaled_image.get_rect(center=(SCREEN_WIDTH // 2, y_offset + target_height // 2))
            screen.blit(scaled_image, image_rect)
            y_offset += target_height + 20

        for line in wrapped:
            line_surf = text_font.render(line, True, (0, 0, 0))
            text_x = box_x + (box_width - line_surf.get_width()) // 2
            screen.blit(line_surf, (text_x, y_offset))
            y_offset += line_height

        event_button_rect = draw_button("OK", 150, 50, SCREEN_WIDTH // 2, y_offset + 30)



mail_messages = []
last_mail_day = -1
answered_mails = set()


def generate_mail():
    global mail_messages, last_mail_day

    if last_mail_day == day_counter:
        return

    last_mail_day = day_counter
    mail_messages = []

    possible_messages = [
        {
            "text": "Dzień dobry, czy można pisać kolosa w innym terminie?",
            "effect": lambda: None,
            "responses": [
                {"text": "Tak, proszę zgłosić się po zajęciach.", "effect": lambda: change_money(-5)},
                {"text": "Nie, obowiązuje termin z sylabusa.", "effect": lambda: add_error()},
                {"text": "Proszę napisać podanie do dziekana.", "effect": lambda: None}
            ]
        },
        {
            "text": "Ocena 3 to chyba pomyłka, prawda?",
            "effect": lambda: None,
            "responses": [
                {"text": "Nie, wszystko się zgadza.", "effect": lambda: None},
                {"text": "Możemy porozmawiać po zajęciach.", "effect": lambda: change_money(-5)},
                {"text": "Sprawdzę jeszcze raz.", "effect": lambda: None}
            ]
        },
        {
            "text": "Czy wpisze mi Pan ocenę wyżej, bo jestem blisko progu?",
            "effect": lambda: None,
            "responses": [
                {"text": "Nie, obowiązuje regulamin.", "effect": lambda: None},
                {"text": "Dobrze, zrobię wyjątek.", "effect": lambda: change_money(-10)},
                {"text": "Zgłoś się do poprawy.", "effect": lambda: None}
            ]
        },
        {
            "text": "Proszę o opinię do awansu zawodowego dr Kowalskiego.",
            "effect": lambda: None,
            "responses": [
                {"text": "Wystawię opinię pozytywną.", "effect": lambda: change_money(10)},
                {"text": "Nie znam jego pracy.", "effect": lambda: None},
            ]
        },
        {
            "text": "Czy może Pan zmienić godzinę zajęć? Mam wtedy angielski.",
            "effect": lambda: None,
            "responses": [
                {"text": "Niestety nie, harmonogram jest ustalony.", "effect": lambda: None},
                {"text": "Zobaczę, co da się zrobić.", "effect": lambda: change_money(-5)},
            ]
        },
        {
            "text": "Panie Profesorze, wysłałem pracę 5 minut po czasie, czy to problem?",
            "effect": lambda: None,
            "responses": [
                {"text": "Tym razem zaliczam.", "effect": lambda: change_money(-5)},
                {"text": "Niestety nie mogę zaakceptować.", "effect": lambda: add_error()}
            ]
        },
        {
            "text": "Witam, jeżeli nie wstawi mi Doktor oceny zaliczającej, spotkamy sie w ciemnej alejce.",
            "effect": lambda: None,
            "responses": [
                {"text": "Dobrze, przepraszam. Już wstawiam.", "effect": lambda: change_money(-10)},
                {"text": "Witam, Dziekan został powiadomiony.", "effect": lambda: None},
                {"text": "Dzień dobry, w takim razie do zobaczenia, 3x3 minuty full mma.", "effect": lambda: change_money(-5)}
            ]
        },
    ]

    selected = random.sample(possible_messages, k=random.randint(1, 3))
    for i, msg in enumerate(selected):
        msg["id"] = f"mail_{day_counter}_{i}"
        msg["effect"]()
        mail_messages.append(msg)


def draw_mail_screen():
    global answered_mails
    screen.fill(szary)
    draw_top_bar()

    y = 150
    button_height = 40
    padding = 10

    for msg in mail_messages:
        mail_id = msg["id"]
        is_answered = mail_id in answered_mails

        box_height = 80
        if not is_answered and "responses" in msg:
            box_height += (button_height + padding) * len(msg["responses"]) + padding

        draw_rounded_rect(screen, 300, y, SCREEN_WIDTH - 600, box_height, (255, 255, 255), 10)
        line_surf = text_font.render(msg["text"], True, (0, 0, 0))
        screen.blit(line_surf, (320, y + 20))

        if not is_answered and "responses" in msg:
            for idx, resp in enumerate(msg["responses"]):
                btn_rect_shadow = pygame.Rect(320, y + 60 + idx * (button_height + padding) + 2, 500 + 2, button_height)
                pygame.draw.rect(screen, (0, 0, 0), btn_rect_shadow, border_radius=6)
                btn_rect = pygame.Rect(320, y + 60 + idx * (button_height + padding), 500, button_height)
                pygame.draw.rect(screen, zolty, btn_rect, border_radius=6)
                text_surf = info_font.render(resp["text"], True, blue)
                text_rect = text_surf.get_rect(center=btn_rect.center)
                screen.blit(text_surf, text_rect)

                if mouse_clicked and btn_rect.collidepoint(mouse_pos):
                    answered_mails.add(mail_id)
                    resp["effect"]()
                    break

        y += box_height + 20

    draw_button("Powrót", 150, 50, SCREEN_WIDTH // 2 + 0, SCREEN_HEIGHT // 2 + 400)

    if mouse_clicked:
        current_screen = "task_screen"


while run:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    if not game_paused and current_screen != "login_form":
        if day_start_time:
            elapsed_seconds = time.time() - day_start_time
            total_minutes = int(elapsed_seconds * 4)
            current_hour = 8 + (total_minutes // 60)
            current_minute = total_minutes % 60

            if timer_flag and not game_paused and current_screen == "task_screen" and random.random() < 0.00002:
                trigger_random_event()

            if current_hour >= 16:
                current_hour = 16
                current_minute = 0
                if current_screen == "task_screen":
                    current_screen = "day_end_screen"

    if current_screen == "task_screen" and completed_tasks >= len(tasks):
        current_screen = "day_end_screen"

    draw_timer()

    for event in pygame.event.get():
        for switch in switch_buttons:
            switch.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_paused = not game_paused
                if game_paused:
                    pause_start_time = time.time()
                else:
                    if pause_start_time:
                        paused_duration = time.time() - pause_start_time
                        day_start_time += paused_duration
                        pause_start_time = None

            if event.key == pygame.K_1:
                money += 100
            if event.key == pygame.K_2:
                money -= 100
            if event.key == pygame.K_3:
                current_screen = "day_end_screen"
            if event.key == pygame.K_4:
                day_counter = 29
                current_screen = "day_end_screen"

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not settings_open:
                previous_screen = current_screen
                current_screen = "settings"
                settings_open = True
            else:
                if previous_screen:
                    current_screen = previous_screen
                settings_open = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if active_input == "nickname":
                    active_input = "password"
                elif active_input == "password":
                    active_input = "nickname"
            else:
                if active_input == "nickname":
                    if event.key == pygame.K_BACKSPACE:
                        login_nickname = login_nickname[:-1]
                    elif len(login_nickname) < 15 and event.unicode.isprintable():
                        login_nickname += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        login_password = login_password[:-1]
                    elif len(login_password) < 15 and event.unicode.isprintable():
                        login_password += event.unicode

    if current_screen == "menu":
        play_rect, settings_rect, exit_rect = draw_menu()
        if mouse_clicked:
            if play_rect.collidepoint(mouse_pos):
                current_screen = "character_select"
                day_start_time = time.time()
            elif settings_rect.collidepoint(mouse_pos):
                current_screen = "settings"
            elif exit_rect.collidepoint(mouse_pos):
                save_settings()
                run = False

    elif current_screen == "settings":
        (back_rect, full_icon_rect, easy_icon_rect, minus_rect, plus_rect,
         snd_minus_rect, snd_plus_rect) = draw_settings()
        if mouse_clicked:
            if back_rect.collidepoint(mouse_pos):
                if settings_open:
                    if previous_screen:
                        current_screen = previous_screen
                    settings_open = False
                else:
                    current_screen = "menu"
            elif full_icon_rect.collidepoint(mouse_pos):
                fullscreen_checked = not fullscreen_checked
                toggle_fullscreen(fullscreen_checked)
            elif easy_icon_rect.collidepoint(mouse_pos):
                easy_mode_checked = not easy_mode_checked
            elif minus_rect.collidepoint(mouse_pos):
                music_volume = max(0, music_volume - 10)
            elif plus_rect.collidepoint(mouse_pos):
                music_volume = min(100, music_volume + 10)
            elif snd_minus_rect.collidepoint(mouse_pos):
                sound_volume = max(0, sound_volume - 10)
            elif snd_plus_rect.collidepoint(mouse_pos):
                sound_volume = min(100, sound_volume + 10)
        save_settings()

    elif current_screen == "character_select":
        char1_rect, char2_rect = draw_character_select()
        if mouse_clicked:
            draw_task_screen()
            handle_character_selection(mouse_pos, mouse_clicked, char1_rect, char2_rect)

    elif current_screen == "task_screen":
        draw_task_screen()
        tab_rects = draw_top_bar()
        if mouse_clicked:
            for tab_name, tab_rect in tab_rects:
                if tab_rect.collidepoint(mouse_pos) and tab_name == "Zaloguj":
                    current_screen = "login_form"
                elif tab_rect.collidepoint(mouse_pos) and tab_name == "Webdziekanat":
                    current_screen = "webdziekanat_screen"
                elif tab_rect.collidepoint(mouse_pos) and tab_name == "Kolokwia":
                    complete_task(2)
                    generate_colloquium()
                    current_screen = "colloquium_screen"
                elif tab_rect.collidepoint(mouse_pos) and tab_name == "Poczta":
                    generate_mail()
                    current_screen = "mail_screen"

    elif current_screen == "login_form":
        draw_login_form()
        if mouse_clicked:
            if nickname_rect.collidepoint(mouse_pos):
                active_input = "nickname"
            elif password_rect.collidepoint(mouse_pos):
                active_input = "password"
            elif login_button_rect.collidepoint(mouse_pos):
                draw_task_screen()
                if "Webdziekanat" not in tabs:
                    tabs.clear()
                    tabs.append("Webdziekanat")
                for idx, task in enumerate(tasks):
                    if "Zaloguj się do systemu" in task["text"]:
                        complete_task(idx)
                        break
                tasks.append({
                    "text": "Otwórz zakładkę 'Webdziekanat', aby zatwierdzić oceny końcowe studentów",
                    "checked": False
                })
                if "Poczta" not in tabs and day_counter >= 1:
                    tabs.append("Poczta")
                    tasks.append({"text": "Sprawdź swoją pocztę klikając zakładkę 'Poczta'", "checked": False})
                current_screen = "task_screen"

    elif current_screen == "webdziekanat_screen":
        if not switches_initialized:
            grades_data = get_grades_data(easy_mode_checked)
            persons = [gd[0] for gd in grades_data]
            correct_states = [
                calculate_final_grade(avg) == final
                for (_, _, avg, final) in grades_data
            ]
            init_switches(persons, easy_mode_checked)
        accept_button_rect = draw_grades_window(grades_data)
        draw_switches()

        if mouse_clicked:
            if accept_button_rect.collidepoint(mouse_pos):
                errors_in_webdziekanat = sum(
                    1 for i, sw in enumerate(switch_buttons)
                    if sw.state != correct_states[i]
                )
                current_error_count += errors_in_webdziekanat
                for idx, task in enumerate(tasks):
                    if "Webdziekanat" in task["text"]:
                        complete_task(idx)
                        break
                if day_counter == 0 or completed_tasks >= len(tasks):
                    current_screen = "day_end_screen"
                else:
                    current_screen = "task_screen"

    elif current_screen == "day_end_screen":
        result = draw_day_end_window(day_counter)
        if result == (None, None, None):
            current_screen = "failure_screen"
        else:
            continue_rect, food_toggle_rect, calculated_total_sum = result
        hovering_food_checkbox = food_toggle_rect.collidepoint(mouse_pos)
        cannot_check = not food_checkbox_checked and calculated_total_sum + -food_price < 0
        if hovering_food_checkbox and cannot_check:
            draw_tooltip("Nie stać Cię na jedzenie — saldo byłoby ujemne.", mouse_pos[0], mouse_pos[1] + 20)

        if mouse_clicked:
            for entry in day_end_data:
                if entry["text"].startswith("Leki (") and "checkbox_rect" in entry:
                    if entry["checkbox_rect"].collidepoint(mouse_pos):
                        role = entry["checkbox_role"]
                        medicine_checkboxes_checked[role] = not medicine_checkboxes_checked.get(role, False)

            if food_toggle_rect.collidepoint(mouse_pos):
                if not food_checkbox_checked:
                    potential_sum = calculated_total_sum + -food_price
                    if potential_sum >= 0:
                        food_checkbox_checked = True
                else:
                    food_checkbox_checked = False

            if continue_rect.collidepoint(mouse_pos):
                update_family_health()
                food_checkbox_checked = False
                money = calculated_total_sum

                if not is_any_family_member_alive():
                    current_screen = "failure_screen"
                if day_counter + 1 >= 30 and is_any_family_member_alive():
                    animate_cup_and_confetti()

                    days_survived = day_counter + 1
                    tasks_completed_total = total_completed_tasks
                    money_left = money
                    total_errors_made = current_error_count
                    current_status_index = current_status_idx
                    achievements_unlocked_count = sum(1 for ach in achievements if ach["unlocked"])

                    final_score = calculate_final_score(
                        days_survived,
                        tasks_completed_total,
                        money_left,
                        total_errors_made,
                        current_status_index,
                        achievements_unlocked_count
                    )

                    nickname = login_nickname or "Anonim"
                    submit_score(nickname, final_score)

                    current_screen = "final_screen"
                else:
                    day_counter += 1
                    completed_tasks = 0
                    current_error_count = 0
                    day_start_time = time.time()
                    current_hour = 8
                    current_minute = 0
                    tasks.clear()
                    tabs.clear()

                    if day_counter == 0:
                        continue
                    else:
                        tasks.append(
                            {"text": "Sprawdź kolokwium studenta w zakładce 'Kolokwia'", "checked": False})
                        tabs.append("Kolokwia")
                        tasks.append(
                            {"text": "Zatwierdź oceny końcowe studentów w zakładce 'Webdziekanat'", "checked": False})
                        tabs.append("Webdziekanat")
                        tasks.append(
                            {"text": "Sprawdź swoją pocztę klikając zakładkę 'Poczta'", "checked": False})
                        tabs.append("Poczta")
                        switches_initialized = False
                        generate_colloquium()
                    current_screen = "task_screen"
                    status_achieved_time = pygame.time.get_ticks()
                    draw_task_screen()
                    save_settings()

    elif current_screen == "colloquium_screen":
        line_rects, accept_button_rect = draw_colloquium_window()
        if mouse_clicked:
            for i, rect in enumerate(line_rects):
                if rect.collidepoint(mouse_pos):
                    selected_lines[i] = not selected_lines[i]
            if accept_button_rect.collidepoint(mouse_pos):
                current_error_count = 0
                errors_in_colloquium = 0
                for i in range(len(selected_lines)):
                    if selected_lines[i] != (i in colloquium_errors):
                        errors_in_colloquium += 1
                current_error_count += errors_in_colloquium
                for idx, task in enumerate(tasks):
                    if "Kolokwia" in task["text"] or "sprawdzanie" in task["text"]:
                        complete_task(idx)
                        break
                current_screen = "task_screen"

    elif current_screen == "final_screen":
        menu_button_rect, leaderboard_button_rect = draw_final_screen()
        if mouse_clicked:
            if menu_button_rect.collidepoint(mouse_pos):
                final_screen_animation_played = False
                current_screen = "menu"
                init_new_game()

            elif leaderboard_button_rect.collidepoint(mouse_pos):
                current_screen = "leaderboard_screen"
                init_new_game()

    elif current_screen == "leaderboard_screen":
        back_button_rect = draw_leaderboard_screen()
        if mouse_clicked and back_button_rect.collidepoint(mouse_pos):
            cached_leaderboard = None
            current_screen = "menu"

    elif current_screen == "failure_screen":
        menu_button_rect, leaderboard_button_rect = draw_failure_screen()
        if mouse_clicked:
            if menu_button_rect.collidepoint(mouse_pos):
                final_screen_animation_played = False
                current_screen = "menu"
                init_new_game()
            elif leaderboard_button_rect.collidepoint(mouse_pos):
                current_screen = "leaderboard_screen"
                init_new_game()

    elif current_screen == "event_popup":
        draw_event_popup()
        if mouse_clicked and event_button_rect and event_button_rect.collidepoint(mouse_pos):
            active_event["effect"]()
            current_screen = "task_screen"
            active_event = None

    elif current_screen == "mail_screen":
        draw_mail_screen()
        if mouse_clicked:
            for msg in mail_messages:
                if "button_rects" in msg:
                    for rect, eff in msg["button_rects"]:
                        if rect.collidepoint(mouse_pos):
                            eff()
                            msg["answered"] = True
                            msg["button_rects"] = []
                            break

    else:
        switches_initialized = False

    pygame.display.update()

save_settings()
pygame.quit()
