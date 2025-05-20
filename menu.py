import pygame
from utilities import *
import json
import os
import random
import time
from colloquium_bank import colloquium_bank

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


# 5c26ce - fioletowy

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
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            fullscreen_checked = settings.get("fullscreen", False)
            easy_mode_checked = settings.get("easy_mode", False)
            music_volume = settings.get("music_volume", 100)
            sound_volume = settings.get("sound_volume", 100)
            # day_counter = settings.get("day_counter", 0)
            # completed_tasks = settings.get("completed_tasks", 0)


pygame.init()
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


def scale_image(image, scale_factor):
    width, height = image.get_size()
    return pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))


switch_ok_icon = scale_image(switch_ok_icon, 1)
switch_no_icon = scale_image(switch_no_icon, 2)

coin_icon = pygame.image.load('images/coin_icon.png')
coin_icon = scale_image(coin_icon, 2)
coins = 0

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
    "Student I stopnia",
    "Student II stopnia",
    "Licencjat",
    "Magister",
    "Doktorant",
    "Doktor",
    "Dr habilitowany",
    "Profesor nadzwyczajny",
    "Profesor uczelni",
    "Profesor zwyczajny"
]
progi = [4, 7, 10, 15, 20, 30, 42, 57, 75, 95]
current_status_idx = 0
total_completed_tasks = 0
show_status_notification = False


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

    draw_text_top_left_from_center("Tryb pełnoekranowy", text_font, 'black', screen, -200, -100)
    fullscreen_icon = checked_icon if fullscreen_checked else frame
    fullscreen_icon_rect = draw_image_top_left_from_center(fullscreen_icon, screen, 170, -95)

    draw_text_top_left_from_center("Łatwy tryb gry", text_font, 'black', screen, -200, -60)
    easy_mode_icon = checked_icon if easy_mode_checked else frame
    easy_mode_icon_rect = draw_image_top_left_from_center(easy_mode_icon, screen, 170, -55)

    draw_text_top_left_from_center("Muzyka", text_font, 'black', screen, -200, -20)
    volume_bar_border_rect = draw_image_top_left_from_center(volume_bar_border_icon, screen, 30, -13)
    minus_icon_rect = draw_image_top_left_from_center(minus_icon, screen, 130, -15)
    plus_icon_rect = draw_image_top_left_from_center(plus_icon, screen, 170, -15)
    fill_width = int(84 * (music_volume / 100))
    pygame.draw.rect(screen, 'black',
                     pygame.Rect(volume_bar_border_rect.left + 3, volume_bar_border_rect.top + 3, fill_width, 20))

    draw_text_top_left_from_center("Dźwięki", text_font, 'black', screen, -200, 20)
    sound_bar_border_rect = draw_image_top_left_from_center(volume_bar_border_icon, screen, 30, 27)
    sound_minus_icon_rect = draw_image_top_left_from_center(minus_icon, screen, 130, 25)
    sound_plus_icon_rect = draw_image_top_left_from_center(plus_icon, screen, 170, 25)
    fill_width_sound = int(84 * (sound_volume / 100))
    pygame.draw.rect(screen, 'black',
                     pygame.Rect(sound_bar_border_rect.left + 3, sound_bar_border_rect.top + 3, fill_width_sound, 20))

    back_rect = draw_text("Powrót", text_font, 'black', screen, 0, 150)
    return (
        back_rect, fullscreen_icon_rect, easy_mode_icon_rect, minus_icon_rect, plus_icon_rect, sound_minus_icon_rect,
        sound_plus_icon_rect)


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
    icon = checked_icon if checkbox_checked else frame
    screen.blit(icon, (checkbox_x, checkbox_y))
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
    if day_counter > 0:
        icon_y = 15
        screen.blit(coin_icon, (15, icon_y))
        coin_surf = text_font.render(f"x{coins}", True, (0, 0, 0))
        screen.blit(coin_surf, (15 + coin_icon.get_width() + 8,
                                icon_y + (coin_icon.get_height() - coin_surf.get_height()) // 2))
        status_x = 15 + coin_icon.get_width() + 8 + coin_surf.get_width() + 20
        status_text = f"Status: {statusy[current_status_idx]}"
        status_surf = text_font.render(status_text, True, (0, 0, 0))
        screen.blit(status_surf, (status_x, 15))

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
    draw_task_screen()
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
    draw_rounded_rect_from_center_offset(screen, -75, 75, 150, 50, zolty, 10)
    login_button_rect = draw_button("Akceptuj", 150, 50, SCREEN_WIDTH // 2 + 0, SCREEN_HEIGHT // 2 + 100)
    question_rect = draw_image_top_left_from_center(question_mark_icon, screen, 210, 160)
    if question_rect.collidepoint(mouse_pos):
        show_info = True
    else:
        show_info = False
    if show_info:
        info_box_x = question_rect.right + 20
        info_box_y = question_rect.top + 20
        draw_info_box((info_box_x, info_box_y))


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


def get_grades_data(easy_mode_checked):
    student_names = [
        'Anna Dąbrowska', 'Bartek Sitek', 'Celina Fikus', 'Daniel Obajtek',
        'Ela Jabłońska', 'Filip Chajzer', 'Gosia Androsiewicz', 'Hubert Urbański'
    ]
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


def draw_day_end_window(day_counter):
    complete_task(3)
    tabs.clear()
    tasks.clear()
    draw_task_screen()
    day_counter = day_counter + 1
    draw_rounded_rect_from_center_offset(screen, -275, -225, 550, 450, (255, 255, 255), 10)
    draw_text(f"Dzień {day_counter} zakończony!", title_font, 'black', screen, 0, -150)
    draw_text("Gratulacje!", text_font, 'black', screen, 0, -50)
    draw_text(f"Ilość błędów: {current_error_count}", text_font, 'black', screen, 0, 0)
    draw_text(f"Ilość zrobionych zadań: {completed_tasks}", text_font, 'black', screen, 0, 50)
    continue_rect = draw_button("Kontynuuj", 150, 50, SCREEN_WIDTH // 2 + 0, SCREEN_HEIGHT // 2 + 150)
    return continue_rect

def generate_colloquium():
    global colloquium_data, colloquium_errors, selected_lines
    student_names = [
        'Anna Dąbrowska', 'Bartek Sitek', 'Celina Fikus', 'Daniel Obajtek',
        'Ela Jabłońska', 'Filip Chajzer', 'Gosia Androsiewicz', 'Hubert Urbański'
    ]
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

    accept_button_rect = draw_button("Zatwierdź sprawdzanie", 300, 50, SCREEN_WIDTH // 2 + 0, SCREEN_HEIGHT // 2 + 400)

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


tasks = [{"text": "Wybierz swój zawód", "checked": False}]
tabs = []

pause_start_time = None
run = True
while run:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    if not game_paused:
        if day_start_time:
            elapsed_seconds = time.time() - day_start_time
            total_minutes = int(elapsed_seconds * 4)
            current_hour = 8 + (total_minutes // 60)
            current_minute = total_minutes % 60
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
                current_error_count = sum(
                    1 for i, sw in enumerate(switch_buttons)
                    if sw.state != correct_states[i]
                )
                for idx, task in enumerate(tasks):
                    if "Webdziekanat" in task["text"]:
                        complete_task(idx)
                        break
                if day_counter == 0 or completed_tasks >= len(tasks):
                    current_screen = "day_end_screen"
                else:
                    current_screen = "task_screen"

    elif current_screen == "day_end_screen":
        continue_rect = draw_day_end_window(day_counter)
        if mouse_clicked and continue_rect.collidepoint(mouse_pos):
            day_counter += 1
            completed_tasks = 0
            current_error_count = 0
            day_start_time = time.time()
            current_hour = 8
            current_minute = 0
            tasks.clear()
            tabs.clear()
            if day_counter == 1:
                tasks.append({"text": "Sprawdź kolokwium studenta w zakładce 'Kolokwia'", "checked": False})
                tabs.append("Kolokwia")
            else:
                tasks.append({"text": "Sprawdź kolokwium studenta w zakładce 'Kolokwia'", "checked": False})
                tabs.append("Kolokwia")
                tasks.append({"text": "Zatwierdź oceny końcowe studentów w zakładce 'Webdziekanat'", "checked": False})
                tabs.append("Webdziekanat")
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
                for i in range(len(selected_lines)):
                    if selected_lines[i] != (i in colloquium_errors):
                        current_error_count += 1
                for idx, task in enumerate(tasks):
                    if "Kolokwia" in task["text"] or "sprawdzanie" in task["text"]:
                        complete_task(idx)
                        break
                current_screen = "task_screen"

    else:
        switches_initialized = False

    pygame.display.update()

save_settings()
pygame.quit()
