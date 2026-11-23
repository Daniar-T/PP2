import pygame
from datetime import datetime
import tools

WIDTH, HEIGHT = 640, 480
BACKGROUND = (0, 0, 0)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(BACKGROUND)

    tool = "brush"
    color = (0, 0, 255)
    brush_size = 5

    drawing = False
    start_pos = None
    last_pos = None
    preview_pos = None

    typing = False
    text = ""
    text_pos = None
    font = pygame.font.SysFont("Arial", 24)

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if typing:
                    if event.key == pygame.K_ESCAPE:
                        typing = False
                        text = ""
                        text_pos = None

                    elif event.key == pygame.K_RETURN:
                        if text:
                            tools.render_text(canvas, text, font, color, text_pos)
                        typing = False
                        text = ""
                        text_pos = None

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]

                    elif event.unicode and event.unicode.isprintable():
                        text += event.unicode

                    continue

                if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"paint_{timestamp}.png"
                    pygame.image.save(canvas, filename)
                    print(f"Canvas saved as {filename}")
                    continue

                if event.key == pygame.K_ESCAPE:
                    running = False

                # Инструменты
                elif event.key == pygame.K_q:
                    tool = "brush"
                elif event.key == pygame.K_w:
                    tool = "line"
                elif event.key == pygame.K_e:
                    tool = "rectangle"
                elif event.key == pygame.K_r:
                    tool = "circle"
                elif event.key == pygame.K_t:
                    tool = "square"
                elif event.key == pygame.K_y:
                    tool = "rtriangle"
                elif event.key == pygame.K_u:
                    tool = "etriangle"
                elif event.key == pygame.K_i:
                    tool = "rhombus"
                elif event.key == pygame.K_o:
                    tool = "fill"
                elif event.key == pygame.K_p:
                    tool = "text"
                elif event.key == pygame.K_l:
                    tool = "eraser"

                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

                elif event.key == pygame.K_a:
                    color = (255, 0, 0)
                elif event.key == pygame.K_s:
                    color = (0, 255, 0)
                elif event.key == pygame.K_d:
                    color = (0, 0, 255)
                elif event.key == pygame.K_f:
                    color = (255, 255, 255)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if tool == "fill":
                    target = canvas.get_at(event.pos)[:3]
                    if target != color:
                        tools.flood_fill(
                            canvas, event.pos[0], event.pos[1], target, color
                        )

                elif tool == "text":
                    text_pos = event.pos
                    text = ""
                    typing = True

                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
                    preview_pos = event.pos

            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    preview_pos = event.pos

                    if tool == "brush":
                        tools.draw_pencil(
                            canvas, color, last_pos, event.pos, brush_size
                        )
                        last_pos = event.pos

                    elif tool == "eraser":
                        pygame.draw.circle(
                            canvas, BACKGROUND, event.pos, max(brush_size, 1)
                        )

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing:
                    end_pos = event.pos

                    if tool == "line":
                        tools.draw_line(
                            canvas, color, start_pos, end_pos, brush_size
                        )
                    elif tool == "rectangle":
                        tools.draw_rectangle(
                            canvas, color, start_pos, end_pos, brush_size
                        )
                    elif tool == "circle":
                        tools.draw_circle(
                            canvas, color, start_pos, end_pos, brush_size
                        )
                    elif tool == "square":
                        tools.draw_square(
                            canvas, color, start_pos, end_pos, brush_size
                        )
                    elif tool == "rtriangle":
                        tools.draw_rtriangle(
                            canvas, color, start_pos, end_pos, brush_size
                        )
                    elif tool == "etriangle":
                        tools.draw_etriangle(
                            canvas, color, start_pos, end_pos, brush_size
                        )
                    elif tool == "rhombus":
                        tools.draw_rhombus(
                            canvas, color, start_pos, end_pos, brush_size
                        )

                    drawing = False
                    preview_pos = None

        screen.blit(canvas, (0, 0))

        if drawing and preview_pos is not None:
            if tool == "line":
                pygame.draw.line(
                    screen, color, start_pos, preview_pos, brush_size
                )

            elif tool == "rectangle":
                rect = pygame.Rect(start_pos, (0, 0))
                rect.update(
                    min(start_pos[0], preview_pos[0]),
                    min(start_pos[1], preview_pos[1]),
                    abs(preview_pos[0] - start_pos[0]),
                    abs(preview_pos[1] - start_pos[1]),
                )
                pygame.draw.rect(screen, color, rect, brush_size)

            elif tool == "circle":
                dx = preview_pos[0] - start_pos[0]
                dy = preview_pos[1] - start_pos[1]
                radius = int((dx ** 2 + dy ** 2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius, brush_size)

            elif tool == "square":
                dx = preview_pos[0] - start_pos[0]
                dy = preview_pos[1] - start_pos[1]
                size = min(abs(dx), abs(dy))
                left = start_pos[0] if dx >= 0 else start_pos[0] - size
                top = start_pos[1] if dy >= 0 else start_pos[1] - size
                pygame.draw.rect(
                    screen, color, (left, top, size, size), brush_size
                )

            elif tool == "rtriangle":
                points = [
                    start_pos,
                    (preview_pos[0], start_pos[1]),
                    preview_pos,
                ]
                pygame.draw.polygon(screen, color, points, brush_size)

            elif tool == "etriangle":
                x1, y1 = start_pos
                x2, y2 = preview_pos
                base_mid_x = (x1 + x2) // 2
                height = abs(x2 - x1) * (3 ** 0.5) / 2
                direction = -1 if y2 >= y1 else 1
                top = (base_mid_x, int(y1 + direction * height))
                pygame.draw.polygon(
                    screen, color, [start_pos, preview_pos, top], brush_size
                )

            elif tool == "rhombus":
                x1, y1 = start_pos
                x2, y2 = preview_pos
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                pygame.draw.polygon(screen, color, points, brush_size)

        if typing and text_pos is not None and text:
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, text_pos)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
