import pygame
import numpy as np
from dataclasses import dataclass
import os
from Helpers.interactive_box import InteractiveBox


"""
This is a simple menu selection UI
"""


class NewGame(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 132, 386, 58)
        self.text = "New Game"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "game_existing_screen"
                # file = prompt_file()
                # if file:
                #     return "game_screen", file


class Continue(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 271, 386, 58)
        self.text = "Continue"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("This hasnt been implemented yet")
            # if self.rect.collidepoint(event.pos):
            #     file = prompt_file()
            #     if file:
            #         return "game_screen", file


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


class GameOptionsScreen:
    def __init__(self) -> None:
        self.new_game_button = NewGame()
        self.continue_button = Continue()
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
