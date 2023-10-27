import pygame
import numpy as np
from dataclasses import dataclass
import os
from Helpers.interactive_box import InteractiveBox


class TrainAgent(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 132, 386, 58)
        self.text = "Train Agent on Board"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return "ai_train_screen"


class PlayAgent(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 271, 386, 58)
        self.text = "Play Trained Agent"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return "ai_play_screen"


class BackButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 410, 386, 58)
        self.text = "Back"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "main_menu_screen"


class AIToolsScreen:
    def __init__(self) -> None:
        self.new_game_button = TrainAgent()
        self.continue_button = PlayAgent()
        self.back_button = BackButton()

    def handle_event(self, event):
        selected = self.continue_button.handle_event(event)
        if selected:
            return selected

        return self.new_game_button.handle_event(
            event
        ) or self.back_button.handle_event(event)

    def reset(self):
        pass

    def update(self, screen):
        screen.fill((198, 198, 198))
        self.new_game_button.draw(screen)
        self.continue_button.draw(screen)
        self.back_button.draw(screen)
        pygame.display.flip()
