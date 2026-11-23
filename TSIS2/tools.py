import pygame
from datetime import datetime


def draw_pencil(surface, color, last_pos, current_pos, size):
    pygame.draw.line(surface, color, last_pos, current_pos, size)


def draw_line(surface, color, start_pos, end_pos, size):
    pygame.draw.line(surface, color, start_pos, end_pos, size)


def flood_fill(surface, x, y, target_color, replacement_color):
    target_color = tuple(target_color[:3])
    replacement_color = tuple(replacement_color[:3])

    if target_color == replacement_color:
        return

    width, height = surface.get_size()

    if not (0 <= x < width and 0 <= y < height):
        return

    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()

        if not (0 <= cx < width and 0 <= cy < height):
            continue

        if tuple(surface.get_at((cx, cy))[:3]) != target_color:
            continue

        surface.set_at((cx, cy), (*replacement_color, 255))

        stack.append((cx + 1, cy))
        stack.append((cx - 1, cy))
        stack.append((cx, cy + 1))
        stack.append((cx, cy - 1))


def save_canvas(surface):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"canvas_{timestamp}.png"
    pygame.image.save(surface, filename)
    print("Saved:", filename)


def render_text(surface, text, font, color, pos):
    image = font.render(text, True, color)
    surface.blit(image, pos)


def draw_rectangle(surface, color, start, end, size):
    left = min(start[0], end[0])
    top = min(start[1], end[1])
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])

    pygame.draw.rect(surface, color, (left, top, width, height), size)


def draw_circle(surface, color, start, end, size):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    radius = int((dx ** 2 + dy ** 2) ** 0.5)

    pygame.draw.circle(surface, color, start, radius, size)


def draw_square(surface, color, start, end, size):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = min(abs(dx), abs(dy))

    left = start[0] if dx >= 0 else start[0] - side
    top = start[1] if dy >= 0 else start[1] - side

    pygame.draw.rect(surface, color, (left, top, side, side), size)


def draw_rtriangle(surface, color, start, end, size):
    points = [start, (end[0], start[1]), end]
    pygame.draw.polygon(surface, color, points, size)


def draw_etriangle(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    base_mid_x = (x1 + x2) // 2
    height = abs(x2 - x1) * (3 ** 0.5) / 2
    direction = -1 if y2 >= y1 else 1
    top = (base_mid_x, int(y1 + direction * height))

    pygame.draw.polygon(surface, color, [start, end, top], size)


def draw_rhombus(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y),
    ]

    pygame.draw.polygon(surface, color, points, size)
