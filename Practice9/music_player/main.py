from pathlib import Path
import pygame

from player import MusicPlayer


pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 26)
clock = pygame.time.Clock()

# Папка music находится рядом с main.py.
music_folder = Path(__file__).parent / "music"
player = MusicPlayer(music_folder)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.previous()
            elif event.key == pygame.K_q:
                running = False

    screen.fill((245, 245, 245))

    track_name = player.get_current_track_name()
    position = player.get_position_seconds()
    time_text = f"{position // 60:02}:{position % 60:02}"

    screen.blit(font.render(track_name, True, (20, 20, 20)), (30, 50))
    screen.blit(
        small_font.render(f"Position: {time_text}", True, (60, 60, 60)),
        (30, 100),
    )
    screen.blit(
        small_font.render(
            "P: Play   S: Stop   N: Next   B: Previous   Q: Quit",
            True,
            (60, 60, 60),
        ),
        (30, 220),
    )

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
