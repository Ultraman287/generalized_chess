# import the pygame module
import pygame
import numpy as np
from dataclasses import dataclass


HEIGHT, WIDTH = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.flip()
running = True
clock = pygame.time.Clock()

BOARD_ROWS, BOARD_COLS = 8, 8

WHITE_COLOR, BLACK_COLOR = (255, 255, 255), (0, 0, 0)

CURRENT_WINDOW = "main_menu"

screen.fill(WHITE_COLOR)


@dataclass
class InputBox:
    """Class for creating input boxes"""

    rect: pygame.Rect
    text: str
    color: tuple
    text_color: tuple
    variable: str = ""
    active: bool = False
    color_active: tuple = (220, 220, 220)
    color_inactive: tuple = (255, 255, 255)

    def draw(self, screen):
        """Draws the input box on the screen"""
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 32)
        text = font.render(self.text, 1, self.text_color)
        screen.blit(text, (self.rect.left + 5, self.rect.top + 5))
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

    def handle_event(self, event):
        """Handles the event of the input box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                if self.text.isnumeric():
                    globals()[self.variable] = int(self.text)


pygame.init()

# Input boxes

input1 = InputBox(
    pygame.Rect(150, 200, 140, 32), "Rows", (255, 255, 255), (0, 0, 0), "BOARD_ROWS"
)


input2 = InputBox(
    pygame.Rect(150, 300, 140, 32), "Columns", (255, 255, 255), (0, 0, 0), "BOARD_COLS"
)


change_button = pygame.Rect(150, 400, 140, 32)

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if change_button.collidepoint(event.pos):
                CURRENT_WINDOW = (
                    "game" if CURRENT_WINDOW == "main_menu" else "main_menu"
                )
                pygame.time.wait(100)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                CURRENT_WINDOW = (
                    "game" if CURRENT_WINDOW == "main_menu" else "main_menu"
                )
                pygame.time.wait(100)
        input1.handle_event(event)
        input2.handle_event(event)

    if CURRENT_WINDOW == "game":
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if row % 2 == col % 2:
                    color = WHITE_COLOR
                else:
                    color = BLACK_COLOR
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        col * WIDTH / BOARD_COLS,
                        row * ((HEIGHT - 100) / BOARD_ROWS) + 100,
                        WIDTH / BOARD_COLS,
                        (HEIGHT - 100) / BOARD_ROWS,
                    ),
                )
    elif CURRENT_WINDOW == "main_menu":
        # Outer boundary
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 800))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 100, 600, 600))

        # Draw the input boxes
        input1.draw(screen)
        input2.draw(screen)

        # Draw the change button
        pygame.draw.rect(screen, (0, 0, 0), change_button)
    clock.tick(60)
    pygame.display.update()
