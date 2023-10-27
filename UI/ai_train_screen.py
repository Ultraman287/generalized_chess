import pygame
import numpy as np
from dataclasses import dataclass
import os
from Helpers.interactive_box import InteractiveBox


class BackButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(15, 200, 700, 100)
        self.text = [
            "KEEP ON PLAYING AND FINISHING GAMES WITH THE VERSION",
            "YOU WANT TO BE TRAINED AND IT WILL BE STORED IN HISTORY AND USED TO TRAIN THE AI",
        ]
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "ai_tools_screen"

    def draw(self, screen):
        super().draw(screen, font_size=15)


class AITrainScreen:
    def __init__(self) -> None:
        self.back_button = BackButton()

    def handle_event(self, event):
        return self.back_button.handle_event(event)

    def reset(self):
        pass

    def update(self, screen):
        screen.fill((198, 198, 198))
        self.back_button.draw(screen)
        pygame.display.flip()
