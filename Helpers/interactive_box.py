import pygame
import numpy as np
from dataclasses import dataclass
import os


BOARD_ROWS, BOARD_COLS = 8, 8
BOX_COLOR = (217, 217, 217)


class InteractiveBox:
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        text_color: tuple,
        function=None,
    ):
        """Class for creating interactive boxes"""
        self.rect = rect
        self.text = text
        self.text_color = text_color
        self.function = function
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def draw(self, screen, font_size=32):
        """Draws the interactive box on the screen"""
        color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        font = pygame.font.Font(None, font_size)
        text = font.render(self.text, 1, self.text_color)
        screen.blit(text, (self.rect.left + 5, self.rect.top + 5))

    def update(self, screen, font_size=32):
        """Updates the interactive box"""
        color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        font = pygame.font.Font(None, font_size)
        text = font.render(self.text, 1, self.text_color)
        screen.blit(text, (self.rect.left + 5, self.rect.top + 5))
