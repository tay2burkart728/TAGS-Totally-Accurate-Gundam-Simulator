import pygame
import sys
from presentation.radar_display import show_radars

clock = pygame.time.Clock()

def ui_tick():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(60)
    pygame.time.delay(120)

UI_STATE = {
    'screen': None,
    'clock': None,
    'portraits': [],
    'positions': [],
    'earth_fighters': [],
    'space_fighters': [],
    'battle_log': [],
    'dots': {},
    'running': True
}

def add_border(img, final_size=180, color=(255, 255, 255)):
    w, h = img.get_size()
    bordered = pygame.Surface((final_size, final_size), pygame.SRCALPHA)
    bordered.fill(color)
    bordered.blit(img, ((final_size - w) // 2, (final_size - h) // 2))
    return bordered

def scale_portrait(img, max_w=150, max_h=150):
    w, h = img.get_size()
    ratio = min(max_w / w, max_h / h)
    return pygame.transform.smoothscale(img, (int(w * ratio), int(h * ratio)))

def grayscale_surface(img):
    return pygame.transform.grayscale(img)

def start_ui(pilots):
    pygame.init()

    WIDTH, HEIGHT = (1280, 720)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Gundam Tournament')

    UI_STATE['screen'] = screen
    UI_STATE['clock'] = pygame.time.Clock()

    portraits = []

    for pilot in pilots:
        img = pygame.image.load(pilot.portrait_path).convert_alpha()
        img = scale_portrait(img)
        img = add_border(img, 180)

        gray = grayscale_surface(img)

        portraits.append((pilot, img, gray))

    print('DEBUG portraits loaded:', len(portraits))
    for p, img, gray in portraits:
        print(' -', p.name, p.portrait_path, img.get_size())

    UI_STATE['portraits'] = portraits

    rows = 4
    portrait_h = 180
    top_margin = 0
    bottom_margin = 0
    usable_height = HEIGHT - top_margin - bottom_margin
    spacing = (usable_height - rows * portrait_h) // (rows - 1)
    y_positions = [top_margin + i * (portrait_h + spacing) for i in range(rows)]

    positions = [
        (100, y_positions[0]),
        (100, y_positions[1]),
        (100, y_positions[2]),
        (100, y_positions[3]),
        (WIDTH - 100 - portrait_h, y_positions[0]),
        (WIDTH - 100 - portrait_h, y_positions[1]),
        (WIDTH - 100 - portrait_h, y_positions[2]),
        (WIDTH - 100 - portrait_h, y_positions[3])
    ]

    UI_STATE['positions'] = positions

    rows = 4
    portrait_h = 180
    top_margin = 0
    bottom_margin = 0
    usable_height = HEIGHT - top_margin - bottom_margin
    spacing = (usable_height - rows * portrait_h) // (rows - 1)
    y_positions = [top_margin + i * (portrait_h + spacing) for i in range(rows)]

    positions = [
        (100, y_positions[0]),
        (100, y_positions[1]),
        (100, y_positions[2]),
        (100, y_positions[3]),
        (WIDTH - 100 - portrait_h, y_positions[0]),
        (WIDTH - 100 - portrait_h, y_positions[1]),
        (WIDTH - 100 - portrait_h, y_positions[2]),
        (WIDTH - 100 - portrait_h, y_positions[3])
    ]

    UI_STATE['positions'] = positions

def ui_draw_once():
    screen = UI_STATE['screen']
    screen.fill((0, 0, 0))

    for (pilot, img, gray), pos in zip(UI_STATE['portraits'], UI_STATE['positions']):
        if getattr(pilot, 'eliminated', False):
            screen.blit(gray, pos)
        else:
            screen.blit(img, pos)

    if getattr(pilot, 'eliminated', False):
        screen.blit(gray, pos)
        w, h = img.get_size()
        pygame.draw.line(screen, (255, 0, 0), pos, (pos[0] + w, pos[1] + h), 6)
        pygame.draw.line(screen, (255, 0, 0), (pos[0] + w, pos[1]), (pos[0], pos[1] + h), 6)
    else:
        screen.blit(img, pos)

    show_radars(
        screen,
        UI_STATE['earth_fighters'],
        UI_STATE['space_fighters']
    )

    draw_log_panel(screen)

    pygame.display.update()

def update_ui_for_round(earth_fighters, space_fighters):
    UI_STATE['earth_fighters'] = earth_fighters
    UI_STATE['space_fighters'] = space_fighters

def register_dots(dots):
    UI_STATE['dots'] = dots

def show_current_match(p1, p2, arena):
    """Put the two pilots who are fighting right now on their arena's radar"""
    if UI_STATE['screen'] is None:
        return
    dots = UI_STATE.get('dots', {})
    if p1 not in dots or p2 not in dots:
        return
    pair = [dots[p1], dots[p2]]
    if arena == "Earth":
        update_ui_for_round(pair, [])
    else:
        update_ui_for_round([], pair)
    ui_draw_once()

def push_log_line(text):
    """Called by announcer.py to push a new log line into UI."""
    UI_STATE['battle_log'].append(text)
    if len(UI_STATE['battle_log']) > 12:
        UI_STATE['battle_log'].pop(0)

def draw_log_panel(screen):
    font = pygame.font.SysFont(None, 24)
    x = 300
    y = 440
    line_height = 25
    max_width = 680

    wrapped = []
    for line in UI_STATE['battle_log']:
        words = line.split()
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if font.size(trial)[0] <= max_width:
                current = trial
            else:
                wrapped.append(current)
                current = word
        wrapped.append(current)

    for line in wrapped[-10:]:
        surf = font.render(line, True, (255, 255, 255))
        screen.blit(surf, (x, y))
        y += line_height

START_BUTTON = pygame.Rect(490, 330, 300, 60)


def wait_for_start():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Gundam Tournament')
    title_font = pygame.font.SysFont(None, 64)
    body_font = pygame.font.SysFont(None, 32)
    hint_font = pygame.font.SysFont(None, 28)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and START_BUTTON.collidepoint(event.pos):
                return
        screen.fill((0, 0, 0))
        title = title_font.render('GUNDAM GRAND TOURNAMENT', True, (255, 255, 255))
        screen.blit(title, ((1280 - title.get_width()) // 2, 220))
        subtitle = body_font.render('8 pilots. Earth vs Space. One champion.', True, (255, 255, 255))
        screen.blit(subtitle, ((1280 - subtitle.get_width()) // 2, 300))
        pygame.draw.rect(screen, (0, 200, 80), START_BUTTON)
        label = body_font.render('START TOURNAMENT', True, (255, 255, 255))
        screen.blit(label, (START_BUTTON.centerx - label.get_width() // 2, START_BUTTON.centery - label.get_height() // 2))
        hint = hint_font.render('Click START to run, or close the window to quit.', True, (255, 255, 255))
        screen.blit(hint, ((1280 - hint.get_width()) // 2, 420))
        pygame.display.flip()
        clock.tick(60)


def ui_loop():
    while UI_STATE['running']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                UI_STATE['running'] = False

        screen = UI_STATE['screen']
        screen.fill((0, 0, 0))

        for (pilot, img, gray), pos in zip(UI_STATE['portraits'], UI_STATE['positions']):
            if getattr(pilot, 'eliminated', False):
                screen.blit(gray, pos)
            else:
                screen.blit(img, pos)

        if getattr(pilot, 'eliminated', False):
            screen.blit(gray, pos)
            w, h = img.get_size()
            pygame.draw.line(screen, (255, 0, 0), pos, (pos[0] + w, pos[1] + h), 6)
            pygame.draw.line(screen, (255, 0, 0), (pos[0] + w, pos[1]), (pos[0], pos[1] + h), 6)
        else:
            screen.blit(img, pos)

        show_radars(
            screen,
            UI_STATE['earth_fighters'],
            UI_STATE['space_fighters']
        )

        draw_log_panel(screen)

        pygame.display.flip()
        UI_STATE['clock'].tick(60)

    pygame.quit()
    sys.exit()
