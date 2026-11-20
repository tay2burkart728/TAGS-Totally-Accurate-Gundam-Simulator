import pygame
import random
import math

def draw_radar(screen, center, radius, fighters):
    pygame.draw.circle(screen, (255, 255, 255), center, radius, 2)

    for f in fighters:
        x = max(0.0, min(1.0, f['x']))
        y = max(0.0, min(1.0, f['y']))

        px = center[0] + int((x - 0.5) * radius * 2)
        py = center[1] + int((y - 0.5) * radius * 2)

        if math.dist((px, py), center) > radius:
            continue

        color = f['color'] if f['alive'] else (80, 80, 80)

        pygame.draw.circle(screen, color, (px, py), 6)

def show_radars(screen, earth_fighters, space_fighters):
    WIDTH, HEIGHT = screen.get_size()

    earth_center = (WIDTH // 2 - WIDTH // 6, HEIGHT // 3)
    space_center = (WIDTH // 2 + WIDTH // 6, HEIGHT // 3)
    radius = min(WIDTH, HEIGHT) // 6

    draw_radar(screen, earth_center, radius, earth_fighters)
    draw_radar(screen, space_center, radius, space_fighters)

    font = pygame.font.SysFont(None, 36)

    earth_label = font.render('EARTH', True, (255, 255, 255))
    space_label = font.render('SPACE', True, (255, 255, 255))

    screen.blit(earth_label, (earth_center[0] - earth_label.get_width() // 2,
                                earth_center[1] + radius + 10))

    screen.blit(space_label, (space_center[0] - space_label.get_width() // 2,
                                space_center[1] + radius + 10))

def make_fighter_dot(pilot, color):
    return {
        'pilot': pilot,
        'x': random.random(),
        'y': random.random(),
        'color': color,
        'alive': True
    }
