import pygame


class Ball:
    def __init__(self, width, height):
        self.radius = 25
        self.x = width // 2
        self.y = height // 2
        self.step = 20
        self.width = width
        self.height = height

    def move(self, key):
        if key == pygame.K_UP and self.y - self.step - self.radius >= 0:
            self.y -= self.step
        elif key == pygame.K_DOWN and self.y + self.step + self.radius <= self.height:
            self.y += self.step
        elif key == pygame.K_LEFT and self.x - self.step - self.radius >= 0:
            self.x -= self.step
        elif key == pygame.K_RIGHT and self.x + self.step + self.radius <= self.width:
            self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)
